# Architecture — Geologi_Taining

## Overview

Local fine-tuning and serving stack for two Ollama models:

1. **geologix** — Veralogix Group multi-subsidiary assistant
2. **geologix-legal** — SA legal IRAC specialist + ZASCA RAG vault

## Pipeline

```
00_ingest_company_context.py
    → data/company_context/ (identity, registry, PROC-* queue)
    → feeds Layer A/B company soul (see docs/geologix-ai-company-context-process.md)
01_prepare_data.py
    → data/zasca_formatted.json + custom JSON templates
02_train_geologix.py
    → models/geologix-general-merged/
03_train_geologix_legal.py
    → models/geologix-legal-merged/
04_export_to_ollama.py (+ Modelfiles)
    → ollama models: geologix, geologix-legal
05_legal_rag.py
    → models/legal_vault/ (Chroma + BGE embeddings)
ask_legal.py
    → retrieve cases → prompt geologix-legal
```

Company knowledge source: `data/veralogix_companys_information/` (portfolio_index + per-company folders + CROSS-PORTFOLIO). Company RAG vault (Layer C) is planned separately from the legal vault.

## Components

| Layer | Tech |
|-------|------|
| Base model | Llama 3.1 8B Instruct (Unsloth 4-bit) |
| Training | Unsloth LoRA + TRL SFTTrainer |
| Serving | Ollama Modelfiles |
| RAG | sentence-transformers `BAAI/bge-large-en-v1.5` + ChromaDB |
| Case corpus | Hugging Face `dsfsi/zasca-sum` |

## Constraints

- Scripts expect **project root** as cwd.
- Large artifacts are gitignored (merged models, LoRA dirs, legal vault, zasca JSON).
- Training needs GPU VRAM (doc targets ~12GB / RTX 5070 class).

## Source of truth

`docs/geologix-complete-setup.md`
