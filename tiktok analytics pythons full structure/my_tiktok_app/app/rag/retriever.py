"""
RAG retriever for TikTok Shop analytics and support.
"""

from typing import List, Dict, Any, Optional
from langchain.schema import Document
import logging

logger = logging.getLogger(__name__)


class TikTokShopRetriever:
    """Retriever for TikTok Shop content with specialized knowledge base."""
    
    def __init__(self):
        self.knowledge_base = self._initialize_knowledge_base()
    
    def _initialize_knowledge_base(self) -> List[Document]:
        """Initialize TikTok Shop knowledge base."""
        return [
            Document(
                page_content="To set up a TikTok Shop: create a TikTok Business account, complete identity verification, add business information, set up payment methods, and list your first products. Verification typically takes 1-3 business days.",
                metadata={"title": "Shop Setup Guide", "category": "setup", "relevance_score": 0.95}
            ),
            Document(
                page_content="Optimize TikTok Shop listings with high-quality images (800x800px minimum), compelling descriptions with keywords, competitive pricing, multiple product images, and detailed specifications. Product videos perform 40% better.",
                metadata={"title": "Product Optimization", "category": "optimization", "relevance_score": 0.92}
            ),
            Document(
                page_content="Effective TikTok marketing: create authentic trending content, use popular hashtags, collaborate with micro-influencers, run TikTok Ads, host live shopping events, and engage with audience. Storytelling content performs 3x better.",
                metadata={"title": "Marketing Strategies", "category": "marketing", "relevance_score": 0.89}
            ),
            Document(
                page_content="Key metrics to track: conversion rate (aim for 2-5%), average order value, customer acquisition cost, ROAS, engagement rate, and customer lifetime value. Top shops have 15-25% month-over-month growth.",
                metadata={"title": "Performance Metrics", "category": "analytics", "relevance_score": 0.88}
            ),
            Document(
                page_content="TikTok Shop policies require accurate descriptions, fair pricing, proper shipping times, responsive customer service, and compliance with local regulations. Violations can result in account suspension.",
                metadata={"title": "Policy Compliance", "category": "compliance", "relevance_score": 0.91}
            )
        ]
    
    def get_relevant_documents(self, query: str, k: int = 5) -> List[Document]:
        """Retrieve relevant documents for a query."""
        query_lower = query.lower()
        relevant_docs = []
        
        for doc in self.knowledge_base:
            relevance = self._calculate_relevance(query_lower, doc)
            if relevance > 0.3:
                doc_copy = Document(
                    page_content=doc.page_content,
                    metadata={**doc.metadata, 'relevance_score': relevance}
                )
                relevant_docs.append(doc_copy)
        
        relevant_docs.sort(key=lambda x: x.metadata.get('relevance_score', 0), reverse=True)
        return relevant_docs[:k]
    
    def _calculate_relevance(self, query: str, document: Document) -> float:
        """Calculate relevance score between query and document."""
        content_lower = document.page_content.lower()
        keywords = ['setup', 'optimize', 'marketing', 'analytics', 'policy', 'shop', 'tiktok', 'product', 'performance']
        
        score = 0.0
        for keyword in keywords:
            if keyword in query and keyword in content_lower:
                score += 0.2
        
        return min(1.0, score)
    
    def get_documents_by_category(self, category: str, limit: int = 10) -> List[Document]:
        """Get documents by category."""
        category_docs = [
            doc for doc in self.knowledge_base 
            if doc.metadata.get('category') == category
        ]
        return category_docs[:limit]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get retrieval statistics."""
        categories = {}
        for doc in self.knowledge_base:
            category = doc.metadata.get('category', 'other')
            categories[category] = categories.get(category, 0) + 1
        
        return {
            "total_documents": len(self.knowledge_base),
            "categories": categories,
            "source_types": {
                "documentation": len([d for d in self.knowledge_base if d.metadata.get('source_type') == 'documentation']),
                "best_practices": len([d for d in self.knowledge_base if d.metadata.get('source_type') == 'best_practices']),
                "strategy": len([d for d in self.knowledge_base if d.metadata.get('source_type') == 'strategy']),
                "analytics": len([d for d in self.knowledge_base if d.metadata.get('source_type') == 'analytics']),
                "policy": len([d for d in self.knowledge_base if d.metadata.get('source_type') == 'policy']),
                "support": len([d for d in self.knowledge_base if d.metadata.get('source_type') == 'support'])
            }
        } 