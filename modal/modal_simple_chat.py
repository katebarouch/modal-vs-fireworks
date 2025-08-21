"""
Modal + Llama model deployment for direct comparison with Fireworks.
This example demonstrates Modal's native model serving capabilities.
"""

import time
from typing import Dict, Any
import modal

# Create Modal app
# Modal requires you to create an app 
# instance that serves as the container for all your serverless functions
# See: https://modal.com/docs/guide/apps
app = modal.App("llama-chat-modal")

# Define the image with required dependencies for Llama
# Modal caches this image, so it only builds once
# see: https://modal.com/docs/examples/llama_cpp (under "Storing Models on Modal")

# Cache the model download using Modal's Volume feature
modal_cache = modal.Volume.from_name("llama-models", create_if_missing=True)

# Define the image with required dependencies for Llama
download_image = modal.Image.debian_slim().pip_install([
    "transformers>=4.35.0",
    "torch>=2.0.0",
    "accelerate>=0.24.0",
    "sentencepiece>=0.1.99",
    "protobuf>=3.20.0"
])


@app.function(
    image=download_image,
    gpu="A10G",  # Use A10G GPU for Llama inference
    volumes={"/cache": modal_cache},  # Mount persistent volume at /cache to store downloaded models across runs
    timeout=600,
    scaledown_window=300,  
)
@modal.concurrent(max_inputs=10)
def generate_text(prompt: str, max_tokens: int = 150) -> Dict[str, Any]:
    """
    Generate text using Llama model via Modal.
    """
    # Import transformers inside the function where dependencies are available
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM
    
    # Start timing the function
    function_start = time.time()
    
    # Load model and tokenizer 
    model_name = "huggyllama/llama-7b" 
    cache_dir = "/cache"  # Use Modal volume for caching
    
    # Start timing the actual model loading
    init_start = time.time()

    # define the tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=cache_dir, use_fast=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        cache_dir=cache_dir,
        torch_dtype=torch.float16,
        device_map="auto",   # puts weights on the GPU
    )
    model.eval()

    # Enable TensorFloat-32 (TF32) math on NVIDIA Ampere+ GPUs (like A10G)
    # This allows certain FP32 matrix multiplications to run on Tensor Cores,
    # giving up to ~2x faster inference with negligible accuracy loss.
    torch.backends.cuda.matmul.allow_tf32 = True
    
    # Start timing the actual inference
    init_time = time.time() - init_start
    inference_start = time.time()
    
    # Tokenize input string
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    
    # Generate response (Turning off gradient tracking for inference)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_tokens, # Prevents runaway generation.
            do_sample=True, # Prevents deterministic output.
            temperature=0.7, # Controls randomness of output.
            pad_token_id=tokenizer.eos_token_id, ## Use EOS token as padding to avoid warnings for models like LLaMA
        )
    
    # Decode response
    response_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    response_text = response_text[len(prompt):].strip()
    
    # Calculate timing metrics
    inference_time = time.time() - inference_start
    total_time = time.time() - function_start
    
    # Calculate token counts
    input_tokens = len(inputs[0])
    output_tokens = len(outputs[0]) - len(inputs[0])
    total_tokens = input_tokens + output_tokens
    
    # Return response
    return {
        "response": response_text,
        "init_time": init_time,           # Model loading time
        "inference_time": inference_time, # Pure inference time
        "total_time": total_time,        # Total function time
        "model": "microsoft/DialoGPT-medium",
        "usage": {
            "prompt_tokens": input_tokens,
            "completion_tokens": output_tokens,
            "total_tokens": total_tokens
        }
    }

@app.local_entrypoint()
def main():
    """
    Test the Modal + Llama function with sample prompts.
    """
    print("Testing Modal + Llama model...")
    
    # Test prompts
    prompt1 = "How many hours would it take to walk across the United States?"
    prompt2 = "What is the most popular dessert in the world?"
    
    # First call (cold start measurement - Modal container + model loading)
    print("\n Cold Start Test (Modal Container + Model Loading)")
    print(f"Prompt: {prompt1}")
    result1 = generate_text.remote(prompt1)
    
    print(f"Response: {result1['response'][:100]}...")
    print(f"Model init time: {result1['init_time']:.2f}s")
    print(f"Inference time: {result1['inference_time']:.2f}s")
    print(f"Total time: {result1['total_time']:.2f}s")
    
    # Second call (warm start measurement - model already loaded)
    print("\n Warm Start Test (Model Already Loaded)")
    print(f"Prompt: {prompt2}")
    result2 = generate_text.remote(prompt2)
    
    print(f"Response: {result2['response'][:100]}...")
    print(f"Model init time: {result2['init_time']:.2f}s")
    print(f"Inference time: {result2['inference_time']:.2f}s")
    print(f"Total time: {result2['total_time']:.2f}s")
    
    # Use second result for cost calculation
    print(f"\nTokens used: {result2['usage']['total_tokens']} ({result2['usage']['prompt_tokens']} prompt + {result2['usage']['completion_tokens']} completion)")
    
    # Cost estimation for Modal GPU usage
    # A10G GPU costs $0.000306/second on Modal (source: https://modal.com/pricing)
    gpu_cost_per_second = 0.000306
    estimated_gpu_cost = result2['total_time'] * gpu_cost_per_second
    print(f"Estimated GPU cost: ${estimated_gpu_cost:.6f}")

if __name__ == "__main__":
    main()