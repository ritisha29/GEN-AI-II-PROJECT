import chromadb
from chromadb.config import Settings as ChromaSettings
from sentence_transformers import SentenceTransformer
from app.core.config import get_settings
from typing import List, Dict, Any

settings = get_settings()

class VectorStoreService:
    def __init__(self):
        # Initialize the Sentence Transformer model
        self.model = SentenceTransformer(settings.EMBEDDING_MODEL_NAME)
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(path=settings.CHROMA_DB_DIR)
        
        # Get or create the collection
        self.collection = self.client.get_or_create_collection(
            name=settings.COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"} # Use cosine similarity
        )

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generates embeddings for a list of texts."""
        embeddings = self.model.encode(texts)
        return embeddings.tolist()

    def add_documents(self, documents: List[str], metadatas: List[Dict[str, Any]], ids: List[str]):
        """Adds documents to the ChromaDB collection."""
        embeddings = self.generate_embeddings(documents)
        self.collection.add(
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

    def search(self, query: str, top_k: int = 5) -> Dict[str, Any]:
        """Searches the Vector DB for the most relevant documents."""
        query_embedding = self.generate_embeddings([query])
        
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=top_k,
            include=["documents", "metadatas", "distances"]
        )
        return results

# Create a singleton instance to be used across the application
vector_store = VectorStoreService()
