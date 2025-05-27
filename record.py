import os
import subprocess
from datetime import datetime
from transcribe import transcribe  # import from transcribe.py

def record_meeting():
    # Create timestamped path
    now = datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")
    time_str = now.strftime("%H-%M-%S")

    recording_dir = os.path.join(os.getcwd(), "recordings", year, month, day)
    os.makedirs(recording_dir, exist_ok=True)

    audio_path = os.path.join(recording_dir, f"{time_str}.wav")

    print(f"[●] Recording... Press Ctrl+C to stop.")

    try:
        # Adjust your audio device names as needed
        # List devices: ffmpeg -list_devices true -f dshow -i dummy
        cmd = [
            "ffmpeg",
            "-f", "dshow",
            "-i", "audio=Microphone Array (Intel® Smart Sound Technology for Digital Microphones)",  # For system + mic audio
            "-acodec", "pcm_s16le",
            "-ar", "44100",
            "-ac", "2",
            audio_path
        ]
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("[⏹] Recording stopped.")
    except Exception as e:
        print(f"[✗] Error: {e}")
        return

    print(f"[✓] Audio saved to: {audio_path}")
    print("[→] Starting transcription...")
    transcribe(audio_path)

if __name__ == "__main__":
    record_meeting()
