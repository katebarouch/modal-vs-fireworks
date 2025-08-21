# Modal Setup Guide

## Prerequisites
- Python 3.8+
- Modal account (sign up at [modal.com](https://modal.com))

## Setup Steps

### 1. Install Modal
```bash
pip install modal
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

### 4. Test Your Setup
```bash
modal run modal/modal_simple_chat.py
```