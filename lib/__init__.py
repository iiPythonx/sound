# Copyright (c) 2025 iiPython

# Initialize Pyaudio
import pyaudio
audio = pyaudio.PyAudio()

# Handle tone data
AVAILABLE_TONES = {
    300:  "0",
    350:  "1",
    400:  "2",
    450:  "3",
    500:  "4",
    550:  "5",
    600:  "6",
    650:  "7",
    700:  "8",
    750:  "9",
    800:  "A",
    850:  "B",
    900:  "C",
    950:  "D",
    1000: "E",
    1050: "F",
    2000: "START",
    3000: "STOP"
}
