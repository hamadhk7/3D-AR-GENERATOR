#!/usr/bin/env python3
"""
Startup script for the MCP server.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.mcp_server.server import main as mcp_main
from src.utils.logger import setup_logging, get_logger


def main():
    """Main entry point for the MCP server."""
    # Set up logging
    setup_logging(
        config_path="config/logging_config.yaml",
        log_level="INFO"
    )
    
    logger = get_logger("mcp_server")
    
    try:
        logger.info("Starting MCP server...")
        asyncio.run(mcp_main())
    except KeyboardInterrupt:
        logger.info("MCP server stopped by user")
    except Exception as e:
        logger.error(f"MCP server failed to start: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 