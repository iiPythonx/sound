import pyaudio
import numpy as np

from . import audio

def listen_for_frequency() -> int:
    stream = audio.open(
        format = pyaudio.paInt16,
        channels = 1,
        rate = 44100,
        input = True,
        frames_per_buffer = 1024
    )

    def close() -> None:
        stream.stop_stream()
        stream.close()

    last_freq, recent_freqs = None, 0
    try:
        while True:
            data = stream.read(1024, exception_on_overflow = False)
            audio_data = np.frombuffer(data, dtype = np.int16)
            fft_data = np.fft.fft(audio_data)
            fft_freq = np.fft.fftfreq(len(fft_data), 1 / 44100)
            magnitude = np.abs(fft_data)
            peak_freq = round(abs(fft_freq[np.argmax(magnitude)]))

            # Handle multiple detection
            if last_freq == peak_freq:
                recent_freqs += 1
                if recent_freqs == 30:
                    close()
                    return peak_freq

            else:
                last_freq, recent_freqs = peak_freq, 0

    except KeyboardInterrupt:
        exit()
