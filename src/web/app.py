"""
Flask web application for 3D AR demo.
"""

import os
from pathlib import Path
from typing import Optional
from datetime import datetime

from flask import Flask, render_template, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
from flask_restful import Api
from werkzeug.exceptions import HTTPException

from ..utils.logger import setup_logging, get_logger
from config.settings import validate_settings, settings
from .routes.api import api_bp
from .routes.models import models_bp


def create_app(config_name: Optional[str] = None) -> Flask:
    """
    Create and configure Flask application.
    
    Args:
        config_name: Configuration name
        
    Returns:
        Configured Flask application
    """
    # Set up logging
    setup_logging(
        config_path="config/logging_config.yaml",
        log_level="INFO"
    )
    
    logger = get_logger("web_server")
    logger.info("Creating Flask application...")
    
    # Validate settings
    try:
        validate_settings()
        logger.info("Settings validated successfully")
    except Exception as e:
        logger.error(f"Settings validation failed: {e}")
        raise
    
    # Create Flask app
    app = Flask(__name__)
    
    # Configure app
    app.config.from_object('config.settings')
    
    # Enable CORS
    CORS(app, origins=settings.cors_origins_list)
    
    # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(models_bp, url_prefix='/models')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal server error: {error}")
        return jsonify({'error': 'Internal server error'}), 500
    
    @app.errorhandler(HTTPException)
    def handle_exception(e):
        logger.error(f"HTTP exception: {e}")
        return jsonify({'error': e.description}), e.code
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        """Health check endpoint for deployment platforms."""
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'service': '3D AR Generator'
        })
    
    # Main routes
    @app.route('/')
    def index():
        """Main application page."""
        return render_template('index.html')
    
    @app.route('/ar-viewer')
    def ar_viewer():
        """AR viewer page."""
        return render_template('ar_viewer.html')
    
    @app.route('/debug-ar')
    def debug_ar():
        """Debug AR viewer page."""
        return send_file('debug_ar_viewer.html', mimetype='text/html')
    
    @app.route('/test-ar')
    def test_ar():
        """Simple AR test page."""
        return send_file('test_ar_simple.html', mimetype='text/html')
    
    @app.route('/static/<path:filename>')
    def static_files(filename):
        """Serve static files."""
        return send_from_directory('static', filename)
    
    @app.route('/public/<path:filename>')
    def public_files(filename):
        """Serve public files."""
        import os
        public_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'public')
        return send_from_directory(public_dir, filename)
    
    # Model viewer endpoint
    @app.route('/view/<model_id>')
    def view_model(model_id):
        """View a specific 3D model."""
        return render_template('model_viewer.html', model_id=model_id)
    
    # API documentation
    @app.route('/api/docs')
    def api_docs():
        """API documentation page."""
        return render_template('api_docs.html')
    
    logger.info("Flask application created successfully")
    return app


def run_app(host: str = "0.0.0.0", port: int = 5000, debug: bool = False):
    """Run the Flask application."""
    # Get port from environment variable for deployment platforms
    port = int(os.environ.get("PORT", port))
    
    logger = get_logger("web_server")
    logger.info(f"Starting web server on {host}:{port}")
    
    # Create the Flask app
    app = create_app()
    
    app.run(
        host=host,
        port=port,
        debug=debug
    )


if __name__ == '__main__':
    run_app() 