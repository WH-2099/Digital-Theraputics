#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import webbrowser
from csv import DictWriter
from datetime import datetime
from os.path import exists
from sys import exit
from threading import Event, Thread
from time import monotonic

import PySimpleGUI as sg

from stimulate import stimulate


def loading_window() -> None:
    """加载窗口"""
    layout = [
        [
            sg.Image(
                filename="logo.png",
                enable_events=True,
                key="-LOGO-",
            )
        ],
        [
            sg.Text(
                text="Digital Theraputics",
                font=(None, 48, "bold"),
                justification="center",
                key="-NAME-",
            )
        ],
        [
            sg.Text(
                text="Molecular Bioengineering lab in WLU",
                font=(None, 20, "bold underline"),
                justification="center",
                key="-LAB-",
                enable_events=True,
            )
        ],
        [
            sg.Text(
                text="Developed by: WH-2099",
                font=(None, 12, "underline"),
                justification="right",
                key="-DEVELOPER-",
                enable_events=True,
            ),
        ],
    ]
    window = sg.Window(
        title="Digital Stimulation - Loading",
        layout=layout,
        finalize=True,
        size=(720, 480),
        no_titlebar=True,
        keep_on_top=True,
    )

    for element in window.element_list():
        element.expand(expand_x=True, expand_y=True)

    while True:
        event, values = window.read(timeout=3000)
        if event in ("-LOGO-", "-LAB-"):
            webbrowser.open_new("https://www.piatkevich-lab.com/")
        if event == "-DEVELOPER-":
            webbrowser.open_new("https://blog.csdn.net/WH2099/?type=blog")
        if event in (sg.WIN_CLOSED, sg.TIMEOUT_EVENT):
            window.close()
            break


def running_window() -> None:
    global config

    layout = [
        [
            sg.Text(
                text="00:00:00",
                font=(None, 100),
                key="-TIME-",
            ),
        ],
        [sg.Text(text="INITIALIZING", font=(None, 60), key="-STATUS-")],
        [
            sg.Text(text=f"Session:", font=(None, 50)),
            sg.Text(text="0", font=(None, 50), key="-SESSION-N-"),
            sg.Text(text=f"/{config['session_number']}", font=(None, 50)),
        ],
    ]
    window = sg.Window(
        title="Digital Stimulating - Running",
        # no_titlebar=True,
        grab_anywhere=True,
        keep_on_top=True,
        layout=layout,
        element_justification="center",
        text_justification="center",
        finalize=True,
    )

    def run_session() -> Event:
        window["-STATUS-"].update("INITIALIZING")
        window.refresh()
        running_event = Event()
        exit_event = Event()

        stimulate_thread = Thread(
            target=stimulate,
            kwargs={
                "running_event": running_event,
                "exit_event": exit_event,
                "config": config,
            },
        )

        stimulate_thread.start()
        running_event.wait()
        return exit_event

    def basic_loop(exit_event: Event):
        while step_target_seconds - monotonic() > 0.1:
            event, values = window.read(timeout=100)

            if event in (sg.WIN_CLOSED, "Exit"):
                exit_event.set()
                window.close()
                exit()
            elif event == sg.TIMEOUT_EVENT:
                hours, remain_seconds = divmod(
                    int(step_target_seconds - monotonic()), 3600
                )
                minutes, seconds = divmod(remain_seconds, 60)
                window["-TIME-"].update(f"{hours:02d}:{minutes:02d}:{seconds:02d}")
                window.refresh()

    for i in range(config["session_number"]):
        exit_event = run_session()
        step_target_seconds = monotonic() + config["session_duration"]
        window["-SESSION-N-"].update(i + 1)
        window["-STATUS-"].update("RUNNING")
        window.refresh()

        basic_loop(exit_event)

        if i < config["session_number"] - 1:
            window["-STATUS-"].update("PAUSING")
            window.refresh()
            step_target_seconds = monotonic() + config["session_intervals"]
            basic_loop(exit_event)

    else:
        save_popup = sg.popup_ok_cancel(
            "Stimulating Finished!",
            "Save the record?",
            font=(None, 20),
            keep_on_top=True,
        )
        if save_popup == "OK":
            record()
        window.close()


def setting_window() -> None:
    """设置窗口"""

    stimu_layout = [
        [
            sg.Text(text="Frequency", font=(None, 16)),
            sg.Input(
                default_text="40",
                font=(None, 16),
                size=(3, 1),
                justification="right",
                key="-STIMU-FREQ-",
            ),
            sg.Text(text="Hz", font=(None, 16)),
        ],
        [
            sg.Text(text="Session Number", font=(None, 16)),
            sg.Input(
                default_text="2",
                font=(None, 16),
                size=(2, 1),
                justification="right",
                key="-STIMU-SESSION-N-",
            ),
        ],
        [
            sg.Text(text="Session Duration", font=(None, 16)),
            sg.Input(
                default_text="1800",
                font=(None, 16),
                size=(5, 1),
                justification="right",
                key="-STIMU-DURA-",
            ),
            sg.Text(text="s", font=(None, 16)),
        ],
        [
            sg.Text(text="Session Intervals", font=(None, 16)),
            sg.Input(
                default_text="60",
                font=(None, 16),
                size=(3, 1),
                justification="right",
                key="-STIMU-SESSION-I-",
            ),
            sg.Text(text="s", font=(None, 16)),
        ],
        [
            sg.Text(text="Delay", font=(None, 16)),
            sg.Input(
                default_text="0.0",
                font=(None, 16),
                size=(5, 1),
                justification="right",
                key="-STIMU-DELAY-",
            ),
            sg.Text(text="ms", font=(None, 16)),
        ],
    ]

    audio_layout = [
        [
            sg.Radio(
                text="Sine",
                group_id="waveform",
                key="-AUDIO-SINE-",
                font=(None, 16),
                default=True,
            ),
            sg.Radio(
                text="Rectangular",
                group_id="waveform",
                key="-AUDIO-RECTANGULAR-",
                font=(None, 16),
            ),
            sg.Radio(
                text="Triangular",
                group_id="waveform",
                key="-AUDIO-TRIANGULAR-",
                font=(None, 16),
            ),
        ],
        [
            sg.Text(text="Frequency", font=(None, 16)),
            sg.Input(
                default_text="10000",
                font=(None, 16),
                size=(6, 1),
                justification="right",
                key="-AUDIO-FREQ-",
            ),
            sg.Text(text="Hz", font=(None, 16)),
        ],
        [
            sg.Text(text="Duty Cycle", font=(None, 16)),
            sg.Input(
                default_text="0.04",
                font=(None, 16),
                size=(5, 1),
                justification="right",
                key="-AUDIO-DUTY-",
            ),
        ],
    ]

    light_layout = [
        [
            sg.Text(text="Duty Cycle", font=(None, 16)),
            sg.Input(
                default_text="0.5",
                font=(None, 16),
                size=(5, 1),
                justification="right",
                key="-LIGHT-DUTY-",
            ),
        ],
    ]
    main_layout = [
        [
            sg.Frame(
                title="Stimulating Setting",
                layout=stimu_layout,
                font=(None, 18, "bold"),
            )
        ],
        [
            sg.Frame(
                title="Audio Setting",
                layout=audio_layout,
                font=(None, 18, "bold"),
            )
        ],
        [
            sg.Frame(
                title="Light Setting",
                layout=light_layout,
                font=(None, 18, "bold"),
            )
        ],
        [
            sg.Column(
                [
                    [
                        sg.Save(font=(None, 14)),
                        sg.OK(font=(None, 30)),
                        sg.Exit(font=(None, 14)),
                    ]
                ],
            )
        ],
    ]

    window = sg.Window(
        title="Digital Stimulation - Setting",
        layout=main_layout,
        size=(720, 480),
        element_justification="center",
        finalize=True,
    )

    if exists("settings"):
        window.load_from_disk("settings")

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, "Exit"):
            window.close()
            break
        elif event == "Save":
            window.save_to_disk("settings")
        elif event == "OK":
            global config
            config = {
                "audio_stimulating_frequency": int(window["-STIMU-FREQ-"].get()),
                "audio_stimulating_duty_cycle": float(window["-AUDIO-DUTY-"].get()),
                "audio_duration": int(window["-STIMU-DURA-"].get()) * 1000,
                "audio_generator": None,
                "audio_generator_frequency": int(window["-AUDIO-FREQ-"].get()),
                "audio_generator_duty_cycle": 0.5,
                "audio_generator_frame_rate": 48000,
                "audio_generator_bit_depth": 16,
                "light_stimulating_frequency": int(window["-STIMU-FREQ-"].get()),
                "light_stimulating_duty_cycle": float(window["-LIGHT-DUTY-"].get()),
                "delay_time": float(window["-STIMU-DELAY-"].get()),
                "session_number": int(window["-STIMU-SESSION-N-"].get()),
                "session_duration": int(window["-STIMU-DURA-"].get()),
                "session_intervals": int(window["-STIMU-SESSION-I-"].get()),
                "start_time": str(datetime.now()),
                "operator": None,
                "experiment_id": None,
            }
            if window["-AUDIO-SINE-"].get():
                config["audio_generator"] = "sine"
            elif window["-AUDIO-RECTANGULAR-"].get():
                config["audio_generator"] = "pulse"
            elif window["Triangular"].get():
                config["audio_generator"] = "sawtooth"

            window.close()

            running_window()


def record() -> None:
    global config
    if exists("record.csv"):
        with open("record.csv", "a", newline="") as file:
            writer = DictWriter(file, config.keys())
            writer.writerow(config)
    else:
        with open("record.csv", "x", newline="") as file:
            writer = DictWriter(file, config.keys())
            writer.writeheader()
            writer.writerow(config)


def main() -> None:
    sg.theme("LightBlue")
    loading_window()
    setting_window()


if __name__ == "__main__":
    main()