# Project Context Index (`.index/`)

Living context store for agents and humans working in **Geologi_Taining**.

## Purpose

Keep architecture, file inventory, and decisions accurate so sessions do not restart from zero.

## Required files

| File | Purpose |
|------|---------|
| `README.md` | This file — how to use the index |
| `file-inventory.md` | Paths + one-line purpose + status |
| `architecture.md` | System overview and pipeline |
| `key-decisions.md` | ADR-style decisions |
| `dead-code.md` | Unused / legacy code log |
| `context-refresh-log.md` | Index refresh history |

## Maintenance

- Update `file-inventory.md` after create/edit/delete.
- Update `architecture.md` / `key-decisions.md` on meaningful changes.
- Log refreshes in `context-refresh-log.md`.

## Source of truth for training

Pipeline details live in `docs/geologix-complete-setup.md`. The index summarizes; the setup doc wins on procedure.
