from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Generator
import time

class BaseProvider(ABC):
    """Abstract base class for LLM providers"""
    
    def __init__(self, api_key: str, model: str):
        """
        Initialize provider
        
        Args:
            api_key: API key for the provider
            model: Model name to use
        """
        self.api_key = api_key
        self.model = model
        self.last_request_time = 0
        self.total_tokens_used = 0
        self.total_cost = 0.0
        self.request_count = 0
        self.error_count = 0
    
    @abstractmethod
    def query(self, prompt: str, stream: bool = True, **kwargs) -> Generator[str, None, None]:
        """
        Send a query to the LLM provider
        
        Args:
            prompt: The user's query
            stream: Whether to stream the response
            **kwargs: Additional provider-specific parameters
            
        Yields:
            Response chunks if streaming, or full response
        """
        pass
    
    @abstractmethod
    def count_tokens(self, text: str) -> int:
        """
        Count tokens in the given text
        
        Args:
            text: Text to count tokens for
            
        Returns:
            Number of tokens
        """
        pass
    
    @abstractmethod
    def estimate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """
        Estimate cost for a request
        
        Args:
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            
        Returns:
            Estimated cost in USD
        """
        pass
    
    @abstractmethod
    def health_check(self) -> bool:
        """
        Check if the provider is available
        
        Returns:
            True if provider is healthy, False otherwise
        """
        pass
    
    def get_provider_name(self) -> str:
        """Get the provider name"""
        return self.__class__.__name__.replace('Provider', '').lower()
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get provider statistics
        
        Returns:
            Dictionary with provider stats
        """
        return {
            'provider': self.get_provider_name(),
            'model': self.model,
            'total_tokens': self.total_tokens_used,
            'total_cost': round(self.total_cost, 4),
            'request_count': self.request_count,
            'error_count': self.error_count,
            'error_rate': round(self.error_count / max(self.request_count, 1), 2)
        }
    
    def update_stats(self, tokens: int, cost: float, is_error: bool = False):
        """Update provider statistics"""
        self.request_count += 1
        if is_error:
            self.error_count += 1
        else:
            self.total_tokens_used += tokens
            self.total_cost += cost
        self.last_request_time = time.time()
    
    def __str__(self):
        return f"{self.get_provider_name()}({self.model})"
