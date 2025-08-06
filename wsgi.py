#!/usr/bin/env python3
"""
WSGI entry point for production deployment.
"""

import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.web.app import create_app

# Create the Flask application
app = create_app()

if __name__ == "__main__":
    # Get port from environment variable
    port = int(os.environ.get("PORT", 5000))
    
    # For production, always use 0.0.0.0 and no debug
    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    ) 