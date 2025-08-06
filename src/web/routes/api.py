"""
API routes for the web application.
"""

import os
import json
import random
import time
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, make_response
from ...utils.logger import get_logger

api_bp = Blueprint('api', __name__)
logger = get_logger(__name__)

def save_demo_model(model_data):
    """Save a demo model to the demo models file."""
    try:
        # Use absolute path from project root
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        demo_models_file = os.path.join(project_root, 'src', 'data', 'demo_models.json')
        os.makedirs(os.path.dirname(demo_models_file), exist_ok=True)
        
        # Load existing models
        existing_models = []
        if os.path.exists(demo_models_file):
            try:
                with open(demo_models_file, 'r') as f:
                    existing_models = json.load(f)
            except:
                existing_models = []
        
        # Add new model
        existing_models.append(model_data)
        
        # Save back to file
        with open(demo_models_file, 'w') as f:
            json.dump(existing_models, f, indent=2)
            
        return True
    except Exception as e:
        logger.error(f"Error saving demo model: {e}")
        return False


# Enhanced demo mode with credit tracking
DEMO_CREDITS_FILE = "data/demo_credits.json"
DEMO_CREDITS_INITIAL = 5220  # User's actual free credits

def load_demo_credits():
    """Load demo credits from file."""
    try:
        if os.path.exists(DEMO_CREDITS_FILE):
            with open(DEMO_CREDITS_FILE, 'r') as f:
                return json.load(f)
        else:
            # Initialize with user's free credits
            credits = {
                "api_wallet": 0,
                "free_wallet": DEMO_CREDITS_INITIAL,
                "total_used": 0,
                "last_updated": datetime.now().isoformat()
            }
            save_demo_credits(credits)
            return credits
    except Exception as e:
        logger.error(f"Error loading demo credits: {e}")
        return {"api_wallet": 0, "free_wallet": DEMO_CREDITS_INITIAL, "total_used": 0}

def save_demo_credits(credits):
    """Save demo credits to file."""
    try:
        os.makedirs(os.path.dirname(DEMO_CREDITS_FILE), exist_ok=True)
        with open(DEMO_CREDITS_FILE, 'w') as f:
            json.dump(credits, f, indent=2)
    except Exception as e:
        logger.error(f"Error saving demo credits: {e}")

def use_demo_credit(amount=1):
    """Use a demo credit and return success status."""
    credits = load_demo_credits()
    
    if credits["free_wallet"] >= amount:
        credits["free_wallet"] -= amount
        credits["total_used"] += amount
        credits["last_updated"] = datetime.now().isoformat()
        save_demo_credits(credits)
        logger.info(f"Used {amount} demo credit. Remaining: {credits['free_wallet']}")
        return True
    else:
        logger.warning(f"Insufficient demo credits. Available: {credits['free_wallet']}, Needed: {amount}")
        return False

def check_credits():
    """Check if user has enough credits for generation."""
    try:
        credits = load_demo_credits()
        if credits["free_wallet"] > 0:
            return {
                'success': True,
                'credits_available': credits["free_wallet"]
            }
        else:
            return {
                'success': False,
                'error': 'Insufficient credits. Please apply for API credits or purchase them.',
                'credits_available': 0
            }
    except Exception as e:
        logger.error(f"Credit check failed: {e}")
        return {
            'success': False,
            'error': f'Credit check failed: {str(e)}'
        }, 500


@api_bp.route('/generate', methods=['POST'])
def generate_model():
    """Generate a 3D model using Tripo AI API."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        prompt = data.get('prompt', '').strip()
        if not prompt:
            return jsonify({
                'success': False,
                'error': 'Prompt is required'
            }), 400
        
        format_type = data.get('format', 'glb')
        quality = data.get('quality', 'high')
        
        logger.info(f"Generating model with prompt: {prompt}")
        
        # Check credits first
        credits_check = check_credits()
        if not credits_check['success']:
            return jsonify(credits_check), 400
        
        # Initialize Tripo API client
        from src.api_clients.tripo_client import TripoAPIClient, TripoGenerationRequest
        from config.settings import get_settings
        
        settings = get_settings()
        
        # Check if we have a valid API key
        if not settings.tripo_api_key or settings.tripo_api_key == "your_tripo_api_key_here":
            logger.warning("No valid Tripo API key found, using demo mode")
            return jsonify({
                'success': False,
                'error': 'Tripo API key not configured. Please add your API key to the .env file.',
                'note': 'Add TRIPO_API_KEY=your_actual_api_key to .env file'
            }), 400
        
        tripo_client = TripoAPIClient(settings.tripo_api_key)
        
        # Create generation request
        generation_request = TripoGenerationRequest(
            prompt=prompt,
            format=format_type,
            quality=quality
        )
        
        # Call Tripo API to generate real 3D model
        import asyncio
        
        async def generate_real_model():
            try:
                # Start the generation
                logger.info("Calling Tripo API to generate real 3D model...")
                response = await tripo_client.generate_model(generation_request)
                
                if response.success:
                    task_id = response.data['id']
                    logger.info(f"Tripo generation started with task ID: {task_id}")
                    
                    # Wait for the generation to complete
                    logger.info("Waiting for generation to complete...")
                    wait_response = await tripo_client.wait_for_generation(task_id, timeout=300)
                    
                    if wait_response.success:
                        # Get the final model info
                        status_response = await tripo_client.get_generation_status(task_id)
                        
                        logger.info(f"Status response: {status_response.success}, data: {status_response.data}")
                        
                        if status_response.success and status_response.data.get('status') in ['completed', 'success']:
                            model_data = status_response.data
                            
                            # Create model record
                            model_id = f"tripo_{task_id}"
                            model_record = {
                                'id': model_id,
                                'prompt': prompt,
                                'format': format_type,
                                'quality': quality,
                                'created_at': model_data.get('created_at', datetime.now().isoformat()),
                                'file_size': model_data.get('file_size', 1024000),
                                'status': 'completed',
                                'download_url': model_data.get('download_url', f'/api/models/{model_id}/download'),
                                'tripo_task_id': task_id,
                                'output': model_data.get('output', {})  # Save the full output data
                            }
                            
                            # Save to demo models file
                            save_demo_model(model_record)
                            
                            # Use a credit for successful generation
                            credit_used = use_demo_credit(1)
                            if credit_used:
                                logger.info(f"Used 1 credit for successful generation. Model: {model_id}")
                            else:
                                logger.warning(f"Failed to use credit for generation. Model: {model_id}")
                            
                            logger.info(f"Real 3D model generated successfully: {model_id}")
                            
                            return {
                                'success': True,
                                'model': model_record,
                                'message': '3D model generated successfully using Tripo AI',
                                'credits_used': 1
                            }
                        else:
                            logger.error(f"Generation failed: {status_response.error}")
                            return {
                                'success': False,
                                'error': f'Generation failed: {status_response.error}'
                            }
                    else:
                        logger.error(f"Generation wait failed: {wait_response.error}")
                        return {
                            'success': False,
                            'error': f'Generation wait failed: {wait_response.error}'
                        }
                else:
                    logger.error(f"Tripo API call failed: {response.error}")
                    return {
                        'success': False,
                        'error': f'Tripo API call failed: {response.error}'
                    }
                    
            except Exception as e:
                logger.error(f"Error in real model generation: {e}")
                import traceback
                logger.error(f"Traceback: {traceback.format_exc()}")
                return {
                    'success': False,
                    'error': f'Generation error: {str(e)}'
                }
        
        # Run the async generation
        try:
            result = asyncio.run(generate_real_model())
            
            if result and result.get('success'):
                return jsonify(result), 200
            else:
                error_msg = result.get('error', 'Unknown error') if result else 'No result returned'
                logger.error(f"Generation failed: {error_msg}")
                return jsonify({
                    'success': False,
                    'error': error_msg
                }), 500
        except Exception as e:
            logger.error(f"Async generation error: {e}")
            import traceback
            logger.error(f"Async traceback: {traceback.format_exc()}")
            return jsonify({
                'success': False,
                'error': f'Async generation failed: {str(e)}'
            }), 500
            
    except Exception as e:
        logger.error(f"Error generating model: {e}")
        return jsonify({
            'success': False,
            'error': f'Generation failed: {str(e)}'
        }), 500


@api_bp.route('/models', methods=['GET'])
def list_models():
    """List all generated models."""
    try:
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        # Start with empty models list
        models = []
        
        # Add any recently generated demo models
        import os
        import json
        from datetime import datetime, timedelta
        
        # Use absolute path from project root
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        demo_models_file = os.path.join(project_root, 'src', 'data', 'demo_models.json')
        logger.info(f"Looking for demo models file at: {demo_models_file}")
        
        try:
            if os.path.exists(demo_models_file):
                logger.info(f"Demo models file found, loading...")
                with open(demo_models_file, 'r') as f:
                    recent_models = json.load(f)
                    logger.info(f"Loaded {len(recent_models)} models from file")
                    # Include all models (removed 24-hour filter)
                    models.extend(recent_models)
            else:
                logger.warning(f"Demo models file not found at: {demo_models_file}")
        except Exception as e:
            logger.error(f"Could not load recent demo models: {e}")
        
        # Add the original demo model if no other models exist
        if not models:
            logger.info("No models loaded from file, adding default demo model")
            models = [
                {
                    'id': 'demo_model_1',
                    'prompt': 'A futuristic robot',
                    'format': 'glb',
                    'quality': 'high',
                    'created_at': '2024-01-01T12:00:00Z',
                    'file_size': 1024000,
                    'status': 'completed'
                }
            ]
        
        # Sort by creation date (newest first), handle None values
        def get_created_at(model):
            created_at = model.get('created_at')
            if created_at is None:
                return '1970-01-01T00:00:00Z'  # Default for None values
            return created_at
        
        models.sort(key=get_created_at, reverse=True)
        logger.info(f"Returning {len(models)} models total")
        
        # Apply limit and offset
        total = len(models)
        models = models[offset:offset + limit]
        
        return jsonify({
            'success': True,
            'models': models,
            'total': total
        })
    
    except Exception as e:
        logger.error(f"Error listing models: {e}")
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500


@api_bp.route('/models/<model_id>', methods=['GET'])
def get_model(model_id):
    """Get details of a specific model."""
    try:
        # First check if it's the original demo model
        if model_id == 'demo_model_1':
            model = {
                'id': model_id,
                'prompt': 'A futuristic robot',
                'format': 'glb',
                'quality': 'high',
                'created_at': '2024-01-01T12:00:00Z',
                'file_size': 1024000,
                'download_url': f'/api/models/{model_id}/download'
            }
        else:
            # Try to find the model in the demo models file
            # Use absolute path from project root
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
            demo_models_file = os.path.join(project_root, 'src', 'data', 'demo_models.json')
            
            if os.path.exists(demo_models_file):
                try:
                    with open(demo_models_file, 'r') as f:
                        recent_models = json.load(f)
                    
                    # Find the specific model
                    model = None
                    for m in recent_models:
                        if m['id'] == model_id:
                            model = m
                            model['download_url'] = f'/api/models/{model_id}/download'
                            break
                    
                    if not model:
                        return jsonify({
                            'success': False,
                            'error': 'Model not found'
                        }), 404
                except Exception as e:
                    logger.error(f"Error reading demo models file: {e}")
                    return jsonify({
                        'success': False,
                        'error': 'Model not found'
                    }), 404
            else:
                return jsonify({
                    'success': False,
                    'error': 'Model not found'
                }), 404
        
        return jsonify({
            'success': True,
            'model': model
        })
    
    except Exception as e:
        logger.error(f"Error getting model {model_id}: {e}")
        return jsonify({
            'success': False,
            'error': 'Model not found'
        }), 404


@api_bp.route('/models/<model_id>/download', methods=['GET', 'OPTIONS'])
def download_model(model_id):
    """Download a model file from Tripo API."""
    
    # Handle CORS preflight requests
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response
    
    try:
        # Get model info first
        import json
        from src.api_clients.tripo_client import TripoAPIClient
        from config.settings import get_settings
        
        # Try to find the model in the demo models file
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        demo_models_file = os.path.join(project_root, 'src', 'data', 'demo_models.json')
        
        model = None
        if os.path.exists(demo_models_file):
            try:
                with open(demo_models_file, 'r') as f:
                    recent_models = json.load(f)
                
                # Find the specific model
                for m in recent_models:
                    if m.get('id') == model_id:
                        model = m
                        break
            except Exception as e:
                logger.error(f"Error loading model data: {e}")
        
        if not model:
            return jsonify({
                'success': False,
                'error': 'Model not found'
            }), 404
        
        # Check if this is a Tripo-generated model
        if model_id.startswith('tripo_') and 'tripo_task_id' in model:
            tripo_task_id = model['tripo_task_id']
            logger.info(f"Downloading real GLB file for Tripo task: {tripo_task_id}")
            
            # Initialize Tripo API client
            from src.api_clients.tripo_client import TripoAPIClient
            from config.settings import get_settings
            
            settings = get_settings()
            tripo_client = TripoAPIClient(settings.tripo_api_key)
            
            # Create output directory
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
            output_dir = os.path.join(project_root, 'data', 'generated_models', 'glb')
            os.makedirs(output_dir, exist_ok=True)
            
            # Download the GLB file directly from the Tripo URL
            import requests
            
            # Get the download URL from the model data
            download_url = None
            if 'output' in model and 'pbr_model' in model['output']:
                download_url = model['output']['pbr_model']
            elif 'download_url' in model:
                download_url = model['download_url']
            
            if not download_url:
                logger.error(f"No download URL found for model {model_id}")
                return jsonify({
                    'success': False,
                    'error': 'Download URL not available'
                }), 404
            
            logger.info(f"Downloading from URL: {download_url}")
            
            try:
                # Check if file already exists locally
                output_path = os.path.join(output_dir, f"{model_id}.glb")
                
                if os.path.exists(output_path):
                    logger.info(f"GLB file already exists locally: {output_path}")
                else:
                    # Download the file directly from Tripo
                    logger.info(f"Downloading GLB file from Tripo...")
                    response = requests.get(download_url, timeout=120, stream=True)
                    
                    if response.status_code == 200:
                        # Save the file
                        with open(output_path, 'wb') as f:
                            for chunk in response.iter_content(chunk_size=8192):
                                f.write(chunk)
                        
                        logger.info(f"GLB file downloaded successfully: {output_path}")
                    else:
                        logger.error(f"Download failed with status {response.status_code}")
                        return jsonify({
                            'success': False,
                            'error': f'Download failed with status {response.status_code}'
                        }), 500
                
                # Serve the file with proper CORS headers for 3D model loading
                from flask import send_file, make_response
                response = make_response(send_file(output_path, as_attachment=True, download_name=f'{model_id}.glb'))
                response.headers['Access-Control-Allow-Origin'] = '*'
                response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
                response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
                response.headers['Content-Type'] = 'application/octet-stream'
                return response
                    
            except Exception as e:
                logger.error(f"Error downloading model: {e}")
                return jsonify({
                    'success': False,
                    'error': f'Download error: {str(e)}'
                }), 500
            
        else:
            # For demo models, return a placeholder response
            logger.warning(f"Demo model download requested for: {model_id}")
            return jsonify({
                'success': False,
                'error': 'GLB file not available',
                'message': 'This is a demo model. Real GLB files are available for Tripo-generated models.'
            }), 404
             
    except Exception as e:
        logger.error(f"Error downloading model {model_id}: {e}")
        return jsonify({
            'success': False,
            'error': f'Download failed: {str(e)}'
        }), 500


@api_bp.route('/convert', methods=['POST'])
def convert_model():
    """Convert model format."""
    try:
        data = request.get_json()
        
        if not data or 'model_id' not in data or 'target_format' not in data:
            return jsonify({
                'success': False,
                'error': 'Model ID and target format are required'
            }), 400
        
        # TODO: Implement format conversion logic
        
        return jsonify({
            'success': True,
            'message': 'Conversion started',
            'job_id': 'convert_job_123'
        })
    
    except Exception as e:
        logger.error(f"Error in model conversion: {e}")
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500 


@api_bp.route('/credits', methods=['GET'])
def get_credits():
    """Get current credit information."""
    try:
        # Use dynamic local credit management
        credits = load_demo_credits()
        
        return jsonify({
            'success': True,
            'api_wallet': 200,  # User's actual API credits (static)
            'free_wallet': credits['free_wallet'],  # Dynamic local credits
            'frozen': 40,  # User's frozen credits (static)
            'source': 'local_management',
            'note': f'Dynamic local credits (starts with {DEMO_CREDITS_INITIAL}, decrements on generation)'
        })
    
    except Exception as e:
        logger.error(f"Credit check error: {e}")
        return jsonify({
            'success': False,
            'error': f'Credit check failed: {str(e)}'
        }), 500 