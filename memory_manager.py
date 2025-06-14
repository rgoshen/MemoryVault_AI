#!/usr/bin/env python3
"""
MemoryVault AI - Memory Manager
==============================
Handles persistent conversation memory storage and retrieval.
Single Responsibility: Memory persistence only.

Architecture: Domain service for memory management
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict


class MemoryManager:
    """Manages persistent conversation memory - the vault's core capability"""

    def __init__(self, memory_file: str = "memory/conversation_memory.json"):
        self.memory_file = memory_file
        self.memory_dir = Path(memory_file).parent
        self.memory_dir.mkdir(exist_ok=True)

        self.conversations = self.load_memory()
        # Smart session management: resume existing session if available
        existing_sessions = self.conversations.get("sessions", [])
        if existing_sessions:
            # Use the most recent existing session
            self.current_session = existing_sessions[-1]["id"]
        else:
            # No existing sessions, create new one
            self.current_session = self.create_session()

    def load_memory(self) -> Dict:
        """Load all conversation memory from persistent storage"""
        try:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, 'r') as f:
                    return json.load(f)
            return {
                "sessions": [],
                "metadata": {
                    "created": datetime.now().isoformat(),
                    "version": "1.0"
                }
            }
        except Exception as e:
            print(f"Warning: Could not load memory: {e}")
            return {
                "sessions": [],
                "metadata": {
                    "created": datetime.now().isoformat(),
                    "version": "1.0"
                }
            }

    def save_memory(self) -> bool:
        """Save memory to persistent storage"""
        try:
            self.conversations["metadata"]["last_updated"] = datetime.now(
            ).isoformat()
            with open(self.memory_file, 'w') as f:
                json.dump(self.conversations, f, indent=2)
            return True
        except Exception as e:
            print(f"Warning: Could not save memory: {e}")
            return False

    def create_session(self) -> str:
        """Create a new conversation session"""
        session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        session_data = {
            "id": session_id,
            "created": datetime.now().isoformat(),
            "messages": [],
            "context": {}
        }
        self.conversations["sessions"].append(session_data)
        self.save_memory()
        return session_id

    def add_message(self, role: str, content: str, metadata: Dict = None) -> bool:
        """Add message to current session"""
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }

        # Find current session and add message
        for session in self.conversations["sessions"]:
            if session["id"] == self.current_session:
                session["messages"].append(message)
                return self.save_memory()

        return False

    def get_recent_context(self, num_messages: int = 10) -> List[Dict]:
        """Get recent conversation context from current session"""
        for session in reversed(self.conversations["sessions"]):
            if session["id"] == self.current_session:
                return session["messages"][-num_messages:]
        return []

    def get_all_sessions(self) -> List[Dict]:
        """Get all conversation sessions"""
        return self.conversations["sessions"]

    def search_conversations(self, query: str, limit: int = 10) -> List[Dict]:
        """Search through conversation history"""
        results = []
        query_lower = query.lower()

        for session in self.conversations["sessions"]:
            for message in session["messages"]:
                if query_lower in message["content"].lower():
                    results.append({
                        "session_id": session["id"],
                        "message": message,
                        "session_date": session["created"]
                    })
                    if len(results) >= limit:
                        return results

        return results

    def clear_memory(self) -> bool:
        """Clear all conversation memory"""
        self.conversations = {
            "sessions": [],
            "metadata": {
                "created": datetime.now().isoformat(),
                "version": "1.0"
            }
        }
        self.current_session = self.create_session()
        return self.save_memory()

    def get_memory_stats(self) -> Dict:
        """Get memory statistics"""
        total_messages = sum(
            len(session["messages"])
            for session in self.conversations["sessions"]
        )

        return {
            "total_sessions": len(self.conversations["sessions"]),
            "current_session": self.current_session,
            "total_messages": total_messages,
            "memory_file": self.memory_file,
            "last_updated": self.conversations["metadata"].get("last_updated"),
            "created": self.conversations["metadata"].get("created")
        }

    def start_new_session(self) -> str:
        """Explicitly start a new conversation session"""
        self.current_session = self.create_session()
        return self.current_session
