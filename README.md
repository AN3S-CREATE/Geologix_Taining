# Geologi_Taining

Local Geologix AI training pipeline (Ollama + Unsloth) for Veralogix Group.

**Source of truth:** [`docs/geologix-complete-setup.md`](docs/geologix-complete-setup.md)

## Folder structure

```
Geologi_Taining/
├── data/
│   ├── geologix_core_training.json      # Paste 51 subsidiary examples here
│   ├── veralogix_legal_training.json    # Paste legal memos here
│   └── zasca_formatted.json             # Created by 01_prepare_data.py
├── scripts/
│   ├── 01_prepare_data.py
│   ├── 02_train_geologix.py
│   ├── 03_train_geologix_legal.py
│   ├── 04_export_to_ollama.py
│   └── 05_legal_rag.py
├── models/
│   ├── Geologix.modelfile
│   ├── GeologixLegal.modelfile
│   ├── geologix-general-merged/         # Created by training
│   ├── geologix-legal-merged/           # Created by training
│   └── legal_vault/                     # Created by 05_legal_rag.py
├── ask_legal.py
└── docs/geologix-complete-setup.md
```

## Pipeline order

1. `python scripts/01_prepare_data.py`
2. Paste custom JSON into `data/geologix_core_training.json` and `data/veralogix_legal_training.json`
3. `python scripts/02_train_geologix.py`
4. `python scripts/03_train_geologix_legal.py`
5. `python scripts/04_export_to_ollama.py`
6. `python scripts/05_legal_rag.py`
7. `python ask_legal.py`
