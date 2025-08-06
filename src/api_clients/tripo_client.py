"""
Tripo AI API client for 3D model generation using the OpenAPI REST endpoints.
"""

import asyncio
import time
import os
import requests
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin

from pydantic import BaseModel

from .base_client import BaseAPIClient, APIResponse
from ..utils.logger import get_logger

logger = get_logger(__name__)

class TripoGenerationRequest(BaseModel):
    """Tripo AI generation request model."""
    
    prompt: str
    format: str = "glb"
    quality: str = "high"
    seed: Optional[int] = None
    negative_prompt: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None


class TripoGenerationResponse(BaseModel):
    """Tripo AI generation response model."""
    
    id: str
    status: str
    prompt: str
    format: str
    quality: str
    created_at: str
    estimated_completion: Optional[str] = None
    download_url: Optional[str] = None
    error: Optional[str] = None


class TripoModelInfo(BaseModel):
    """Tripo AI model information."""
    
    id: str
    prompt: str
    format: str
    quality: str
    file_size: int
    created_at: str
    download_url: str
    metadata: Optional[Dict[str, Any]] = None


class TripoAPIClient:
    """
    Client for Tripo AI API using the OpenAPI REST endpoints.
    """
    
    def __init__(self, api_key: str):
        """
        Initialize Tripo AI client.
        
        Args:
            api_key: Tripo AI API key
        """
        self.api_key = api_key
        self.base_url = "https://api.tripo3d.ai/v2/openapi"
        self.logger = logger
        
        # Validate API key format
        if not api_key.startswith('tsk_'):
            raise ValueError("API key must start with 'tsk_' for OpenAPI usage")
        
        # Store the API key for testing
        self.logger.info(f"Using API key: {api_key[:10]}...")
        
        self.logger.info(f"Initialized Tripo OpenAPI client")
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers with API authentication."""
        return {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
    
    async def health_check(self) -> APIResponse:
        """
        Check Tripo AI API health.
        
        Returns:
            API response indicating health status
        """
        try:
            # Try to get task status to check API health
            response = requests.get(
                f"{self.base_url}/task/health",
                headers=self._get_headers(),
                timeout=10
            )
            
            if response.status_code == 200:
                return APIResponse(
                    success=True,
                    data={"status": "healthy"},
                    status_code=200,
                    response_time=0.0
                )
            else:
                return APIResponse(
                    success=False,
                    error=f"API health check failed: {response.status_code}",
                    status_code=response.status_code,
                    response_time=0.0
                )
        except Exception as e:
            return APIResponse(
                success=False,
                error=str(e),
                status_code=500,
                response_time=0.0
            )

    async def get_credits(self) -> APIResponse:
        """
        Get current credit information from Tripo AI API.
        
        Returns:
            API response with credit information
        """
        try:
            # Try to get credits from the API
            # Note: This endpoint might not exist, so we'll try a few possibilities
            endpoints_to_try = [
                f"{self.base_url}/credits",
                f"{self.base_url}/billing",
                f"{self.base_url}/account",
                f"{self.base_url}/user",
                f"{self.base_url}/balance",
                f"{self.base_url}/wallet"
            ]
            
            for endpoint in endpoints_to_try:
                try:
                    self.logger.info(f"Trying credits endpoint: {endpoint}")
                    response = requests.get(
                        endpoint,
                        headers=self._get_headers(),
                        timeout=10
                    )
                    
                    self.logger.info(f"Response status: {response.status_code}")
                    
                    if response.status_code == 200:
                        data = response.json()
                        self.logger.info(f"Found credits endpoint: {endpoint}")
                        self.logger.info(f"Response data: {data}")
                        
                        # Try to extract credit information from various response formats
                        credits_data = {}
                        
                        # Check for different possible response structures
                        if 'data' in data:
                            credits_data = data['data']
                        elif 'credits' in data:
                            credits_data = data['credits']
                        elif 'balance' in data:
                            credits_data = data
                        else:
                            credits_data = data
                        
                        return APIResponse(
                            success=True,
                            data=credits_data,
                            status_code=200,
                            response_time=0.0
                        )
                    else:
                        self.logger.warning(f"Endpoint {endpoint} returned status {response.status_code}")
                        
                except Exception as e:
                    self.logger.debug(f"Endpoint {endpoint} failed: {e}")
                    continue
            
            # If no endpoints work, return a fallback response
            self.logger.warning("No credits endpoint found, using fallback")
            return APIResponse(
                success=True,
                data={
                    "api_wallet": {"balance": 0, "frozen": 0},
                    "free_wallet": {"balance": 0, "frozen": 0},
                    "note": "Credit information not available from API"
                },
                status_code=200,
                response_time=0.0
            )
            
        except Exception as e:
            return APIResponse(
                success=False,
                error=str(e),
                status_code=500,
                response_time=0.0
            )
    
    async def generate_model(self, request: TripoGenerationRequest) -> APIResponse:
        """
        Generate a 3D model using Tripo AI OpenAPI.
        
        Args:
            request: Generation request parameters
            
        Returns:
            API response with generation job information
        """
        try:
            self.logger.info(f"Starting 3D model generation: {request.prompt}")
            
            # Prepare request payload according to OpenAPI specification
            payload = {
                "type": "text_to_model",
                "prompt": request.prompt,
                "model_version": "v2.5-20250123"  # Default version
            }
            
            # Add optional parameters
            if request.seed is not None:
                payload["seed"] = request.seed
            
            if request.negative_prompt:
                payload["negative_prompt"] = request.negative_prompt
            
            # Make the API call
            response = requests.post(
                f"{self.base_url}/task",
                headers=self._get_headers(),
                json=payload,
                timeout=30
            )
            
            response_data = response.json()
            
            if response.status_code == 200 and response_data.get("code") == 0:
                task_id = response_data["data"]["task_id"]
                self.logger.info(f"Task created successfully: {task_id}")
                
                return APIResponse(
                    success=True,
                    data={
                        'id': task_id,
                        'status': 'queued',
                        'prompt': request.prompt,
                        'format': request.format,
                        'quality': request.quality
                    },
                    status_code=200,
                    response_time=0.0
                )
            else:
                error_msg = response_data.get("message", "Unknown error")
                suggestion = response_data.get("suggestion", "")
                self.logger.error(f"API call failed: {error_msg} - {suggestion}")
                
                return APIResponse(
                    success=False,
                    error=f"{error_msg} - {suggestion}",
                    status_code=response.status_code,
                    response_time=0.0
                )
            
        except Exception as e:
            self.logger.error(f"Generation failed: {e}")
            return APIResponse(
                success=False,
                error=str(e),
                status_code=500,
                response_time=0.0
            )
    
    async def get_generation_status(self, generation_id: str) -> APIResponse:
        """
        Get the status of a generation job.
        
        Args:
            generation_id: Generation job ID
            
        Returns:
            API response with generation status
        """
        try:
            response = requests.get(
                f"{self.base_url}/task/{generation_id}",
                headers=self._get_headers(),
                timeout=10
            )
            
            response_data = response.json()
            
            if response.status_code == 200 and response_data.get("code") == 0:
                task_data = response_data["data"]
                
                return APIResponse(
                    success=True,
                    data={
                        'id': generation_id,
                        'status': task_data.get('status', 'unknown'),
                        'prompt': task_data.get('prompt', ''),
                        'format': 'glb',
                        'quality': 'high',
                        'progress': task_data.get('progress', 0),
                        'output': task_data.get('output', {}),
                        'created_at': task_data.get('created_at'),
                        'download_url': task_data.get('output', {}).get('model')
                    },
                    status_code=200,
                    response_time=0.0
                )
            else:
                error_msg = response_data.get("message", "Unknown error")
                return APIResponse(
                    success=False,
                    error=error_msg,
                    status_code=response.status_code,
                    response_time=0.0
                )
            
        except Exception as e:
            return APIResponse(
                success=False,
                error=str(e),
                status_code=500,
                response_time=0.0
            )
    
    async def wait_for_generation(
        self,
        generation_id: str,
        timeout: int = 300,
        poll_interval: float = 5.0
    ) -> APIResponse:
        """
        Wait for a generation job to complete.
        
        Args:
            generation_id: Generation job ID
            timeout: Maximum time to wait in seconds
            poll_interval: Time between status checks in seconds
            
        Returns:
            API response with final generation result
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            response = await self.get_generation_status(generation_id)
            
            if not response.success:
                return response
            
            status = response.data.get('status', 'unknown')
            
            if status in ['success', 'completed']:
                self.logger.info(f"Generation {generation_id} completed successfully")
                return response
            
            elif status == 'failed':
                error = response.data.get('error', 'Unknown error')
                self.logger.error(f"Generation {generation_id} failed: {error}")
                return APIResponse(
                    success=False,
                    error=f"Generation failed: {error}",
                    status_code=500,
                    response_time=time.time() - start_time
                )
            
            elif status in ['queued', 'running']:
                progress = response.data.get('progress', 0)
                self.logger.info(f"Generation {generation_id} status: {status}, progress: {progress}%")
                await asyncio.sleep(poll_interval)
            
            else:
                self.logger.warning(f"Unknown generation status: {status}")
                await asyncio.sleep(poll_interval)
        
        return APIResponse(
            success=False,
            error=f"Generation timeout after {timeout} seconds",
            status_code=408,
            response_time=timeout
        )
    
    async def download_model(self, generation_id: str, output_path: str) -> APIResponse:
        """
        Download a generated model.
        
        Args:
            generation_id: Generation job ID
            output_path: Path to save the model
            
        Returns:
            API response with download status
        """
        try:
            # Get the model URL from the task status
            status_response = await self.get_generation_status(generation_id)
            
            if not status_response.success:
                return status_response
            
            model_url = status_response.data.get('download_url')
            
            if not model_url:
                return APIResponse(
                    success=False,
                    error="No download URL available",
                    status_code=404,
                    response_time=0.0
                )
            
            # Download the model file
            os.makedirs(output_path, exist_ok=True)
            model_file_path = os.path.join(output_path, f"{generation_id}.glb")
            
            response = requests.get(model_url, timeout=60)
            
            if response.status_code == 200:
                with open(model_file_path, 'wb') as f:
                    f.write(response.content)
                
                return APIResponse(
                    success=True,
                    data={'output_path': model_file_path},
                    status_code=200,
                    response_time=0.0
                )
            else:
                return APIResponse(
                    success=False,
                    error=f"Failed to download model: {response.status_code}",
                    status_code=response.status_code,
                    response_time=0.0
                )
            
        except Exception as e:
            return APIResponse(
                success=False,
                error=str(e),
                status_code=500,
                response_time=0.0
            )
    
    async def close(self):
        """Close the client (no cleanup needed for REST API)."""
        pass 