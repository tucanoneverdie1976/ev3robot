#!/usr/bin/env python3
import os
import subprocess
import time


MOTOR_ROOT = "/sys/class/tacho-motor"
MOTOR_PORTS = ("ev3-ports:outA", "ev3-ports:outB")

SPEED_SP = 1050
DRIVE_TIME_MS = 1000
PAUSE_BETWEEN_MOVES_SEC = 0.2
RAMP_UP_MS = 0
RAMP_DOWN_MS = 0

BEEP_FREQ_HZ = 880
BEEP_TIME_MS = 250


def read_text(path):
    with open(path, "r") as handle:
        return handle.read().strip()


def write_text(path, value):
    with open(path, "w") as handle:
        handle.write(str(value))


def find_motor_by_port(port):
    for name in os.listdir(MOTOR_ROOT):
        motor_path = os.path.join(MOTOR_ROOT, name)
        address_path = os.path.join(motor_path, "address")
        if os.path.exists(address_path) and read_text(address_path) == port:
            return motor_path
    raise RuntimeError("No motor found on {}".format(port))


def beep():
    try:
        subprocess.call(
            ["beep", "-f", str(BEEP_FREQ_HZ), "-l", str(BEEP_TIME_MS)]
        )
    except OSError:
        print("\a")


def stop_motors(motors):
    for motor in motors:
        try:
            write_text(os.path.join(motor, "command"), "stop")
        except IOError:
            pass


def run_timed(motors, speed_sp, time_ms):
    stop_motors(motors)
    time.sleep(0.05)

    for motor in motors:
        write_text(os.path.join(motor, "stop_action"), "coast")
        write_text(os.path.join(motor, "ramp_up_sp"), RAMP_UP_MS)
        write_text(os.path.join(motor, "ramp_down_sp"), RAMP_DOWN_MS)
        write_text(os.path.join(motor, "speed_sp"), speed_sp)
        write_text(os.path.join(motor, "time_sp"), time_ms)

    for motor in motors:
        write_text(os.path.join(motor, "command"), "run-timed")

    deadline = time.time() + (time_ms / 1000.0) + 2.0
    while time.time() < deadline:
        states = [
            read_text(os.path.join(motor, "state")).split()
            for motor in motors
        ]
        if not any("running" in state for state in states):
            break
        time.sleep(0.05)

    stop_motors(motors)


def main():
    motors = [find_motor_by_port(port) for port in MOTOR_PORTS]

    beep()
    run_timed(motors, SPEED_SP, DRIVE_TIME_MS)
    time.sleep(PAUSE_BETWEEN_MOVES_SEC)
    run_timed(motors, -SPEED_SP, DRIVE_TIME_MS)


if __name__ == "__main__":
    main()
