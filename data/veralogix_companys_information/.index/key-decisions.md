# Key Decisions Log

This log records major structural and architectural decisions made for the workspace.

## ADR-001: Consolidated Parent Holdings
- **Date**: 2026-07-08
- **Context**: Workspace was fragmented with duplicate naming, inconsistent spellings, and flat folders.
- **Decision**: Merged duplicate companies and grouped business units under explicit parent group folders (e.g. `Veralogix Group`, `Treadstone`, `Salaria`, `Veramani`).
- **Rationale**: Restores a hierarchy that matches real-world ownership and business divisions, making cross-selling and sector analysis easier.

## ADR-002: Bioniq (ISP) and Vcom Excluded from Veramani
- **Date**: 2026-07-12
- **Context**: Bioniq and Vcom were initially nested under Veramani, but the user requested keeping them independent.
- **Decision**: Moved `Bioniq (ISP)` and `Vcom` back to root level.
- **Rationale**: Preserves their identity as standalone infrastructure/consumer entities rather than internal IT departments.

## ADR-003: Processing & Plant Restored for Woestalleen *(SUPERSEDED by ADR-005)*
- **Date**: 2026-07-12
- **Context**: The user commented "Woestaleen" on `Processing & Plant`.
- **Decision**: Recreated `Processing & Plant` folder and moved `Veralogix Plant (Woestalleen)` into it.
- **Rationale**: Specifically aligns the toll washing/beneficiation operations under the appropriate sector division.

---

## ADR-004: Bioniq (ISP) and Vcom Moved Under Veramani *(reverses ADR-002)*
- **Date**: 2026-07-13
- **Context**: Deep read of all Prompt.md files confirmed Veramani is explicitly the IT holding company for the Veralogix Group. Vcom is a Fibre Network Operator (FNO), Bioniq is an ISP — both are IT/connectivity businesses, not standalone industrial entities.
- **Decision**: Bioniq (ISP) and Vcom reside under `Veramani/`. This is their confirmed final home.
- **Rationale**: Aligns with actual corporate ownership and IT holding structure. Both entities sit correctly under an IT/connectivity holding umbrella.

## ADR-005: Veralogix Plant (Woestalleen) Moved to Veralogix Group *(supersedes ADR-003)*
- **Date**: 2026-07-13
- **Context**: Deep read of Prompt.md confirmed Veralogix Plant is a Veralogix Group operational entity (ROM crushing, DMS coal washing, rail siding at Woestalleen). `Processing & Plant` was a sector-tag folder, not a group.
- **Decision**: `Veralogix Plant (Woestalleen)` moved to `Veralogix Group/`. `Processing & Plant/` folder deleted.
- **Rationale**: Keeps all Veralogix operating divisions under one group parent, consistent with the rest of the structure.

## ADR-006: Veralift Confirmed Under Veralogix Group
- **Date**: 2026-07-13
- **Context**: Veralift provides crane hire and heavy lifting services to construction, mining, and industrial sectors — a direct operational complement to the Veralogix fleet and project businesses.
- **Decision**: `Veralift/` stays under `Veralogix Group/` as a confirmed operating division.
- **Rationale**: Matches real-world group ownership and cross-selling relationship with Veralogix Rentals and Veralogix Projects.
