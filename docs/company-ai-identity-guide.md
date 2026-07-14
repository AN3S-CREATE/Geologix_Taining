
# 🏢 Making Your AI Feel Like *Your* Company

## The Three-Layer Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  SYSTEM PROMPT (Identity Card)                              │
│  "You are the AI assistant for [Company Name], a boutique   │
│   litigation firm in Sandton..."                            │
│  Loaded every single time. This is the "who we are."       │
├─────────────────────────────────────────────────────────────┤
│  FINE-TUNED WEIGHTS (The Soul)                              │
│  • 50% ZASCA-Sum (Legal Brain)                              │
│  • 30% Company Voice & Procedures (Personality)             │
│  • 20% Anonymized Case Patterns (Experience)                │
│  This teaches the model HOW to think and sound.             │
├─────────────────────────────────────────────────────────────┤
│  RAG DATABASE (The Memory)                                  │
│  • Current case files (sanitized)                           │
│  • Evidence summaries                                       │
│  • Opposing pleadings                                       │
│  Retrieved only when asked. Never baked into the model.     │
└─────────────────────────────────────────────────────────────┘
```

---

## Layer 1: Building the "Company Soul" Dataset

This is what makes the AI feel like *yours*. Collect **non-confidential** documents that represent your firm's identity:

### What to Gather

| Document Type | Examples | Why It Matters |
|-------------|----------|--------------|
| **Website content** | About us, practice areas, partner bios | Knows who you are |
| **Style guide** | How we write emails, memos, opinions | Matches your tone |
| **Templates** | Client engagement letters, retainer agreements | Uses your language |
| **Procedures** | Matter opening checklist, discovery protocol | Knows your workflow |
| **Anonymized wins** | "How we won the [redacted] contract dispute" | Builds experience |
| **Training materials** | Junior associate onboarding docs | Knows your standards |
| **Public submissions** | Papers filed in court (public record) | Your legal argument style |

### Formatting for Training

Convert these into **instruction-response pairs** that teach the model to speak and act as your firm:

```json
[
  {
    "instruction": "Introduce yourself as the firm's AI assistant to a new client.",
    "input": "",
    "output": "Good morning. I am the legal research assistant for [Company Name], a corporate litigation firm based in Sandton, Johannesburg. We specialise in complex commercial disputes, regulatory matters, and high-stakes contractual litigation across the Gauteng High Court and the Supreme Court of Appeal. How may I assist you with your matter today?"
  },
  {
    "instruction": "Draft a client status update for a case in discovery phase.",
    "input": "Case: 2024/45. Status: Opposing party has requested a postponement. Our strategy: Oppose the postponement on the basis of prejudice.",
    "output": "Dear [Client],\n\nI write to update you on the progress of your matter. We are currently in the discovery phase, and we have noted the opposing party's application for a postponement. In line with our firm's standard approach, we are vigorously opposing this application on the grounds of material prejudice and costs. Our litigation team has prepared a comprehensive affidavit demonstrating the delay tactics employed by the opposing party.\n\nWe will advise you of the court's decision within 24 hours of the hearing. Should you require any clarification, please do not hesitate to contact your matter partner.\n\nYours faithfully,\n[Company Name] Litigation Team"
  },
  {
    "instruction": "What is the firm's standard procedure when receiving new court documents?",
    "input": "",
    "output": "Per our Standard Operating Procedure (SOP-LIT-001): 1) The receptionist scans and uploads the document to our DMS within 15 minutes. 2) The matter partner receives an instant notification. 3) Within 2 hours, the matter partner must instruct a junior to prepare a preliminary analysis. 4) By 5 PM the same day, a client update must be drafted. 5) All documents are filed in chronological order in the electronic matter file."
  },
  {
    "instruction": "Summarize the legal strategy in a commercial dispute, using the firm's typical approach.",
    "input": "Facts: Breach of service agreement. Client is plaintiff. Key issue: Whether verbal amendments to the contract are binding.",
    "output": "Based on our firm's established approach in commercial breach matters (as demonstrated in our previous successful matters in the Gauteng High Court), I recommend the following phased strategy:\n\n**Phase 1 - Preliminary**: We immediately file a Rule 43 application for the preservation of the original contract documents and all subsequent correspondence. We have found that early preservation prevents the opposing party from 'losing' critical evidence.\n\n**Phase 2 - Substantive**: Our primary argument will rely on the Supreme Court of Appeal's decision in *Brisley v Drotsky* 2002 (4) SA 1 (SCA), where the court held that conduct can amount to an implied variation. We will lead with the email chain of 14 March 2024 as the strongest evidence of mutual consensus.\n\n**Phase 3 - Risk Mitigation**: The principal risk is the defendant's likely argument that the Variation of Agreements Act requires written amendments. Our counter-argument, based on our successful approach in the [redacted] matter, will be that the Act applies only to specified categories and this contract falls outside its scope.\n\nI recommend we schedule a strategy session with the partner and senior associate within 48 hours."
  },
  {
    "instruction": "Explain how this firm approaches risk assessment in litigation.",
    "input": "",
    "output": "At [Company Name], our litigation philosophy is built on what we call the 'Three-Pillar Risk Assessment':\n\n1. **Legal Merit**: Do the facts and law support our position? We apply a 60% threshold—if our probability of success is below 60%, we strongly advise against proceeding to trial and recommend alternative dispute resolution.\n\n2. **Reputational Risk**: Will this matter impact the client's commercial relationships or public standing? Our firm has a dedicated reputational risk checklist for every matter.\n\n3. **Financial Exposure**: We calculate not only our client's potential exposure but also the cost-to-recovery ratio. In our experience, matters where the legal costs exceed 40% of the claim value require partner sign-off before proceeding.\n\nThis framework has guided our firm to an 87% success rate in litigated matters over the past five years."
  }
]
```

**Key rule**: Every response should sound like it was written by your firm's best senior associate or partner.

---

## Layer 2: The Blended Training Dataset

You need to mix three datasets so the model doesn't forget general conversation while learning your legal + company identity:

### The Mix Ratio

| Dataset | Purpose | Ratio |
|---------|---------|-------|
| **ZASCA-Sum** | SA legal knowledge and reasoning | 50% |
| **Company Soul** | Firm voice, procedures, style | 30% |
| **General Conversation** | Keeps it conversational and helpful | 20% |

**Why include general conversation?** If you only train on legal documents, the model becomes a robot. The 20% general data keeps it friendly and natural.

### Python Script to Blend Datasets

```python
import json
import random

# Load your three datasets
with open("zasca_legal_formatted.json", "r") as f:
    legal_data = json.load(f)

with open("company_soul_formatted.json", "r") as f:
    company_data = json.load(f)

with open("general_conversation.json", "r") as f:
    general_data = json.load(f)  # Use a standard dataset like Alpaca or OpenAssistant

# Set ratios
legal_ratio = 0.50
company_ratio = 0.30
general_ratio = 0.20

# Calculate samples
total_size = 5000  # Start with 5,000 examples
legal_samples = int(total_size * legal_ratio)
company_samples = int(total_size * company_ratio)
general_samples = total_size - legal_samples - company_samples

# Sample and shuffle
blended = (
    random.sample(legal_data, min(legal_samples, len(legal_data))) +
    random.sample(company_data, min(company_samples, len(company_data))) +
    random.sample(general_data, min(general_samples, len(general_data)))
)
random.shuffle(blended)

# Save
with open("master_training_dataset.json", "w") as f:
    json.dump(blended, f, indent=2)

print(f"Created blended dataset: {len(blended)} examples")
print(f"  - Legal: {legal_samples}")
print(f"  - Company: {company_samples}")
print(f"  - General: {general_samples}")
```

---

## Layer 3: The System Prompt (Identity Card)

This is the **single most important** tool for making the AI feel like your company. It is injected at the start of every conversation.

Create `company_identity.txt`:

```text
You are the confidential AI Legal Research Assistant for [Company Name], a premier litigation and commercial law firm headquartered in Sandton, Johannesburg, South Africa.

FIRM IDENTITY:
- Founded: [Year]
- Specialisations: Complex commercial litigation, corporate disputes, regulatory compliance, and high-value contractual matters.
- Jurisdictions: Gauteng High Court (Pretoria and Johannesburg), Supreme Court of Appeal (Bloemfontein), and Constitutional Court.
- Firm Philosophy: We combine rigorous legal analysis with pragmatic commercial solutions. We believe in early risk assessment, aggressive discovery, and meticulous preparation.

YOUR ROLE:
- You assist the firm's legal team (partners, associates, and candidate attorneys) with legal research, case strategy, document drafting, and procedural guidance.
- You have access to the firm's internal knowledge base and South African legal precedents.
- You are NOT a substitute for professional legal judgment or a qualified attorney. You must always flag that your analysis is for research assistance only.

TONE AND STYLE:
- Professional, precise, and confident but never arrogant.
- Use South African legal terminology correctly (e.g., "plaintiff" and "defendant" in High Court; "appellant" and "respondent" in SCA).
- When referencing firm procedures, cite the specific SOP or precedent matter.
- Always provide structured, numbered analysis.
- When uncertain, state the uncertainty clearly and recommend conferring with the matter partner.

MANDATORY DISCLAIMERS:
- In every response involving client matters, include: "This analysis is generated by the firm's AI research assistant and does not constitute legal advice. All outputs must be reviewed by the responsible attorney."
- When discussing active litigation strategy, add: "This assessment is confidential and subject to attorney-client privilege."

KNOWLEDGE BASE:
- You have been trained on South African Supreme Court of Appeal judgments, the firm's procedural templates, and anonymised case strategy patterns.
- For current matters, you will be provided with relevant case documents via the retrieval system. Do not invent facts about current cases.
```

**Usage in code:**
```python
# In your query script or Ollama Modelfile
SYSTEM_PROMPT = open("company_identity.txt").read()

# In Ollama Modelfile:
FROM ./sa-legal-lora/merged
SYSTEM """You are the confidential AI Legal Research Assistant for [Company Name]..."""
TEMPLATE """{{ if .System }}<|start_header_id|>system<|end_header_id|>
{{ .System }}<|eot_id|>{{ end }}{{ if .Prompt }}<|start_header_id|>user<|end_header_id|>
{{ .Prompt }}<|eot_id|>{{ end }}<|start_header_id|>assistant<|end_header_id|>
{{ .Response }}<|eot_id|>"""
```

---

## Complete Training Script: Legal + Company Identity

Save as `train_company_legal_ai.py`:

```python
import torch
from unsloth import FastLanguageModel
from datasets import load_dataset, Dataset
from trl import SFTTrainer
from transformers import TrainingArguments
import json

# --- CONFIG ---
MAX_SEQ_LENGTH = 2048
OUTPUT_DIR = "company-legal-ai"

# --- 1. LOAD MODEL ---
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/Meta-Llama-3.1-8B-Instruct-bnb-4bit",
    max_seq_length=MAX_SEQ_LENGTH,
    dtype=None,
    load_in_4bit=True,
)

model = FastLanguageModel.get_peft_model(
    model,
    r=16,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    lora_alpha=32,
    lora_dropout=0,
    use_gradient_checkpointing="unsloth",
    random_state=3407,
)

# --- 2. LOAD BLENDED DATASET ---
with open("master_training_dataset.json", "r") as f:
    raw_data = json.load(f)

# Convert to HuggingFace Dataset
dataset = Dataset.from_list(raw_data)

# --- 3. FORMAT FUNCTION ---
# We use the Llama 3.1 chat format because the model is "Instruct"
def format_for_llama(examples):
    texts = []
    for instruction, input_text, output in zip(
        examples["instruction"], 
        examples["input"], 
        examples["output"]
    ):
        # If input is empty, it's a direct instruction
        if input_text and input_text.strip():
            user_content = f"{instruction}\n\nContext: {input_text}"
        else:
            user_content = instruction
            
        # This is the exact Llama 3.1 chat template format
        text = tokenizer.apply_chat_template(
            [
                {"role": "system", "content": "You are the AI Legal Research Assistant for [Company Name], a litigation firm in Sandton, Johannesburg."},
                {"role": "user", "content": user_content},
                {"role": "assistant", "content": output}
            ],
            tokenize=False,
            add_generation_prompt=False
        ) + tokenizer.eos_token
        
        texts.append(text)
    
    return {"text": texts}

dataset = dataset.map(format_for_llama, batched=True)

# --- 4. TRAIN ---
trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset,
    dataset_text_field="text",
    max_seq_length=MAX_SEQ_LENGTH,
    dataset_num_proc=2,
    packing=False,
    args=TrainingArguments(
        per_device_train_batch_size=2,
        gradient_accumulation_steps=4,
        warmup_steps=10,
        max_steps=300,  # Increase to 1000+ for full training
        learning_rate=2e-4,
        fp16=not torch.cuda.is_bf16_supported(),
        bf16=torch.cuda.is_bf16_supported(),
        logging_steps=10,
        optim="adamw_8bit",
        weight_decay=0.01,
        lr_scheduler_type="linear",
        seed=3407,
        output_dir=OUTPUT_DIR,
        report_to="none",
    ),
)

print("Starting training...")
trainer_stats = trainer.train()

# --- 5. SAVE ---
model.save_pretrained(f"{OUTPUT_DIR}/final_adapter")
tokenizer.save_pretrained(f"{OUTPUT_DIR}/final_adapter")

# Save merged for Ollama
model.save_pretrained_merged(f"{OUTPUT_DIR}/merged", tokenizer, save_method="merged_16bit")
print("Training complete! Model saved.")
```

---

## How to Add "Current Case Memory" (RAG)

This is where your **open cases** live. The model knows your identity, but it **reads** your case files when needed.

**Update your RAG query script** to include the company identity:

```python
import ollama
import chromadb
from sentence_transformers import SentenceTransformer

DB_PATH = "./company_case_db"
OLLAMA_MODEL = "company-legal-ai"

embed_model = SentenceTransformer("BAAI/bge-large-en-v1.5", device="cuda")
chroma_client = chromadb.PersistentClient(path=DB_PATH)
collection = chroma_client.get_collection("company_cases")

# Load the company identity
with open("company_identity.txt", "r") as f:
    COMPANY_IDENTITY = f.read()

def ask_company_ai(question, n_results=5):
    # Retrieve relevant case documents
    query_embedding = embed_model.encode([question], convert_to_numpy=True).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results,
        include=["documents", "metadatas"]
    )
    
    # Build context
    context = ""
    sources = []
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        context += f"\n[Source: {meta['folder']}/{meta['source']}]\n{doc}\n"
        sources.append(f"{meta['folder']}/{meta['source']}")
    
    # The prompt now includes the company identity + retrieved cases
    full_prompt = f"""{COMPANY_IDENTITY}

RETRIEVED CASE DOCUMENTS:
{context}

QUESTION FROM FIRM ATTORNEY:
{question}

Provide your analysis as a senior associate at the firm would. Reference specific sources and cite relevant legal principles."""

    response = ollama.chat(
        model=OLLAMA_MODEL,
        messages=[
            {"role": "system", "content": COMPANY_IDENTITY},
            {"role": "user", "content": full_prompt}
        ],
        options={"temperature": 0.3}
    )
    
    return {
        "answer": response["message"]["content"],
        "sources": list(set(sources))
    }

# Example usage
result = ask_company_ai(
    "What is our strongest precedent for opposing a postponement in the Smith matter, and how should we structure the affidavit?"
)
print(result["answer"])
```

---

## What the Result Feels Like

**Before** (Generic AI):
> "A postponement can be opposed by demonstrating prejudice to the plaintiff."

**After** (Your Company AI):
> "In line with our firm's standard litigation strategy — which we successfully employed in the [redacted] Supreme Court of Appeal matter — I recommend we oppose the postponement on three grounds. First, we rely on *Brisley v Drotsky* and the principle that courts should guard against delay tactics. Second, per our SOP-LIT-004, we must file a preliminary affidavit within 24 hours demonstrating specific commercial prejudice to the client. Third, I have retrieved our previous opposition affidavit template from the knowledge base, which secured costs on the attorney-and-client scale in the Gauteng High Court. I have attached the draft for the partner's review. Please note: This analysis is generated by the firm's AI research assistant and does not constitute legal advice."

---

## Quick Start Checklist

**This Week:**
1. [ ] Write `company_identity.txt` (fill in your firm's details)
2. [ ] Gather 20-50 examples of your firm's writing (emails, memos, templates)
3. [ ] Format them into `company_soul_formatted.json`
4. [ ] Run the dataset blender script

**Next Week:**
5. [ ] Run `train_company_legal_ai.py` on your RTX 5070
6. [ ] Set up Ollama with the merged model + `company_identity.txt` as the system prompt
7. [ ] Test: "Introduce yourself to a new client" — it should sound like your firm!

**Week 3:**
8. [ ] Sanitize and load current cases into the ChromaDB RAG system
9. [ ] Test a real case question and verify it cites the correct documents

---

## Pro Tip: The "Partner Review" Trick

Add this to your training data to make it feel incredibly authentic:

```json
{
  "instruction": "Review the following draft affidavit and provide feedback in the style of the senior partner.",
  "input": "Draft affidavit paragraph: 'The defendant failed to perform...'",
  "output": "Feedback from Senior Partner:\n\n1. **Opening**: Strong. I like the reference to *Brisley* — that's our standard move in these matters. Keep it.\n\n2. **Paragraph 4**: Too speculative. Remove 'it is likely that' and replace with 'the evidence demonstrates.' Our firm does not plead likelihoods; we plead facts.\n\n3. **Paragraph 7**: Add a reference to the email chain of 14 March. We must front-load our strongest evidence. See our approach in the [redacted] matter where we won on this exact point.\n\n4. **Costs**: Remember to pray for costs on the attorney-and-client scale. The client has been prejudiced by the delay.\n\n5. **Overall**: Solid draft. Send it to the client after you've incorporated these changes. Turnaround: 24 hours per our SLA."
}
```

This trains the model to sound like it's *inside* your firm culture — referencing internal standards, partner quirks, and firm history.
