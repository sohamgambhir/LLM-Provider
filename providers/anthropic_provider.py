from typing import Generator, Dict, Any
import anthropic
from providers.base_provider import BaseProvider

class AnthropicProvider(BaseProvider):
    """Anthropic Claude provider implementation"""
    
    # Pricing per 1M tokens (as of 2024)
    PRICING = {
        'claude-3-opus-20240229': {'input': 15.00, 'output': 75.00},
        'claude-3-sonnet-20240229': {'input': 3.00, 'output': 15.00},
        'claude-3-haiku-20240307': {'input': 0.25, 'output': 1.25},
    }
    
    def __init__(self, api_key: str, model: str = 'claude-3-sonnet-20240229'):
        super().__init__(api_key, model)
        self.client = anthropic.Anthropic(api_key=api_key)
    
    def query(self, prompt: str, stream: bool = True, **kwargs) -> Generator[str, None, None]:
        """Send query to Anthropic Claude"""
        try:
            max_tokens = kwargs.get('max_tokens', 4096)
            
            if stream:
                full_response = ""
                with self.client.messages.stream(
                    model=self.model,
                    max_tokens=max_tokens,
                    messages=[{"role": "user", "content": prompt}]
                ) as stream:
                    for text in stream.text_stream:
                        full_response += text
                        yield text
                
                # Update stats after streaming complete
                input_tokens = self.count_tokens(prompt)
                output_tokens = self.count_tokens(full_response)
                cost = self.estimate_cost(input_tokens, output_tokens)
                self.update_stats(input_tokens + output_tokens, cost)
            else:
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=max_tokens,
                    messages=[{"role": "user", "content": prompt}]
                )
                content = response.content[0].text
                
                # Update stats
                input_tokens = response.usage.input_tokens
                output_tokens = response.usage.output_tokens
                cost = self.estimate_cost(input_tokens, output_tokens)
                self.update_stats(input_tokens + output_tokens, cost)
                
                yield content
                
        except Exception as e:
            self.update_stats(0, 0, is_error=True)
            raise Exception(f"Anthropic error: {str(e)}")
    
    def count_tokens(self, text: str) -> int:
        """Estimate token count for Claude"""
        # Claude uses similar tokenization to GPT
        # Rough estimation: ~4 characters per token
        return len(text) // 4
    
    def estimate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Estimate cost based on token usage"""
        pricing = self.PRICING.get(self.model, self.PRICING['claude-3-sonnet-20240229'])
        input_cost = (input_tokens / 1_000_000) * pricing['input']
        output_cost = (output_tokens / 1_000_000) * pricing['output']
        return input_cost + output_cost
    
    def health_check(self) -> bool:
        """Check if Anthropic API is accessible"""
        try:
            # Try a minimal request
            self.client.messages.create(
                model=self.model,
                max_tokens=10,
                messages=[{"role": "user", "content": "Hi"}]
            )
            return True
        except:
            return False
