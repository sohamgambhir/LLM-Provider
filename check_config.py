"""
Troubleshooting script to check .env file configuration
"""
import os
from pathlib import Path
from dotenv import load_dotenv

print("=" * 60)
print("🔍 LLM Router - Configuration Troubleshooter")
print("=" * 60)

# Check if .env file exists
env_file = Path('.env')
if not env_file.exists():
    print("\n❌ ERROR: .env file not found!")
    print("   Please create it by copying .env.example:")
    print("   copy .env.example .env")
    exit(1)
else:
    print(f"\n✓ .env file found at: {env_file.absolute()}")

# Load environment variables
load_dotenv()

print("\n" + "=" * 60)
print("Checking API Keys...")
print("=" * 60)

# Check each API key
keys_found = 0

# OpenAI
openai_key = os.getenv('OPENAI_API_KEY', '')
if openai_key and openai_key != 'your_openai_api_key_here':
    if openai_key.startswith('sk-'):
        print("\n✓ OpenAI API Key: CONFIGURED")
        print(f"  Format: {openai_key[:10]}...{openai_key[-4:]}")
        keys_found += 1
    else:
        print("\n⚠ OpenAI API Key: INVALID FORMAT")
        print("  Should start with 'sk-'")
else:
    print("\n✗ OpenAI API Key: NOT CONFIGURED")
    print("  Add: OPENAI_API_KEY=sk-proj-your_key_here")

# Anthropic
anthropic_key = os.getenv('ANTHROPIC_API_KEY', '')
if anthropic_key and anthropic_key != 'your_anthropic_api_key_here':
    if anthropic_key.startswith('sk-ant-'):
        print("\n✓ Anthropic API Key: CONFIGURED")
        print(f"  Format: {anthropic_key[:10]}...{anthropic_key[-4:]}")
        keys_found += 1
    else:
        print("\n⚠ Anthropic API Key: INVALID FORMAT")
        print("  Should start with 'sk-ant-'")
else:
    print("\n✗ Anthropic API Key: NOT CONFIGURED")
    print("  Add: ANTHROPIC_API_KEY=sk-ant-your_key_here")

# Google
google_key = os.getenv('GOOGLE_API_KEY', '')
if google_key and google_key != 'your_google_api_key_here':
    if google_key.startswith('AIzaSy'):
        print("\n✓ Google API Key: CONFIGURED")
        print(f"  Format: {google_key[:10]}...{google_key[-4:]}")
        keys_found += 1
    else:
        print("\n⚠ Google API Key: INVALID FORMAT")
        print("  Should start with 'AIzaSy'")
else:
    print("\n✗ Google API Key: NOT CONFIGURED")
    print("  Add: GOOGLE_API_KEY=AIzaSy_your_key_here")

print("\n" + "=" * 60)
print(f"Summary: {keys_found} API key(s) configured")
print("=" * 60)

if keys_found == 0:
    print("\n❌ NO API KEYS CONFIGURED!")
    print("\nCommon issues:")
    print("1. Make sure you copied .env.example to .env")
    print("2. Replace the placeholder text with your actual keys")
    print("3. Remove any quotes around the keys")
    print("4. Make sure there are no extra spaces")
    print("\nExample .env file:")
    print("  OPENAI_API_KEY=sk-proj-abc123...")
    print("  ANTHROPIC_API_KEY=sk-ant-xyz789...")
    print("  GOOGLE_API_KEY=AIzaSy123456...")
else:
    print(f"\n✓ Configuration looks good! {keys_found} provider(s) available.")
    print("\nYou can now run: python app.py")

print("\n" + "=" * 60)
