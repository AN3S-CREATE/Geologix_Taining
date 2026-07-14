# Geologix AI — Company Context Learning & Training Process

**Purpose:** Turn `data/veralogix_companys_information/` into durable context for **Geologix AI** (Veralogix Group internal AI).  
**Scope for this phase:** Company identity, subsidiary routing, and market-intelligence memory. Legal ZASCA training stays in the existing Phase 1–7 pipeline.

---

## Source of truth

| Asset | Path | Role |
|-------|------|------|
| Portfolio map | `data/veralogix_companys_information/portfolio_index.json` | Master company list + data readiness |
| Per-company card | `{Company}/index.json` | Overview, sector, related companies, read order |
| Research brief | `{Company}/Prompt.md` | Company facts + intelligence gaps |
| Structured intel | `{Company}/market_intelligence.json` and/or `01_*.json` / `doc*_*.json` | Facts for RAG + example grounding |
| Cross-group rules | `CROSS-PORTFOLIO/index.json` (+ docs) | Multi-subsidiary trigger → routing |
| Generated pack | `data/company_context/` | Outputs of Process P1–P3 (ingest script) |

**Traversal rule (from portfolio):** for any company, read `index.json` first, then `chunks_manifest.json` / `market_intelligence.json`, then section chunks, then `Prompt.md`.

---

## Three layers (how company knowledge is used)

```
┌─────────────────────────────────────────────────────────────┐
│  LAYER A — SYSTEM PROMPT (Identity Card)                    │
│  Who Geologix AI is; Group HQ; subsidiary map; tone rules.  │
│  Loaded every session. Source: portfolio + Group index.     │
├─────────────────────────────────────────────────────────────┤
│  LAYER B — FINE-TUNE (Company Soul)                         │
│  Instruction/response pairs: intros, routing, procedures,   │
│  cross-portfolio coordination. → geologix_core_training.json│
├─────────────────────────────────────────────────────────────┤
│  LAYER C — RAG (Company Memory)                             │
│  Market intel chunks, tenders, competitors, triggers.       │
│  Retrieved on demand. Never baked into weights as raw docs. │
└─────────────────────────────────────────────────────────────┘
```

Confidential live operational data (current contracts, personal data, unpublished pricing) stays out of Layer B. Prefer anonymised patterns and public/market intel for training examples.

---

## Process catalogue (learning & training)

### P0 — Inventory & readiness gate

1. Run / refresh ingest (`scripts/00_ingest_company_context.py`).
2. Confirm `portfolio_index.json` company count matches folders with `index.json`.
3. Classify each entity by `data_status`:
   - `complete` / `complete_chunked` → eligible for Layer B examples + Layer C RAG
   - `prompt_plus_docs` / `chunked_from_docs` → Layer A identity + Layer C from chunks; Layer B only after fact check
   - `prompt_only` → identity stub only until research lands
4. Gate: do not train Layer B from folders still `prompt_only` without human-written facts.

**Output:** `data/company_context/company_registry.json`, readiness summary in `training_process_manifest.json`.

---

### P1 — Identity card (Layer A)

1. Pull Group HQ, sector, holding narrative from `Veralogix Group/index.json` + `Prompt.md` COMPANY CONTEXT block.
2. Build subsidiary taxonomy from `portfolio_index.json` (folder, display_name, group, sector, hq).
3. Write Geologix AI identity rules:
   - Internal assistant for Veralogix Group / Geologix Vanguard portfolio
   - Route to the correct subsidiary; surface cross-portfolio dependencies
   - Modular, scalable, ROI-driven; cite sources when retrieved
   - Strategic decisions remain with human leadership
4. Update `models/Geologix.modelfile` SYSTEM block when identity pack changes (count and clusters must match registry).

**Output:** `data/company_context/geologix_identity.json`.

---

### P2 — Company-soul training pairs (Layer B)

For each **ready** company, generate Alpaca-style examples (`instruction` / `input` / `output`) covering these **process types**:

| Process ID | Example type | Teaches the model to… |
|------------|--------------|------------------------|
| PROC-ID | Identity / intro | Introduce Geologix AI and the entity in Group voice |
| PROC-ROUTE | Single-subsidiary routing | Send a query to the correct company and explain why |
| PROC-XPORT | Cross-portfolio coordination | Expand a trigger event into a multi-entity action chain |
| PROC-SOP | Operating procedure | Describe standard response / escalation (non-confidential) |
| PROC-OFFER | Capability brief | Explain what the subsidiary sells / delivers |
| PROC-RISK | Risk & compliance handoff | Flag MHSA / POPIA / environmental / security handoffs |

**Minimum coverage target (core model):**

- 1× PROC-ID for Geologix AI + Group
- ≥1× PROC-ROUTE per operating company (prefer ready companies first)
- All `cross_portfolio_triggers` as PROC-XPORT examples
- Existing curated set in `data/geologix-core-training.json` remains the seed; new pairs append after review

**Blend for `02_train_geologix.py` (company model):** keep general conversational ability; company soul should dominate identity/routing, not drown the model in raw market-intel dumps.

**Output:** reviewed pairs merged into `data/geologix_core_training.json` (canonical underscore name for scripts).

---

### P3 — Cross-portfolio routing processes (Layer B + ops)

1. Load `CROSS-PORTFOLIO/index.json` → `cross_portfolio_triggers`.
2. For each trigger, define a training process:
   - Event name
   - Lead subsidiary (primary custody)
   - Supporting subsidiaries
   - Suggested first action (joint review window, document pull, etc.)
3. Encode as PROC-XPORT instruction/response pairs.
4. Keep the machine-readable trigger list for RAG and future router logic.

**Output:** `data/company_context/cross_portfolio_triggers.json` + training pairs.

---

### P4 — Company RAG vault (Layer C)

*Separate from legal vault (`models/legal_vault/`).*

1. Index, per company (when present):
   - `market_intelligence.json`
   - Sectional `01_*.json` … `05_*.json`
   - Chunk files listed in `chunks_manifest.json`
2. Metadata on every chunk: `company`, `group`, `sector`, `section`, `source_file`, `as_of`.
3. Query path: retrieve → attribute subsidiary → answer in Geologix voice.
4. Exclude `_research_archive/` and blocked pharma/personal materials.

**Output (later script):** e.g. `models/company_vault/` (not built in this phase).

---

### P5 — Merge into training run

1. Validate JSON (no markdown fences, unique instructions where possible).
2. Ensure `geologix_core_training.json` is the file `02_train_geologix.py` loads.
3. Run existing Phase 2–5: prepare → train general → export Ollama `geologix`.
4. Legal track (`veralogix_legal_training.json` + ZASCA + `geologix-legal`) stays independent unless a company example is explicitly legal.

---

### P6 — Evaluation gate (before calling it “trained”)

Sample checks:

1. “Who are you?” → Geologix AI / Veralogix Group, correct scope.
2. Random subsidiary intro → correct sector + HQ region + ≥1 related company.
3. Each CROSS-PORTFOLIO trigger → correct triggered companies.
4. Ambiguous multi-issue query → lead + support subsidiaries named.
5. Refusal / escalation: strategic decisions left to humans; no invented live contract numbers.

Fail any critical check → fix Layer A/B examples, do not ship Modelfile.

---

## Recommended cadence

| Cadence | Action |
|---------|--------|
| When portfolio intel updates | Re-run P0 ingest; refresh Layer C chunks |
| Weekly (or after ≥3 company updates) | Add/review Layer B pairs; re-run P6 spot checks |
| After identity or company-count change | Update Modelfile SYSTEM + re-export Ollama |

---

## What this phase delivers now

1. This process document (human + agent SOP).
2. `scripts/00_ingest_company_context.py` — builds the Layer A/B scaffolding pack under `data/company_context/`.
3. No model training run yet — ingest + process definition only.

## Next (after you approve)

1. Draft PROC-* training pairs from the generated pack into `geologix_core_training.json`.
2. Align Modelfile subsidiary count with the live registry (portfolio currently tracks **30** companies).
3. Add company RAG script (P4) parallel to `05_legal_rag.py`.
