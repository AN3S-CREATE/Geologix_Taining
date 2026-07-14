# Key Decisions — Geologi_Taining

## 2026-07-13 — Repo root is the training project

- **Decision:** Use this repository root as `geologix-ai` (not a separate `~/geologix-ai` home folder).
- **Rationale:** Workspace is already `Geologi_Taining`; keeps docs and pipeline in one place.
- **Source:** `docs/geologix-complete-setup.md` Phase 2 layout applied here.

## 2026-07-13 — Setup doc is procedural source of truth

- **Decision:** Follow `docs/geologix-complete-setup.md` for phases, scripts, and Modelfiles.
- **Rationale:** User designated it as the source of truth for the AI training layout.

## 2026-07-13 — `04_export_to_ollama.py` wraps Phase 5

- **Decision:** Implement the checklist script as an Ollama `create` helper over the Modelfiles.
- **Rationale:** Phase 2 lists the file; Phase 5 defines the Modelfile + `ollama create` steps.

## 2026-07-13 — Remotes renamed Geologi → Geologix

- **Decision:** Point `origin` at `AN3S-CREATE/Geologix_Taining` and `veralogix` at `VeralogixCatalyst/geologix_taining`; rename GitHub repos to match.
- **Rationale:** User requested Geologix branding on both remotes.
