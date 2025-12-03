import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration management for LLM routing service"""
    
    # API Keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', '')
    
    # Server Configuration
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'
    
    # Request Configuration
    REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', 30))
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', 3))
    
    # Routing Rules
    ROUTING_RULES_FILE = 'routing_rules.json'
    
    @classmethod
    def load_routing_rules(cls):
        """Load routing rules from JSON file"""
        try:
            with open(cls.ROUTING_RULES_FILE, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: {cls.ROUTING_RULES_FILE} not found. Using default rules.")
            return cls.get_default_rules()
        except json.JSONDecodeError as e:
            print(f"Error parsing {cls.ROUTING_RULES_FILE}: {e}. Using default rules.")
            return cls.get_default_rules()
    
    @classmethod
    def get_default_rules(cls):
        """Return default routing rules if file is not found"""
        return {
            "rules": [],
            "fallback_order": ["openai", "anthropic", "google"],
            "default_provider": "openai",
            "default_model": "gpt-3.5-turbo",
            "timeout_seconds": 30,
            "max_retries": 3
        }
    
    @classmethod
    def get_available_providers(cls):
        """Return list of providers with configured API keys"""
        providers = []
        if cls.OPENAI_API_KEY:
            providers.append('openai')
        if cls.ANTHROPIC_API_KEY:
            providers.append('anthropic')
        if cls.GOOGLE_API_KEY:
            providers.append('google')
        return providers
    
    @classmethod
    def validate_config(cls):
        """Validate configuration and return any warnings"""
        warnings = []
        
        if not cls.OPENAI_API_KEY:
            warnings.append("OpenAI API key not configured")
        if not cls.ANTHROPIC_API_KEY:
            warnings.append("Anthropic API key not configured")
        if not cls.GOOGLE_API_KEY:
            warnings.append("Google API key not configured")
        
        if not any([cls.OPENAI_API_KEY, cls.ANTHROPIC_API_KEY, cls.GOOGLE_API_KEY]):
            warnings.append("WARNING: No API keys configured! Please add at least one API key to .env file")
        
        return warnings
