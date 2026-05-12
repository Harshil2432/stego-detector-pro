import wave
import numpy as np

def detect_audio_stego(audio_path):
    try:
        audio = wave.open(audio_path, mode='rb')
        frames = audio.readframes(audio.getnframes())

        samples = np.frombuffer(frames, dtype=np.int16)
        lsb = samples & 1

        unique, counts = np.unique(lsb, return_counts=True)

        print("[+] Audio LSB Distribution:", dict(zip(unique, counts)))

        if abs(counts[0] - counts[1]) < 500:
            print("[!] Suspicious audio detected")
            return True, "Suspicious Audio Steganography"
        else:
            print("[+] Audio seems clean")
            return False, "Clean Audio"

    except Exception as e:
        print("[ERROR]", e)
        return False, "Error processing audio"