import faiss
import numpy as np

"""
    Splits a given text into chunks of a specified size.

    Parameters:
    - text (str): The text to be chunked.
    - chunk_size (int): The number of words per chunk.

    Returns:
    - list: A list of text chunks.
"""
def chunk_text(text, chunk_size=500, overlap=50):
    if not text or chunk_size <= 0 or overlap >= chunk_size:
        return []

    chunks = []
    words = text.split()
    step_size = chunk_size - overlap

    for i in range(0, len(words), step_size):
        chunk = ' '.join(words[i:i+chunk_size])
        chunks.append(chunk)
    return chunks


"""
Stores given embeddings in a Faiss index.

Parameters:
- embeddings (np.ndarray): The embeddings to store.

Returns:
- faiss.IndexFlatL2: The Faiss index containing the embeddings.
"""
def store_embeddings(embeddings):
    if embeddings is None or not isinstance(embeddings, np.ndarray):
        raise ValueError("Embeddings must be a numpy array.")

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    try:
        index.add(embeddings)
    except Exception as e:
        raise ValueError(f"Failed to add embeddings to the index: {e}")
    return index

"""
Saves a Faiss index to a file.

Parameters:
- index (faiss.IndexFlatL2): The Faiss index to save.
- file_path (str): The path to the file where the index will be saved.
"""
def save_index(index, file_path):

    try:
        faiss.write_index(index, file_path)
    except Exception as e:
        raise IOError(f"Failed to save index to {file_path}: {e}")
    
"""
    Loads a Faiss index from a file.

    Parameters:
    - file_path (str): The path to the file from which to load the index.

    Returns:
    - faiss.IndexFlatL2: The loaded Faiss index.
"""
def load_index(file_path):
    
    try:
        return faiss.read_index(file_path)
    except Exception as e:
        raise IOError(f"Failed to load index from {file_path}: {e}")