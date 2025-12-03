from typing import Dict, Any, Optional, Generator, List
import time
from config import Config
from providers import OpenAIProvider, AnthropicProvider, GoogleProvider, BaseProvider
from utils import QueryAnalyzer, TokenCounter

class LLMRouter:
    """Main routing engine for LLM providers"""
    
    def __init__(self):
        """Initialize the router with available providers"""
        self.config = Config()
        self.routing_rules = Config.load_routing_rules()
        self.providers: Dict[str, BaseProvider] = {}
        self.provider_status: Dict[str, Dict[str, Any]] = {}  # Track all provider statuses
        self._initialize_providers()
        
    def _initialize_providers(self):
        """Initialize all available providers based on API keys"""
        # Initialize OpenAI
        if Config.OPENAI_API_KEY:
            try:
                self.providers['openai'] = OpenAIProvider(
                    Config.OPENAI_API_KEY,
                    'gpt-4'
                )
                self.provider_status['openai'] = {
                    'available': True,
                    'model': 'gpt-4',
                    'error': None
                }
                print("✓ OpenAI provider initialized")
            except Exception as e:
                self.provider_status['openai'] = {
                    'available': False,
                    'model': 'gpt-4',
                    'error': str(e)
                }
                print(f"✗ Failed to initialize OpenAI: {e}")
        else:
            self.provider_status['openai'] = {
                'available': False,
                'model': 'gpt-4',
                'error': 'API key not configured'
            }
        
        # Initialize Anthropic
        if Config.ANTHROPIC_API_KEY:
            try:
                self.providers['anthropic'] = AnthropicProvider(
                    Config.ANTHROPIC_API_KEY,
                    'claude-3-sonnet-20240229'
                )
                self.provider_status['anthropic'] = {
                    'available': True,
                    'model': 'claude-3-sonnet-20240229',
                    'error': None
                }
                print("✓ Anthropic provider initialized")
            except Exception as e:
                self.provider_status['anthropic'] = {
                    'available': False,
                    'model': 'claude-3-sonnet-20240229',
                    'error': str(e)
                }
                print(f"✗ Failed to initialize Anthropic: {e}")
        else:
            self.provider_status['anthropic'] = {
                'available': False,
                'model': 'claude-3-sonnet-20240229',
                'error': 'API key not configured'
            }
        
        # Initialize Google
        if Config.GOOGLE_API_KEY:
            try:
                self.providers['google'] = GoogleProvider(
                    Config.GOOGLE_API_KEY,
                    'gemini-2.5-flash'
                )
                self.provider_status['google'] = {
                    'available': True,
                    'model': 'gemini-2.5-flash',
                    'error': None
                }
                print("✓ Google provider initialized")
            except Exception as e:
                self.provider_status['google'] = {
                    'available': False,
                    'model': 'gemini-2.5-flash',
                    'error': str(e)
                }
                print(f"✗ Failed to initialize Google: {e}")
        else:
            self.provider_status['google'] = {
                'available': False,
                'model': 'gemini-2.5-flash',
                'error': 'API key not configured'
            }
        
        if not self.providers:
            print("⚠ WARNING: No providers initialized! Please configure API keys in .env file")
    
    def route_query(self, query: str, user_preference: Optional[str] = None) -> Dict[str, Any]:
        """
        Route a query to the best provider
        
        Args:
            query: User's query
            user_preference: Optional user-specified provider preference
            
        Returns:
            Dictionary with routing decision
        """
        # Analyze the query
        query_metadata = QueryAnalyzer.analyze(query)
        
        # If user specified a preference, try to use it
        if user_preference and user_preference in self.providers:
            selected_provider = user_preference
            selected_model = self.providers[user_preference].model
            reason = f"User preference: {user_preference}"
        else:
            # Apply routing rules
            selected_provider, selected_model, reason = self._apply_routing_rules(query_metadata)
        
        return {
            'provider': selected_provider,
            'model': selected_model,
            'reason': reason,
            'query_metadata': query_metadata,
            'fallback_order': self._get_fallback_order(selected_provider)
        }
    
    def _apply_routing_rules(self, query_metadata: Dict[str, Any]) -> tuple:
        """Apply routing rules to select the best provider"""
        # Sort rules by priority
        rules = sorted(
            self.routing_rules.get('rules', []),
            key=lambda x: x.get('priority', 999)
        )
        
        # Try each rule
        for rule in rules:
            if self._rule_matches(rule, query_metadata):
                provider = rule['provider']
                model = rule['model']
                
                # Check if provider is available
                if provider in self.providers:
                    # Update provider's model
                    self.providers[provider].model = model
                    return provider, model, rule.get('description', rule['name'])
        
        # No rule matched, use default
        default_provider = self.routing_rules.get('default_provider', 'openai')
        default_model = self.routing_rules.get('default_model', 'gpt-3.5-turbo')
        
        # Check if default provider is available
        if default_provider in self.providers:
            self.providers[default_provider].model = default_model
            return default_provider, default_model, "Default routing"
        
        # If default not available, use first available provider
        if self.providers:
            first_provider = list(self.providers.keys())[0]
            first_model = self.providers[first_provider].model
            return first_provider, first_model, "First available provider"
        
        return None, None, "No providers available"
    
    def _rule_matches(self, rule: Dict[str, Any], query_metadata: Dict[str, Any]) -> bool:
        """Check if a routing rule matches the query metadata"""
        condition = rule.get('condition', {})
        
        # Check query type
        if 'query_type' in condition:
            if condition['query_type'] != query_metadata['query_type']:
                return False
        
        # Check token count minimum
        if 'token_count_min' in condition:
            if query_metadata['token_count'] < condition['token_count_min']:
                return False
        
        # Check token count maximum
        if 'token_count_max' in condition:
            if query_metadata['token_count'] > condition['token_count_max']:
                return False
        
        # Check complexity
        if 'complexity' in condition:
            if condition['complexity'] != query_metadata['complexity']:
                return False
        
        return True
    
    def _get_fallback_order(self, primary_provider: str) -> List[str]:
        """Get fallback order with OpenAI as default, then other working providers"""
        # Always start with OpenAI if available (unless it's already the primary)
        order = []
        
        # If primary is not OpenAI and OpenAI is available, use it first
        if primary_provider != 'openai' and 'openai' in self.providers:
            order.append('openai')
        
        # Add the primary provider
        if primary_provider and primary_provider in self.providers:
            order.append(primary_provider)
        elif primary_provider == 'openai' and 'openai' in self.providers:
            # If primary is OpenAI, add it first
            order.append('openai')
        
        # Add remaining providers from fallback order
        fallback = self.routing_rules.get('fallback_order', ['openai', 'anthropic', 'google'])
        for provider in fallback:
            if provider not in order and provider in self.providers:
                order.append(provider)
        
        # If no providers in order yet, add any available provider
        if not order:
            for provider in self.providers.keys():
                if provider not in order:
                    order.append(provider)
        
        return order
    
    def query_with_fallback(
        self,
        query: str,
        user_preference: Optional[str] = None,
        stream: bool = True
    ) -> Generator[Dict[str, Any], None, None]:
        """
        Query with automatic fallback on failure
        
        Args:
            query: User's query
            user_preference: Optional provider preference
            stream: Whether to stream responses
            
        Yields:
            Response chunks with metadata
        """
        # Get routing decision
        routing = self.route_query(query, user_preference)
        fallback_order = routing['fallback_order']
        
        # Yield routing decision
        yield {
            'type': 'routing',
            'data': routing
        }
        
        # Try each provider in fallback order
        for provider_name in fallback_order:
            if provider_name not in self.providers:
                continue
            
            provider = self.providers[provider_name]
            
            try:
                # Yield provider info
                yield {
                    'type': 'provider',
                    'data': {
                        'provider': provider_name,
                        'model': provider.model,
                        'status': 'attempting'
                    }
                }
                
                # Query the provider
                start_time = time.time()
                response_started = False
                
                for chunk in provider.query(query, stream=stream):
                    if not response_started:
                        response_started = True
                        yield {
                            'type': 'provider',
                            'data': {
                                'provider': provider_name,
                                'model': provider.model,
                                'status': 'success'
                            }
                        }
                    
                    yield {
                        'type': 'content',
                        'data': chunk
                    }
                
                # Success! No need to try fallback
                elapsed_time = time.time() - start_time
                yield {
                    'type': 'complete',
                    'data': {
                        'provider': provider_name,
                        'model': provider.model,
                        'elapsed_time': round(elapsed_time, 2),
                        'stats': provider.get_stats()
                    }
                }
                return
                
            except Exception as e:
                # Provider failed, try next one
                yield {
                    'type': 'error',
                    'data': {
                        'provider': provider_name,
                        'error': str(e),
                        'attempting_fallback': True
                    }
                }
                continue
        
        # All providers failed
        yield {
            'type': 'error',
            'data': {
                'error': 'All providers failed',
                'attempted_providers': fallback_order
            }
        }
    
    def get_provider_stats(self) -> List[Dict[str, Any]]:
        """Get statistics for all providers (including unavailable ones)"""
        stats = []
        
        # Return stats for all providers, not just initialized ones
        for name in ['openai', 'anthropic', 'google']:
            if name in self.providers:
                # Provider is working
                provider_stats = self.providers[name].get_stats()
                provider_stats['available'] = True
                provider_stats['error'] = None
                stats.append(provider_stats)
            elif name in self.provider_status:
                # Provider failed to initialize but we have status info
                stats.append({
                    'provider': name,
                    'model': self.provider_status[name]['model'],
                    'available': False,
                    'error': self.provider_status[name]['error'],
                    'total_tokens': 0,
                    'total_cost': 0,
                    'request_count': 0,
                    'error_count': 0,
                    'error_rate': 0
                })
        
        return stats
    
    def health_check(self) -> Dict[str, bool]:
        """Check health of all providers"""
        health = {}
        for name, provider in self.providers.items():
            try:
                health[name] = provider.health_check()
            except:
                health[name] = False
        return health
