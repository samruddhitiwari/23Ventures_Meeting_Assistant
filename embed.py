import spacy
import os

model_path = os.path.join(spacy.util.get_package_path("en_core_web_md"))  # Get the installed model path
nlp = spacy.load(model_path)  # Load explicitly from the correct location

def get_embedding(text):
    """Generate a single embedding for the entire text."""
    doc = nlp(text)
    vectors = np.array([token.vector for token in doc if token.has_vector])

    if len(vectors) == 0:
        return np.zeros(nlp("test").vector.shape)  # Default zero vector if no embeddings exist

    return np.mean(vectors, axis=0)  # Average word embeddings to create a sentence-level vector
