from fastapi import APIRouter, HTTPException, Depends, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime
import json

from app.rag.rag_pipeline import RAGPipeline
from app.core.database import get_db, ChatSession, ChatMessage
from app.core.config import settings

router = APIRouter()

# Templates
templates = Jinja2Templates(directory="app/templates")

# Initialize RAG pipeline
rag_pipeline = RAGPipeline()

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    user_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    sources: List[Dict[str, Any]]
    confidence: float
    session_id: str
    suggestions: List[str] = []

@router.post("/send", response_model=ChatResponse)
async def send_message(request: ChatRequest):
    """Send a message to the RAG chatbot"""
    try:
        # Generate session ID if not provided
        session_id = request.session_id or str(uuid.uuid4())
        
        # Get response from RAG pipeline
        response_data = await rag_pipeline.get_response(
            query=request.message,
            session_id=session_id
        )
        
        # Get suggestions for follow-up questions
        suggestions = await rag_pipeline.get_suggestions()
        
        return ChatResponse(
            response=response_data["response"],
            sources=response_data.get("sources", []),
            confidence=response_data.get("confidence", 0.8),
            session_id=session_id,
            suggestions=suggestions[:5]  # Return top 5 suggestions
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")

@router.get("/sessions")
async def get_chat_sessions(user_id: str):
    """Get chat sessions for a user"""
    try:
        # This would typically query the database
        # For now, return dummy data
        sessions = [
            {
                "id": str(uuid.uuid4()),
                "title": "TikTok Shop Setup Help",
                "created_at": datetime.now().isoformat(),
                "message_count": 5,
                "last_message": "How do I verify my business account?"
            },
            {
                "id": str(uuid.uuid4()),
                "title": "Marketing Strategy Discussion",
                "created_at": datetime.now().isoformat(),
                "message_count": 8,
                "last_message": "What are the best hashtags to use?"
            },
            {
                "id": str(uuid.uuid4()),
                "title": "Product Optimization Tips",
                "created_at": datetime.now().isoformat(),
                "message_count": 3,
                "last_message": "How can I improve my product images?"
            }
        ]
        
        return {
            "success": True,
            "data": sessions
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching sessions: {str(e)}")

@router.get("/session/{session_id}/messages")
async def get_session_messages(session_id: str):
    """Get messages for a specific session"""
    try:
        # This would typically query the database
        # For now, return dummy data
        messages = [
            {
                "id": str(uuid.uuid4()),
                "user_message": "How do I set up my TikTok Shop?",
                "assistant_message": "Setting up a TikTok Shop involves several steps. First, you'll need to create a TikTok Business account and apply for TikTok Shop access. The process includes business verification, setting up payment methods, and adding your products. The approval process typically takes 2-3 business days.",
                "sources": [
                    {
                        "title": "TikTok Shop Setup Guide",
                        "url": "https://docs.tiktok.com/shop-setup",
                        "relevance": 0.95
                    }
                ],
                "created_at": datetime.now().isoformat()
            },
            {
                "id": str(uuid.uuid4()),
                "user_message": "What are the requirements?",
                "assistant_message": "The requirements for TikTok Shop include: a valid business license, tax identification number, bank account for payments, product compliance with TikTok policies, shipping capabilities, and customer service setup. You must be 18+ and have a valid business entity.",
                "sources": [
                    {
                        "title": "TikTok Shop Requirements",
                        "url": "https://docs.tiktok.com/requirements",
                        "relevance": 0.87
                    }
                ],
                "created_at": datetime.now().isoformat()
            }
        ]
        
        return {
            "success": True,
            "data": messages
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching messages: {str(e)}")

@router.post("/session/new")
async def create_new_session(user_id: str):
    """Create a new chat session"""
    try:
        session_id = str(uuid.uuid4())
        
        # This would typically save to database
        session = {
            "id": session_id,
            "user_id": user_id,
            "title": "New Chat",
            "created_at": datetime.now().isoformat()
        }
        
        return {
            "success": True,
            "data": session
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating session: {str(e)}")

@router.delete("/session/{session_id}")
async def delete_session(session_id: str):
    """Delete a chat session"""
    try:
        # This would typically delete from database
        return {
            "success": True,
            "message": "Session deleted successfully"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting session: {str(e)}")

@router.get("/knowledge-base")
async def get_knowledge_topics():
    """Get available knowledge base topics"""
    topics = [
        {
            "id": "setup",
            "title": "Shop Setup",
            "description": "How to create and configure your TikTok Shop",
            "articles": 15,
            "icon": "🏪"
        },
        {
            "id": "scaling",
            "title": "Scaling Strategies",
            "description": "Tips for growing your TikTok Shop business",
            "articles": 23,
            "icon": "📈"
        },
        {
            "id": "marketing",
            "title": "Marketing & Advertising",
            "description": "Effective TikTok marketing strategies",
            "articles": 18,
            "icon": "📢"
        },
        {
            "id": "technical",
            "title": "Technical Issues",
            "description": "Troubleshooting common technical problems",
            "articles": 12,
            "icon": "🔧"
        },
        {
            "id": "policies",
            "title": "Policies & Compliance",
            "description": "Understanding TikTok Shop policies and requirements",
            "articles": 8,
            "icon": "📋"
        },
        {
            "id": "analytics",
            "title": "Analytics & Insights",
            "description": "Understanding your shop performance data",
            "articles": 14,
            "icon": "📊"
        }
    ]
    
    return {
        "success": True,
        "data": topics
    }

@router.get("/suggestions")
async def get_chat_suggestions():
    """Get suggested questions for the chatbot"""
    try:
        suggestions = await rag_pipeline.get_suggestions()
        return {
            "success": True,
            "data": suggestions
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching suggestions: {str(e)}")

@router.get("/chatbot", response_class=HTMLResponse)
async def chatbot_page(request: Request):
    """Render the chatbot page"""
    return templates.TemplateResponse("chatbot.html", {
        "request": request,
        "suggestions": [
            "How do I set up my TikTok Shop?",
            "What are the best marketing strategies?",
            "How can I increase my sales?",
            "What are the policy requirements?",
            "How do I optimize my product listings?"
        ]
    }) 