import subprocess
import sys
import os
from datetime import datetime

def transcribe(input_path: str):
    try:
        # Get current datetime
        now = datetime.now()
        year = now.strftime("%Y")
        month = now.strftime("%m")
        day = now.strftime("%d")
        time_str = now.strftime("%H-%M-%S")  # e.g., 13-45-30

        # Create folder structure: ./YYYY/MM/DD/
        output_dir = os.path.join(os.getcwd(), year, month, day)
        os.makedirs(output_dir, exist_ok=True)

        # Define output file path
        output_txt = os.path.join(output_dir, f"{time_str}.txt")

        # Command to run whisper-cli
        cmd = [
            r"C:\Users\Samruddhi\Desktop\independent_test\whisper.cpp\build\bin\Release\whisper-cli.exe",
            "--model", r"C:\Users\Samruddhi\Desktop\independent_test\models\ggml-base.en.bin",
            input_path
        ]

        # Run command and capture output
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)

        # Save transcript to file
        with open(output_txt, "w", encoding="utf-8") as f:
            f.write(result.stdout)

        print(f"[✓] Transcript saved to {output_txt}")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Transcription failed: {e}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error during transcription: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python transcribe.py <input_audio.wav>")
    else:
        transcribe(sys.argv[1])
