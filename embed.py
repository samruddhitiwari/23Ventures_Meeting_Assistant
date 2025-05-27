from sentence_transformers import SentenceTransformer


EMBED_MODEL_NAME = "all-MiniLM-L6-v2"

def load_embedder():
    """Return a SentenceTransformer instance for embedding texts."""
    return SentenceTransformer(EMBED_MODEL_NAME)

def get_embedding(text):
    """
    Generate and return the embedding for the given text using the model.
    Returns a list of floats (the embedding vector).
    """
    model = load_embedder()
    return model.encode(text)
