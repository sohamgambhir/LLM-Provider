from flask import Flask, render_template, request, jsonify, Response, stream_with_context
import json
from llm_router import LLMRouter
from config import Config

app = Flask(__name__)
router = LLMRouter()

@app.route('/')
def index():
    """Serve the main application page"""
    return render_template('index.html')

@app.route('/api/query', methods=['POST'])
def query():
    """Handle query requests with streaming response"""
    data = request.json
    user_query = data.get('query', '')
    user_preference = data.get('provider', None)
    
    if not user_query:
        return jsonify({'error': 'Query is required'}), 400
    
    def generate():
        """Generate streaming response"""
        try:
            for event in router.query_with_fallback(user_query, user_preference, stream=True):
                # Send as server-sent event
                yield f"data: {json.dumps(event)}\n\n"
        except Exception as e:
            error_event = {
                'type': 'error',
                'data': {'error': str(e)}
            }
            yield f"data: {json.dumps(error_event)}\n\n"
    
    return Response(
        stream_with_context(generate()),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no'
        }
    )

@app.route('/api/providers', methods=['GET'])
def get_providers():
    """Get available providers and their stats"""
    stats = router.get_provider_stats()
    available_providers = list(router.providers.keys())
    
    return jsonify({
        'providers': available_providers,
        'stats': stats,
        'routing_rules': router.routing_rules
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Check health of all providers"""
    health = router.health_check()
    return jsonify(health)

@app.route('/api/config', methods=['GET'])
def get_config():
    """Get current configuration"""
    warnings = Config.validate_config()
    
    return jsonify({
        'available_providers': Config.get_available_providers(),
        'warnings': warnings,
        'routing_rules': router.routing_rules
    })

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 LLM Routing Service Starting...")
    print("="*60)
    
    # Validate configuration
    warnings = Config.validate_config()
    if warnings:
        print("\n⚠️  Configuration Warnings:")
        for warning in warnings:
            print(f"   - {warning}")
        print()
    
    # Show available providers
    available = Config.get_available_providers()
    if available:
        print(f"\n✓ Available providers: {', '.join(available)}")
    else:
        print("\n✗ No providers available!")
        print("   Please add API keys to .env file")
        print("   Copy .env.example to .env and add your keys")
    
    print(f"\n🌐 Server starting at http://localhost:{Config.PORT}")
    print("="*60 + "\n")
    
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )
