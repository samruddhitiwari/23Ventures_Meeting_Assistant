import numpy as np
import spacy

nlp = spacy.load("en_core_web_md")

def get_embedding(text):
    """Generate a single embedding for the entire text."""
    doc = nlp(text)
    vectors = np.array([token.vector for token in doc if token.has_vector])

    if len(vectors) == 0:
        return np.zeros(nlp("test").vector.shape)  # Default zero vector if no embeddings exist

    return np.mean(vectors, axis=0)  # Average word embeddings to create a sentence-level vector
