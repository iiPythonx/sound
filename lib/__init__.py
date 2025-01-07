# Copyright (c) 2025 iiPython

# Initialize Pyaudio
import pyaudio
audio = pyaudio.PyAudio()

# Handle tone data
AVAILABLE_TONES = {
    200:  "0",
    3000: "1",  # My specific mic sucks at picking up 300Hz
    400:  "2",
    500:  "3",
    600:  "4",
    700:  "5",
    800:  "6",
    900:  "7",
    1000: "8",
    1100: "9",
    1200: "A",
    1300: "B",
    1400: "C",
    1500: "D",
    1600: "E",
    1700: "F",
    1800: "START",
    1900: "STOP"
}
