"""
MCP (Model Context Protocol) server for 3D AR demo.
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional

from mcp import ServerSession, StdioServerParameters
from mcp.server import NotificationOptions
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server

from ..utils.logger import setup_logging, get_logger
from config.settings import validate_settings
from .tools import get_tools
from .handlers import ToolHandler


class MCPServer:
    """
    MCP server for 3D model generation and management.
    """
    
    def __init__(self):
        """Initialize the MCP server."""
        self.logger = get_logger("mcp_server")
        self.tool_handler = ToolHandler()
        self.session: Optional[ServerSession] = None
        
        # Set up logging
        setup_logging(
            config_path="config/logging_config.yaml",
            log_level="DEBUG"
        )
        
        # Validate settings
        try:
            validate_settings()
            self.logger.info("Settings validated successfully")
        except Exception as e:
            self.logger.error(f"Settings validation failed: {e}")
            raise
    
    async def initialize(self, session: ServerSession) -> None:
        """
        Initialize the MCP server session.
        
        Args:
            session: MCP server session
        """
        self.session = session
        
        # Set up tools
        tools = get_tools()
        
        # Register tools with the session
        await session.set_tools(tools)
        
        self.logger.info("MCP server initialized successfully")
        
        # Send initialization notification
        await session.notify(
            "mcp/3d-ar-demo/initialized",
            {"message": "3D AR Demo MCP server initialized"}
        )
    
    async def handle_tool_call(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle tool calls from the client.
        
        Args:
            name: Tool name
            arguments: Tool arguments
            
        Returns:
            Tool result
        """
        self.logger.info(f"Handling tool call: {name}")
        
        try:
            result = await self.tool_handler.handle_tool(name, arguments)
            self.logger.info(f"Tool {name} completed successfully")
            return result
        
        except Exception as e:
            self.logger.error(f"Tool {name} failed: {e}")
            return {
                "error": str(e),
                "success": False
            }
    
    async def handle_list_tools(self) -> List[Dict[str, Any]]:
        """
        Handle list tools request.
        
        Returns:
            List of available tools
        """
        return get_tools()
    
    async def handle_list_resources(self) -> List[Dict[str, Any]]:
        """
        Handle list resources request.
        
        Returns:
            List of available resources
        """
        # Return available 3D models as resources
        try:
            models = await self.tool_handler.list_models()
            return [
                {
                    "uri": f"model://{model['id']}",
                    "name": model['prompt'][:50] + "..." if len(model['prompt']) > 50 else model['prompt'],
                    "description": f"3D model: {model['prompt']}",
                    "mimeType": f"model/{model['format']}",
                    "metadata": {
                        "format": model['format'],
                        "quality": model['quality'],
                        "created_at": model['created_at'],
                        "file_size": model['file_size']
                    }
                }
                for model in models
            ]
        except Exception as e:
            self.logger.error(f"Failed to list resources: {e}")
            return []
    
    async def handle_read_resource(self, uri: str) -> Dict[str, Any]:
        """
        Handle read resource request.
        
        Args:
            uri: Resource URI
            
        Returns:
            Resource content
        """
        if uri.startswith("model://"):
            model_id = uri[8:]  # Remove "model://" prefix
            try:
                model_info = await self.tool_handler.get_model_info(model_id)
                return {
                    "contents": [
                        {
                            "uri": uri,
                            "mimeType": f"model/{model_info['format']}",
                            "text": json.dumps(model_info, indent=2)
                        }
                    ]
                }
            except Exception as e:
                self.logger.error(f"Failed to read resource {uri}: {e}")
                return {"error": str(e)}
        
        return {"error": f"Unknown resource URI: {uri}"}
    
    async def handle_list_prompts(self) -> List[Dict[str, Any]]:
        """
        Handle list prompts request.
        
        Returns:
            List of available prompts
        """
        return [
            {
                "name": "generate_3d_model",
                "description": "Generate a 3D model from text description",
                "arguments": {
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
                    }
                }
            },
            {
                "name": "list_models",
                "description": "List all generated 3D models",
                "arguments": {
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
        ]
    
    async def handle_call_prompt(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle prompt call request.
        
        Args:
            name: Prompt name
            arguments: Prompt arguments
            
        Returns:
            Prompt result
        """
        if name == "generate_3d_model":
            return await self.handle_tool_call("generate_3d_model", arguments)
        elif name == "list_models":
            return await self.handle_tool_call("list_models", arguments)
        else:
            return {"error": f"Unknown prompt: {name}"}


async def main():
    """Main entry point for the MCP server."""
    # Set up logging
    setup_logging(
        config_path="config/logging_config.yaml",
        log_level="INFO"
    )
    
    logger = get_logger("mcp_server")
    logger.info("Starting MCP server...")
    
    # Create server instance
    server = MCPServer()
    
    # Create server parameters
    params = StdioServerParameters(
        name="3d-ar-demo",
        version="1.0.0",
        command="python",
        args=["-m", "src.mcp_server.server"]
    )
    
    # Create initialization options
    init_options = InitializationOptions(
        server_name="3D AR Demo MCP Server",
        server_version="1.0.0",
        capabilities={
            "tools": {},
            "resources": {
                "listChanged": True
            },
            "prompts": {}
        }
    )
    
    # Run the server
    async with stdio_server(params) as (read_stream, write_stream):
        async with ServerSession(
            read_stream,
            write_stream,
            init_options
        ) as session:
            await server.initialize(session)
            
            # Handle incoming requests
            async for request in session:
                try:
                    if request.method == "tools/call":
                        result = await server.handle_tool_call(
                            request.params["name"],
                            request.params["arguments"]
                        )
                        await request.respond(result)
                    
                    elif request.method == "tools/list":
                        tools = await server.handle_list_tools()
                        await request.respond({"tools": tools})
                    
                    elif request.method == "resources/list":
                        resources = await server.handle_list_resources()
                        await request.respond({"resources": resources})
                    
                    elif request.method == "resources/read":
                        content = await server.handle_read_resource(
                            request.params["uri"]
                        )
                        await request.respond(content)
                    
                    elif request.method == "prompts/list":
                        prompts = await server.handle_list_prompts()
                        await request.respond({"prompts": prompts})
                    
                    elif request.method == "prompts/call":
                        result = await server.handle_call_prompt(
                            request.params["name"],
                            request.params["arguments"]
                        )
                        await request.respond(result)
                    
                    else:
                        await request.respond(
                            {"error": f"Unknown method: {request.method}"},
                            is_error=True
                        )
                
                except Exception as e:
                    logger.error(f"Error handling request: {e}")
                    await request.respond(
                        {"error": str(e)},
                        is_error=True
                    )
    
    logger.info("MCP server stopped")


if __name__ == "__main__":
    asyncio.run(main()) 