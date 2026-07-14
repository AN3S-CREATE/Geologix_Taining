"""Phase 3: Train the general geologix multi-subsidiary model."""
import json
import random

import torch
from datasets import Dataset
from trl import SFTConfig, SFTTrainer
from unsloth import FastLanguageModel

print("=" * 50)
print("🏗️  TRAINING: geologix (General Multi-Subsidiary)")
print("=" * 50)

# Load data
with open("data/zasca_formatted.json", encoding="utf-8") as f:
    legal = json.load(f)
with open("data/geologix_core_training.json", encoding="utf-8") as f:
    core = json.load(f)

# Blend: 60% legal reasoning, 40% group identity
target = 3000
legal_sample = random.sample(legal, min(len(legal), int(target * 0.6)))
core_sample = (
    core * 10
    if len(core) < 100
    else random.sample(core, min(len(core), int(target * 0.4)))
)
all_data = legal_sample + core_sample
random.shuffle(all_data)
print(f"Training on {len(all_data)} examples")

dataset = Dataset.from_list(all_data)

# Load model (4-bit for 12GB VRAM)
model, tokenizer = FastLanguageModel.from_pretrained(
    "unsloth/Meta-Llama-3.1-8B-Instruct-bnb-4bit",
    max_seq_length=2048,
    load_in_4bit=True,
)

model = FastLanguageModel.get_peft_model(
    model,
    r=128,
    target_modules="all-linear",
    lora_alpha=16,
    lora_dropout=0,
    use_gradient_checkpointing="unsloth",
    random_state=3407,
)

SYSTEM = (
    "You are Geologix AI, the unified intelligence system for Veralogix Group. "
    "You serve 17 subsidiaries across Mining, Logistics, Engineering, IT, and "
    "Specialized Services. You are modular, scalable, and ROI-driven. "
    "Route queries to the correct subsidiary expertise."
)


def fmt(examples):
    texts = []
    for i, inp, out in zip(
        examples["instruction"], examples["input"], examples["output"]
    ):
        u = i if not (inp and inp.strip()) else f"{i}\nContext: {inp}"
        t = (
            tokenizer.apply_chat_template(
                [
                    {"role": "system", "content": SYSTEM},
                    {"role": "user", "content": u},
                    {"role": "assistant", "content": out},
                ],
                tokenize=False,
                add_generation_prompt=False,
            )
            + tokenizer.eos_token
        )
        texts.append(t)
    return {"text": texts}


dataset = dataset.map(fmt, batched=True)

trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset,
    dataset_text_field="text",
    args=SFTConfig(
        output_dir="models/geologix-general-lora",
        num_train_epochs=2,
        per_device_train_batch_size=1,
        gradient_accumulation_steps=4,
        learning_rate=1.5e-4,
        warmup_ratio=0.1,
        logging_steps=10,
        bf16=torch.cuda.is_bf16_supported(),
        max_seq_length=2048,
        report_to="none",
    ),
)

print("\nTraining general model... ~2 hours")
trainer.train()

print("\nSaving merged model...")
model.save_pretrained_merged(
    "models/geologix-general-merged", tokenizer, save_method="merged_16bit"
)
print("✅ General model saved to models/geologix-general-merged/")
