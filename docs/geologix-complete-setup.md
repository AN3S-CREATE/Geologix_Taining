
# 🦙 Geologix AI — Complete Ollama Pipeline

## Phase 0: Install Everything (One Terminal Session)

Open your terminal (Linux/WSL2 on Windows) and run these **exact** commands:

```bash
# 1. Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 2. Verify Ollama works and pull the base model
ollama --version
ollama pull llama3.1:8b

# 3. Test Ollama (type your question, Ctrl+D to exit)
ollama run llama3.1:8b

# 4. Stop Ollama temporarily so it doesn't steal VRAM during training
sudo systemctl stop ollama

# 5. Install Python toolspip uninstall unsloth -y  # remove old if exists
pip install --upgrade --no-cache-dir unsloth datasets trl transformers accelerate bitsandbytes sentence-transformers chromadb ollama

# 6. Make your project folder
mkdir -p D:/andries_development/andries_ai/Geologi_Taining/geologix-ai/{data,models,scripts}
cd D:/andries_development/andries_ai/Geologi_Taining/geologix-ai
```

---

## Phase 1: Download & Format the SA Legal Data

Save this as `~/geologix-ai/scripts/01_prepare_data.py` and run it.

```python
import json, os
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
        "output": row.get("output", "")[:1500]
    })

with open("data/zasca_formatted.json", "w") as f:
    json.dump(legal_cases, f, indent=2)

print(f"Saved {len(legal_cases)} formatted cases to data/zasca_formatted.json")

# Create placeholder files for your custom data
for name in ["geologix_core_training.json", "veralogix_legal_training.json"]:
    path = f"data/{name}"
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump([], f)
        print(f" Created empty placeholder: {path}")
 print(f"   --> PASTE your training data into {path} before training")

print("\nPlace your custom files in ~/geologix-ai/data/ before running Phase 2.")
```

Run it:
```bash
cd ~/geologix-ai
python scripts/01_prepare_data.py
```

---

## Phase 2: Folder Checklist Before Training

Your folder should look like this:

```
~/geologix-ai/
├── data/
│   ├── zasca_formatted.json # Created by 01_prepare_data.py
│   ├── geologix_core_training.json # PASTE your 51 subsidiary examples here
│   └── veralogix_legal_training.json   # PASTE your legal memos here
├── scripts/
│   ├── 01_prepare_data.py
│   ├── 02_train_geologix.py            # Phase 3
│   ├── 03_train_geologix_legal.py    # Phase 4
│   ├── 04_export_to_ollama.py         # Phase 5
│   └── 05_legal_rag.py               # Phase 7
└── models/
    ├── geologix-general-merged/       # Will be created
    └── geologix-legal-merged/         # Will be created
```

> **Where to get your training data:** Copy-paste the JSON blocks from the previous artifacts (`geologix_core_training.json`, `veralogix_legal_training.json`) into these files. If a file is empty `[]`, the script still runs but only trains on ZASCA-Sum.

---

## Phase 3: Train the General `geologix` Model

Save this as `~/geologix-ai/scripts/02_train_geologix.py`

```python
import os, json, random, torch
from datasets import Dataset
from unsloth import FastLanguageModel
from trl import SFTTrainer, SFTConfig

print("=" * 50)
print("🏗️  TRAINING: geologix (General Multi-Subsidiary)")
print("=" * 50)

# Load data
with open("data/zasca_formatted.json") as f: legal = json.load(f)
with open("data/geologix_core_training.json") as f: core = json.load(f)

# Blend: 60% legal reasoning, 40% group identity
target = 3000
legal_sample = random.sample(legal, min(len(legal), int(target*0.6)))
core_sample = core * 10 if len(core) < 100 else random.sample(core, min(len(core), int(target*0.4)))
all_data = legal_sample + core_sample
random.shuffle(all_data)
print(f"Training on {len(all_data)} examples")

dataset = Dataset.from_list(all_data)

# Load model (4-bit for 12GB VRAM)
model, tokenizer = FastLanguageModel.from_pretrained(
    "unsloth/Meta-Llama-3.1-8B-Instruct-bnb-4bit",
    max_seq_length=2048, load_in_4bit=True,
)

model = FastLanguageModel.get_peft_model(
    model, r=128, target_modules="all-linear",
    lora_alpha=16, lora_dropout=0,
    use_gradient_checkpointing="unsloth", random_state=3407,
)

SYSTEM = """You are Geologix AI, the unified intelligence system for Veralogix Group. You serve 17 subsidiaries across Mining, Logistics, Engineering, IT, and Specialized Services. You are modular, scalable, and ROI-driven. Route queries to the correct subsidiary expertise."""

def fmt(examples):
    texts = []
    for i, inp, out in zip(examples["instruction"], examples["input"], examples["output"]):
        u = i if not (inp and inp.strip()) else f"{i}\nContext: {inp}"
        t = tokenizer.apply_chat_template(
            [{"role":"system","content":SYSTEM},{"role":"user","content":u},{"role":"assistant","content":out}],
            tokenize=False, add_generation_prompt=False
        ) + tokenizer.eos_token
        texts.append(t)
    return {"text": texts}

dataset = dataset.map(fmt, batched=True)

trainer = SFTTrainer(
    model=model, tokenizer=tokenizer, train_dataset=dataset, dataset_text_field="text",
    args=SFTConfig(
        output_dir="models/geologix-general-lora",
        num_train_epochs=2, per_device_train_batch_size=1,
        gradient_accumulation_steps=4, learning_rate=1.5e-4,
        warmup_ratio=0.1, logging_steps=10, bf16=torch.cuda.is_bf16_supported(),
        max_seq_length=2048, report_to="none",
    ),
)

print("\nTraining general model... ~2 hours")
trainer.train()

print("\nSaving merged model...")
model.save_pretrained_merged("models/geologix-general-merged", tokenizer, save_method="merged_16bit")
print("✅ General model saved to models/geologix-general-merged/")
```

Run:
```bash
python scripts/02_train_geologix.py
```
> This takes **2-3 hours** on RTX 5070. Do not close the terminal.

---

## Phase 4: Train the `geologix-legal` Model

Save as `~/geologix-ai/scripts/03_train_geologix_legal.py`

```python
import os, json, random, torch
from datasets import Dataset
from unsloth import FastLanguageModel
from trl import SFTTrainer, SFTConfig

print("=" * 50)
print("⚖️  TRAINING: geologix-legal (Dedicated Legal AI)")
print("=" * 50)

with open("data/zasca_formatted.json") as f: legal = json.load(f)
with open("data/veralogix_legal_training.json") as f: custom = json.load(f)

# Blend: 60% case law, 40% custom legal memos
target = 3000
zasca = random.sample(legal, min(len(legal), int(target*0.6)))
vlegal = custom * 15 if len(custom) < 50 else random.sample(custom, min(len(custom), int(target*0.4)))
all_data = zasca + vlegal
random.shuffle(all_data)
print(f"Training on {len(all_data)} examples")

dataset = Dataset.from_list(all_data)

model, tokenizer = FastLanguageModel.from_pretrained(
    "unsloth/Meta-Llama-3.1-8B-Instruct-bnb-4bit",
    max_seq_length=2048, load_in_4bit=True,
)

model = FastLanguageModel.get_peft_model(
    model, r=256, target_modules="all-linear",  # Higher rank for legal reasoning
    lora_alpha=32, lora_dropout=0,
    use_gradient_checkpointing="unsloth", random_state=3407,
)

LEGAL_SYSTEM = """You are Geologix Legal, the AI legal research assistant for Veralogix Group. You apply IRAC methodology. You cite specific South African statutes and precedents. Every output is ATTORNEY-CLIENT PRIVILEGED and INTERNAL USE ONLY."""

def fmt(examples):
    texts = []
    for i, inp, out in zip(examples["instruction"], examples["input"], examples["output"]):
        u = i if not (inp and inp.strip()) else f"{i}\nFacts: {inp}"
        t = tokenizer.apply_chat_template(
            [{"role":"system","content":LEGAL_SYSTEM},{"role":"user","content":u},{"role":"assistant","content":out}],
            tokenize=False, add_generation_prompt=False
        ) + tokenizer.eos_token
        texts.append(t)
    return {"text": texts}

dataset = dataset.map(fmt, batched=True)

trainer = SFTTrainer(
    model=model, tokenizer=tokenizer, train_dataset=dataset, dataset_text_field="text",
    args=SFTConfig(
        output_dir="models/geologix-legal-lora",
        num_train_epochs=3, per_device_train_batch_size=1,  # 3 epochs for legal depth
        gradient_accumulation_steps=4, learning_rate=1.5e-4,
 warmup_ratio=0.1, logging_steps=10, bf16=torch.cuda.is_bf16_supported(),
        max_seq_length=2048, report_to="none",
    ),
)

print("\nTraining legal model... ~3-4 hours")
trainer.train()

print("\nSaving merged model...")
model.save_pretrained_merged("models/geologix-legal-merged", tokenizer, save_method="merged_16bit")
print("✅ Legal model saved to models/geologix-legal-merged/")
```

Run:
```bash
python scripts/03_train_geologix_legal.py
```

---

## Phase 5: Create Ollama Models

Restart Ollama first:
```bash
sudo systemctl start ollama
ollama list  # confirm it's running
```

### Step A: Modelfile for General `geologix`

Create `~/geologix-ai/models/Geologix.modelfile`:

```dockerfile
FROM ./geologix-general-merged
SYSTEM """You are Geologix AI, the unified intelligence system for Veralogix Group. You serve 17 subsidiaries. You route queries to the correct expertise. You are modular, scalable, and ROI-driven. You always cite sources when available."""
TEMPLATE """{{ if .System }}system
{{ .System }}{{ end }}{{ if .Prompt }}user
{{ .Prompt }}{{ end }}assistant
{{ .Response }}"""
PARAMETER temperature 0.5
PARAMETER num_ctx 4096
```

### Step B: Modelfile for Legal `geologix-legal`

Create `~/geologix-ai/models/GeologixLegal.modelfile`:

```dockerfile
FROM ./geologix-legal-merged
SYSTEM """You are Geologix Legal, the dedicated AI legal research assistant for Veralogix Group. You apply IRAC methodology (Issue, Rule, Application, Conclusion). You cite specific South African statutes, regulations, and precedents. You are direct, structured, and privilege-conscious. Every output is ATTORNEY-CLIENT PRIVILEGED and for internal Veralogix Group legal staff only."""
TEMPLATE """{{ if .System }}system
{{ .System }}{{ end }}{{ if .Prompt }}user
{{ .Prompt }}{{ end }}assistant
{{ .Response }}"""
PARAMETER temperature 0.2
PARAMETER num_ctx 4096
```

### Step C: Register Both Models

```bash
cd ~/geologix-ai/models

# Create general model
ollama create geologix -f Geologix.modelfile

# Create legal model
ollama create geologix-legal -f GeologixLegal.modelfile

# Verify both exist
ollama list
```

You should see:
```
NAME ID      SIZE    MODIFIED
geologix:latest ...     ~16 GB ...
geologix-legal:latest ... ~16 GB  ...
llama3.1:8b             ...     ~4.7 GB ...
```

### Step D: Test Both Models

```bash
# Test general model
ollama run geologix>>> What Veralogix Group subsidiary handles heavy equipment rentals?
Ctrl+D to exit

# Test legal model
ollama run geologix-legal
>>> What is the legal test for negligence in South African mining law?
Ctrl+D to exit
```

---

## Phase 6: Adding All SA Legal Cases to the END (RAG Setup)

Ollama runs the model. It does NOT have built-in memory of documents. To make Geologix Legal "know" all 4,000+ ZASCA cases, you need a **RAG vault** that feeds relevant case chunks to the model before every question.

### Step A: Build the Legal Knowledge Vault

Save as `~/geologix-ai/scripts/05_legal_rag.py`:

```python
import os
from datasets import load_dataset
from sentence_transformers import SentenceTransformer
import chromadb

print("Building Legal RAG vault for geologix-legal...")

# 1. Embedding model (runs on your RTX 5070)
embedder = SentenceTransformer("BAAI/bge-large-en-v1.5", device="cuda")

# 2. Vector database (local file, never leaves your machine)
client = chromadb.PersistentClient(path="models/legal_vault")
collection = client.get_or_create_collection(
    name="zasca_cases",
    metadata={"hnsw:space": "cosine"}
)

# 3. Load all ZASCA cases
ds = load_dataset("dsfsi/zasca-sum", split="train")
print(f"Loaded {len(ds)} cases from Hugging Face")

# 4. Chunk and store
batch, ids, docs, metas = [], [], [], []
for idx, row in enumerate(ds):
    case_id = row.get("id", f"case_{idx}")
    year = row.get("year", "unknown")
    case_type = row.get("type", "unknown")
    text = f"{row.get('input', '')}\n\nSUMMARY: {row.get('output', '')}"
    
    # Simple semantic chunking (every512 words)
    words = text.split()
    chunks = [" ".join(words[i:i+512]) for i in range(0, len(words), 400)]  # overlap    for cidx, chunk in enumerate(chunks):
        batch.append(chunk)
        ids.append(f"{case_id}_chunk{cidx}")
        metas.append({
            "case_id": case_id,
            "year": str(year),
            "type": case_type,
            "chunk_index": cidx,
            "source": "ZASCA-Sum"
        })
    
    if len(batch) >= 64:
        embs = embedder.encode(batch).tolist()
        collection.add(ids=ids, embeddings=embs, documents=batch, metadatas=metas)
        print(f"   Indexed {idx+1}/{len(ds)} cases...")
        batch, ids, docs, metas = [], [], [], []

# Flush remainder
if batch:
    embs = embedder.encode(batch).tolist()
    collection.add(ids=ids, embeddings=embs, documents=batch, metadatas=metas)

print(f"\n✅ Legal vault complete!")
print(f"   Location: ~/geologix-ai/models/legal_vault/")
print(f"   Cases: {len(ds)}")
print(f"   Total chunks: {collection.count()}")
print("   This database stays on your machine. Air-gapped. POPIA-safe.")
```

Run:
```bash
python scripts/05_legal_rag.py
```
> This takes **20-40 minutes** as it embeds 4,000+ judgments. One-time only.

### Step B: Query Script That Uses Both

Save as `~/geologix-ai/ask_legal.py`. This is how you actually **use** the legal AI with all cases:

```python
import sys
from sentence_transformers import SentenceTransformer
import chromadb
import ollama

print("=" * 60)
print("⚖️ GEOLIX LEGAL — SA Case Law + Ollama Query Interface")
print("   Model: geologix-legal")
print("   Vault: ZASCA-Sum (4,000+ SCA judgments)")
print("=" * 60)

# Load vaultembedder = SentenceTransformer("BAAI/bge-large-en-v1.5", device="cuda")
client = chromadb.PersistentClient(path="models/legal_vault")
collection = client.get_collection("zasca_cases")

def ask(question):
    # 1. Find relevant cases
    q_embed = embedder.encode([question]).tolist()
    results = collection.query(
        query_embeddings=q_embed,
        n_results=5,
        include=["documents", "metadatas"]
    )
    
    # 2. Build context
    context = ""
    sources = []
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        context += f"\n[Case {meta['case_id']} ({meta['year']})]\n{doc[:800]}...\n"
        sources.append(f"{meta['case_id']} ({meta['year']})")
    
    # 3. Send to geologix-legal via Ollama with retrieved context
    prompt = f"""SA LEGAL CASES RETRIEVED FROM VAULT:
{context}

LEGAL QUESTION: {question}

Answer using the retrieved cases and your training knowledge. Cite specific case names and legal principles. Structure as IRAC."""
    response = ollama.chat(
        model="geologix-legal",
        messages=[
            {"role": "user", "content": prompt}
        ],
        options={"temperature": 0.2, "num_ctx": 4096}
    )
    
    return response["message"]["content"], sources

# Interactive loop
while True:
    q = input("\nLegal Question > ").strip()
    if q.lower() in ["exit", "quit"]: break
    if not q: continue
    
    print("🔍 Searching ZASCA vault...")
    answer, sources = ask(q)
    
    print(f"\n┌── GEOLIX LEGAL RESPONSE ──")
    print(f"│")
    print(f"│ {answer}")
    print(f"│")
    print(f"│ Sources: {', '.join(sources)}")
    print(f"└─────────────────────────────")

```

Run and ask:
```bash
cd ~/geologix-ai
python ask_legal.py
```

Example session:
```
Legal Question > What is the test for dolus eventualis in South African murder cases?

🔍 Searching ZASCA vault...

┌── GEOLIX LEGAL RESPONSE ──
│
│ ISSUE: The legal test for dolus eventualis (legal intention) in South African...
││ RULE: The Supreme Court of Appeal in *S v De Oliveira*... confirmed that dolus eventualis requires...
│
│ APPLICATION: In mining manslaughter contexts...
│
│ CONCLUSION: The test comprises three elements...
│
│ Sources: s_v_de_oliveira (1993), s_v_makwanyane (1995)
└─────────────────────────────
```

---

## Phase 7: Daily Usage Commands

| What You Want | Command |
|--------------|---------|
| Chat with general Geologix | `ollama run geologix` |
| Chat with legal specialist | `ollama run geologix-legal` |
| Ask legal with full case RAG | `python ~/geologix-ai/ask_legal.py` |
| Check what models exist | `ollama list` |
| Check Ollama is running | `ollama serve` (in a separate terminal) |
| Stop Ollama to free VRAM | `sudo systemctl stop ollama` |

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `CUDA out of memory` during training | Lower `max_seq_length` to 1024 or use `r=64` in LoRA |
| `ollama: command not found` | Re-run the install curl command, then `sudo systemctl restart ollama` |
| `FROM` path not found in Modelfile | Use absolute path: `FROM /home/username/geologix-ai/models/geologix-general-merged` |
| Model responds generically | Your training data was empty. Check that JSON files contain actual examples. |
| RAG says "No cases found" | Re-run `05_legal_rag.py`. The `models/legal_vault/` folder must exist. |
| Need to retrain after adding new examples | Just re-run the training script. Old merged folder gets overwritten. |

---

## The Complete Chain

```
01_prepare_data.py      → Download ZASCA-Sum + make empty templates
02_train_geologix.py    → Train general model (2 hours)
03_train_geologix_legal.py → Train legal model (3 hours)
ollama create geologix  → Register general model
ollama create geologix-legal → Register legal model
05_legal_rag.py         → Build searchable case database (30 mins)
ask_legal.py            → Query with RAG + Ollama (instant)
```

You now have:
- ✅ `geologix` — 17-subsidiary group intelligence
- ✅ `geologix-legal` — South African legal reasoning specialist
- ✅ ZASCA-Sum legal vault — 4,000+ searchable Supreme Court cases
- ✅ Everything running locally on RTX 5070