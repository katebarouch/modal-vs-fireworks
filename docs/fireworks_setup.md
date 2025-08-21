# Fireworks AI Setup Guide

## Overview
Fireworks AI is a managed inference platform that provides fast, cost-effective access to open-source LLMs through a simple API.

## Prerequisites
- Python 3.8+
- Fireworks AI account and API key
- Custom model deployment on Fireworks (required for this comparison)

## Installation

1. **Install required packages:**
   ```bash
   pip install requests
   ```

2. **Set up your API key:**
   ```bash
   export FIREWORKS_API_KEY="your-fireworks-api-key-here"
   ```

## Custom Model Deployment

1. **Create a deployment on Fireworks dashboard:**
   - Go to [Fireworks Dashboard](https://app.fireworks.ai/dashboard)
   - Navigate to "Deployments" → "Create"
   - Select model: `accounts/fireworks/models/gpt-oss-20b`
   - Configure performance settings (can skip speculative decoding to save costs)
   - Set display name: `simple_llm` (or your preferred name)
   - Deploy the model

2. **Update the model endpoint in `fireworks/simple_chat.py`:**

Just change one line - replace `YOUR_MODEL_ID` with your actual deployed model ID:

```python
"model": "accounts/k8b/deployedModels/YOUR_MODEL_ID",
```

For example:
```python
"model": "accounts/k8b/deployedModels/llama-v3p1-8b-instruct-zoobeb06",
```

3. **Test your setup:**
```bash
python fireworks/simple_chat.py
```
