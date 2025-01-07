import numpy as np
import pyaudio

def listen_for_frequency(frequency: int) -> int | None:
    p = pyaudio.PyAudio()
    stream = p.open(
        format = pyaudio.paInt16,
        channels = 1,
        rate = 44100,
        input = True,
        frames_per_buffer = 1024
    )

    def close() -> None:
        stream.stop_stream()
        stream.close()
        p.terminate()

    last_freq, recent_freqs = None, 0
    try:
        while True:
            data = stream.read(1024, exception_on_overflow = False)
            audio_data = np.frombuffer(data, dtype = np.int16)
            fft_data = np.fft.fft(audio_data)
            fft_freq = np.fft.fftfreq(len(fft_data), 1 / 44100)
            magnitude = np.abs(fft_data)
            peak_freq = abs(fft_freq[np.argmax(magnitude)])

            peak_freq = round(peak_freq)

            # Handle multiple detection
            if last_freq == peak_freq:
            # if abs(peak_freq - frequency) < 5:
                recent_freqs += 1
                if recent_freqs == 30:
                    close()
                    return last_freq

            else:
                print(peak_freq)
                last_freq, recent_freqs = peak_freq, 0
                # recent_freqs = 0
            # if abs(peak_freq - frequency) < 5:
            #     print(f"Detected target frequency: {peak_freq:.2f} Hz")
            #     exit()

            # else:
            #     print(f"Peak frequency: {peak_freq:.2f} Hz")

    except KeyboardInterrupt:
        print("Stopping...")

    finally:
        close()

    return None

if __name__ == "__main__":
    print(listen_for_frequency(1300))
