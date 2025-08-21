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
├── fireworks/
│   ├── simple_chat.py          # Basic chat completion example using llama on Fireworks
├── docs/
│   ├── modal_setup.md          # Modal setup instructions
│   └── fireworks_setup.md      # Fireworks setup instructions
└── README.md                   
```

### Prerequisites

- Python 3.8+
- API keys for both platforms:
  - Modal account and API key
  - Fireworks AI API key

### Setup

1. Clone this repository:
```bash
git clone https://github.com/katebarouch/modal-vs-fireworks.git
cd modal-vs-fireworks
```

2. Follow the setup instructions for each platform:
- [Modal Setup](docs/modal_setup.md)
- [Fireworks Setup](docs/fireworks_setup.md)

3. Run the examples:
```bash
# Modal
modal run modal/modal_simple_chat.py

# Fireworks
python fireworks/fireworks_simple_chat.py
```

## Results Summary


| Metric | Modal + Llama 7B | Fireworks + Llama 3.1 8B On-Demand | Fireworks + Llama 3.1 8B Serverless | Winner |
|--------|------------------|-------------------------------------|-------------------------------------|--------|
| Cold Start | 9.31s | 0s | 0s | **Fireworks** |
| Warm Start | 3.53s | 0s | 0.0s | **Fireworks** |
| Inference Time | 6.11s | 2.04s | 2.03s | **Fireworks** |
| Cost per Call | $0.000341 (GPU time) | $0.0000340000 (170 tokens) | TBD (but expensive) | **Unclear** |
| Ease of Use | Complex (model management) | Simple (API calls) | **Fireworks** |

### A Note on Cost
I was accidentally using Fireworks On-Demand instead of Fireworks Serverless offerings for deployment, which was much more expensive. Avoid my mistake!

### A Note on Model Selection & Comparison Strategy 
I compared the platforms with their different models (llama-7b for Modal because it's a non-gated model and llama-3.1-8b-instruct for Fireworks because 7b isn't available):
- **Modal**: llama-7b 
- **Fireworks**: llama-3.1-8b-instruct via Fireworks API

### Key Takeaways

**Performance:**
- **Fireworks dominates completely on Model init time**: 2.44s cold / 2.04s warm vs 9.31s cold / 3.53s warm for Modal (130x+ faster!)
- **Fireworks has faster Inference time**: ~2.04s vs ~6.11s for Modal (2.7x faster!)
- **Modal has loading overhead**: Modal requires multiple mins for initial model loading (we do this once and cache), Fireworks has pre-loaded model (no loading time)

**Cost:**
- **Currently exploring this further**: It appears fireworks may be cheaper using serverless, which is different than what I intially thought. It is unclear if Modal is charging for cold start time, so I am trying to dif into that further. Modal is technically free right now ($30 credit)

**Ease of Use:**
- **Fireworks is much simpler**: Just API calls vs complex model management
- **Modal requires significant setup**: Docker images, GPU configuration, model downloading/caching, reading through Modal documentation
- **Fireworks abstracts complexity**: Pre-optimized models, instant deployment, no infrastructure management

**Final Verdict:** 

Fireworks wins by a landslide in ease of use and performance. Modal has a free trial period, and is a better choice if you want to use your own code. Still exploring cost, but they appear to be somewhat on par for serverless options. 