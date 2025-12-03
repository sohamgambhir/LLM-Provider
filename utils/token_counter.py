class TokenCounter:
    """Utility for counting tokens across different providers"""
    
    @staticmethod
    def estimate_tokens(text: str, provider: str = 'generic') -> int:
        """
        Estimate token count for a given text
        
        Args:
            text: Text to count tokens for
            provider: Provider name (openai, anthropic, google, generic)
            
        Returns:
            Estimated token count
        """
        # Different providers have slightly different tokenization
        # This is a rough estimation
        
        if provider == 'openai':
            # OpenAI uses tiktoken, roughly 4 chars per token
            return len(text) // 4
        elif provider == 'anthropic':
            # Claude uses similar tokenization
            return len(text) // 4
        elif provider == 'google':
            # Gemini tokenization
            return len(text) // 4
        else:
            # Generic estimation
            return len(text.split())
    
    @staticmethod
    def check_context_limit(token_count: int, model: str) -> bool:
        """
        Check if token count is within model's context limit
        
        Args:
            token_count: Number of tokens
            model: Model name
            
        Returns:
            True if within limit, False otherwise
        """
        # Context limits for various models
        CONTEXT_LIMITS = {
            'gpt-3.5-turbo': 4096,
            'gpt-3.5-turbo-16k': 16384,
            'gpt-4': 8192,
            'gpt-4-turbo-preview': 128000,
            'claude-3-opus-20240229': 200000,
            'claude-3-sonnet-20240229': 200000,
            'claude-3-haiku-20240307': 200000,
            'gemini-1.5-pro': 1000000,
            'gemini-1.5-flash': 1000000,
            'gemini-pro': 32768,
        }
        
        limit = CONTEXT_LIMITS.get(model, 4096)
        return token_count <= limit
    
    @staticmethod
    def get_context_limit(model: str) -> int:
        """Get context limit for a model"""
        CONTEXT_LIMITS = {
            'gpt-3.5-turbo': 4096,
            'gpt-3.5-turbo-16k': 16384,
            'gpt-4': 8192,
            'gpt-4-turbo-preview': 128000,
            'claude-3-opus-20240229': 200000,
            'claude-3-sonnet-20240229': 200000,
            'claude-3-haiku-20240307': 200000,
            'gemini-1.5-pro': 1000000,
            'gemini-1.5-flash': 1000000,
            'gemini-pro': 32768,
        }
        
        return CONTEXT_LIMITS.get(model, 4096)
