"""
Image utilities for the chatbot application.
Provides image compression and safe base64 encoding functionality.
"""

import base64
import io
from typing import Optional, Tuple, Union
from PIL import Image, ImageOps
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Default compression settings
DEFAULT_MAX_SIZE = (800, 600)  # Max dimensions for compressed images
DEFAULT_QUALITY = 85           # JPEG quality (1-100, higher = better quality)
DEFAULT_FORMAT = 'JPEG'        # Output format for compressed images


def compress_image(
    image_data: Union[bytes, Image.Image],
    max_size: Tuple[int, int] = DEFAULT_MAX_SIZE,
    quality: int = DEFAULT_QUALITY,
    format: str = DEFAULT_FORMAT,
    optimize: bool = True
) -> bytes:
    """
    Compress an image to reduce file size while maintaining reasonable quality.
    
    Args:
        image_data: Image as bytes or PIL Image object
        max_size: Maximum dimensions (width, height) for the output image
        quality: JPEG quality (1-100, higher = better quality)
        format: Output format ('JPEG', 'PNG', 'WEBP')
        optimize: Whether to optimize the image file size
        
    Returns:
        Compressed image as bytes
        
    Raises:
        ValueError: If image data is invalid
        IOError: If image processing fails
    """
    try:
        # Handle input data
        if isinstance(image_data, bytes):
            image = Image.open(io.BytesIO(image_data))
        elif isinstance(image_data, Image.Image):
            image = image_data
        else:
            raise ValueError("image_data must be bytes or PIL Image object")
        
        # Convert to RGB if necessary (for JPEG output)
        if format.upper() == 'JPEG' and image.mode in ('RGBA', 'P', 'LA'):
            # Create white background for transparent images
            background = Image.new('RGB', image.size, (255, 255, 255))
            if image.mode == 'P':
                image = image.convert('RGBA')
            background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
            image = background
        elif format.upper() == 'PNG' and image.mode == 'P':
            image = image.convert('RGBA')
            
        # Auto-orient image based on EXIF data
        image = ImageOps.exif_transpose(image)
        
        # Resize if larger than max_size
        if image.size[0] > max_size[0] or image.size[1] > max_size[1]:
            image.thumbnail(max_size, Image.Resampling.LANCZOS)
            logger.debug(f"Image resized to {image.size}")
        
        # Compress and save to bytes
        output_buffer = io.BytesIO()
        save_kwargs = {
            'format': format,
            'optimize': optimize
        }
        
        if format.upper() == 'JPEG':
            save_kwargs['quality'] = quality
        elif format.upper() == 'PNG':
            save_kwargs['compress_level'] = 6  # PNG compression level (0-9)
        elif format.upper() == 'WEBP':
            save_kwargs['quality'] = quality
            save_kwargs['method'] = 4  # WebP compression method (0-6)
            
        image.save(output_buffer, **save_kwargs)
        compressed_data = output_buffer.getvalue()
        
        # Log compression results
        original_size = len(image_data) if isinstance(image_data, bytes) else 0
        compressed_size = len(compressed_data)
        if original_size > 0:
            compression_ratio = (1 - compressed_size / original_size) * 100
            logger.debug(f"Image compressed: {original_size} → {compressed_size} bytes "
                        f"({compression_ratio:.1f}% reduction)")
        
        return compressed_data
        
    except Exception as e:
        logger.error(f"Image compression failed: {str(e)}")
        raise IOError(f"Failed to compress image: {str(e)}")


def safe_base64_encode(data: bytes, url_safe: bool = False) -> str:
    """
    Safely encode bytes to base64 string with error handling.
    
    Args:
        data: Bytes to encode
        url_safe: Whether to use URL-safe base64 encoding
        
    Returns:
        Base64 encoded string
        
    Raises:
        ValueError: If data is not bytes
    """
    if not isinstance(data, bytes):
        raise ValueError("Data must be bytes")
        
    try:
        if url_safe:
            encoded = base64.urlsafe_b64encode(data)
        else:
            encoded = base64.b64encode(data)
        return encoded.decode('ascii')
    except Exception as e:
        logger.error(f"Base64 encoding failed: {str(e)}")
        raise ValueError(f"Failed to encode data to base64: {str(e)}")


def safe_base64_decode(encoded_str: str, url_safe: bool = False) -> bytes:
    """
    Safely decode base64 string to bytes with error handling.
    
    Args:
        encoded_str: Base64 encoded string
        url_safe: Whether to use URL-safe base64 decoding
        
    Returns:
        Decoded bytes
        
    Raises:
        ValueError: If string is not valid base64
    """
    try:
        if url_safe:
            decoded = base64.urlsafe_b64decode(encoded_str)
        else:
            decoded = base64.b64decode(encoded_str)
        return decoded
    except Exception as e:
        logger.error(f"Base64 decoding failed: {str(e)}")
        raise ValueError(f"Failed to decode base64 string: {str(e)}")


def get_image_info(image_data: Union[bytes, Image.Image]) -> dict:
    """
    Get basic information about an image.
    
    Args:
        image_data: Image as bytes or PIL Image object
        
    Returns:
        Dictionary with image information
    """
    try:
        if isinstance(image_data, bytes):
            image = Image.open(io.BytesIO(image_data))
            size_bytes = len(image_data)
        elif isinstance(image_data, Image.Image):
            image = image_data
            size_bytes = None
        else:
            raise ValueError("image_data must be bytes or PIL Image object")
            
        return {
            'size': image.size,
            'mode': image.mode,
            'format': getattr(image, 'format', None),
            'has_transparency': image.mode in ('RGBA', 'LA') or 'transparency' in image.info,
            'size_bytes': size_bytes
        }
    except Exception as e:
        logger.error(f"Failed to get image info: {str(e)}")
        return {}


# Convenience function for chat image processing
def prepare_chat_image(
    image_bytes: bytes,
    max_size: Tuple[int, int] = (600, 600),
    quality: int = 80
) -> Tuple[bytes, str]:
    """
    Prepare an image for chat by compressing and encoding it.
    Optimized for chat applications with smaller file sizes.
    
    Args:
        image_bytes: Original image bytes
        max_size: Maximum dimensions for chat images
        quality: Compression quality
        
    Returns:
        Tuple of (compressed_image_bytes, base64_encoded_string)
    """
    try:
        # Compress image for chat usage
        compressed_bytes = compress_image(
            image_bytes,
            max_size=max_size,
            quality=quality,
            format='JPEG'
        )
        
        # Encode to base64 for embedding
        base64_str = safe_base64_encode(compressed_bytes)
        
        return compressed_bytes, base64_str
        
    except Exception as e:
        logger.error(f"Chat image preparation failed: {str(e)}")
        # Return original if compression fails
        base64_str = safe_base64_encode(image_bytes)
        return image_bytes, base64_str