# Copyright (c) 2025 iiPython

# Modules
import math
import time
import json
from pathlib import Path

import click
import brotli

from lib import AVAILABLE_TONES
from lib.sine import generate_tone
from lib.microphone import listen_for_frequency

# Initialization

# Commands
@click.group()
def group_dialup() -> None:
    """Tool to send files and other data through sound waves.
    Copyright (c) 2025 iiPython"""
    pass

@group_dialup.command("calibrate")
@click.option("--fast", "-f", is_flag = True, help = "Enable faster transmission, at the cost of accuracy.")
def command_calibrate(fast: bool) -> None:
    """Calibrate the connection between two devices."""
    match input("Calibrate the connection on the (1) send side, or (2) the receive side?\n> "):
        case "1":
            for elapsed in range(5):
                print(f"Calibration begins in {5 - elapsed}...\r", end = "", flush = True)
                time.sleep(1)

            print()
            for tone, value in AVAILABLE_TONES.items():
                print(f"{tone}Hz\t| Mapped value: {value}\t| Sending...", end = "", flush = True)
                generate_tone(tone, 2, 1)
                print(f"\033[2K\r{tone}Hz\t| Mapped value: {value}\t| Sent!")

        case "2":
            calibrated_tones = {}
            for tone, value in AVAILABLE_TONES.items():
                print(f"{tone}Hz\t| Normal: N/A\t\t| Mapped value: {value}\t| Calibrating...", end = "", flush = True)

                while True:
                    calibrated_value = listen_for_frequency(fast)
                    if calibrated_value is None:
                        exit("Failed calibration!")

                    if calibrated_value not in calibrated_tones and calibrated_value:
                        break

                print(f"\033[2K\r{tone}Hz\t| Normal: {calibrated_value}Hz \t| Mapped value: {value}\t| Calibrated!")
                calibrated_tones[calibrated_value] = tone

            Path("calibration.json").write_text(json.dumps(calibrated_tones, indent = 4))
            print("Calibration complete!")

@group_dialup.command("receive")
@click.argument("file", type = Path)
@click.option("--fast", "-f", is_flag = True, help = "Enable faster transmission, at the cost of accuracy. Must be enabled on both sides.")
def command_receive(file: Path, fast: bool) -> None:
    """Receive a file from a remote system."""
    calibration_data = {int(k): v for k, v in json.loads(Path("calibration.json").read_text()).items()}

    print("Now receiving a file...")

    total_value = ""
    while True:
        received_value = listen_for_frequency(fast)
        if received_value is None:
            break

        actual_value = calibration_data.get(received_value)
        if actual_value is None:
            print("Received an unknown frequency! Recalibrating is recommended!")
            exit()

        hex_value = AVAILABLE_TONES[actual_value]
        print(f"[Recv] {hex_value}")
        if hex_value == "START":
            continue

        if hex_value == "STOP":
            break

        total_value += hex_value

    file.write_bytes(brotli.decompress(bytes.fromhex(total_value)))
    print(len(total_value), "bytes written to", file.name)

@group_dialup.command("send")
@click.option("--fast", "-f", is_flag = True, help = "Enable faster transmission, at the cost of accuracy. Must be enabled on both sides.")
@click.argument("file", type = Path)
def command_send(file: Path, fast: bool) -> None:
    """Send a file to a remote system."""

    file_data = file.read_bytes()
    compressed = brotli.compress(file_data)
    hex_data = compressed.hex().upper()

    print(f"\nFile size: {len(file_data)} bytes | Compressed: {len(compressed)} bytes | Hex: {len(hex_data)} chars")

    reversed_tone_map = {v: k for k, v in AVAILABLE_TONES.items()}
    def send_tone(index: int, tone_code: str) -> None:
        percent = index / len(hex_data)
        print(
            f"\033[2K{str(index + 1).zfill(4)}/{str(len(hex_data)).zfill(4)} {tone_code}\t[{'#' * round(32 * percent)}{' ' * (32 - round(32 * percent))}]\r",
            end = "",
            flush = True
        )
        generate_tone(
            reversed_tone_map[tone_code],
            .3 if fast else 1,
            1.0
        )

    eta = len(hex_data) * (0.611 if fast else 1.071)  # Measured via tone length irl
    minutes = math.floor(eta / 60)
    eta -= (60 * minutes)
    print(f"Send ETA: {minutes} minute(s), {round(eta, 2)} second(s)\n")

    send_tone(0, "START")
    for index, byte in enumerate(hex_data):
        send_tone(index + 1, byte)

    send_tone(len(file_data) + 1, "STOP")

if __name__ == "__main__":
    group_dialup()
