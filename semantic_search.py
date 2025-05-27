import os
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Tuple

# Constants - adjust to your paths
MEETINGS_DIR = os.path.join(os.getcwd(), "recordings")  # or wherever your transcripts are saved
SUMMARIES_DIR = os.path.join(os.getcwd(), "summaries")  # your summaries folder
INDEX_DIR = os.path.join(os.getcwd(), "faiss_index")    # folder to save index and metadata

os.makedirs(INDEX_DIR, exist_ok=True)

# Load embedding model once
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
embedder = SentenceTransformer(EMBEDDING_MODEL_NAME)

# Chunk size for splitting large texts (characters)
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

def chunk_text(text: str, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP) -> List[str]:
    """Split long text into overlapping chunks."""
    chunks = []
    start = 0
    text_len = len(text)
    while start < text_len:
        end = min(start + chunk_size, text_len)
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

def load_texts_from_folder(folder_path: str) -> List[Tuple[str, str]]:
    """Recursively load .txt files from folder; return list of (filepath, content)."""
    texts = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".txt"):
                full_path = os.path.join(root, file)
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    texts.append((full_path, content))
                except Exception as e:
                    print(f"Failed to read {full_path}: {e}")
    return texts

def prepare_corpus(meetings_folder: str, summaries_folder: str):
    """
    Load transcripts and summaries, chunk them, and prepare list of (chunk_text, source_path).
    Returns:
        corpus_chunks: list of chunk strings
        metadata: list of dicts { 'source': filepath, 'chunk_id': int }
    """
    corpus_chunks = []
    metadata = []

    # Load and chunk transcripts
    transcripts = load_texts_from_folder(meetings_folder)
    for filepath, content in transcripts:
        chunks = chunk_text(content)
        for idx, chunk in enumerate(chunks):
            corpus_chunks.append(chunk)
            metadata.append({"source": filepath, "chunk_id": idx, "type": "transcript"})

    # Load and chunk summaries
    summaries = load_texts_from_folder(summaries_folder)
    for filepath, content in summaries:
        chunks = chunk_text(content)
        for idx, chunk in enumerate(chunks):
            corpus_chunks.append(chunk)
            metadata.append({"source": filepath, "chunk_id": idx, "type": "summary"})

    return corpus_chunks, metadata

def build_faiss_index(corpus_chunks: List[str]):
    """
    Embed all chunks and build FAISS index.
    Returns:
        index: FAISS index object
        embeddings: numpy array of embeddings
    """
    print("[*] Encoding chunks with embedding model...")
    embeddings = embedder.encode(corpus_chunks, convert_to_numpy=True, show_progress_bar=True)
    dimension = embeddings.shape[1]

    print(f"[*] Creating FAISS index with dimension: {dimension}")
    index = faiss.IndexFlatIP(dimension)  # Using Inner Product (cosine similarity if embeddings normalized)

    # Normalize embeddings for cosine similarity
    faiss.normalize_L2(embeddings)
    index.add(embeddings)
    print(f"[*] Indexed {index.ntotal} chunks.")

    return index, embeddings

def save_index_and_metadata(index, metadata, index_path, meta_path):
    print("[*] Saving FAISS index and metadata...")
    faiss.write_index(index, index_path)
    with open(meta_path, 'wb') as f:
        pickle.dump(metadata, f)
    print("[✓] Saved successfully.")

def load_index_and_metadata(index_path, meta_path):
    print("[*] Loading FAISS index and metadata...")
    if not os.path.exists(index_path) or not os.path.exists(meta_path):
        raise FileNotFoundError("Index or metadata files not found. Build the index first.")
    index = faiss.read_index(index_path)
    with open(meta_path, 'rb') as f:
        metadata = pickle.load(f)
    print("[✓] Loaded successfully.")
    return index, metadata

def search(query: str, index, metadata, corpus_chunks: List[str], top_k=5):
    """
    Search query in the FAISS index.
    Returns a list of dict with keys: 'source', 'chunk_id', 'text', 'score'.
    """
    print(f"[*] Searching for query: {query}")
    query_vec = embedder.encode([query], convert_to_numpy=True)
    faiss.normalize_L2(query_vec)

    distances, indices = index.search(query_vec, top_k)
    results = []
    for dist, idx in zip(distances[0], indices[0]):
        if idx == -1:
            continue
        results.append({
            "source": metadata[idx]["source"],
            "chunk_id": metadata[idx]["chunk_id"],
            "text": corpus_chunks[idx],
            "score": float(dist)
        })
    return results

# Paths for index and metadata persistence
INDEX_FILE = os.path.join(INDEX_DIR, "faiss.index")
METADATA_FILE = os.path.join(INDEX_DIR, "metadata.pkl")

def build_or_load_index():
    """
    Build the index from transcripts & summaries or load existing index.
    """
    if os.path.exists(INDEX_FILE) and os.path.exists(METADATA_FILE):
        return load_index_and_metadata(INDEX_FILE, METADATA_FILE)
    
    print("[*] Building new FAISS index...")
    corpus_chunks, metadata = prepare_corpus(MEETINGS_DIR, SUMMARIES_DIR)
    index, embeddings = build_faiss_index(corpus_chunks)
    save_index_and_metadata(index, metadata, INDEX_FILE, METADATA_FILE)
    return index, metadata, corpus_chunks

def run_search_interface():
    """
    Minimal CLI interface to query the indexed data.
    """
    index, metadata, corpus_chunks = None, None, None
    try:
        index, metadata = load_index_and_metadata(INDEX_FILE, METADATA_FILE)
        # Load corpus_chunks from metadata - actually we must save corpus_chunks for retrieval, or rebuild.
        # For simplicity, rebuild corpus_chunks now
        transcripts = load_texts_from_folder(MEETINGS_DIR)
        summaries = load_texts_from_folder(SUMMARIES_DIR)
        all_texts = [chunk for _, content in transcripts+summaries for chunk in chunk_text(content)]
        corpus_chunks = all_texts
    except FileNotFoundError:
        print("[!] No existing index found, building from scratch...")
        corpus_chunks, metadata = prepare_corpus(MEETINGS_DIR, SUMMARIES_DIR)
        index, _ = build_faiss_index(corpus_chunks)
        save_index_and_metadata(index, metadata, INDEX_FILE, METADATA_FILE)

    print("=== Semantic Search Interface ===")
    print("Type 'exit' to quit.")
    while True:
        query = input("Enter your query: ").strip()
        if query.lower() == 'exit':
            break
        results = search(query, index, metadata, corpus_chunks)
        if not results:
            print("No relevant results found.")
            continue
        for i, res in enumerate(results):
            print(f"\n[{i+1}] Score: {res['score']:.4f}")
            print(f"Source file: {res['source']}")
            print(f"Excerpt:\n{res['text'][:500]}...\n")

if __name__ == "__main__":
    run_search_interface()
