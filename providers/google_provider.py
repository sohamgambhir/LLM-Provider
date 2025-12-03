from typing import Generator, Dict, Any
import google.generativeai as genai
from providers.base_provider import BaseProvider

class GoogleProvider(BaseProvider):
    """Google Gemini provider implementation"""
    
    # Pricing per 1M tokens (as of 2024)
    PRICING = {
        'gemini-1.5-pro': {'input': 3.50, 'output': 10.50},
        'gemini-1.5-flash': {'input': 0.35, 'output': 1.05},
        'gemini-pro': {'input': 0.50, 'output': 1.50},
    }
    
    def __init__(self, api_key: str, model: str = 'gemini-1.5-flash'):
        super().__init__(api_key, model)
        genai.configure(api_key=api_key)
        self.client = genai.GenerativeModel(model)
    
    def query(self, prompt: str, stream: bool = True, **kwargs) -> Generator[str, None, None]:
        """Send query to Google Gemini"""
        try:
            if stream:
                full_response = ""
                response = self.client.generate_content(prompt, stream=True)
                
                for chunk in response:
                    if chunk.text:
                        full_response += chunk.text
                        yield chunk.text
                
                # Update stats after streaming complete
                input_tokens = self.count_tokens(prompt)
                output_tokens = self.count_tokens(full_response)
                cost = self.estimate_cost(input_tokens, output_tokens)
                self.update_stats(input_tokens + output_tokens, cost)
            else:
                response = self.client.generate_content(prompt)
                content = response.text
                
                # Update stats
                input_tokens = self.count_tokens(prompt)
                output_tokens = self.count_tokens(content)
                cost = self.estimate_cost(input_tokens, output_tokens)
                self.update_stats(input_tokens + output_tokens, cost)
                
                yield content
                
        except Exception as e:
            self.update_stats(0, 0, is_error=True)
            raise Exception(f"Google error: {str(e)}")
    
    def count_tokens(self, text: str) -> int:
        """Estimate token count for Gemini"""
        try:
            # Use Gemini's token counting if available
            result = self.client.count_tokens(text)
            return result.total_tokens
        except:
            # Fallback: rough estimation
            return len(text) // 4
    
    def estimate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Estimate cost based on token usage"""
        pricing = self.PRICING.get(self.model, self.PRICING['gemini-1.5-flash'])
        input_cost = (input_tokens / 1_000_000) * pricing['input']
        output_cost = (output_tokens / 1_000_000) * pricing['output']
        return input_cost + output_cost
    
    def health_check(self) -> bool:
        """Check if Google API is accessible"""
        try:
            # Try a minimal request
            self.client.generate_content("Hi")
            return True
        except:
            return False
