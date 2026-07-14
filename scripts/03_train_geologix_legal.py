"""Phase 4: Train the dedicated geologix-legal model."""
import json
import random

import torch
from datasets import Dataset
from trl import SFTConfig, SFTTrainer
from unsloth import FastLanguageModel

print("=" * 50)
print("⚖️  TRAINING: geologix-legal (Dedicated Legal AI)")
print("=" * 50)

with open("data/zasca_formatted.json", encoding="utf-8") as f:
    legal = json.load(f)
with open("data/veralogix_legal_training.json", encoding="utf-8") as f:
    custom = json.load(f)

# Blend: 60% case law, 40% custom legal memos
target = 3000
zasca = random.sample(legal, min(len(legal), int(target * 0.6)))
vlegal = (
    custom * 15
    if len(custom) < 50
    else random.sample(custom, min(len(custom), int(target * 0.4)))
)
all_data = zasca + vlegal
random.shuffle(all_data)
print(f"Training on {len(all_data)} examples")

dataset = Dataset.from_list(all_data)

model, tokenizer = FastLanguageModel.from_pretrained(
    "unsloth/Meta-Llama-3.1-8B-Instruct-bnb-4bit",
    max_seq_length=2048,
    load_in_4bit=True,
)

model = FastLanguageModel.get_peft_model(
    model,
    r=256,
    target_modules="all-linear",  # Higher rank for legal reasoning
    lora_alpha=32,
    lora_dropout=0,
    use_gradient_checkpointing="unsloth",
    random_state=3407,
)

LEGAL_SYSTEM = (
    "You are Geologix Legal, the AI legal research assistant for Veralogix Group. "
    "You apply IRAC methodology. You cite specific South African statutes and "
    "precedents. Every output is ATTORNEY-CLIENT PRIVILEGED and INTERNAL USE ONLY."
)


def fmt(examples):
    texts = []
    for i, inp, out in zip(
        examples["instruction"], examples["input"], examples["output"]
    ):
        u = i if not (inp and inp.strip()) else f"{i}\nFacts: {inp}"
        t = (
            tokenizer.apply_chat_template(
                [
                    {"role": "system", "content": LEGAL_SYSTEM},
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
        output_dir="models/geologix-legal-lora",
        num_train_epochs=3,
        per_device_train_batch_size=1,  # 3 epochs for legal depth
        gradient_accumulation_steps=4,
        learning_rate=1.5e-4,
        warmup_ratio=0.1,
        logging_steps=10,
        bf16=torch.cuda.is_bf16_supported(),
        max_seq_length=2048,
        report_to="none",
    ),
)

print("\nTraining legal model... ~3-4 hours")
trainer.train()

print("\nSaving merged model...")
model.save_pretrained_merged(
    "models/geologix-legal-merged", tokenizer, save_method="merged_16bit"
)
print("✅ Legal model saved to models/geologix-legal-merged/")
