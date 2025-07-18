"""
Embeddings module for RAG system.
"""

from typing import List, Dict, Any, Optional
from langchain.embeddings import HuggingFaceEmbeddings, OpenAIEmbeddings
from langchain.schema import Document
import numpy as np
import logging
import json

from ..core.config import settings

logger = logging.getLogger(__name__)


class EmbeddingManager:
    """Manages text embeddings for RAG system."""
    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model_name = model_name
        
        # Initialize embeddings model
        if settings.OPENAI_API_KEY:
            self.embeddings = OpenAIEmbeddings(
                openai_api_key=settings.OPENAI_API_KEY,
                model="text-embedding-ada-002"
            )
        else:
            self.embeddings = HuggingFaceEmbeddings(
                model_name=model_name,
                model_kwargs={'device': 'cpu'}
            )
    
    def embed_text(self, text: str) -> List[float]:
        """Embed a single text string."""
        try:
            embedding = self.embeddings.embed_query(text)
            return embedding
        except Exception as e:
            logger.error(f"Error embedding text: {e}")
            return []
    
    def embed_documents(self, documents: List[str]) -> List[List[float]]:
        """Embed multiple documents."""
        try:
            embeddings = self.embeddings.embed_documents(documents)
            return embeddings
        except Exception as e:
            logger.error(f"Error embedding documents: {e}")
            return []
    
    def embed_langchain_documents(self, documents: List[Document]) -> List[List[float]]:
        """Embed LangChain documents."""
        texts = [doc.page_content for doc in documents]
        return self.embed_documents(texts)
    
    def similarity_search(
        self,
        query: str,
        documents: List[Document],
        k: int = 5
    ) -> List[Document]:
        """Find most similar documents to query."""
        try:
            # Get query embedding
            query_embedding = self.embed_text(query)
            if not query_embedding:
                return documents[:k]
            
            # Get document embeddings
            doc_embeddings = self.embed_langchain_documents(documents)
            
            # Calculate similarities
            similarities = []
            for doc_emb in doc_embeddings:
                if doc_emb:
                    similarity = self._cosine_similarity(query_embedding, doc_emb)
                    similarities.append(similarity)
                else:
                    similarities.append(0.0)
            
            # Sort documents by similarity
            doc_similarity_pairs = list(zip(documents, similarities))
            doc_similarity_pairs.sort(key=lambda x: x[1], reverse=True)
            
            # Return top k documents
            top_docs = [doc for doc, _ in doc_similarity_pairs[:k]]
            
            # Add similarity scores to metadata
            for i, (doc, similarity) in enumerate(doc_similarity_pairs[:k]):
                if i < len(top_docs):
                    top_docs[i].metadata['similarity_score'] = similarity
            
            return top_docs
            
        except Exception as e:
            logger.error(f"Error in similarity search: {e}")
            return documents[:k]
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        try:
            vec1 = np.array(vec1)
            vec2 = np.array(vec2)
            
            dot_product = np.dot(vec1, vec2)
            norm1 = np.linalg.norm(vec1)
            norm2 = np.linalg.norm(vec2)
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            return dot_product / (norm1 * norm2)
        except Exception as e:
            logger.error(f"Error calculating cosine similarity: {e}")
            return 0.0
    
    def batch_embed(self, texts: List[str], batch_size: int = 32) -> List[List[float]]:
        """Embed texts in batches."""
        all_embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            batch_embeddings = self.embed_documents(batch)
            all_embeddings.extend(batch_embeddings)
        
        return all_embeddings


# Global embedding manager instance
embedding_manager = EmbeddingManager() 