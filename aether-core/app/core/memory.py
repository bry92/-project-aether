import chromadb
from chromadb.utils import embedding_functions
from app.core.supabase import supabase
import os
import uuid

class NeuralMemory:
    def __init__(self, path: str = "./memory_db"):
        self.client = chromadb.PersistentClient(path=path)
        self.embedding_fn = embedding_functions.DefaultEmbeddingFunction()
        self.collection = self.client.get_or_create_collection(
            name="aether_memory",
            embedding_function=self.embedding_fn
        )

    def store(self, content: str, metadata: dict = None, id: str = None):
        """Store a piece of information in vector memory and Supabase."""
        if not id: id = str(uuid.uuid4())
        
        # Local Vector Storage
        self.collection.add(
            documents=[content],
            metadatas=[metadata] if metadata else [{}],
            ids=[id]
        )
        
        # Supabase Persistence (PostgreSQL)
        try:
            supabase.table("memory").insert({
                "id": id,
                "content": content,
                "metadata": metadata
            }).execute()
        except Exception as e:
            print(f"Supabase store error: {e}")
            
        return id

    def query(self, text: str, n_results: int = 3):
        """Retrieve relevant context from memory."""
        # Query local vector db for speed and semantic search
        results = self.collection.query(
            query_texts=[text],
            n_results=n_results
        )
        return results["documents"][0]

memory = NeuralMemory()
