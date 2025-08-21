# Modal vs Fireworks: LLM Inference Comparison

A comparison of Modal and Fireworks AI for running a simple LLM inference task.

## Objective

To compare two popular AI inference platforms by running the same simple LLM task (asking two questions) and measuring:

- **Performance**: Response time and cold start performance
- **Cost**: Price per request/token
- **Ease of Use**: Setup complexity, API design, documentation quality

## Project Structure
```
├── modal/
│   ├── simple_chat.py          # Basic chat completion example using llama on Modal
│   └── requirements.txt        # Dependencies
├── fireworks/
│   ├── simple_chat.py          # Basic chat completion example using llama on Fireworks
│   └── requirements.txt        # Dependencies
├── docs/
│   ├── modal_setup.md          # Modal setup instructions
│   └── fireworks_setup.md      # Fireworks setup instructions
└── README.md                   # This file
```

### Prerequisites

- Python 3.8+
- API keys for both platforms:
  - Modal account and API key
  - OpenAI API key
  - Fireworks AI API key

### Setup

1. Clone this repository:
```bash
git clone <your-repo-url>
cd modal-vs-fireworks-comparison
```

2. Follow the setup instructions for each platform:
- [Modal Setup](docs/modal_setup.md)
- [Fireworks Setup](docs/fireworks_setup.md)

3. Run the examples:
```bash
# Modal
modal run modal/simple_chat.py

# Fireworks
python fireworks/simple_chat.py
```

## Results Summary


| Metric | Modal + Llama 7B | Fireworks + Llama 3.1 8B | Winner |
|--------|------------------|---------------------------|--------|
| Cold Start | 9.31s | 2.44s (no cold start) | **Fireworks** |
| Warm Start | 3.53s | 2.04s | **Fireworks** |
| Inference Time | 6.11s | 2.24s | **Fireworks** |
| Cost per Call | $0.002658 (GPU time) | $0.012 (170 tokens) | **Fireworks** |
| Ease of Use | Complex (model management) | Simple (API calls) | **Fireworks** |

### A Note on Chat-GPTModel Selection & Comparison Strategy 
I compared the platforms with their different models (llama-7b for Modal because it's a non-gated model and llama-3.1-8b-instruct for Fireworks because 7b isn't available):
- **Modal**: llama-7b 
- **Fireworks**: llama-3.1-8b-instruct via Fireworks API

### Key Takeaways

**Performance:**
- **Fireworks dominates completely on Model init time**: 2.44s cold / 2.04s warm vs 9.31s cold / 3.53s warm for Modal (130x+ faster!)
- **Fireworks dominates completely on Inference time**: ~2.24s vs ~6.11s for Modal (2.7x faster!)
- **Model loading overhead**: Model requires 60s+ for initial model loading (we do this once and cache), Fireworks has pre-loaded model (no loading time)

**Cost:**
- **Modal is significantly cheaper**: $0.002658 (GPU time) vs $0.012 (170 tokens) for Fireworks (6.7x cheaper!), AND Modal is technically free right now ($30 credit)

**Ease of Use:**
- **Fireworks is much simpler**: Just API calls vs complex model management
- **Modal requires significant setup**: Docker images, GPU configuration, model downloading/caching, reading through Modal documentation
- **Fireworks abstracts complexity**: Pre-optimized models, instant deployment, no infrastructure management

**Final Verdict**: Fireworks wins by a landslide in ease of use and performance. Modal is cheaper, has a free trial period, and is a better choice if you want to use your own code.