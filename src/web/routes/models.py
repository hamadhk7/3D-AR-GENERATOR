"""
Model serving routes for the web application.
"""

from flask import Blueprint, render_template, request, jsonify, send_file
from pathlib import Path
from ...utils.logger import get_logger

models_bp = Blueprint('models', __name__)
logger = get_logger("web_server")


@models_bp.route('/')
def list_models():
    """List all models page."""
    return render_template('models/list.html')


@models_bp.route('/<model_id>')
def view_model(model_id):
    """View a specific model."""
    return render_template('models/view.html', model_id=model_id)


@models_bp.route('/<model_id>/download')
def download_model(model_id):
    """Download a model file."""
    try:
        # TODO: Implement actual file serving logic
        # This would serve the actual model file from storage
        
        logger.info(f"Download request for model: {model_id}")
        
        # For now, return a placeholder response
        return jsonify({
            'success': True,
            'message': f'Download for model {model_id} would be served here'
        })
    
    except Exception as e:
        logger.error(f"Error serving model {model_id}: {e}")
        return jsonify({
            'success': False,
            'error': 'File not found'
        }), 404


@models_bp.route('/<model_id>/ar')
def ar_viewer(model_id):
    """AR viewer for a specific model."""
    return render_template('models/ar_viewer.html', model_id=model_id) 