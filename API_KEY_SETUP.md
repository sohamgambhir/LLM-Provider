# 🔑 API Key Setup Guide

This guide will help you configure your API keys for the LLM Routing Service.

## Where to Insert API Keys

All API keys should be added to a `.env` file in the root directory of the project.

### Step-by-Step Setup

#### 1. Create the .env file

Copy the example file to create your own `.env` file:

```bash
# On Windows (PowerShell)
Copy-Item .env.example .env

# On Windows (Command Prompt)
copy .env.example .env

# On macOS/Linux
cp .env.example .env
```

#### 2. Open the .env file

Open the `.env` file in any text editor (Notepad, VS Code, etc.)

#### 3. Add Your API Keys

Replace the placeholder values with your actual API keys:

```env
# OpenAI API Key
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Anthropic API Key
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Google AI API Key
GOOGLE_API_KEY=AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## Getting API Keys

### OpenAI API Key

1. Go to [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key (starts with `sk-proj-` or `sk-`)
5. Paste it in your `.env` file as `OPENAI_API_KEY`

**Models Available:**
- GPT-4 (best quality, higher cost)
- GPT-3.5-turbo (fast, cost-effective)

### Anthropic API Key

1. Go to [https://console.anthropic.com/](https://console.anthropic.com/)
2. Sign in or create an account
3. Navigate to "API Keys" section
4. Click "Create Key"
5. Copy the key (starts with `sk-ant-`)
6. Paste it in your `.env` file as `ANTHROPIC_API_KEY`

**Models Available:**
- Claude 3 Opus (most capable)
- Claude 3 Sonnet (balanced)
- Claude 3 Haiku (fastest, cheapest)

### Google AI API Key

1. Go to [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key (starts with `AIzaSy`)
5. Paste it in your `.env` file as `GOOGLE_API_KEY`

**Models Available:**
- Gemini 1.5 Pro (high capability, large context)
- Gemini 1.5 Flash (fast, cost-effective)

## Important Notes

### ⚠️ Security

- **NEVER** commit the `.env` file to version control (it's already in `.gitignore`)
- **NEVER** share your API keys publicly
- Keep your `.env` file secure and private

### 💡 You Don't Need All Keys

The application works with whatever providers you configure:
- **Minimum**: 1 API key (any provider)
- **Recommended**: 2-3 API keys for fallback functionality
- The system will automatically detect which providers are available

### 💰 Costs

Each provider has different pricing:
- **OpenAI**: Pay per token (GPT-3.5: ~$0.002/1K tokens, GPT-4: ~$0.03/1K tokens)
- **Anthropic**: Pay per token (Claude 3 Sonnet: ~$3/1M input tokens)
- **Google**: Free tier available, then pay per token (Gemini Flash: ~$0.35/1M tokens)

The application tracks costs in real-time!

## Verification

After adding your API keys, you can verify they work:

1. Start the application:
   ```bash
   python app.py
   ```

2. Check the console output:
   ```
   ✓ OpenAI provider initialized
   ✓ Anthropic provider initialized
   ✓ Google provider initialized
   ```

3. If a provider fails to initialize, check:
   - The API key is correct
   - There are no extra spaces in the `.env` file
   - The key has the correct prefix

## Example .env File

Here's what your `.env` file should look like (with your actual keys):

```env
# ============================================
# LLM ROUTING SERVICE - API KEYS
# ============================================

# OpenAI API Key
OPENAI_API_KEY=sk-proj-abc123def456ghi789jkl012mno345pqr678stu901vwx234yz

# Anthropic API Key
ANTHROPIC_API_KEY=sk-ant-api03-xyz789abc123def456ghi789jkl012mno345pqr678stu901

# Google AI API Key
GOOGLE_API_KEY=AIzaSyABC123DEF456GHI789JKL012MNO345PQR678STU

# ============================================
# OPTIONAL CONFIGURATION
# ============================================

REQUEST_TIMEOUT=30
MAX_RETRIES=3
DEBUG=false
```

## Troubleshooting

### "No providers available" error

**Problem**: The application can't find any valid API keys.

**Solution**:
1. Make sure the `.env` file exists in the project root
2. Check that API keys are correctly formatted
3. Verify there are no typos in the variable names

### Provider initialization fails

**Problem**: A specific provider fails to initialize.

**Solution**:
1. Verify the API key is valid
2. Check your internet connection
3. Ensure you have credits/quota with that provider
4. Try regenerating the API key

### "Module not found" errors

**Problem**: Python can't find required packages.

**Solution**:
```bash
pip install -r requirements.txt
```

## Need Help?

If you encounter issues:
1. Check the console output for specific error messages
2. Verify your API keys are active and have quota
3. Make sure all dependencies are installed
4. Check the provider's status page for outages

---

**Ready to start?** Once you've added at least one API key, run:

```bash
python app.py
```

Then open your browser to `http://localhost:5000` and start chatting! 🚀
