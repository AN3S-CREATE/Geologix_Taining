# Architecture Overview

This workspace contains market and competitive intelligence profiles for all business units
under the Geologix Vanguard portfolio. The consolidation and cleanup are **complete** as of 2026-07-13.

## Final Root Structure — FLAT (AI Knowledge Base Optimised)

All 27 companies sit directly at root level. No group nesting. Each folder = one company.

```
Companys Information/
├── Veralogix Group/                    ← group holding entity + subsidiary map
├── Veralogix Mining (Pty) Ltd/
├── Veralogix Rentals/
├── Veralogix Plant (Woestalleen)/
├── Veralogix Diesel/
├── Veralogix Drilling & Blasting/
├── Veralogix Projects (Pty) Ltd/
├── Veralogix Properties (Pty) Ltd/
├── Alpha Industries SA/
├── Alpha Technical Solutions/
├── Endeto Project Services/
├── Coal Processors International/
├── Veralift/
├── Treadstone Logistics/               ← renamed from Treadstone/Logistics
├── Treadstone CPM/                     ← renamed from Treadstone/CPM
├── CG Transport/
├── Salaria Mining Services/            ← renamed from Salaria/Mining Services
├── Salaria Safety Services/            ← renamed from Salaria/Safety Services
├── Mining Safety Services/
├── Aiguille Security/                  ← renamed from Aiguille/Security
├── Aiguille Tools & Edges/             ← renamed from Aiguille/Tools & Edges
├── Veramani IT/                        ← renamed from Veramani/IT Division
├── Veramani IT Holding/                ← renamed from Veramani/IT Holding Company
├── Bioniq (ISP)/
├── Vcom/
├── YAL.ai/
├── Vera-Commodities/
├── Ritz International/
├── IO Green/
├── Pencox Auto Air/
├── CROSS-PORTFOLIO/                    ← cross-company intelligence (kept at root)
├── Mining & Exploration/               ← sector placeholder (no entities yet)
└── _research_archive/                  ← raw research docs + blocked items
```

**Rationale:** Flat structure ensures AI can locate each company's knowledge directly
without navigating group hierarchies. Group membership is documented in each `Prompt.md`.


│   ├── _GROUP/                         ← group-level docs (Holdings brief, etc.)
│   ├── Alpha/
│   │   ├── Industries SA/
│   │   └── Technical Solutions/
│   ├── Coal Processors International/
│   ├── Endeto Project Services/
│   ├── Veralift/
│   ├── Veralogix Diesel/
│   ├── Veralogix Drilling & Blasting/
│   ├── Veralogix Mining (Pty) Ltd/
│   ├── Veralogix Plant (Woestalleen)/
│   ├── Veralogix Projects (Pty) Ltd/
│   ├── Veralogix Properties (Pty) Ltd/
│   └── Veralogix Rentals/
├── Treadstone/
│   ├── CG Transport/
│   ├── CPM/
│   ├── Logistics/
│   └── Logistics & Transport/          ← sector reference folder (README.md)
├── Salaria/
│   ├── Mining Safety Services/
│   ├── Mining Services/
│   └── Safety Services/
├── Aiguille/
│   ├── Security/
│   └── Tools & Edges/
├── Veramani/
│   ├── Bioniq (ISP)/
│   ├── IT Division/
│   ├── IT Holding Company/
│   ├── Vcom/
│   └── YAL.ai/
├── Commodities & Trading/
│   ├── Ritz International/
│   └── Vera-Commodities/
├── Energy & Engineering/
│   └── IO Green/
├── Equipment & Fleet/
│   └── Pencox Auto Air/
├── Mining & Exploration/               ← sector reference (README.md, no entities yet)
└── _research_archive/                  ← raw research docs + prompts (not intel data)
    ├── research_needed.md
    ├── [pharma docs — BLOCKED]
    └── ...
```

---

## Group Breakdown

### 1. Veralogix Group *(main operating group)*
Holding vehicle: **Veralogix Mining (Pty) Ltd**. All heavy mining operations sit here.

| Entity | Business | Status |
|---|---|---|
| Veralogix Mining (Pty) Ltd | Holding company / contract mining | Prompt + docs |
| Veralogix Rentals | 320+ unit heavy equipment rental fleet | ✅ COMPLETE |
| Veralogix Plant (Woestalleen) | ROM crushing, DMS coal washing, rail siding | ✅ COMPLETE |
| Veralogix Diesel | Diesel/fuel supply | Prompt + docs |
| Veralogix Drilling & Blasting | Drilling & blasting operations | Prompt + docs |
| Veralogix Projects (Pty) Ltd | Project delivery (corporate vehicle) | Prompt only |
| Veralogix Properties (Pty) Ltd | Property holding (3A Laver St, Middelburg) | Prompt + docs |
| Alpha / Industries SA | Crushing, screening & material handling | Prompt + docs |
| Alpha / Technical Solutions | Technical arm of Alpha | ✅ COMPLETE |
| Endeto Project Services | Engineering, fabrication, maintenance, OEM | ✅ COMPLETE |
| Coal Processors International | Coal plant labour & operational management | ✅ COMPLETE |
| Veralift | Mobile crane hire and heavy lifting | ✅ COMPLETE |

---

### 2. Treadstone Group *(logistics & bulk road transport)*

| Entity | Business | Status |
|---|---|---|
| Logistics | Treadstone bulk haulage | ✅ COMPLETE |
| CPM | Treadstone CPM (acronym TBC) | Prompt + docs |
| CG Transport | Bulk commodity transport | Prompt + docs |
| Logistics & Transport | Sector reference folder | README only |

---

### 3. Salaria Group *(mining technical services & safety)*

| Entity | Business | Status |
|---|---|---|
| Mining Services | Resource mgmt, mine planning, rock engineering | ✅ COMPLETE |
| Mining Safety Services | Safety audits, training, compliance | ✅ COMPLETE |
| Safety Services | Salaria safety arm | Prompt + docs |

---

### 4. Aiguille Group *(security & tooling)*

| Entity | Business | Status |
|---|---|---|
| Security | Mining & industrial security services | Prompt + docs |
| Tools & Edges | GET, cutting edges, wear parts supply | Prompt + docs |

---

### 5. Veramani *(IT holding company for Veralogix Group)*

| Entity | Business | Status |
|---|---|---|
| IT Division | Software dev, web, connectivity | Prompt + docs |
| IT Holding Company | Holding entity | Prompt only |
| Bioniq (ISP) | ISP, managed Wi-Fi, hotspot analytics | ✅ COMPLETE |
| Vcom | Aerial fibre FNO — VEA Group / townships | ✅ COMPLETE |
| YAL.ai | AI anti-phishing cybersecurity SaaS | Prompt + docs |

---

### 6. Commodities & Trading

| Entity | Business | Status |
|---|---|---|
| Vera-Commodities | Bulk mineral commodity trading | ✅ COMPLETE |
| Ritz International | Diesel trading & bulk fuel supply | ✅ COMPLETE |

---

### 7. Energy & Engineering

| Entity | Business | Status |
|---|---|---|
| IO Green | Solar & electrical supply/installation | Prompt + docs |

---

### 8. Equipment & Fleet

| Entity | Business | Status |
|---|---|---|
| Pencox Auto Air | Vehicle & earthmoving A/C and auto electrical | ✅ COMPLETE |

---

### 9. Mining & Exploration *(sector placeholder)*
No registered entities yet. Holds README.md.

---

### CROSS-PORTFOLIO *(root-level — cross-group by design)*
Contains cross-portfolio market intelligence, tender monitoring, and signal routing documents.
Do not move into any group folder.

---

## Data Conventions

| File/Folder | Purpose |
|---|---|
| `Prompt.md` | Market research brief for Gemini intelligence generation |
| `market_intelligence.json` | Primary compiled intelligence output |
| `01_*.json` … `05_*.json` | Sectoral sub-documents (Bioniq model) |
| `doc_*.json` | Raw intelligence documents |
| `*.docx` / `*.pdf` | Research reports allocated from `_research_archive/` |
| `README.md` | Sector reference or placeholder notes |
| `_GROUP/` | Group-level documents spanning multiple subsidiaries |
| `_research_archive/` | Raw research docs, prompts, and blocked items |

## Cleanup History
- **2026-07-13 — Full cleanup executed:**
  - Deleted 5,000+ K/Q/C/D OneDrive sync dump items from Vcom, Bioniq, Properties, Mining & Exploration
  - Renamed `company_information_reseach/` → `_research_archive/` (fixed typo)
  - Created `Veralogix Group/_GROUP/` for group-level documents
  - Added README.md to Treadstone/Logistics & Transport and Mining & Exploration
  - Moved `research_needed.md` into `_research_archive/`
  - Result: Zero junk folders, clean two-level hierarchy throughout
