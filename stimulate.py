#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import atexit
from threading import Event
from time import sleep

import simpleaudio
import wiringpi
from pydub import AudioSegment
from pydub.generators import Pulse, Sawtooth, Sine, WhiteNoise

MUTE_PORT: int = 3  # IQaudio HAT 静音控制口
RESET_PORT: int = 21  # Arduino 重置口
LIGHT_PORT: int = 22  # Arduino 灯光控制口

# Arduino USB 串行通信参数
SERIAL_DEVICE_PATH: str = "/dev/ttyACM0"
SERIAL_BIT_RATE: int = 38400


def init_arduino() -> None:
    """初始化 Arduino 板"""
    wiringpi.pinMode(RESET_PORT, wiringpi.OUTPUT)
    wiringpi.digitalWrite(RESET_PORT, wiringpi.LOW)
    sleep(0.1)
    wiringpi.digitalWrite(RESET_PORT, wiringpi.HIGH)
    sleep(5)


def set_iqaudio_mute(flag: bool) -> None:
    """控制 IQaudio HAT 静音"""
    # 通过 GPIO3 控制，高电平为关闭静音
    signal = wiringpi.LOW if flag else wiringpi.HIGH
    wiringpi.pinMode(MUTE_PORT, wiringpi.OUTPUT)
    wiringpi.digitalWrite(MUTE_PORT, signal)


def init_serial() -> None:
    """初始化串行通信"""
    global serial
    serial = wiringpi.serialOpen(SERIAL_DEVICE_PATH, SERIAL_BIT_RATE)
    sleep(3)


def init_stimulating_light(
    light_stimulating_frequency: int,
    light_stimulating_duty_cycle: float,
    **kwargs,
) -> None:
    """初始化光刺激"""

    cycle_time = 1000_000 / light_stimulating_frequency
    work_time = round(cycle_time * light_stimulating_duty_cycle)
    sleep_time = round(cycle_time - work_time)

    global serial
    while True:
        wiringpi.serialPuts(serial, f"{work_time},{sleep_time}")
        check = (work_time + sleep_time) % 256
        if wiringpi.serialGetchar(serial) == check:
            return
        else:
            init_arduino()
            sleep(3)
            init_serial()


def init_stimulating_audio(
    audio_stimulating_frequency: int,
    audio_stimulating_duty_cycle: float,
    audio_duration: int,
    audio_generator: str,
    audio_generator_frequency: int,
    audio_generator_duty_cycle: float,
    audio_generator_frame_rate: int,
    audio_generator_bit_depth: int,
    export_audio_file: bool = False,
    **kwargs,
) -> None:
    """初始化声刺激"""

    if audio_generator == "sine":
        generator = Sine(
            freq=audio_generator_frequency,
            sample_rate=audio_generator_frame_rate,
            bit_depth=audio_generator_bit_depth,
        )
    elif audio_generator == "whitenoise":
        generator = WhiteNoise(
            sample_rate=audio_generator_frame_rate, bit_depth=audio_generator_bit_depth
        )
    elif audio_generator == "pulse":
        generator = Pulse(
            freq=audio_generator_frequency,
            duty_cycle=audio_generator_duty_cycle,
            sample_rate=audio_generator_frame_rate,
            bit_depth=audio_generator_bit_depth,
        )
    elif audio_generator == "sawtooth":
        generator = Sawtooth(
            freq=audio_generator_frequency,
            duty_cycle=audio_generator_duty_cycle,
            sample_rate=audio_generator_frame_rate,
            bit_depth=audio_generator_bit_depth,
        )

    cycle_duration = 1000 // audio_stimulating_frequency
    work_duration = cycle_duration * audio_stimulating_duty_cycle
    silent_duration = cycle_duration - work_duration

    work_audio_segment = generator.to_audio_segment(duration=work_duration)
    slient_audio_segment = AudioSegment.silent(
        duration=silent_duration, frame_rate=generator.sample_rate
    )
    cycle_audio_segment = work_audio_segment + slient_audio_segment
    second_audio_segment = cycle_audio_segment * audio_stimulating_frequency

    s = audio_duration // 1000

    global audio
    audio = second_audio_segment * s

    set_iqaudio_mute(False)

    if export_audio_file:
        audio.export("audio.wav", format="wav")


def start_light() -> None:
    wiringpi.pinMode(LIGHT_PORT, wiringpi.OUTPUT)
    wiringpi.digitalWrite(LIGHT_PORT, wiringpi.HIGH)


def stop_light() -> None:
    wiringpi.pinMode(LIGHT_PORT, wiringpi.OUTPUT)
    wiringpi.digitalWrite(LIGHT_PORT, wiringpi.LOW)


def start_audio() -> None:
    global audio, playback
    playback = simpleaudio.play_buffer(
        audio.raw_data,
        num_channels=audio.channels,
        bytes_per_sample=audio.sample_width,
        sample_rate=audio.frame_rate,
    )


def wait_done(exit_event:Event) -> None:
    global playback
    while playback.is_playing:
        if exit_event.is_set():
            exit()
        sleep(0.05)
        


def stop_audio() -> None:
    global playback
    playback.stop()


def stimulate(running_event: Event, exit_event:Event,config: dict) -> None:
    """主流程"""
    # 实时性优化
    wiringpi.wiringPiSetup()
    wiringpi.piHiPri(99)

    init_arduino()
    init_serial()
    init_stimulating_audio(**config)
    init_stimulating_light(**config)


    atexit.register(stop_audio)
    atexit.register(stop_light)
    start_light()
    sleep(config["delay_time"] / 1000)
    start_audio()
    running_event.set()
    wait_done(exit_event)



if __name__ == "__main__":
    stimulate()
