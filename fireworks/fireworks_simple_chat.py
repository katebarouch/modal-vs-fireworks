"""
Simple chat completion example using Fireworks AI for LLM inference.
This example demonstrates basic usage and measures response time.
"""

import os
import time
import requests
import json

def generate_text(prompt, max_tokens=150):
    """Generate text using Fireworks AI custom deployment."""
    function_start = time.time()
    
    # Get API key from environment
    api_key = os.environ.get("FIREWORKS_API_KEY")
    if not api_key:
        raise ValueError("FIREWORKS_API_KEY environment variable is required")
        
    # Start timing the actual API request
    inference_start = time.time()

    url = "https://api.fireworks.ai/inference/v1/chat/completions"
    payload = {

        # copy and paste your model ID here
        "model": "accounts/k8b/deployedModels/llama-v3p1-8b-instruct-zoobeb06",
    
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
    inference_end = time.time()
    
    # Calculate timing metrics
    init_time = function_start - inference_start
    inference_time = inference_end - inference_start
    total_time = inference_end - function_start
            
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
        "init_time": init_time,
        "inference_time": inference_time,
        "total_time": total_time,
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
    
    # Test prompts
    prompt1 = "How many hours would it take to walk across the United States?"
    prompt2 = "What is the most popular dessert in the world?"
    
    # First call (cold start measurement)
    print("\n Cold Start Test")
    print(f"Prompt: {prompt1}")
    result1 = generate_text(prompt1)
    print(f"Response: {result1['response'][:100]}...")
    print(f"Init time: {result1['init_time']:.2f}s")
    print(f"Inference time: {result1['inference_time']:.2f}s")
    print(f"Total time: {result1['total_time']:.2f}s")
    
    # Second call (warm start measurement)
    print("\n Warm Start Test")
    print(f"Prompt: {prompt2}")
    result2 = generate_text(prompt2)
    print(f"Response: {result2['response'][:100]}...")
    print(f"Init time: {result2['init_time']:.2f}s")
    print(f"Inference time: {result2['inference_time']:.2f}s")
    print(f"Total time: {result2['total_time']:.2f}s")
    
    # Use second result for cost calculation
    result = result2
    print(f"\nTokens used: {result['usage']['total_tokens']} ({result['usage']['prompt_tokens']} prompt + {result['usage']['completion_tokens']} completion)")
    
    # Cost estimation (approximate rates for serverless deployment)
    estimated_cost = result['usage']['total_tokens'] * (0.20 / 1_000_000)  # = total_tokens * 0.0000002  # Rough estimate based on $0.20 Per 1M Tokensfor this model(as of 2025-08-21)
    print(f"Estimated cost: ${estimated_cost:.4f}")

    # Cost estimation (approximate rates for on-demand deployment)
    # estimated_cost = need to look up pricing further

if __name__ == "__main__":
    main()
