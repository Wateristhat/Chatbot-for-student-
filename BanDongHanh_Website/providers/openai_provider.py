"""
OpenAI Provider Module
Encapsulates OpenAI API integration with error handling, retry logic, and message formatting.
"""

import os
import base64
import logging
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

# Configure logging
logger = logging.getLogger(__name__)

# Default configuration
DEFAULT_MODELS = [
    "gpt-4o-mini",    # Multi-modal (image + text)
    "gpt-4o",         # Multi-modal (image + text) 
    "gpt-4-1106-preview",  # Text only
    "gpt-3.5-turbo"   # Text fallback
]

DEFAULT_SYSTEM_PROMPT = (
    "Bạn là 'Bạn Đồng Hành' – một trợ lý thân thiện, ấm áp, hỗ trợ cảm xúc. "
    "Không chẩn đoán y khoa. Giữ câu trả lời tự nhiên, khích lệ, dùng tiếng Việt gần gũi. "
    "Khi người dùng mô tả cảm xúc tiêu cực, hãy thừa nhận cảm xúc đó và gợi ý hành vi nhẹ nhàng. "
    "Tránh hứa hẹn tuyệt đối. Có thể đặt câu hỏi mở để họ chia sẻ thêm."
)


class OpenAIProvider:
    """
    OpenAI API provider with comprehensive error handling and retry logic.
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        models: List[str] = DEFAULT_MODELS,
        system_prompt: str = DEFAULT_SYSTEM_PROMPT,
        default_temperature: float = 0.7,
        default_max_tokens: int = 600,
        retry_attempts: int = 3
    ):
        """
        Initialize OpenAI provider.
        
        Args:
            api_key: OpenAI API key (if None, reads from environment)
            models: List of preferred models in priority order
            system_prompt: Default system prompt for conversations
            default_temperature: Default temperature for completions
            default_max_tokens: Default max tokens for completions
            retry_attempts: Number of retry attempts for failed requests
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "").strip()
        self.models = models
        self.system_prompt = system_prompt
        self.default_temperature = default_temperature
        self.default_max_tokens = default_max_tokens
        self.retry_attempts = retry_attempts
        self._client = None
        
        if not self.api_key:
            logger.warning("No OpenAI API key provided. Provider will not be functional.")
    
    @property
    def is_available(self) -> bool:
        """Check if the OpenAI provider is available (has API key)."""
        return bool(self.api_key)
    
    def _get_client(self):
        """Lazy initialization of OpenAI client."""
        if self._client is None and self.is_available:
            try:
                from openai import OpenAI
                self._client = OpenAI(api_key=self.api_key)
                logger.debug("OpenAI client initialized successfully")
            except ImportError:
                logger.error("OpenAI library not installed. Install with: pip install openai")
                raise
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI client: {str(e)}")
                raise
        return self._client
    
    def _select_model(self) -> str:
        """Select the first available model from the preferred list."""
        # For now, return the first model. 
        # In a production system, you might want to test model availability
        return self.models[0]
    
    def _encode_image_base64(self, image_bytes: bytes) -> str:
        """Encode image bytes to base64 string."""
        return base64.b64encode(image_bytes).decode('utf-8')
    
    def _format_messages(
        self,
        messages: List[Dict[str, Any]],
        include_system_prompt: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Format messages for OpenAI API.
        
        Args:
            messages: List of message dictionaries with 'role', 'content', and optional 'images'
            include_system_prompt: Whether to include system prompt
            
        Returns:
            Formatted messages for OpenAI API
        """
        formatted_messages = []
        
        # Add system prompt if requested
        if include_system_prompt and self.system_prompt:
            formatted_messages.append({
                "role": "system", 
                "content": self.system_prompt
            })
        
        # Format each message
        for msg in messages:
            role = "assistant" if msg["role"] == "assistant" else "user"
            
            # Handle messages with images (multi-modal)
            if msg.get("images") and len(msg["images"]) > 0:
                content_parts = [{"type": "text", "text": msg["content"]}]
                
                # Add each image
                for img_bytes in msg["images"]:
                    b64_image = self._encode_image_base64(img_bytes)
                    content_parts.append({
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{b64_image}",
                            "detail": "auto"  # Can be "low", "high", or "auto"
                        }
                    })
                
                formatted_messages.append({
                    "role": role,
                    "content": content_parts
                })
            else:
                # Text-only message
                formatted_messages.append({
                    "role": role,
                    "content": msg["content"]
                })
        
        return formatted_messages
    
    def generate_response(
        self,
        messages: List[Dict[str, Any]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        model: Optional[str] = None
    ) -> Tuple[Optional[str], Dict[str, Any]]:
        """
        Generate a response using OpenAI API.
        
        Args:
            messages: List of conversation messages
            temperature: Randomness of response (0.0-2.0)
            max_tokens: Maximum tokens in response
            model: Model to use (if None, uses default selection)
            
        Returns:
            Tuple of (response_text, metadata)
            Returns (None, error_info) if generation fails
        """
        if not self.is_available:
            logger.warning("OpenAI provider not available - no API key")
            return None, {"error": "No OpenAI API key configured"}
        
        # Use defaults if not specified
        temperature = temperature or self.default_temperature
        max_tokens = max_tokens or self.default_max_tokens
        model = model or self._select_model()
        
        try:
            client = self._get_client()
            if not client:
                return None, {"error": "Failed to initialize OpenAI client"}
            
            # Format messages for OpenAI
            formatted_messages = self._format_messages(messages)
            
            # Log request details (without sensitive content)
            logger.debug(f"OpenAI request: model={model}, messages={len(formatted_messages)}, "
                        f"temp={temperature}, max_tokens={max_tokens}")
            
            # Make API request with retry logic
            last_exception = None
            for attempt in range(self.retry_attempts):
                try:
                    response = client.chat.completions.create(
                        model=model,
                        messages=formatted_messages,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        stream=False
                    )
                    
                    # Extract response
                    if response.choices and len(response.choices) > 0:
                        content = response.choices[0].message.content
                        
                        # Prepare metadata
                        metadata = {
                            "model": model,
                            "usage": {
                                "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
                                "completion_tokens": response.usage.completion_tokens if response.usage else 0,
                                "total_tokens": response.usage.total_tokens if response.usage else 0
                            },
                            "finish_reason": response.choices[0].finish_reason,
                            "timestamp": datetime.now().isoformat()
                        }
                        
                        logger.debug(f"OpenAI response successful: {len(content)} chars, "
                                   f"{metadata['usage']['total_tokens']} tokens")
                        
                        return content, metadata
                    else:
                        logger.error("OpenAI response has no choices")
                        return None, {"error": "No response choices returned"}
                        
                except Exception as e:
                    last_exception = e
                    logger.warning(f"OpenAI API attempt {attempt + 1} failed: {str(e)}")
                    
                    # Don't retry on certain errors
                    error_str = str(e).lower()
                    if any(phrase in error_str for phrase in [
                        "invalid_api_key", "insufficient_quota", "model_not_found"
                    ]):
                        logger.error(f"Non-retryable OpenAI error: {str(e)}")
                        break
                        
                    # Wait before retry (simple exponential backoff)
                    if attempt < self.retry_attempts - 1:
                        import time
                        wait_time = 2 ** attempt
                        logger.debug(f"Waiting {wait_time}s before retry...")
                        time.sleep(wait_time)
            
            # All attempts failed
            error_msg = f"OpenAI API failed after {self.retry_attempts} attempts: {str(last_exception)}"
            logger.error(error_msg)
            return None, {"error": error_msg, "exception": str(last_exception)}
            
        except Exception as e:
            logger.error(f"Unexpected error in OpenAI provider: {str(e)}")
            return None, {"error": f"Unexpected error: {str(e)}"}
    
    def estimate_tokens(self, text: str) -> int:
        """
        Estimate token count for text (rough approximation).
        For accurate counts, use tiktoken library.
        
        Args:
            text: Text to estimate tokens for
            
        Returns:
            Estimated token count
        """
        # Rough approximation: 1 token ≈ 4 characters for English/Vietnamese mix
        return max(1, len(text) // 4)
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about configured models and settings."""
        return {
            "available": self.is_available,
            "preferred_models": self.models,
            "current_model": self._select_model() if self.is_available else None,
            "default_temperature": self.default_temperature,
            "default_max_tokens": self.default_max_tokens,
            "retry_attempts": self.retry_attempts,
            "system_prompt_length": len(self.system_prompt) if self.system_prompt else 0
        }


# Convenience functions for backwards compatibility
def create_provider(**kwargs) -> OpenAIProvider:
    """Create an OpenAI provider with custom settings."""
    return OpenAIProvider(**kwargs)


def generate_chat_response(
    messages: List[Dict[str, Any]],
    api_key: Optional[str] = None,
    **kwargs
) -> Tuple[Optional[str], Dict[str, Any]]:
    """
    Convenience function to generate a single chat response.
    
    Args:
        messages: List of conversation messages
        api_key: OpenAI API key (optional, reads from env if not provided)
        **kwargs: Additional arguments for generation
        
    Returns:
        Tuple of (response_text, metadata)
    """
    provider = OpenAIProvider(api_key=api_key)
    return provider.generate_response(messages, **kwargs)