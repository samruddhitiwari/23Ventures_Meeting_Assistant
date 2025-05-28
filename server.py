from fastapi import FastAPI, UploadFile, File
from record import record_meeting
from transcribe import transcribe
from summarize import main as summarize_main
from search import query_faiss

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
