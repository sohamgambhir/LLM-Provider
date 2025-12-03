from typing import Generator, Dict, Any
import openai
import tiktoken
from providers.base_provider import BaseProvider

class OpenAIProvider(BaseProvider):
    """OpenAI provider implementation"""
    
    # Pricing per 1K tokens (as of 2024)
    PRICING = {
        'gpt-4': {'input': 0.03, 'output': 0.06},
        'gpt-4-turbo-preview': {'input': 0.01, 'output': 0.03},
        'gpt-3.5-turbo': {'input': 0.0005, 'output': 0.0015},
        'gpt-3.5-turbo-16k': {'input': 0.003, 'output': 0.004},
    }
    
    def __init__(self, api_key: str, model: str = 'gpt-3.5-turbo'):
        super().__init__(api_key, model)
        openai.api_key = api_key
        self.client = openai.OpenAI(api_key=api_key)
        
        # Initialize tokenizer
        try:
            self.encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            self.encoding = tiktoken.get_encoding("cl100k_base")
    
    def query(self, prompt: str, stream: bool = True, **kwargs) -> Generator[str, None, None]:
        """Send query to OpenAI"""
        try:
            messages = [{"role": "user", "content": prompt}]
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=stream,
                **kwargs
            )
            
            if stream:
                full_response = ""
                for chunk in response:
                    if chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        full_response += content
                        yield content
                
                # Update stats after streaming complete
                input_tokens = self.count_tokens(prompt)
                output_tokens = self.count_tokens(full_response)
                cost = self.estimate_cost(input_tokens, output_tokens)
                self.update_stats(input_tokens + output_tokens, cost)
            else:
                content = response.choices[0].message.content
                input_tokens = self.count_tokens(prompt)
                output_tokens = self.count_tokens(content)
                cost = self.estimate_cost(input_tokens, output_tokens)
                self.update_stats(input_tokens + output_tokens, cost)
                yield content
                
        except Exception as e:
            self.update_stats(0, 0, is_error=True)
            raise Exception(f"OpenAI error: {str(e)}")
    
    def count_tokens(self, text: str) -> int:
        """Count tokens using tiktoken"""
        try:
            return len(self.encoding.encode(text))
        except:
            # Fallback: rough estimation
            return len(text) // 4
    
    def estimate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Estimate cost based on token usage"""
        pricing = self.PRICING.get(self.model, self.PRICING['gpt-3.5-turbo'])
        input_cost = (input_tokens / 1000) * pricing['input']
        output_cost = (output_tokens / 1000) * pricing['output']
        return input_cost + output_cost
    
    def health_check(self) -> bool:
        """Check if OpenAI API is accessible"""
        try:
            self.client.models.list()
            return True
        except:
            return False
