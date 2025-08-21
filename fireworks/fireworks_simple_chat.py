"""
Simple chat completion example using Fireworks AI for LLM inference.
This example demonstrates basic usage and measures response time.
"""

import os
import time
import requests
import json

def generate_text(prompt, max_tokens=150, is_first_call=False):
    """Generate text using Fireworks AI custom deployment."""
    function_start = time.time()
    
    # Get API key from environment
    api_key = os.environ.get("FIREWORKS_API_KEY")
    if not api_key:
        raise ValueError("FIREWORKS_API_KEY environment variable is required")
        
    # Start timing the actual API request
    request_start = time.time()

    url = "https://api.fireworks.ai/inference/v1/chat/completions"
    payload = {

        # copy and paste your model ID here
        "model": "accounts/k8b/deployedModels/YOUR_MODEL_ID",
    
        "max_tokens": max_tokens,
        "top_p": 1,
        "top_k": 40,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "temperature": 0.6,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # send and collect response
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    # get the time it took to get the response
    request_end = time.time()
    
    # Calculate timing metrics
    request_latency = request_end - request_start  # Pure latency
    total_time = request_end - function_start      # Total time
            
    # parse response
    response_data = response.json()
        
    # extract content and reasoning_content fields from response
    message = response_data['choices'][0]['message']
    if 'content' in message and message['content']:
        response_text = message['content']
    else:
        response_text = "No content available"
        
    # return response
    return {
        "response": response_text,
        "request_latency": request_latency,  # Pure API request time
        "total_time": total_time,           # Total function time
        "is_cold_start": is_first_call,     # Cold start indicator
        "usage": {
            "prompt_tokens": response_data['usage']['prompt_tokens'],
            "completion_tokens": response_data['usage']['completion_tokens'],
            "total_tokens": response_data['usage']['total_tokens']
        }
    }

def main():
    """
    Test the Fireworks AI function with sample prompts.
    """
    print("Testing Fireworks AI LLM inference...")
    
    # Check for API key
    if not os.getenv("FIREWORKS_API_KEY"):
        print("Error: FIREWORKS_API_KEY environment variable not set")
        print("Please set it with: export FIREWORKS_API_KEY='your_api_key'")
        return
    
    # Test prompts
    prompt1 = "How many hours would it take to walk across the United States?"
    prompt2 = "What is the most popular dessert in the world?"
    
    # First call (cold start measurement)
    print("\n Cold Start Test")
    print(f"Prompt: {prompt1}")
    result1 = generate_text(prompt1, is_first_call=True)
    print(f"Response: {result1['response'][:100]}...")
    print(f"Request latency: {result1['request_latency']:.2f}s")
    print(f"Total time: {result1['total_time']:.2f}s")
    print(f"Cold start: {result1['is_cold_start']}")
    
    # Second call (warm start measurement)
    print("\n Warm Start Test")
    print(f"Prompt: {prompt2}")
    result2 = generate_text(prompt2, is_first_call=False)
    print(f"Response: {result2['response'][:100]}...")
    print(f"Request latency: {result2['request_latency']:.2f}s")
    print(f"Total time: {result2['total_time']:.2f}s")
    print(f"Cold start: {result2['is_cold_start']}")
    
    # Use second result for cost calculation
    result = result2
    print(f"\nTokens used: {result['usage']['total_tokens']} ({result['usage']['prompt_tokens']} prompt + {result['usage']['completion_tokens']} completion)")
    
    # Cost estimation (approximate rates for custom deployment)
    estimated_cost = result['usage']['total_tokens'] * 0.00007  # Rough estimate
    print(f"Estimated cost: ${estimated_cost:.4f}")

if __name__ == "__main__":
    main()
