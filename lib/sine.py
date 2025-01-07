# Copyright (c) 2025 iiPython

# Modules
import math

from . import audio

# Handle tone generation
# https://stackoverflow.com/questions/974071/python-library-for-playing-fixed-frequency-sound
def generate_tone(frequency: int, duration: float, volume: float = 1, sample_rate = 22050) -> None:
    n_samples = int(sample_rate * duration)
    restframes = n_samples % sample_rate

    stream = audio.open(
        format = audio.get_format_from_width(1),
        channels = 1,
        rate = sample_rate,
        output = True
    )

    def process(sample: float) -> float:
        return volume * math.sin(2 * math.pi * frequency * sample / sample_rate)

    samples = (int(process(t) * 0x7f + 0x80) for t in range(n_samples))
    for buf in zip(*[samples] * sample_rate):
        stream.write(bytes(bytearray(buf)))

    stream.write(b"\x80" * restframes)
    stream.stop_stream()
    stream.close()
