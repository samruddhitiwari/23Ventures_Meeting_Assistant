import sys
print("Python version:", sys.version)
print("Installed packages:", sys.modules.keys())

import tensorflow as tf
print("TensorFlow version:", tf.__version__)

from tensorflow import keras
print("Keras version:", keras.__version__)
print("Importing FastAPI...")
from fastapi import FastAPI, UploadFile, File
print("FastAPI imported.")

print("Importing record_meeting...")
from record import record_meeting
print("record_meeting imported.")

print("Importing transcribe...")
from transcribe import transcribe
print("transcribe imported.")

print("Importing summarize_main...")
from summarize import main as summarize_main
print("summarize_main imported.")

print("Importing query_faiss...")
from search import query_faiss
print("query_faiss imported.")

app = FastAPI()

@app.post("/record")
def start_recording():
    record_meeting()
    return "Recording started!"

@app.post("/stop")
def stop_recording():
    return "Recording stopped!"

@app.post("/summarize")
def summarize(file: UploadFile = File(...)):
    content = file.file.read().decode("utf-8")
    summary = summarize_main(content)
    return summary

@app.get("/search")
def search(query: str):
    return query_faiss(query)


from fastapi import FastAPI
app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}
