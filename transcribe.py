import subprocess
import sys
import os
from datetime import datetime
from query_parser import parse_query
from embed import get_embedding
import spacy

nlp = spacy.load("en_core_web_sm")

def transcribe(input_path: str):
    try:
        now = datetime.now()
        output_dir = os.path.join(os.getcwd(), now.strftime("%Y"), now.strftime("%m"), now.strftime("%d"))
        os.makedirs(output_dir, exist_ok=True)

        output_txt = os.path.join(output_dir, f"{now.strftime('%H-%M-%S')}.txt")

        cmd = [
            r"C:\Users\Samruddhi\Desktop\independent_test\whisper.cpp\build\bin\Release\whisper-cli.exe",
            "--model", r"C:\Users\Samruddhi\Desktop\independent_test\models\ggml-base.en.bin",
            input_path
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, check=True)

        with open(output_txt, "w", encoding="utf-8") as f:
            f.write(result.stdout)

        print(f"[✓] Transcript saved to {output_txt}")

        # === Process Transcript with Spacy ===
        with open(output_txt, "r", encoding="utf-8") as f:
            transcript = f.read()

        doc = nlp(transcript)
        tokens = [token.text for token in doc]

        parsed_data = parse_query(transcript)
        parsed_output_file = os.path.join(output_dir, f"{now.strftime('%H-%M-%S')}_parsed.txt")

        with open(parsed_output_file, "w", encoding="utf-8") as f:
            f.write("Parsed Info:\n")
            f.write(f"Tokens:\n{tokens}\n")
            f.write(f"Date Ranges:\n{parsed_data['date_ranges']}\n")
            f.write(f"Actions:\n{parsed_data['actions']}\n")
            f.write(f"Topics:\n{parsed_data['topics']}\n")

        print(f"[✓] Parsed data saved to {parsed_output_file}")

        # === Generate Embeddings ===
        embedding = get_embedding(transcript)
        embedding_file = os.path.join(output_dir, f"{now.strftime('%H-%M-%S')}_embedding.txt")
        with open(embedding_file, "w", encoding="utf-8") as f:
            f.write(','.join(map(str, embedding)))

        print(f"[✓] Embedding saved to {embedding_file}")

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Transcription failed: {e}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error during transcription: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python transcribe.py <input_audio.wav>")
    else:
        transcribe(sys.argv[1])
