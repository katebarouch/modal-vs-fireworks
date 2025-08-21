# Modal Setup Guide

## Prerequisites
- Python 3.8+
- Modal account (sign up at [modal.com](https://modal.com))

## Setup Steps

### 1. Install Modal
```bash
pip install modal
```

**Note for Conda users**: If you're using conda/miniconda, you may need to install in the correct environment:
```bash
# Check which python you're using
which python

# If using conda, install directly with conda's pip
/path/to/your/conda/bin/pip install modal openai
```

### 2. Create Modal Account
1. Go to [modal.com](https://modal.com) and sign up
2. Verify your email address

### 3. Authenticate
```bash
modal token new
```
This will open a browser window to authenticate with Modal. You should see:
```
Web authentication finished successfully!
Token is connected to the [your-username] workspace.
Token verified successfully!
```

### 4. Create API Key Secrets
Modal runs in isolated containers, so API keys must be stored as Modal secrets:

```bash
# Create OpenAI secret (replace with your actual API key)
modal secret create openai-secret OPENAI_API_KEY="sk-proj-your-key-here"
```

### 5. Test Your Setup
```bash
cd modal/
modal run simple_chat.py
```