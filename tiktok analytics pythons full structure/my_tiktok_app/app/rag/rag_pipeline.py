import openai
from typing import Dict, List, Any, Optional
import json
import uuid
from datetime import datetime
from app.core.config import settings

# Set OpenAI API key
openai.api_key = settings.OPENAI_API_KEY

class RAGPipeline:
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        
        # Dummy knowledge base for TikTok Shop
        self.knowledge_base = [
            {
                "title": "TikTok Shop Setup Guide",
                "content": "To set up your TikTok Shop, you need to: 1) Create a TikTok Business account, 2) Apply for TikTok Shop access, 3) Complete business verification, 4) Set up payment methods, 5) Add your products. The process typically takes 2-3 business days for approval.",
                "url": "https://docs.tiktok.com/shop-setup",
                "category": "setup"
            },
            {
                "title": "TikTok Shop Requirements",
                "content": "Requirements for TikTok Shop include: Valid business license, Tax identification number, Bank account for payments, Product compliance with TikTok policies, Shipping capabilities, Customer service setup. You must be 18+ and have a valid business entity.",
                "url": "https://docs.tiktok.com/requirements",
                "category": "setup"
            },
            {
                "title": "Marketing Strategies for TikTok Shop",
                "content": "Effective TikTok Shop marketing includes: Creating engaging product videos, Using trending hashtags, Collaborating with influencers, Running TikTok ads, Hosting live shopping events, Offering exclusive discounts, Building a community around your brand.",
                "url": "https://docs.tiktok.com/marketing",
                "category": "marketing"
            },
            {
                "title": "Scaling Your TikTok Shop",
                "content": "To scale your TikTok Shop: Focus on high-performing products, Optimize your product listings, Use data analytics to understand trends, Expand to multiple markets, Build a strong brand presence, Automate order processing, Invest in customer retention.",
                "url": "https://docs.tiktok.com/scaling",
                "category": "scaling"
            },
            {
                "title": "TikTok Shop Analytics",
                "content": "Key metrics to track: Sales conversion rate, Average order value, Customer acquisition cost, Return on ad spend, Product performance, Customer lifetime value, Traffic sources, Engagement rates. Use TikTok's built-in analytics dashboard.",
                "url": "https://docs.tiktok.com/analytics",
                "category": "analytics"
            },
            {
                "title": "Customer Service Best Practices",
                "content": "Provide excellent customer service by: Responding quickly to inquiries, Offering clear return policies, Providing detailed product information, Using chatbots for common questions, Following up with customers, Handling complaints professionally.",
                "url": "https://docs.tiktok.com/customer-service",
                "category": "customer-service"
            },
            {
                "title": "Product Sourcing Strategies",
                "content": "Effective product sourcing: Research trending products, Find reliable suppliers, Negotiate bulk discounts, Ensure product quality, Consider dropshipping options, Build relationships with manufacturers, Diversify your product range.",
                "url": "https://docs.tiktok.com/sourcing",
                "category": "sourcing"
            },
            {
                "title": "TikTok Shop Policies",
                "content": "Important policies: No counterfeit products, Accurate product descriptions, Fair pricing, Proper shipping times, Clear return policies, No misleading advertising, Compliance with local laws, Respect intellectual property rights.",
                "url": "https://docs.tiktok.com/policies",
                "category": "policies"
            }
        ]

    async def get_response(self, query: str, session_id: str) -> Dict[str, Any]:
        """Get RAG response for a user query"""
        try:
            # Find relevant knowledge base entries
            relevant_docs = self._find_relevant_documents(query)
            
            # Create context from relevant documents
            context = self._create_context(relevant_docs)
            
            # Generate response using OpenAI
            response = await self._generate_response(query, context)
            
            # Format sources
            sources = self._format_sources(relevant_docs)
            
            return {
                "response": response,
                "sources": sources,
                "confidence": 0.9,
                "session_id": session_id
            }
            
        except Exception as e:
            return {
                "response": f"I apologize, but I encountered an error: {str(e)}. Please try again or contact support.",
                "sources": [],
                "confidence": 0.0,
                "session_id": session_id
            }

    def _find_relevant_documents(self, query: str) -> List[Dict]:
        """Find relevant documents from knowledge base"""
        query_lower = query.lower()
        relevant_docs = []
        
        for doc in self.knowledge_base:
            # Simple keyword matching (in production, use vector similarity)
            if any(keyword in query_lower for keyword in doc["content"].lower().split()[:10]):
                relevant_docs.append(doc)
        
        # If no exact matches, return general documents
        if not relevant_docs:
            relevant_docs = self.knowledge_base[:3]
        
        return relevant_docs[:3]  # Return top 3 most relevant

    def _create_context(self, documents: List[Dict]) -> str:
        """Create context string from relevant documents"""
        context_parts = []
        for doc in documents:
            context_parts.append(f"Title: {doc['title']}\nContent: {doc['content']}\n")
        
        return "\n".join(context_parts)

    async def _generate_response(self, query: str, context: str) -> str:
        """Generate response using OpenAI"""
        try:
            prompt = f"""You are a helpful TikTok Shop expert assistant. Use the following context to answer the user's question. If the context doesn't contain enough information, provide general helpful advice about TikTok Shop.

Context:
{context}

User Question: {query}

Please provide a helpful, accurate, and detailed response. Include specific tips and actionable advice when possible."""

            response = self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are a TikTok Shop expert assistant. Provide helpful, accurate, and actionable advice."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"I apologize, but I'm having trouble generating a response right now. Please try again later. Error: {str(e)}"

    def _format_sources(self, documents: List[Dict]) -> List[Dict]:
        """Format sources for response"""
        sources = []
        for doc in documents:
            sources.append({
                "title": doc["title"],
                "url": doc["url"],
                "relevance": 0.9,
                "category": doc["category"]
            })
        return sources

    async def get_suggestions(self) -> List[str]:
        """Get suggested questions"""
        return [
            "How do I set up my TikTok Shop?",
            "What are the requirements for TikTok Shop?",
            "How can I increase my shop sales?",
            "What marketing strategies work best?",
            "How do I handle customer service?",
            "What are the best product categories?",
            "How do I optimize my product listings?",
            "What are the payment processing options?",
            "How do I manage inventory?",
            "What are the shipping requirements?"
        ]

# Initialize RAG pipeline
rag_pipeline = RAGPipeline() 