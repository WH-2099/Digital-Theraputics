from time import sleep
from threading import Event


def f(running_event: Event, exit_event: Event, config: dict):
    sleep(1.5)
    running_event.set()
    print("RUNNING")
    sleep(config["audio_duration"] / 1000)

    print("DONE")
