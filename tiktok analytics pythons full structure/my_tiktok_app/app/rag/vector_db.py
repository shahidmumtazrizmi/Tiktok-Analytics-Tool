"""
Vector database module for RAG system.
"""

from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings
import logging
import json
import os

from ..core.config import settings

logger = logging.getLogger(__name__)


class VectorDatabase:
    """Vector database for storing and retrieving embeddings."""
    
    def __init__(self, collection_name: str = "tiktok_shop_knowledge"):
        self.collection_name = collection_name
        self.client = None
        self.collection = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize ChromaDB client."""
        try:
            # Use persistent storage
            persist_directory = "data/chroma_db"
            os.makedirs(persist_directory, exist_ok=True)
            
            self.client = chromadb.PersistentClient(
                path=persist_directory,
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )
            
            # Get or create collection
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"description": "TikTok Shop knowledge base"}
            )
            
            logger.info(f"Initialized vector database with collection: {self.collection_name}")
            
        except Exception as e:
            logger.error(f"Error initializing vector database: {e}")
            self.client = None
            self.collection = None
    
    def add_documents(
        self,
        documents: List[str],
        metadatas: List[Dict[str, Any]],
        ids: Optional[List[str]] = None
    ) -> bool:
        """Add documents to vector database."""
        try:
            if not self.collection:
                logger.error("Vector database not initialized")
                return False
            
            # Generate IDs if not provided
            if not ids:
                ids = [f"doc_{i}" for i in range(len(documents))]
            
            # Add documents to collection
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            
            logger.info(f"Added {len(documents)} documents to vector database")
            return True
            
        except Exception as e:
            logger.error(f"Error adding documents to vector database: {e}")
            return False
    
    def search(
        self,
        query: str,
        n_results: int = 5,
        where: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Search for similar documents."""
        try:
            if not self.collection:
                logger.error("Vector database not initialized")
                return []
            
            # Search collection
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results,
                where=where,
                include=["documents", "metadatas", "distances"]
            )
            
            # Format results
            formatted_results = []
            if results["documents"] and results["documents"][0]:
                for i, doc in enumerate(results["documents"][0]):
                    result = {
                        "document": doc,
                        "metadata": results["metadatas"][0][i] if results["metadatas"] and results["metadatas"][0] else {},
                        "distance": results["distances"][0][i] if results["distances"] and results["distances"][0] else 0.0
                    }
                    formatted_results.append(result)
            
            logger.info(f"Found {len(formatted_results)} similar documents")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error searching vector database: {e}")
            return []
    
    def get_documents_by_metadata(
        self,
        metadata_filter: Dict[str, Any],
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Get documents by metadata filter."""
        try:
            if not self.collection:
                return []
            
            results = self.collection.query(
                query_texts=[""],  # Empty query to get all documents
                n_results=limit,
                where=metadata_filter,
                include=["documents", "metadatas"]
            )
            
            formatted_results = []
            if results["documents"] and results["documents"][0]:
                for i, doc in enumerate(results["documents"][0]):
                    result = {
                        "document": doc,
                        "metadata": results["metadatas"][0][i] if results["metadatas"] and results["metadatas"][0] else {}
                    }
                    formatted_results.append(result)
            
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error getting documents by metadata: {e}")
            return []
    
    def delete_documents(self, ids: List[str]) -> bool:
        """Delete documents by IDs."""
        try:
            if not self.collection:
                return False
            
            self.collection.delete(ids=ids)
            logger.info(f"Deleted {len(ids)} documents from vector database")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting documents: {e}")
            return False
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get collection statistics."""
        try:
            if not self.collection:
                return {"error": "Collection not initialized"}
            
            count = self.collection.count()
            return {
                "total_documents": count,
                "collection_name": self.collection_name
            }
            
        except Exception as e:
            logger.error(f"Error getting collection stats: {e}")
            return {"error": str(e)}
    
    def reset_collection(self) -> bool:
        """Reset the collection (delete all documents)."""
        try:
            if not self.collection:
                return False
            
            # Delete and recreate collection
            self.client.delete_collection(self.collection_name)
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "TikTok Shop knowledge base"}
            )
            
            logger.info("Reset vector database collection")
            return True
            
        except Exception as e:
            logger.error(f"Error resetting collection: {e}")
            return False


# Global vector database instance
vector_db = VectorDatabase() 