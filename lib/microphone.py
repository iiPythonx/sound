# Copyright (c) 2025 iiPython

# Modules
import pyaudio
import numpy as np

from . import audio

# Handle listening
def listen_for_frequency(fast: bool) -> int:

    # Handle calibrating settings for going /fast/
    frame_size = 512 if fast else 1024
    sample_size = 20 if fast else 30

    # Setup stream and everything else
    stream = audio.open(
        format = pyaudio.paInt16,
        channels = 1,
        rate = 44100,
        input = True,
        frames_per_buffer = frame_size
    )

    def close() -> None:
        stream.stop_stream()
        stream.close()

    last_freq, recent_freqs = None, 0
    try:
        while True:
            data = stream.read(frame_size, exception_on_overflow = False)
            audio_data = np.frombuffer(data, dtype = np.int16)
            fft_data = np.fft.fft(audio_data)
            fft_freq = np.fft.fftfreq(len(fft_data), 1 / 44100)
            magnitude = np.abs(fft_data)
            peak_freq = round(abs(fft_freq[np.argmax(magnitude)]))

            # Handle multiple detection
            if last_freq == peak_freq:
                recent_freqs += 1
                if recent_freqs == sample_size:
                    close()
                    return peak_freq

            else:
                last_freq, recent_freqs = peak_freq, 0

    except KeyboardInterrupt:
        exit()
