import os
from typing import List, Dict, Tuple
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

class SRMVectorStore:
    def __init__(self, db_path: str = "./vector_db/srm_insider_db"):
        self.db_path = db_path
        os.makedirs(db_path, exist_ok=True)
        
        # Initialize embedding model
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(
            name="srm_insider_knowledge",
            metadata={"description": "SRM INSIDER knowledge base"}
        )
    
    def add_documents(self, documents: List[Dict], ids: List[str] = None):
       
        if ids is None:
            ids = [f"doc_{i}" for i in range(len(documents))]
        
        # Extract content and metadata
        contents = []
        metadatas = []
        
        for doc in documents:
            content = doc.get('content', '') or doc.get('answer', '') or doc.get('caption', '')
            if content:
                contents.append(content)
                # Create metadata without nested structures
                metadata = {k: str(v) for k, v in doc.items() 
                           if k not in ['content', 'answer', 'caption'] and v is not None}
                metadatas.append(metadata)
        
        if not contents:
            print("No valid content to add")
            return
        
        # Generate embeddings
        embeddings = self.embedding_model.encode(contents).tolist()
        
        # Add to collection
        self.collection.add(
            embeddings=embeddings,
            documents=contents,
            metadatas=metadatas,
            ids=ids[:len(contents)],
        )
        
        print(f"Added {len(contents)} documents to vector store")
    
    def search(self, query: str, n_results: int = 5) -> List[Tuple[str, Dict, float]]:
      
        # Generate query embedding
        query_embedding = self.embedding_model.encode([query]).tolist()
        
        # Search
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=n_results,
            include=["documents", "metadatas", "distances"],
        )
        
        # Format results
        formatted_results = []
        if results['documents'] and results['documents'][0]:
            for i, doc in enumerate(results['documents'][0]):
                metadata = results['metadatas'][0][i] if results['metadatas'] else {}
                distance = results['distances'][0][i] if results['distances'] else 0
                formatted_results.append((doc, metadata, distance))
        
        return formatted_results
    
    def get_collection_stats(self) -> Dict:
        """Get statistics about the collection"""
        return {
            "count": self.collection.count(),
            "name": self.collection.name,
        }
    
    def clear_collection(self):
        """Clear all documents from the collection"""
        self.client.delete_collection("srm_insider_knowledge")
        self.collection = self.client.create_collection(
            name="srm_insider_knowledge",
            metadata={"description": "SRM INSIDER knowledge base"}
        )
        print("Collection cleared")