# LLM Routing Service

A robust web application that intelligently routes user queries to multiple LLM providers based on configurable rules, with automatic fallback mechanisms for reliability.

## Features

- 🎯 **Intelligent Routing**: Routes queries based on type, token count, and cost optimization
- 🔄 **Automatic Fallback**: Switches to backup providers on failure/timeout
- 🌐 **Modern Web Interface**: Beautiful chat UI with real-time streaming responses
- 📊 **Provider Dashboard**: Visual status of all providers and routing decisions
- ⚙️ **Configurable Rules**: JSON-based routing rules you can customize
- 💰 **Cost Tracking**: Monitors and optimizes API costs

## Supported Providers

- **OpenAI** (GPT-4, GPT-3.5-turbo)
- **Anthropic** (Claude 3 models)
- **Google** (Gemini Pro, Gemini Flash)

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Keys

Copy the `.env.example` file to `.env`:

```bash
cp .env.example .env
```

Then edit the `.env` file and add your API keys:

```
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
GOOGLE_API_KEY=your_google_key_here
```

**Note**: You don't need all API keys. The system will work with whatever providers you configure.

### 3. Customize Routing Rules (Optional)

Edit `routing_rules.json` to customize how queries are routed to different providers.

### 4. Run the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Usage

1. Open your browser to `http://localhost:5000`
2. Type your query in the chat interface
3. The system will automatically:
   - Analyze your query
   - Select the best provider based on routing rules
   - Stream the response in real-time
   - Fall back to alternative providers if needed

## Configuration

### Routing Rules

The `routing_rules.json` file defines how queries are routed:

- **Query Type**: Route based on content type (code, general, creative, analytical)
- **Token Count**: Route based on query length
- **Cost Optimization**: Prefer cheaper providers for simple queries
- **Fallback Order**: Define backup providers

### Environment Variables

All API keys are stored in the `.env` file (never commit this file to version control):

- `OPENAI_API_KEY`: Your OpenAI API key
- `ANTHROPIC_API_KEY`: Your Anthropic API key
- `GOOGLE_API_KEY`: Your Google AI API key

## Project Structure

```
.
├── app.py                      # Flask application server
├── llm_router.py              # Main routing engine
├── config.py                  # Configuration management
├── routing_rules.json         # Routing rules configuration
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variable template
├── .env                      # Your API keys (create this)
├── providers/
│   ├── base_provider.py      # Abstract provider interface
│   ├── openai_provider.py    # OpenAI integration
│   ├── anthropic_provider.py # Anthropic integration
│   └── google_provider.py    # Google Gemini integration
├── utils/
│   ├── token_counter.py      # Token counting utilities
│   └── query_analyzer.py     # Query analysis
├── static/
│   ├── css/
│   │   └── style.css         # Application styles
│   └── js/
│       └── app.js            # Frontend logic
└── templates/
    └── index.html            # Main application page
```

## License

MIT
