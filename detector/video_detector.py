import cv2
import numpy as np

def analyze_video(video_path):
    try:
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            print("[ERROR] Cannot open video file")
            return False, "Error opening video"

        frame_count = 0
        suspicious_frames = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Analyze every 30th frame (performance optimization)
            if frame_count % 30 == 0:
                lsb = frame & 1
                unique, counts = np.unique(lsb, return_counts=True)

                print(f"[+] Frame {frame_count} LSB:", dict(zip(unique, counts)))

                if abs(counts[0] - counts[1]) < 1000:
                    suspicious_frames += 1

            frame_count += 1

        cap.release()

        if suspicious_frames > 0:
            print(f"[!] Suspicious frames detected: {suspicious_frames}")
            return True, "Suspicious Video Steganography"
        else:
            print("[+] Video seems clean")
            return False, "Clean Video"

    except Exception as e:
        print("[ERROR]", e)
        return False, "Error processing video"