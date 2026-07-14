# File Inventory — Geologi_Taining

| Path | Purpose | Status |
|------|---------|--------|
| `README.md` | Project overview + folder map | Active |
| `docs/geologix-complete-setup.md` | Source of truth: full Ollama/Unsloth pipeline | Active |
| `ask_legal.py` | Interactive RAG + `geologix-legal` via Ollama | Active |
| `data/geologix_core_training.json` | Custom subsidiary training examples (placeholder `[]`) | Active |
| `data/veralogix_legal_training.json` | Custom legal memo training examples (placeholder `[]`) | Active |
| `data/zasca_formatted.json` | Generated Alpaca-format ZASCA cases | Generated |
| `scripts/01_prepare_data.py` | Download ZASCA-Sum + ensure data placeholders | Active |
| `scripts/02_train_geologix.py` | Fine-tune general Geologix model | Active |
| `scripts/03_train_geologix_legal.py` | Fine-tune legal Geologix model | Active |
| `scripts/04_export_to_ollama.py` | `ollama create` from Modelfiles | Active |
| `scripts/05_legal_rag.py` | Build Chroma legal vault | Active |
| `models/Geologix.modelfile` | Ollama Modelfile for general model | Active |
| `models/GeologixLegal.modelfile` | Ollama Modelfile for legal model | Active |
| `models/geologix-general-merged/` | Merged general weights (training output) | Generated |
| `models/geologix-legal-merged/` | Merged legal weights (training output) | Generated |
| `models/legal_vault/` | ChromaDB ZASCA embeddings | Generated |
| `.gitignore` | Ignores large weights, vault, generated ZASCA JSON | Active |
| `REPO_ANALYSIS_MEMORY.md` | Agent cumulative analysis state | Active |
| `.index/*` | Project context index | Active |
| `Geologi_Taining.code-workspace` | VS Code/Cursor workspace file | Active |
| `docs/geologix-ai-company-context-process.md` | P0–P6 SOP: company info → Geologix AI identity / soul / RAG | Active |
| `scripts/00_ingest_company_context.py` | Ingest portfolio into `data/company_context/` pack | Active |
| `data/veralogix_companys_information/` | Veralogix / Geologix Vanguard company knowledge base | Active |
| `data/company_context/company_registry.json` | Generated per-company registry + readiness | Generated |
| `data/company_context/geologix_identity.json` | Generated Geologix AI identity card + system prompt draft | Generated |
| `data/company_context/cross_portfolio_triggers.json` | Generated cross-portfolio triggers + PROC-XPORT templates | Generated |
| `data/company_context/learning_process_queue.json` | Generated PROC-* learning/training queue | Generated |
| `data/company_context/training_process_manifest.json` | Generated ingest manifest + next steps | Generated |
| `data/geologix-core-training.json` | Curated ~54 subsidiary routing/soul examples (hyphen name) | Active |
