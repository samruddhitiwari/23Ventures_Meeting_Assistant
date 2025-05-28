from transformers import pipeline
from tkinter import Tk, filedialog, messagebox
import os
from datetime import datetime
from embed import get_embedding  # Add this import

def summarize_text_local(text):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summary_list = summarizer(text, max_length=150, min_length=40, do_sample=False)
    return summary_list[0]['summary_text']

def main():
    root = Tk()
    root.withdraw()

    filepath = filedialog.askopenfilename(
        title="Select Transcribed Meeting File",
        filetypes=[("Text Files", "*.txt")]
    )

    if not filepath:
        messagebox.showinfo("No file selected", "Operation cancelled.")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    summary = summarize_text_local(content)

    basename = os.path.basename(filepath)
    try:
        meeting_time = datetime.strptime(basename[:-4], "%H-%M-%S")
        today = datetime.today()
        timestamp = datetime(
            year=today.year,
            month=today.month,
            day=today.day,
            hour=meeting_time.hour,
            minute=meeting_time.minute,
            second=meeting_time.second
        )
    except ValueError:
        timestamp = datetime.now()

    output_dir = os.path.join("summaries", timestamp.strftime("%Y"), timestamp.strftime("%m"), timestamp.strftime("%d"))
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"{timestamp.strftime('%H-%M-%S')}_summary.txt")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(summary)

 
    embedding = get_embedding(summary)
    embedding_file = os.path.join(output_dir, f"{timestamp.strftime('%H-%M-%S')}_summary_embedding.txt")
    with open(embedding_file, 'w', encoding='utf-8') as f:
        f.write(','.join(map(str, embedding)))

    messagebox.showinfo("Success", f"Summary and embedding saved at:\n{output_file}\n{embedding_file}")

if __name__ == "__main__":
    main()
