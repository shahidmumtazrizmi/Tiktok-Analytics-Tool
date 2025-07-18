#!/usr/bin/env python3
"""
Startup script for TikTok Analytics + RAG Chatbot
"""

import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    print("🚀 Starting TikTok Analytics + RAG Chatbot...")
    print("📊 Analytics Dashboard: http://localhost:8000")
    print("🤖 Chatbot: http://localhost:8000/chatbot")
    print("📚 API Docs: http://localhost:8000/docs")
    print("🏥 Health Check: http://localhost:8000/health")
    print("\nPress Ctrl+C to stop the server")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 