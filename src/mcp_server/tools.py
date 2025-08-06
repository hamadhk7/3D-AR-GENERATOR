"""
MCP tools definitions.
"""

from typing import List, Dict, Any


def get_tools() -> List[Dict[str, Any]]:
    """
    Get list of available MCP tools.
    
    Returns:
        List of tool definitions
    """
    return [
        {
            "name": "generate_3d_model",
            "description": "Generate a 3D model from text description",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "Text description of the 3D model to generate"
                    },
                    "format": {
                        "type": "string",
                        "description": "Output format (glb, usdz, obj)",
                        "default": "glb"
                    },
                    "quality": {
                        "type": "string",
                        "description": "Generation quality (low, medium, high, ultra)",
                        "default": "high"
                    },
                    "seed": {
                        "type": "integer",
                        "description": "Random seed for reproducibility"
                    }
                },
                "required": ["prompt"]
            }
        },
        {
            "name": "list_models",
            "description": "List all generated 3D models",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of models to return",
                        "default": 50
                    },
                    "offset": {
                        "type": "integer",
                        "description": "Number of models to skip",
                        "default": 0
                    }
                }
            }
        },
        {
            "name": "get_model_info",
            "description": "Get information about a specific model",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "model_id": {
                        "type": "string",
                        "description": "Model ID"
                    }
                },
                "required": ["model_id"]
            }
        },
        {
            "name": "convert_model_format",
            "description": "Convert a model to a different format",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "model_id": {
                        "type": "string",
                        "description": "Model ID"
                    },
                    "target_format": {
                        "type": "string",
                        "description": "Target format (glb, usdz, obj)"
                    }
                },
                "required": ["model_id", "target_format"]
            }
        }
    ] 