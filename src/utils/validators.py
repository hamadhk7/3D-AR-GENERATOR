"""
Input validation utilities.
"""

import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlparse

from pydantic import BaseModel, Field, validator


class ValidationError(Exception):
    """Custom validation error."""
    pass


def validate_prompt(prompt: str, max_length: int = 1000) -> str:
    """
    Validate text prompt for 3D model generation.
    
    Args:
        prompt: Text prompt to validate
        max_length: Maximum allowed length
        
    Returns:
        Validated prompt
        
    Raises:
        ValidationError: If prompt is invalid
    """
    if not prompt or not isinstance(prompt, str):
        raise ValidationError("Prompt must be a non-empty string")
    
    prompt = prompt.strip()
    if len(prompt) < 3:
        raise ValidationError("Prompt must be at least 3 characters long")
    
    if len(prompt) > max_length:
        raise ValidationError(f"Prompt must be no more than {max_length} characters")
    
    # Check for potentially harmful content
    harmful_patterns = [
        r'\b(hack|crack|steal|illegal|unauthorized)\b',
        r'\b(exploit|vulnerability|backdoor)\b',
        r'\b(porn|adult|nsfw|explicit)\b',
        r'\b(violence|gore|blood|death)\b'
    ]
    
    for pattern in harmful_patterns:
        if re.search(pattern, prompt.lower()):
            raise ValidationError("Prompt contains potentially harmful content")
    
    return prompt


def validate_model_format(format_name: str) -> str:
    """
    Validate 3D model format.
    
    Args:
        format_name: Format name to validate
        
    Returns:
        Validated format name
        
    Raises:
        ValidationError: If format is invalid
    """
    valid_formats = ['glb', 'usdz', 'obj', 'fbx', 'stl']
    
    if not format_name or not isinstance(format_name, str):
        raise ValidationError("Format must be a non-empty string")
    
    format_name = format_name.lower().strip()
    if format_name not in valid_formats:
        raise ValidationError(f"Invalid format. Must be one of: {', '.join(valid_formats)}")
    
    return format_name


def validate_quality(quality: str) -> str:
    """
    Validate model quality setting.
    
    Args:
        quality: Quality setting to validate
        
    Returns:
        Validated quality setting
        
    Raises:
        ValidationError: If quality is invalid
    """
    valid_qualities = ['low', 'medium', 'high', 'ultra']
    
    if not quality or not isinstance(quality, str):
        raise ValidationError("Quality must be a non-empty string")
    
    quality = quality.lower().strip()
    if quality not in valid_qualities:
        raise ValidationError(f"Invalid quality. Must be one of: {', '.join(valid_qualities)}")
    
    return quality


def validate_file_path(file_path: Union[str, Path]) -> Path:
    """
    Validate file path.
    
    Args:
        file_path: File path to validate
        
    Returns:
        Validated Path object
        
    Raises:
        ValidationError: If path is invalid
    """
    if not file_path:
        raise ValidationError("File path cannot be empty")
    
    path = Path(file_path)
    
    # Check for path traversal attempts
    try:
        path.resolve()
    except (RuntimeError, OSError):
        raise ValidationError("Invalid file path")
    
    # Check if path contains suspicious patterns
    path_str = str(path)
    suspicious_patterns = ['..', '~', '/etc', '/var', '/usr', 'C:\\Windows']
    
    for pattern in suspicious_patterns:
        if pattern in path_str:
            raise ValidationError("Path contains suspicious patterns")
    
    return path


def validate_url(url: str) -> str:
    """
    Validate URL.
    
    Args:
        url: URL to validate
        
    Returns:
        Validated URL
        
    Raises:
        ValidationError: If URL is invalid
    """
    if not url or not isinstance(url, str):
        raise ValidationError("URL must be a non-empty string")
    
    url = url.strip()
    
    try:
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            raise ValidationError("Invalid URL format")
        
        # Check for allowed schemes
        allowed_schemes = ['http', 'https', 'ftp']
        if parsed.scheme not in allowed_schemes:
            raise ValidationError(f"URL scheme must be one of: {', '.join(allowed_schemes)}")
        
    except Exception as e:
        raise ValidationError(f"Invalid URL: {e}")
    
    return url


def validate_api_key(api_key: str) -> str:
    """
    Validate API key format.
    
    Args:
        api_key: API key to validate
        
    Returns:
        Validated API key
        
    Raises:
        ValidationError: If API key is invalid
    """
    if not api_key or not isinstance(api_key, str):
        raise ValidationError("API key must be a non-empty string")
    
    api_key = api_key.strip()
    
    # Basic format validation (adjust based on actual API key format)
    if len(api_key) < 10:
        raise ValidationError("API key is too short")
    
    if len(api_key) > 200:
        raise ValidationError("API key is too long")
    
    # Check for common placeholder values
    placeholder_patterns = [
        r'your_.*_here',
        r'placeholder',
        r'test_.*',
        r'demo_.*'
    ]
    
    for pattern in placeholder_patterns:
        if re.search(pattern, api_key.lower()):
            raise ValidationError("API key appears to be a placeholder")
    
    return api_key


class GenerationRequest(BaseModel):
    """Pydantic model for 3D model generation requests."""
    
    prompt: str = Field(..., description="Text prompt for 3D model generation")
    format: str = Field("glb", description="Output format")
    quality: str = Field("high", description="Generation quality")
    seed: Optional[int] = Field(None, description="Random seed for reproducibility")
    negative_prompt: Optional[str] = Field(None, description="Negative prompt")
    parameters: Optional[Dict[str, Any]] = Field(None, description="Additional parameters")
    
    @validator('prompt')
    def validate_prompt_field(cls, v):
        return validate_prompt(v)
    
    @validator('format')
    def validate_format_field(cls, v):
        return validate_model_format(v)
    
    @validator('quality')
    def validate_quality_field(cls, v):
        return validate_quality(v)
    
    @validator('seed')
    def validate_seed(cls, v):
        if v is not None and (v < 0 or v > 2**32 - 1):
            raise ValidationError("Seed must be between 0 and 2^32 - 1")
        return v
    
    @validator('negative_prompt')
    def validate_negative_prompt(cls, v):
        if v is not None:
            return validate_prompt(v, max_length=500)
        return v


class ModelMetadata(BaseModel):
    """Pydantic model for 3D model metadata."""
    
    id: str = Field(..., description="Unique model identifier")
    prompt: str = Field(..., description="Generation prompt")
    format: str = Field(..., description="Model format")
    quality: str = Field(..., description="Generation quality")
    file_size: int = Field(..., description="File size in bytes")
    created_at: str = Field(..., description="Creation timestamp")
    file_path: str = Field(..., description="File path")
    seed: Optional[int] = Field(None, description="Random seed used")
    generation_time: Optional[float] = Field(None, description="Generation time in seconds")
    parameters: Optional[Dict[str, Any]] = Field(None, description="Generation parameters")
    
    @validator('id')
    def validate_id(cls, v):
        if not v or not isinstance(v, str):
            raise ValidationError("ID must be a non-empty string")
        if len(v) > 100:
            raise ValidationError("ID is too long")
        return v
    
    @validator('file_size')
    def validate_file_size(cls, v):
        if v < 0:
            raise ValidationError("File size cannot be negative")
        if v > 100 * 1024 * 1024:  # 100MB
            raise ValidationError("File size is too large")
        return v


def validate_generation_parameters(parameters: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate generation parameters.
    
    Args:
        parameters: Parameters to validate
        
    Returns:
        Validated parameters
        
    Raises:
        ValidationError: If parameters are invalid
    """
    if not isinstance(parameters, dict):
        raise ValidationError("Parameters must be a dictionary")
    
    validated_params = {}
    
    # Validate specific parameter types and ranges
    for key, value in parameters.items():
        if key == 'steps':
            if not isinstance(value, int) or value < 1 or value > 1000:
                raise ValidationError("Steps must be an integer between 1 and 1000")
            validated_params[key] = value
        
        elif key == 'guidance_scale':
            if not isinstance(value, (int, float)) or value < 0.1 or value > 50:
                raise ValidationError("Guidance scale must be a number between 0.1 and 50")
            validated_params[key] = float(value)
        
        elif key == 'width' or key == 'height':
            if not isinstance(value, int) or value < 64 or value > 2048:
                raise ValidationError(f"{key} must be an integer between 64 and 2048")
            validated_params[key] = value
        
        else:
            # Allow other parameters but log them
            validated_params[key] = value
    
    return validated_params 