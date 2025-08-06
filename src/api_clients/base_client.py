"""
Base API client class for external API integrations.
"""

import asyncio
import json
import time
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Union
from urllib.parse import urljoin

import aiohttp
import httpx
import requests
from pydantic import BaseModel

from ..utils.logger import get_logger, LoggerMixin
from ..utils.validators import validate_api_key, validate_url


class APIResponse(BaseModel):
    """Standard API response model."""
    
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    status_code: int
    headers: Dict[str, str] = {}
    response_time: float = 0.0


class BaseAPIClient(ABC, LoggerMixin):
    """
    Base class for API clients with common functionality.
    """
    
    def __init__(
        self,
        base_url: str,
        api_key: str,
        timeout: int = 30,
        max_retries: int = 3,
        retry_delay: float = 1.0
    ):
        """
        Initialize the API client.
        
        Args:
            base_url: Base URL for the API
            api_key: API key for authentication
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries
            retry_delay: Delay between retries in seconds
        """
        self.base_url = validate_url(base_url)
        self.api_key = validate_api_key(api_key)
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        
        self.session = None
        self.async_session = None
        
        self.logger.info(f"Initialized API client for {base_url}")
    
    def _get_headers(self, additional_headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """
        Get default headers for API requests.
        
        Args:
            additional_headers: Additional headers to include
            
        Returns:
            Dictionary of headers
        """
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': '3D-AR-Demo/1.0.0'
        }
        
        if additional_headers:
            headers.update(additional_headers)
        
        return headers
    
    def _build_url(self, endpoint: str) -> str:
        """
        Build full URL for API endpoint.
        
        Args:
            endpoint: API endpoint path
            
        Returns:
            Full URL
        """
        return urljoin(self.base_url, endpoint.lstrip('/'))
    
    def _handle_response(
        self,
        response: Union[requests.Response, httpx.Response, aiohttp.ClientResponse],
        start_time: float
    ) -> APIResponse:
        """
        Handle API response and convert to standard format.
        
        Args:
            response: HTTP response object
            start_time: Request start time
            
        Returns:
            Standardized API response
        """
        response_time = time.time() - start_time
        
        try:
            if hasattr(response, 'json'):
                data = response.json()
            else:
                data = None
            
            return APIResponse(
                success=response.status_code < 400,
                data=data,
                error=None if response.status_code < 400 else f"HTTP {response.status_code}",
                status_code=response.status_code,
                headers=dict(response.headers),
                response_time=response_time
            )
        
        except Exception as e:
            self.logger.error(f"Error parsing response: {e}")
            return APIResponse(
                success=False,
                error=f"Failed to parse response: {e}",
                status_code=response.status_code,
                response_time=response_time
            )
    
    def _handle_error(self, error: Exception, start_time: float) -> APIResponse:
        """
        Handle API request errors.
        
        Args:
            error: Exception that occurred
            start_time: Request start time
            
        Returns:
            Error response
        """
        response_time = time.time() - start_time
        self.logger.error(f"API request failed: {error}")
        
        return APIResponse(
            success=False,
            error=str(error),
            status_code=0,
            response_time=response_time
        )
    
    def request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> APIResponse:
        """
        Make synchronous HTTP request.
        
        Args:
            method: HTTP method
            endpoint: API endpoint
            data: Request data
            headers: Additional headers
            params: Query parameters
            
        Returns:
            API response
        """
        url = self._build_url(endpoint)
        request_headers = self._get_headers(headers)
        
        self.logger.debug(f"Making {method} request to {url}")
        start_time = time.time()
        
        for attempt in range(self.max_retries + 1):
            try:
                response = requests.request(
                    method=method,
                    url=url,
                    json=data,
                    headers=request_headers,
                    params=params,
                    timeout=self.timeout
                )
                
                api_response = self._handle_response(response, start_time)
                
                if api_response.success or attempt == self.max_retries:
                    return api_response
                
                self.logger.warning(f"Request failed (attempt {attempt + 1}/{self.max_retries + 1})")
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay * (2 ** attempt))  # Exponential backoff
                
            except Exception as e:
                if attempt == self.max_retries:
                    return self._handle_error(e, start_time)
                
                self.logger.warning(f"Request error (attempt {attempt + 1}/{self.max_retries + 1}): {e}")
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay * (2 ** attempt))
        
        return APIResponse(
            success=False,
            error="Max retries exceeded",
            status_code=0,
            response_time=time.time() - start_time
        )
    
    async def async_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> APIResponse:
        """
        Make asynchronous HTTP request.
        
        Args:
            method: HTTP method
            endpoint: API endpoint
            data: Request data
            headers: Additional headers
            params: Query parameters
            
        Returns:
            API response
        """
        url = self._build_url(endpoint)
        request_headers = self._get_headers(headers)
        
        self.logger.debug(f"Making async {method} request to {url}")
        start_time = time.time()
        
        if self.async_session is None:
            self.async_session = aiohttp.ClientSession()
        
        for attempt in range(self.max_retries + 1):
            try:
                async with self.async_session.request(
                    method=method,
                    url=url,
                    json=data,
                    headers=request_headers,
                    params=params,
                    timeout=aiohttp.ClientTimeout(total=self.timeout)
                ) as response:
                    api_response = self._handle_response(response, start_time)
                    
                    if api_response.success or attempt == self.max_retries:
                        return api_response
                    
                    self.logger.warning(f"Async request failed (attempt {attempt + 1}/{self.max_retries + 1})")
                    if attempt < self.max_retries:
                        await asyncio.sleep(self.retry_delay * (2 ** attempt))
                
            except Exception as e:
                if attempt == self.max_retries:
                    return self._handle_error(e, start_time)
                
                self.logger.warning(f"Async request error (attempt {attempt + 1}/{self.max_retries + 1}): {e}")
                if attempt < self.max_retries:
                    await asyncio.sleep(self.retry_delay * (2 ** attempt))
        
        return APIResponse(
            success=False,
            error="Max retries exceeded",
            status_code=0,
            response_time=time.time() - start_time
        )
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> APIResponse:
        """Make GET request."""
        return self.request('GET', endpoint, params=params)
    
    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> APIResponse:
        """Make POST request."""
        return self.request('POST', endpoint, data=data)
    
    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> APIResponse:
        """Make PUT request."""
        return self.request('PUT', endpoint, data=data)
    
    def delete(self, endpoint: str) -> APIResponse:
        """Make DELETE request."""
        return self.request('DELETE', endpoint)
    
    async def async_get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> APIResponse:
        """Make async GET request."""
        return await self.async_request('GET', endpoint, params=params)
    
    async def async_post(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> APIResponse:
        """Make async POST request."""
        return await self.async_request('POST', endpoint, data=data)
    
    async def async_put(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> APIResponse:
        """Make async PUT request."""
        return await self.async_request('PUT', endpoint, data=data)
    
    async def async_delete(self, endpoint: str) -> APIResponse:
        """Make async DELETE request."""
        return await self.async_request('DELETE', endpoint)
    
    def close(self):
        """Close HTTP sessions."""
        if self.session:
            self.session.close()
    
    async def aclose(self):
        """Close async HTTP sessions."""
        if self.async_session:
            await self.async_session.close()
    
    @abstractmethod
    def health_check(self) -> APIResponse:
        """Check API health/connectivity."""
        pass
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
    
    async def __aenter__(self):
        """Async context manager entry."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.aclose() 