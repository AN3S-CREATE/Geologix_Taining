# 🇿🇦 Your South African Legal AI: Complete Beginner Roadmap

## What You're Building
A conversational AI that understands South African law — from Supreme Court judgments to acts like POPIA, the Cybercrimes Act, and Companies Act. It won't replace a lawyer, but it will be an excellent research assistant and legal Q&A tool.

---

## Step 1: Understand Your Path (QLoRA + Unsloth)

| Technique | VRAM Needed | Your RTX 5070 | Quality |
|---|---|---|---|
| **Full Fine-tuning** | ~80GB+ | ❌ Impossible | Best |
| **LoRA** | ~24GB | ❌ Too big | Very Good |
| **QLoRA** | ~6-12GB | ✅ Perfect! | 85-93% of full |

**QLoRA** is the beginner's best friend. It:
- Runs a 4-bit compressed version of the model (saves 75% memory)
- Only trains 1% of the parameters (small "adapters")
- Keeps your base model frozen (preserves general knowledge)

**Unsloth** makes it 2x faster and uses 70% less VRAM than standard QLoRA.

---

## Step 2: Pick Your Base Model

For a **12GB RTX 5070**, use:

**`unsloth/Meta-Llama-3.1-8B-Instruct-bnb-4bit`**

- 8 billion parameters (powerful enough for legal reasoning)
- Pre-trained for conversations (the "Instruct" part)
- Already 4-bit quantized for your GPU
- Apache 2.0 license (free to use commercially)

---

## Step 3: Get Your South African Legal Data

The best ready-made dataset for you:

### 🏛️ ZASCA-Sum (Supreme Court of Appeal Judgments)
- **4,000+ judgments** from the South African Supreme Court of Appeal
- Each has the **full judgment text** + **media summary**
- Perfect for training: "Summarize this case" or "What was the ruling in...?"
- **License**: CC BY-SA 4.0 (free to use)
- **Link**: [https://huggingface.co/datasets/dsfsi/zasca-sum](https://huggingface.co/datasets/dsfsi/zasca-sum)

**Dataset structure:**
| Column | Content |
|---|---|
| `id` | Case ID |
| `type` | Case type |
| `year` | Year of judgment |
| `input` | Full judgment text |
| `output` | Media summary |

**Other useful SA datasets:**
- **POPIA Compliance NLI**: [labrat-aiko/popia-compliance-nli](https://huggingface.co/datasets/labrat-aiko/popia-compliance-nli) — for data privacy Q&A
- **SA Law MCP Server**: [Ansvar-Systems/southafrica-law-mcp](https://github.com/Ansvar-Systems/southafrica-law-mcp) — for scraping more legislation

---

## Step 4: Format Your Data (The "Alpaca" Format)

Your model needs to learn from **instruction → response** pairs. Convert ZASCA-Sum into this format:

```json
[
  {
    "instruction": "Summarize the following South African Supreme Court of Appeal case.",
    "input": "[paste full judgment text here]",
    "output": "[paste media summary here]"
  },
  {
    "instruction": "What was the legal principle established in this case?",
    "input": "[paste full judgment text here]",
    "output": "The court held that..."
  }
]
```

**For a legal chatbot**, you also want general Q&A pairs like:
```json
{
  "instruction": "What are the key requirements of POPIA for small businesses?",
  "input": "",
  "output": "Under the Protection of Personal Information Act (POPIA), small businesses must: 1) Obtain consent before collecting personal information, 2) Only collect information necessary for lawful purposes, 3) Implement reasonable security safeguards, 4) Notify the Information Regulator and affected individuals in case of a data breach..."
}
```

---

## Step 5: Your Complete Training Code

Save this as `train_sa_legal.py` and run it on your RTX 5070:

```python
# ============================================
# SOUTH AFRICAN LEGAL AI - FINE-TUNING SCRIPT
# For RTX 5070 (12GB VRAM) using Unsloth + QLoRA
# ============================================

# 1. INSTALL (run once)
# pip install unsloth transformers datasets trl accelerate bitsandbytes

import torch
from unsloth import FastLanguageModel
from datasets import load_dataset
from trl import SFTTrainer
from transformers import TrainingArguments
from peft import LoraConfig

# --- CONFIGURATION ---
MAX_SEQ_LENGTH = 2048        # How long each example can be (tokens)
LORA_RANK = 16               # Adapter complexity (start with 16)
LORA_ALPHA = 32              # Usually 2x rank
BATCH_SIZE = 2               # How many examples per step (keep low for 12GB)
GRADIENT_ACCUMULATION = 4    # Effective batch = 2 * 4 = 8
LEARNING_RATE = 2e-4         # LoRA needs higher LR than full fine-tuning
NUM_EPOCHS = 1               # Start with 1 (prevent overfitting)
OUTPUT_DIR = "sa-legal-lora" # Where to save your adapter

# --- 2. LOAD MODEL (4-bit quantized) ---
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/Meta-Llama-3.1-8B-Instruct-bnb-4bit",
    max_seq_length=MAX_SEQ_LENGTH,
    dtype=None,              # Auto-detect
    load_in_4bit=True,       # Essential for 12GB VRAM
    token=None,              # Add your HF token if model is gated
)

# --- 3. ADD LoRA ADAPTERS ---
model = FastLanguageModel.get_peft_model(
    model,
    r=LORA_RANK,
    target_modules=[
        "q_proj", "k_proj", "v_proj", "o_proj",   # Attention layers
        "gate_proj", "up_proj", "down_proj",      # MLP layers
    ],
    lora_alpha=LORA_ALPHA,
    lora_dropout=0,           # 0 is optimized for Unsloth
    bias="none",
    use_gradient_checkpointing="unsloth",  # Saves VRAM
    random_state=3407,
)

# --- 4. FORMAT YOUR DATASET ---
# Load ZASCA-Sum from Hugging Face
dataset = load_dataset("dsfsi/zasca-sum", split="train")

# Define the Alpaca prompt template
alpaca_prompt = """Below is an instruction that describes a legal task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
{}

### Input:
{}

### Response:
{}"""

# Format function
def format_dataset(examples):
    instructions = []
    inputs = []
    outputs = []
    
    for i in range(len(examples["input"])):
        instructions.append("Summarize the following South African Supreme Court of Appeal case.")
        inputs.append(examples["input"][i])    # Full judgment text
        outputs.append(examples["output"][i])    # Media summary
    
    texts = []
    for instruction, input_text, output in zip(instructions, inputs, outputs):
        # Must end with EOS token so model learns when to stop
        text = alpaca_prompt.format(instruction, input_text, output) + tokenizer.eos_token
        texts.append(text)
    
    return {"text": texts}

# Apply formatting
dataset = dataset.map(format_dataset, batched=True)

# --- 5. TRAIN ---
trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset,
    dataset_text_field="text",
    max_seq_length=MAX_SEQ_LENGTH,
    dataset_num_proc=2,
    packing=False,  # Set True for faster training on short sequences

    args=TrainingArguments(
        per_device_train_batch_size=BATCH_SIZE,
        gradient_accumulation_steps=GRADIENT_ACCUMULATION,
        warmup_steps=5,
        max_steps=60,           # Use max_steps for quick testing
        # num_train_epochs=NUM_EPOCHS,  # Use this for full training
        learning_rate=LEARNING_RATE,
        fp16=not torch.cuda.is_bf16_supported(),
        bf16=torch.cuda.is_bf16_supported(),
        logging_steps=10,
        optim="adamw_8bit",
        weight_decay=0.01,
        lr_scheduler_type="linear",
        seed=3407,
        output_dir=OUTPUT_DIR,
        report_to="none",      # Set to "wandb" for tracking
    ),
)

# Show VRAM stats
gpu_stats = torch.cuda.get_device_properties(0)
start_gpu_memory = round(torch.cuda.max_memory_reserved() / 1024 / 1024 / 1024, 3)
max_memory = round(gpu_stats.total_memory / 1024 / 1024 / 1024, 3)
print(f"GPU: {gpu_stats.name}")
print(f"Max memory: {max_memory} GB")
print(f"Reserved memory: {start_gpu_memory} GB")

# Start training!
trainer_stats = trainer.train()

# Print results
used_memory = round(torch.cuda.max_memory_reserved() / 1024 / 1024 / 1024, 3)
print(f"\nTraining complete!")
print(f"Peak memory: {used_memory} GB")

# --- 6. SAVE YOUR ADAPTER ---
model.save_pretrained(f"{OUTPUT_DIR}/final_adapter")
tokenizer.save_pretrained(f"{OUTPUT_DIR}/final_adapter")
print(f"Saved to {OUTPUT_DIR}/final_adapter")

# --- 7. OPTIONAL: MERGE AND EXPORT FOR OLLAMA ---
# This creates a single file you can run with Ollama locally
model.save_pretrained_merged(f"{OUTPUT_DIR}/merged", tokenizer, save_method="merged_16bit")
print("Merged model saved for Ollama/llama.cpp")
```

---

## Step 6: Run It on Your RTX 5070

```bash
# 1. Create a Python environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install Unsloth (this installs everything you need)
pip install unsloth

# 3. Run training
python train_sa_legal.py
```

**Expected VRAM usage**: ~10-11 GB on your RTX 5070  
**Expected time**: ~1-2 hours for 1,500 examples

---

## Step 7: Use Your Model

### Option A: Python Inference
```python
from unsloth import FastLanguageModel

# Load base model + your adapter
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/Meta-Llama-3.1-8B-Instruct-bnb-4bit",
    max_seq_length=2048,
    load_in_4bit=True,
)

# Attach your trained adapter
model = FastLanguageModel.get_peft_model(model, r=16)
model.load_adapter("sa-legal-lora/final_adapter")

# Ask a legal question
messages = [
    {"role": "user", "content": "What is the legal test for negligence in South African law?"}
]
inputs = tokenizer.apply_chat_template(messages, tokenize=True, return_tensors="pt").to("cuda")
outputs = model.generate(inputs, max_new_tokens=512, temperature=0.7)
print(tokenizer.batch_decode(outputs)[0])
```

### Option B: Run with Ollama (Recommended for Chat)
```bash
# Convert your merged model to GGUF format
# Then create a Modelfile:
FROM ./sa-legal-lora/merged
TEMPLATE """{{ if .System }}<|start_header_id|>system<|end_header_id|>
{{ .System }}<|eot_id|>{{ end }}{{ if .Prompt }}<|start_header_id|>user<|end_header_id|>
{{ .Prompt }}<|eot_id|>{{ end }}<|start_header_id|>assistant<|end_header_id|>
{{ .Response }}<|eot_id|>"""
SYSTEM "You are a helpful South African legal research assistant. Provide accurate information based on South African law, but always note that you are not a substitute for professional legal advice."

# Run it
ollama create sa-legal -f Modelfile
ollama run sa-legal
```

---

## Step 8: Google Colab Alternative (Free!)

If you want to experiment before running locally, use Unsloth's **official Colab notebook**:

📒 **Notebook**: [Llama-3 Ollama Colab](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/Llama3_(8B)-Ollama.ipynb)

Just swap the dataset loading cell to:
```python
from datasets import load_dataset
dataset = load_dataset("dsfsi/zasca-sum", split="train")
```

Colab free tier gives you ~15GB VRAM — enough for this exact setup!

---

## Your Next Steps

1. **Week 1**: Run the Unsloth Colab notebook with ZASCA-Sum to prove it works
2. **Week 2**: Run locally on your RTX 5070, experiment with the full dataset
3. **Week 3**: Build your own Q&A dataset (scrape SA Government Gazette, SAFLII, etc.)
4. **Week 4**: Merge and deploy with Ollama for a local ChatGPT-style legal assistant

---

## Pro Tips for Legal AI

| Tip | Why It Matters |
|---|---|
| **Start with 1 epoch** | Legal text is dense; overfitting happens fast |
| **Use `r=16` first** | Complex enough for legal reasoning, small enough to not overfit |
| **Add a system prompt** | Always remind it "I am not a lawyer" for liability |
| **Include case citations** | Train it to cite actual case names/numbers for credibility |
| **Mix general + legal data** | 80% legal + 20% general conversation prevents "catastrophic forgetting" |

---

## Resources

- **Unsloth Docs**: [https://unsloth.ai/docs](https://unsloth.ai/docs)
- **ZASCA-Sum Dataset**: [https://huggingface.co/datasets/dsfsi/zasca-sum](https://huggingface.co/datasets/dsfsi/zasca-sum)
- **DSFSI Datasets**: [https://github.com/Avelanda/dsfsi-datasets](https://github.com/Avelanda/dsfsi-datasets)
- **Fine-Tuning Guide 2026**: [https://www.sitepoint.com/fine-tune-local-llms-2026/](https://www.sitepoint.com/fine-tune-local-llms-2026/)

---

**Good luck!** Your RTX 5070 is more than capable of this. Start with the Colab notebook to get comfortable, then run the full script locally. 🚀