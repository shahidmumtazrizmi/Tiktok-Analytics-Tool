"""
RAG Agent for TikTok Shop Analytics
"""

from typing import Dict, Any, List, Optional
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage
from langchain.memory import ConversationBufferWindowMemory
import logging
import time
import json

from .retriever import TikTokShopRetriever
from ..core.config import settings

logger = logging.getLogger(__name__)


class TikTokShopRAGAgent:
    """RAG Agent specialized for TikTok Shop analytics and support."""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model_name="gpt-4",
            temperature=0.7,
            openai_api_key=settings.OPENAI_API_KEY
        )
        self.retriever = TikTokShopRetriever()
        self.memory = ConversationBufferWindowMemory(k=5, return_messages=True)
        
        # System prompt for TikTok Shop expertise
        self.system_prompt = """You are an expert TikTok Shop consultant and analytics specialist. You help users with:

1. **TikTok Shop Setup & Management**
   - Account creation and verification
   - Product listing and optimization
   - Payment and shipping setup
   - Policy compliance

2. **Analytics & Performance**
   - Understanding shop metrics
   - Sales optimization strategies
   - Product performance analysis
   - Market trend insights

3. **Marketing & Growth**
   - TikTok marketing strategies
   - Content creation tips
   - Influencer collaboration
   - Advertising optimization

4. **Technical Support**
   - Platform troubleshooting
   - API integration help
   - Data export and reporting
   - Performance optimization

Always provide practical, actionable advice based on TikTok Shop best practices. Cite specific sources when available and be encouraging but realistic about expectations."""

    def generate_response(
        self,
        query: str,
        conversation_context: Optional[str] = None,
        use_memory: bool = True
    ) -> Dict[str, Any]:
        """
        Generate RAG response for TikTok Shop queries.
        
        Args:
            query: User query
            conversation_context: Previous conversation context
            use_memory: Whether to use conversation memory
            
        Returns:
            Dict containing response and metadata
        """
        start_time = time.time()
        
        try:
            # Retrieve relevant documents
            documents = self.retriever.get_relevant_documents(query, k=5)
            
            # Prepare context from retrieved documents
            context = self._prepare_context(documents)
            
            # Build conversation history
            if use_memory and conversation_context:
                full_context = f"Previous conversation:\n{conversation_context}\n\nRelevant information:\n{context}"
            else:
                full_context = context
            
            # Create messages for LLM
            messages = [
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=f"Context:\n{full_context}\n\nUser Question: {query}")
            ]
            
            # Generate response
            response = self.llm.invoke(messages)
            
            # Update memory
            if use_memory:
                self.memory.save_context(
                    {"input": query},
                    {"output": response.content}
                )
            
            # Prepare sources and citations
            sources = self._extract_sources(documents)
            citations = self._generate_citations(documents, response.content)
            
            processing_time = time.time() - start_time
            
            return {
                "answer": response.content,
                "sources": sources,
                "citations": citations,
                "processing_time": processing_time,
                "confidence": self._calculate_confidence(documents, query),
                "documents_retrieved": len(documents)
            }
            
        except Exception as e:
            logger.error(f"Error generating RAG response: {e}")
            return {
                "answer": "I apologize, but I'm having trouble processing your request right now. Please try again or contact support if the issue persists.",
                "sources": [],
                "citations": [],
                "processing_time": time.time() - start_time,
                "confidence": 0.0,
                "documents_retrieved": 0
            }
    
    def _prepare_context(self, documents: List[Any]) -> str:
        """Prepare context from retrieved documents."""
        if not documents:
            return "No specific information found. I'll provide general TikTok Shop advice."
        
        context_parts = []
        for i, doc in enumerate(documents, 1):
            content = doc.page_content if hasattr(doc, 'page_content') else str(doc)
            metadata = doc.metadata if hasattr(doc, 'metadata') else {}
            
            source_info = f"Source {i}"
            if metadata.get('title'):
                source_info += f": {metadata['title']}"
            elif metadata.get('url'):
                source_info += f": {metadata['url']}"
            
            context_parts.append(f"{source_info}\n{content[:500]}...")
        
        return "\n\n".join(context_parts)
    
    def _extract_sources(self, documents: List[Any]) -> List[Dict[str, Any]]:
        """Extract source information from documents."""
        sources = []
        for doc in documents:
            metadata = doc.metadata if hasattr(doc, 'metadata') else {}
            source = {
                "title": metadata.get('title', 'TikTok Shop Documentation'),
                "url": metadata.get('url', ''),
                "type": metadata.get('source_type', 'documentation'),
                "relevance": metadata.get('relevance_score', 0.8),
                "timestamp": metadata.get('timestamp', '')
            }
            sources.append(source)
        return sources
    
    def _generate_citations(self, documents: List[Any], response: str) -> List[Dict[str, Any]]:
        """Generate citations for the response."""
        citations = []
        for doc in documents:
            metadata = doc.metadata if hasattr(doc, 'metadata') else {}
            citation = {
                "source": metadata.get('title', 'TikTok Shop Documentation'),
                "text": doc.page_content[:200] + "..." if hasattr(doc, 'page_content') else str(doc)[:200] + "...",
                "confidence": metadata.get('relevance_score', 0.8)
            }
            citations.append(citation)
        return citations
    
    def _calculate_confidence(self, documents: List[Any], query: str) -> float:
        """Calculate confidence score based on document relevance."""
        if not documents:
            return 0.3  # Low confidence when no documents found
        
        # Calculate average relevance score
        total_relevance = 0.0
        for doc in documents:
            metadata = doc.metadata if hasattr(doc, 'metadata') else {}
            relevance = metadata.get('relevance_score', 0.5)
            total_relevance += relevance
        
        avg_relevance = total_relevance / len(documents)
        
        # Boost confidence based on number of relevant documents
        confidence = min(0.95, avg_relevance + (len(documents) * 0.05))
        
        return confidence
    
    def get_suggestions(self, user_context: Optional[str] = None) -> List[str]:
        """Get suggested questions based on user context."""
        suggestions = [
            "How do I set up my TikTok Shop?",
            "What are the best practices for product listings?",
            "How can I improve my shop's performance?",
            "What marketing strategies work best on TikTok?",
            "How do I handle customer service issues?",
            "What analytics should I focus on?",
            "How do I optimize my product pricing?",
            "What are the common policy violations to avoid?"
        ]
        
        # Add context-specific suggestions
        if user_context:
            if "setup" in user_context.lower():
                suggestions.extend([
                    "What documents do I need for verification?",
                    "How long does the approval process take?",
                    "What are the minimum requirements?"
                ])
            elif "performance" in user_context.lower():
                suggestions.extend([
                    "How do I increase my conversion rate?",
                    "What metrics indicate success?",
                    "How do I analyze my competitors?"
                ])
        
        return suggestions[:8]  # Return top 8 suggestions 