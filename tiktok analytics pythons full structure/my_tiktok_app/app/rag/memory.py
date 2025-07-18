"""
Memory module for managing conversation history and context.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
import json
import logging
import uuid

logger = logging.getLogger(__name__)


class ConversationMemory:
    """Manages conversation memory and context for RAG system."""
    
    def __init__(self):
        self.conversations = {}  # In production, use database
        self.max_history = 10
    
    def create_conversation(self, user_id: str, title: Optional[str] = None) -> str:
        """Create a new conversation."""
        try:
            conversation_id = str(uuid.uuid4())
            title = title or f"Conversation {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            
            conversation = {
                "id": conversation_id,
                "user_id": user_id,
                "title": title,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "messages": [],
                "is_active": True
            }
            
            self.conversations[conversation_id] = conversation
            
            logger.info(f"Created conversation {conversation_id} for user {user_id}")
            return conversation_id
            
        except Exception as e:
            logger.error(f"Error creating conversation: {e}")
            return None
    
    def add_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Add a message to a conversation."""
        try:
            if conversation_id not in self.conversations:
                logger.error(f"Conversation {conversation_id} not found")
                return False
            
            message = {
                "id": str(uuid.uuid4()),
                "role": role,
                "content": content,
                "metadata": metadata or {},
                "created_at": datetime.now().isoformat()
            }
            
            self.conversations[conversation_id]["messages"].append(message)
            self.conversations[conversation_id]["updated_at"] = datetime.now().isoformat()
            
            # Keep only recent messages
            if len(self.conversations[conversation_id]["messages"]) > self.max_history:
                self.conversations[conversation_id]["messages"] = \
                    self.conversations[conversation_id]["messages"][-self.max_history:]
            
            logger.info(f"Added {role} message to conversation {conversation_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding message: {e}")
            return False
    
    def get_conversation_history(
        self,
        conversation_id: str,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get conversation history."""
        try:
            if conversation_id not in self.conversations:
                return []
            
            messages = self.conversations[conversation_id]["messages"]
            if limit:
                messages = messages[-limit:]
            
            return messages
            
        except Exception as e:
            logger.error(f"Error getting conversation history: {e}")
            return []
    
    def get_user_conversations(self, user_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Get user's conversations."""
        try:
            user_conversations = [
                conv for conv in self.conversations.values()
                if conv["user_id"] == user_id and conv["is_active"]
            ]
            
            # Sort by updated_at
            user_conversations.sort(key=lambda x: x["updated_at"], reverse=True)
            
            return user_conversations[:limit]
            
        except Exception as e:
            logger.error(f"Error getting user conversations: {e}")
            return []
    
    def get_conversation_context(
        self,
        conversation_id: str,
        max_tokens: int = 2000
    ) -> str:
        """Get conversation context for RAG system."""
        try:
            messages = self.get_conversation_history(conversation_id)
            
            context_parts = []
            current_tokens = 0
            
            for message in messages:
                # Rough token estimation (1 token ≈ 4 characters)
                message_tokens = len(message["content"]) // 4
                
                if current_tokens + message_tokens > max_tokens:
                    break
                
                role_label = "User" if message["role"] == "user" else "Assistant"
                context_parts.append(f"{role_label}: {message['content']}")
                current_tokens += message_tokens
            
            return "\n".join(context_parts)
            
        except Exception as e:
            logger.error(f"Error getting conversation context: {e}")
            return ""
    
    def clear_conversation(self, conversation_id: str) -> bool:
        """Clear a conversation (mark as inactive)."""
        try:
            if conversation_id not in self.conversations:
                return False
            
            self.conversations[conversation_id]["is_active"] = False
            self.conversations[conversation_id]["messages"] = []
            
            logger.info(f"Cleared conversation {conversation_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error clearing conversation: {e}")
            return False
    
    def clear_user_conversations(self, user_id: str) -> int:
        """Clear all conversations for a user."""
        try:
            cleared_count = 0
            
            for conv_id, conv in self.conversations.items():
                if conv["user_id"] == user_id and conv["is_active"]:
                    conv["is_active"] = False
                    conv["messages"] = []
                    cleared_count += 1
            
            logger.info(f"Cleared {cleared_count} conversations for user {user_id}")
            return cleared_count
            
        except Exception as e:
            logger.error(f"Error clearing user conversations: {e}")
            return 0
    
    def get_conversation_summary(self, conversation_id: str) -> Dict[str, Any]:
        """Get conversation summary."""
        try:
            if conversation_id not in self.conversations:
                return {}
            
            conv = self.conversations[conversation_id]
            messages = conv["messages"]
            
            summary = {
                "id": conv["id"],
                "title": conv["title"],
                "message_count": len(messages),
                "created_at": conv["created_at"],
                "updated_at": conv["updated_at"],
                "is_active": conv["is_active"]
            }
            
            return summary
            
        except Exception as e:
            logger.error(f"Error getting conversation summary: {e}")
            return {}


# Global memory instance
conversation_memory = ConversationMemory() 