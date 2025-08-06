#!/usr/bin/env python3
"""
Startup script for the web server.
"""

import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.web.app import run_app
from src.utils.logger import setup_logging, get_logger
from config.settings import settings


def main():
    """Main entry point for the web server."""
    # Set up logging
    setup_logging(
        config_path="config/logging_config.yaml",
        log_level="INFO"
    )
    
    logger = get_logger("web_server")
    
    try:
        logger.info("Starting web server...")
        run_app(
            host=settings.web_server_host,
            port=settings.web_server_port,
            debug=settings.debug
        )
    except KeyboardInterrupt:
        logger.info("Web server stopped by user")
    except Exception as e:
        logger.error(f"Web server failed to start: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 