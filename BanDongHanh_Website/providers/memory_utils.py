"""
Memory Utilities Module
Provides scaffolding for memory management and conversation summarization.
"""

import json
import os
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict

# Configure logging
logger = logging.getLogger(__name__)

# Default configuration
DEFAULT_MEMORY_DIR = Path("data")
DEFAULT_MEMORY_FILE = "memory_chat.json"
DEFAULT_UPDATE_INTERVAL = 12  # Number of messages before memory update
DEFAULT_MAX_HISTORY_SIZE = 40  # Maximum messages to include in summarization


@dataclass
class MemoryEntry:
    """Represents a memory entry with metadata."""
    summary: str
    version: int
    updated_at: str
    message_count: int = 0
    last_topics: List[str] = None
    user_preferences: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.last_topics is None:
            self.last_topics = []
        if self.user_preferences is None:
            self.user_preferences = {}


class MemoryManager:
    """
    Manages long-term memory persistence and summarization for chat conversations.
    """
    
    def __init__(
        self,
        memory_dir: Path = DEFAULT_MEMORY_DIR,
        memory_file: str = DEFAULT_MEMORY_FILE,
        update_interval: int = DEFAULT_UPDATE_INTERVAL,
        max_history_size: int = DEFAULT_MAX_HISTORY_SIZE
    ):
        """
        Initialize memory manager.
        
        Args:
            memory_dir: Directory to store memory files
            memory_file: Name of the memory file
            update_interval: Number of messages between memory updates
            max_history_size: Maximum messages to include in summarization
        """
        self.memory_dir = Path(memory_dir)
        self.memory_file = self.memory_dir / memory_file
        self.update_interval = update_interval
        self.max_history_size = max_history_size
        
        # Create memory directory if it doesn't exist
        self.memory_dir.mkdir(exist_ok=True, parents=True)
        
        # Current memory state
        self._current_memory: Optional[MemoryEntry] = None
        
        logger.debug(f"MemoryManager initialized: file={self.memory_file}, "
                    f"interval={update_interval}")
    
    @property
    def memory_exists(self) -> bool:
        """Check if memory file exists."""
        return self.memory_file.exists()
    
    def load_memory(self) -> MemoryEntry:
        """
        Load memory from file.
        
        Returns:
            MemoryEntry object (empty if file doesn't exist or is invalid)
        """
        if not self.memory_exists:
            logger.debug("No memory file found, creating empty memory")
            self._current_memory = MemoryEntry(
                summary="",
                version=0,
                updated_at=datetime.now().isoformat()
            )
            return self._current_memory
        
        try:
            data = json.loads(self.memory_file.read_text(encoding="utf-8"))
            self._current_memory = MemoryEntry(**data)
            logger.debug(f"Memory loaded: version={self._current_memory.version}, "
                        f"length={len(self._current_memory.summary)}")
            return self._current_memory
        except Exception as e:
            logger.error(f"Failed to load memory file: {str(e)}")
            # Return empty memory on error
            self._current_memory = MemoryEntry(
                summary="",
                version=0,
                updated_at=datetime.now().isoformat()
            )
            return self._current_memory
    
    def save_memory(self, memory: Optional[MemoryEntry] = None) -> bool:
        """
        Save memory to file.
        
        Args:
            memory: MemoryEntry to save (uses current memory if None)
            
        Returns:
            True if successful, False otherwise
        """
        memory_to_save = memory or self._current_memory
        if not memory_to_save:
            logger.warning("No memory to save")
            return False
        
        try:
            # Update timestamp
            memory_to_save.updated_at = datetime.now().isoformat()
            
            # Convert to dict and save
            data = asdict(memory_to_save)
            self.memory_file.write_text(
                json.dumps(data, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            
            self._current_memory = memory_to_save
            logger.debug(f"Memory saved: version={memory_to_save.version}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save memory file: {str(e)}")
            return False
    
    def get_current_memory(self) -> Optional[MemoryEntry]:
        """Get current memory (loads from file if not in memory)."""
        if self._current_memory is None:
            return self.load_memory()
        return self._current_memory
    
    def should_update_memory(self, message_count: int) -> bool:
        """
        Check if memory should be updated based on message count.
        
        Args:
            message_count: Current number of messages in conversation
            
        Returns:
            True if memory should be updated
        """
        return message_count > 0 and message_count % self.update_interval == 0
    
    def clear_memory(self) -> bool:
        """
        Clear memory (delete file and reset current memory).
        
        Returns:
            True if successful, False otherwise
        """
        try:
            if self.memory_file.exists():
                self.memory_file.unlink()
                logger.info("Memory file deleted")
            
            self._current_memory = MemoryEntry(
                summary="",
                version=0,
                updated_at=datetime.now().isoformat()
            )
            return True
            
        except Exception as e:
            logger.error(f"Failed to clear memory: {str(e)}")
            return False
    
    def backup_memory(self, backup_suffix: str = None) -> Optional[Path]:
        """
        Create a backup of current memory file.
        
        Args:
            backup_suffix: Custom suffix for backup file (uses timestamp if None)
            
        Returns:
            Path to backup file if successful, None otherwise
        """
        if not self.memory_exists:
            logger.warning("No memory file to backup")
            return None
        
        try:
            suffix = backup_suffix or datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = self.memory_file.with_suffix(f".{suffix}.bak")
            
            # Copy memory file to backup
            backup_file.write_text(
                self.memory_file.read_text(encoding="utf-8"),
                encoding="utf-8"
            )
            
            logger.info(f"Memory backup created: {backup_file}")
            return backup_file
            
        except Exception as e:
            logger.error(f"Failed to create memory backup: {str(e)}")
            return None
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get statistics about current memory."""
        memory = self.get_current_memory()
        if not memory:
            return {"exists": False}
        
        stats = {
            "exists": True,
            "version": memory.version,
            "summary_length": len(memory.summary),
            "last_updated": memory.updated_at,
            "message_count": memory.message_count,
            "topics_count": len(memory.last_topics),
            "preferences_count": len(memory.user_preferences),
            "file_size": self.memory_file.stat().st_size if self.memory_exists else 0
        }
        
        return stats


class MemorySummarizer:
    """
    Provides scaffolding for conversation summarization.
    Can be extended with AI-powered summarization or use heuristic methods.
    """
    
    def __init__(self, max_summary_length: int = 800):
        """
        Initialize summarizer.
        
        Args:
            max_summary_length: Maximum length of generated summaries
        """
        self.max_summary_length = max_summary_length
        logger.debug(f"MemorySummarizer initialized: max_length={max_summary_length}")
    
    def summarize_conversation(
        self,
        messages: List[Dict[str, Any]],
        current_summary: str = "",
        method: str = "heuristic"
    ) -> str:
        """
        Summarize a conversation, optionally building on existing summary.
        
        Args:
            messages: List of conversation messages
            current_summary: Existing summary to build upon
            method: Summarization method ("heuristic", "ai", or "hybrid")
            
        Returns:
            Updated summary text
        """
        if not messages:
            return current_summary
        
        # Filter relevant messages (exclude system messages)
        relevant_messages = [
            msg for msg in messages[-self.max_summary_length:]
            if msg.get("role") in ("user", "assistant")
        ]
        
        if method == "ai":
            return self._ai_summarize(relevant_messages, current_summary)
        elif method == "hybrid":
            # Try AI first, fall back to heuristic
            try:
                return self._ai_summarize(relevant_messages, current_summary)
            except Exception as e:
                logger.warning(f"AI summarization failed, using heuristic: {str(e)}")
                return self._heuristic_summarize(relevant_messages, current_summary)
        else:
            return self._heuristic_summarize(relevant_messages, current_summary)
    
    def _heuristic_summarize(
        self,
        messages: List[Dict[str, Any]],
        current_summary: str
    ) -> str:
        """
        Create summary using simple heuristic rules.
        
        Args:
            messages: List of messages to summarize
            current_summary: Existing summary
            
        Returns:
            Updated summary
        """
        # Extract user messages for pattern recognition
        user_messages = [
            msg["content"] for msg in messages
            if msg.get("role") == "user" and msg.get("content")
        ]
        
        if not user_messages:
            return current_summary
        
        # Simple keyword extraction for topics
        topics = self._extract_topics(user_messages)
        
        # Build summary components
        summary_parts = []
        
        if current_summary:
            # Preserve existing summary (truncated)
            truncated_current = current_summary[:400] if len(current_summary) > 400 else current_summary
            summary_parts.append(f"Trước đó: {truncated_current}")
        
        # Add recent topics
        if topics:
            topics_text = ", ".join(topics[:5])  # Top 5 topics
            summary_parts.append(f"Chủ đề gần đây: {topics_text}")
        
        # Add recent message context (last few user messages)
        recent_messages = user_messages[-3:]  # Last 3 user messages
        if recent_messages:
            recent_text = " | ".join([msg[:100] + "..." if len(msg) > 100 else msg for msg in recent_messages])
            summary_parts.append(f"Nội dung gần đây: {recent_text}")
        
        # Combine and truncate
        full_summary = " — ".join(summary_parts)
        if len(full_summary) > self.max_summary_length:
            full_summary = full_summary[:self.max_summary_length - 3] + "..."
        
        return full_summary
    
    def _ai_summarize(
        self,
        messages: List[Dict[str, Any]],
        current_summary: str
    ) -> str:
        """
        Create summary using AI provider (placeholder for future implementation).
        
        Args:
            messages: List of messages to summarize
            current_summary: Existing summary
            
        Returns:
            Updated summary
        """
        # This is a placeholder for AI-powered summarization
        # In a full implementation, this would use OpenAI or another LLM
        # to generate intelligent summaries
        
        logger.info("AI summarization not implemented, falling back to heuristic")
        return self._heuristic_summarize(messages, current_summary)
    
    def _extract_topics(self, messages: List[str]) -> List[str]:
        """
        Extract topics from messages using simple keyword matching.
        
        Args:
            messages: List of message texts
            
        Returns:
            List of identified topics
        """
        # Vietnamese topic keywords
        topic_keywords = {
            "học tập": ["học", "bài tập", "thi", "kiểm tra", "điểm", "lớp"],
            "cảm xúc": ["buồn", "vui", "lo âu", "stress", "áp lực", "hạnh phúc"],
            "gia đình": ["bố", "mẹ", "anh", "chị", "em", "gia đình"],
            "bạn bè": ["bạn", "bạn bè", "tình bạn", "kết bạn"],
            "sức khỏe": ["khỏe", "bệnh", "đau", "mệt", "ngủ"],
            "tương lai": ["tương lai", "ước mơ", "mục tiêu", "kế hoạch"]
        }
        
        combined_text = " ".join(messages).lower()
        found_topics = []
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in combined_text for keyword in keywords):
                found_topics.append(topic)
        
        return found_topics


# Convenience functions
def create_memory_manager(**kwargs) -> MemoryManager:
    """Create a memory manager with custom settings."""
    return MemoryManager(**kwargs)


def create_summarizer(**kwargs) -> MemorySummarizer:
    """Create a memory summarizer with custom settings."""
    return MemorySummarizer(**kwargs)