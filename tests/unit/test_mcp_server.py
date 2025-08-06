"""
Unit tests for MCP server.
"""

import pytest
from unittest.mock import Mock, patch

from src.mcp_server.handlers import ToolHandler


class TestToolHandler:
    """Test cases for ToolHandler."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.handler = ToolHandler()
    
    @pytest.mark.asyncio
    async def test_generate_3d_model(self):
        """Test 3D model generation."""
        arguments = {
            "prompt": "A futuristic robot",
            "format": "glb",
            "quality": "high"
        }
        
        result = await self.handler.generate_3d_model(arguments)
        
        assert result["success"] is True
        assert "model_id" in result
        assert result["status"] == "completed"
    
    @pytest.mark.asyncio
    async def test_list_models(self):
        """Test model listing."""
        arguments = {
            "limit": 10,
            "offset": 0
        }
        
        result = await self.handler.list_models(arguments)
        
        assert result["success"] is True
        assert "models" in result
        assert isinstance(result["models"], list)
    
    @pytest.mark.asyncio
    async def test_get_model_info(self):
        """Test model info retrieval."""
        arguments = {
            "model_id": "test_model_123"
        }
        
        result = await self.handler.get_model_info(arguments)
        
        assert result["success"] is True
        assert "model" in result
        assert result["model"]["id"] == "test_model_123"
    
    @pytest.mark.asyncio
    async def test_convert_model_format(self):
        """Test model format conversion."""
        arguments = {
            "model_id": "test_model_123",
            "target_format": "usdz"
        }
        
        result = await self.handler.convert_model_format(arguments)
        
        assert result["success"] is True
        assert "converted_model_id" in result
        assert result["message"] == "Model test_model_123 converted to usdz"
    
    @pytest.mark.asyncio
    async def test_handle_unknown_tool(self):
        """Test handling of unknown tools."""
        result = await self.handler.handle_tool("unknown_tool", {})
        
        assert result["success"] is False
        assert "error" in result
        assert "Unknown tool" in result["error"] 