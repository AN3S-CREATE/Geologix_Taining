"""Phase 1: Download ZASCA-Sum and prepare training JSON placeholders."""
import json
import os

from datasets import load_dataset

os.makedirs("data", exist_ok=True)

print("Downloading ZASCA-Sum from Hugging Face...")
ds = load_dataset("dsfsi/zasca-sum", split="train")
print(f"   Downloaded {len(ds)} Supreme Court cases")

# Convert ZASCA-Sum to Alpaca format for training
legal_cases = []
for row in ds:
    legal_cases.append({
        "instruction": "Summarize the following South African Supreme Court of Appeal case.",
        "input": row.get("input", "")[:2500],
        "output": row.get("output", "")[:1500],
    })

with open("data/zasca_formatted.json", "w", encoding="utf-8") as f:
    json.dump(legal_cases, f, indent=2)

print(f"Saved {len(legal_cases)} formatted cases to data/zasca_formatted.json")

# Create placeholder files for custom data
for name in ["geologix_core_training.json", "veralogix_legal_training.json"]:
    path = f"data/{name}"
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump([], f)
        print(f" Created empty placeholder: {path}")
    print(f"   --> PASTE your training data into {path} before training")

print("\nPlace your custom files in data/ before running Phase 2.")
