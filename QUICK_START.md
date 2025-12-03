# 🔑 QUICK START: Where to Add Your API Keys

## TL;DR - 3 Simple Steps

### Step 1: Copy the template file
```bash
copy .env.example .env
```

### Step 2: Open `.env` file in any text editor

### Step 3: Replace the placeholder text with your actual API keys

```env
# BEFORE (template):
OPENAI_API_KEY=your_openai_api_key_here

# AFTER (your actual key):
OPENAI_API_KEY=sk-proj-abc123xyz789...
```

---

## 📍 Exact Location

**File to edit:** `d:/Work/Carnot_Research/New folder/.env`

If this file doesn't exist, create it by copying `.env.example`

---

## 🔑 API Key Format Examples

### OpenAI
```env
OPENAI_API_KEY=sk-proj-1234567890abcdefghijklmnopqrstuvwxyz
```
- Starts with: `sk-proj-` or `sk-`
- Get it from: https://platform.openai.com/api-keys

### Anthropic
```env
ANTHROPIC_API_KEY=sk-ant-api03-1234567890abcdefghijklmnopqrstuvwxyz
```
- Starts with: `sk-ant-`
- Get it from: https://console.anthropic.com/

### Google
```env
GOOGLE_API_KEY=AIzaSy1234567890abcdefghijklmnopqrstuvwxyz
```
- Starts with: `AIzaSy`
- Get it from: https://makersuite.google.com/app/apikey

---

## ✅ Complete Example

Your `.env` file should look like this:

```env
# OpenAI API Key
OPENAI_API_KEY=sk-proj-abc123def456ghi789jkl012mno345pqr678

# Anthropic API Key
ANTHROPIC_API_KEY=sk-ant-api03-xyz789abc123def456ghi789jkl012

# Google AI API Key
GOOGLE_API_KEY=AIzaSyABC123DEF456GHI789JKL012MNO345PQR
```

---

## ⚠️ Important Notes

1. **You don't need all 3 keys** - The app works with any combination (minimum 1)
2. **Never commit this file** - It's already in `.gitignore`
3. **No quotes needed** - Just paste the key directly
4. **No spaces** - Make sure there are no extra spaces

---

## 🚀 After Adding Keys

Run the application:
```bash
python app.py
```

You should see:
```
✓ OpenAI provider initialized
✓ Anthropic provider initialized
✓ Google provider initialized
```

Then open: **http://localhost:5000**

---

## 🆘 Need More Help?

See the detailed guide: [API_KEY_SETUP.md](file:///d:/Work/Carnot_Research/New%20folder/API_KEY_SETUP.md)
