import chromadb
from chromadb.utils import embedding_functions
import os

class NeuralMemory:
    def __init__(self, path: str = "./memory_db"):
        self.client = chromadb.PersistentClient(path=path)
        self.embedding_fn = embedding_functions.DefaultEmbeddingFunction()
        self.collection = self.client.get_or_create_collection(
            name="aether_memory",
            embedding_function=self.embedding_fn
        )

    def store(self, content: str, metadata: dict = None, id: str = None):
        """Store a piece of information in vector memory."""
        import uuid
        if not id: id = str(uuid.uuid4())
        self.collection.add(
            documents=[content],
            metadatas=[metadata] if metadata else [{}],
            ids=[id]
        )
        return id

    def query(self, text: str, n_results: int = 3):
        """Retrieve relevant context from memory."""
        results = self.collection.query(
            query_texts=[text],
            n_results=n_results
        )
        return results["documents"][0]

memory = NeuralMemory()
