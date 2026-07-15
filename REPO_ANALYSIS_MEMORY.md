# Repository Analysis State — Geologi_Taining

## Current Analysis Phase & Progress
Phase 3: Company-context learning process for Geologix AI — process definition + ingest pack complete (~40%). Training-pair fill and Modelfile sync not started.

## Key Architectural Insights Discovered
- Insight 1: Source of truth is `docs/geologix-complete-setup.md` (Ollama + Unsloth pipeline for `geologix` and `geologix-legal`).
- Insight 2: Layout is `data/` + `scripts/` + `models/` plus root `ask_legal.py` for RAG queries.
- Insight 3: Custom training JSON starts empty (`[]`); ZASCA and merged weights are generated artifacts.
- Insight 4: The current scripts expect strict JSON in `data/geologix_core_training.json` and `data/veralogix_legal_training.json`; the checked data files include markdown/preamble wrappers, and the clean 54-example group dataset is currently in `data/geologix-core-training.json`.
- Insight 5: Production hardening gaps identified in the scaffold: no JSON normalization step, no structured run logging/correlation IDs, no persistent checkpoints for RAG ingestion, and GPU-only embedding assumptions in `05_legal_rag.py` and `ask_legal.py`.
- Insight 6: Company knowledge source is `data/veralogix_companys_information/` (flat folders + `portfolio_index.json` + `CROSS-PORTFOLIO/`). Feeds Geologix AI via three layers: identity prompt, company-soul fine-tune, company RAG (separate from legal vault).
- Insight 7: Portfolio tracks ~30 companies; ingest registry currently 31 including sector placeholder `Mining & Exploration`. Modelfile still says “17 subsidiaries” and must be updated after identity review.

## Files Deeply Reviewed
- `docs/geologix-complete-setup.md` (Summary: Full Phase 0–7 setup: prepare data, train general/legal, Ollama Modelfiles, Chroma RAG vault.)
- `docs/company-ai-identity-guide.md` (Summary: Three-layer company identity system: system prompt, fine-tuned weights, RAG memory; includes 50/30/20 blend model and company identity prompt.)
- `docs/sa-legal-ai-guide.md` (Summary: Beginner QLoRA/Unsloth roadmap for SA legal model on RTX 5070-class GPU, with ZASCA-Sum, POPIA examples, and Ollama export.)
- `docs/sa-legal-rag-guide.md` (Summary: Secure legal RAG architecture, POPIA sanitization, AnythingLLM/OpenWebUI fast track, and Python Chroma/Ollama pipeline.)
- `docs/company-training-examples (1).md` (Summary: Five fictional firm examples and template patterns for company-soul training data.)
- `scripts/01_prepare_data.py` through `scripts/05_legal_rag.py`, `ask_legal.py`, and both Ollama Modelfiles (Summary: Current implemented training, export, RAG indexing, and legal query scripts.)
- `data/veralogix_companys_information/portfolio_index.json` + sample `index.json` / `Prompt.md` / `CROSS-PORTFOLIO` (Summary: Geologix Vanguard portfolio knowledge base; AI read-order and cross-portfolio triggers.)
- `docs/geologix-ai-company-context-process.md` (Summary: P0–P6 company-context learning/training SOP for Geologix AI.)
- `scripts/00_ingest_company_context.py` (Summary: Builds `data/company_context/` identity, registry, triggers, process queue.)

## Open Questions & Areas Needing Investigation
- Q1: Where are the filled `geologix_core_training.json` / `veralogix_legal_training.json` example artifacts to paste?
- Q2: Should the canonical group training file be renamed from `data/geologix-core-training.json` to `data/geologix_core_training.json`, or should scripts support both names?
- Q3: Which storage target is canonical for production vaults: local workstation disk, TrueNAS share, or an air-gapped removable/encrypted volume?
- Q4: Should `Mining & Exploration` stay in the Geologix AI registry as a sector stub, or be excluded from identity/company_count?

## Decisions Made & Rationale
- Decision: Scaffold structure at repo root (not `~/geologix-ai`) so this git repo is the working project.
  Rationale: Matches the user's Geologi_Taining workspace and keeps docs + code together.
- Decision: Implement `04_export_to_ollama.py` as an Ollama `create` wrapper around the Modelfiles.
  Rationale: Listed in Phase 2 checklist but not fully scripted in the doc; Phase 5 steps are the behavior.
- Decision: Company context for Geologix AI is ingested via P0–P3 process + `00_ingest_company_context.py` before generating new Alpaca pairs or training.
  Rationale: User asked to populate context from `veralogix_companys_information` and define learning/training processes only for this step.

## Next Immediate Steps
1. Fill PROC-ROUTE / PROC-XPORT templates from `data/company_context/learning_process_queue.json` into Alpaca pairs.
2. Append reviewed pairs into canonical `data/geologix_core_training.json` (keep curated seed in `geologix-core-training.json`).
3. Update `models/Geologix.modelfile` SYSTEM from `geologix_identity.json` (company count + groups).
4. Later: company RAG vault (P4) parallel to legal vault.
5. Install deps / run Phase 0–2 training when ready.

## Patterns & Recurring Issues Noticed
- Pattern: Scripts assume cwd is project root (`data/`, `models/` relative paths).
- Pattern: The docs separate model identity into system prompt, fine-tuned behavior, and RAG memory; production implementation should preserve this separation and keep confidential current matters out of weights.
- Pattern: Some company JSON files use UTF-8 BOM — ingest must open with `utf-8-sig`.
- Recurring Issue: Training examples and Modelfile still reference “17 subsidiaries” while portfolio/registry is ~30+.

## Session Log
- [2026-07-13] Initialized memory. Scaffolded data/scripts/models from setup doc. Created .index/.
- [2026-07-13] Remotes updated + GitHub repos renamed: origin → AN3S-CREATE/Geologix_Taining, veralogix → VeralogixCatalyst/geologix_taining.
- [2026-07-14] Reviewed source docs, scripts, modelfiles, `.index`, and training data for first-person Andries build specification. Recorded data-format and hardening gaps.
- [2026-07-14] Built company-context process doc + ingest script; generated `data/company_context/` pack (31 companies, 7 XPORT + 30 ROUTE templates). No model training run.
- [2026-07-14] Committed `81bc6c9` and pushed branch `main-geologix-training-scaffold` to origin (AN3S-CREATE/Geologix_Taining) and veralogix (VeralogixCatalyst/geologix_taining). Nested company-pack `.git` renamed to `.git_nested_disabled` so files track in parent repo.
- [2026-07-14] Removed nested company-pack `.index/` and blocked `_research_archive/` pharma docs from tracked tree; pushed cleanup to both remotes.
- [2026-07-14] Merged `main-geologix-training-scaffold` into `main` on both remotes at `a0000ea` (Veralogix used `--force-with-lease` for unrelated history).
- [2026-07-14] Restored local working tree with `git reset --hard a0000ea`; local `main` clean and matches both remotes.
- [2026-07-14] Fixed stale `main-geologix-training-scaffold` (behind main by 2 merge commits, not conflicted). Fast-forwarded to `a0000ea` and pushed to both remotes; GitHub compare now `identical`.
- [2026-07-14] Verified identical on both remotes; deleted merged `main-geologix-training-scaffold` locally and on origin + veralogix. Only `main` remains at `a0000ea`.
