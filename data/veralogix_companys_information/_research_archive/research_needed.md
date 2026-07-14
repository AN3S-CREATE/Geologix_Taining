# Research Needed — Gemini + Google Drive Prompts

**Created:** 2026-07-13  
**Purpose:** Copy-paste prompts for **Google Gemini** (with Google Drive access) to extract company facts from Drive, then produce market/tender intelligence for every Veralogix / Geologix portfolio entity.  
**Canonical entity list:** `Geologix Vanguard/Geologix Vanguard/data/knowledge-base/portfolio/company_registry.json` (30 entities, 2026-06-30)  
**Curated KB status:** `Companys Information/.project-intel/docs/component-catalog.md`

---

## How to use (Gemini + Drive)

1. Open **Gemini** while signed into the Google account that owns the Drive.  
2. Attach / enable **Google Drive** grounding (or `@` the relevant folders/files).  
3. Paste **Prompt 0 (Drive locator)** once per company to find source files.  
4. Paste **Prompt A (Company profile from Drive)** to fill the internal profile.  
5. Paste the **company-specific market intel prompt** (sections below) for external competitive/tender research.  
6. Save Gemini’s JSON into the matching folder under `Companys Information/` as:
   - `Prompt.md` context (keep/update)  
   - `market_intelligence.json` (research product)  
   - Optionally update `Geologix Vanguard/.../knowledge-base/companies/<slug>/profile/company_profile.json`

**Output rule for every prompt:** Return **valid JSON only** (no markdown fences unless asked). Cite Drive file names / URLs in a `sources` array.

**Priority order (do first):** MVP trio → EMPTY operating companies → PROMPT_ONLY normalize → COMPLETE refresh → corporate vehicles (light).

| Priority | Entities | Why |
| --- | --- | --- |
| **P0 MVP** | Salaria Mining Services, Veralogix Rentals, IO Green | `mvp: true` in registry; Geologix Vanguard Phase-1 focus |
| **P1 EMPTY ops** | Aiguille Security, Tools & Edges, CG Transport, CG Auto Transport, Tread Stone CPM, Veralogix Diesel, Drilling & Blasting, Veralogix Mining, Alpha Industries SA, Salaria Safety Services, YAL.ai, Veralogix Projects/Properties (light) | Missing Prompt/intel in Companys Information |
| **P2 Normalize** | IO Green, Veramani IT | Have Prompt + `doc_*.json` but not standard `market_intelligence.json` |
| **P3 Refresh** | All COMPLETE leaves | Drive may have newer facts than June 2026 JSON |
| **Blocked** | TBD Pharma | No registered name yet |

---

## Extra sources found outside `Companys Information`

Use these as Drive/OneDrive starting points when Gemini searches:

| Location | What it contains |
| --- | --- |
| `Geologix Vanguard/Geologix Vanguard/data/knowledge-base/companies/*` | Entity folders + mostly **empty** `company_profile.json` stubs |
| `Geologix Vanguard/Geologix Vanguard/data/archive/backups/*/knowledge-base/companies/*` | Same stubs (2026-07-01 / 07 / 08) |
| `Geologix Vanguard/Veralogix Group/doc_2f6417.md` | Long Veralogix Group corporate research report (Middelburg HQ, subsidiaries narrative) |
| `Geologix Vanguard/Veralogix Rentals/Veralogix Rentals.md` + `.json` | Rentals deep research |
| `Geologix Vanguard/Salaria Mining Services/doc_40617f.md` + `.json` | Salaria deep research |
| `Geologix Vanguard/IO_Green/doc_8f86fe.md` | IO Green market intel (competitors, tenders) |
| `Geologix Vanguard/The Pitch/*` | Strategy PDF + DB schema research prompts |
| `Geologix Vanguard/Research/Bioniq/` + `Veramani_IT_Devision/` | Extra Bioniq / Veramani research |
| `Geologix Vanguard/chronicle/Chronicle.md` | Group chronicle notes |
| `Companys Information/**/Prompt.md` + `market_intelligence.json` | Existing curated intel (14 COMPLETE) |
| `Companys Information/**/K|Q|C|D/` | Raw Drive mirrors — rich but noisy; ask Gemini to **filter** |

---

## Prompt 0 — Drive locator (run per company)

```text
You have access to my Google Drive. Search for ALL files and folders related to the South African company:

COMPANY: {{DISPLAY_NAME}}
ALSO SEARCH: {{ALIASES}}
GROUP CONTEXT: Veralogix Group / Geologix Vanguard / Middelburg Mpumalanga

Tasks:
1. List the top 30 most relevant Drive files (name, path/folder, type, last modified if available).
2. Tag each file: company_profile | financial | tender | legal | marketing | ops | fleet | unrelated.
3. Identify the 5 best files to build an accurate company profile.
4. Flag any sensitive files (ID docs, bank details, passwords, personal WhatsApp) — do NOT quote their contents; only note path + "SENSITIVE".

Return JSON:
{
  "company": "",
  "search_terms_used": [],
  "files": [{"name":"","path":"","type":"","tag":"","why_relevant":""}],
  "best_5": [],
  "sensitive_paths": [],
  "gaps": ["what we still cannot find on Drive"]
}
```

**Suggested Drive search terms per company** (paste into Drive search too):

| Company | Search terms |
| --- | --- |
| Aiguille Security | `Aiguille` `security` `PSIRA` `Middelburg security` |
| Aiguille Tools & Edges | `Aiguille Tools` `edges` `cutting tools` `GET` |
| Alpha Industries SA | `Alpha Industries` `Alpha SA` `crushing` |
| Alpha Technical Solutions | `Alpha Technical` `crushing screening` |
| Bioniq | `Bioniq` `ISP` `hotspot` `Wi-Fi` |
| CG Transport | `CG Transport` `CG Transport Pty` |
| CG Auto Transport | `CG Auto` `vehicle transport` `car carrier` |
| Coal Processors International | `CPI` `Coal Processors` `plant labour` |
| Endeto | `Endeto` `fabrication` `OEM` |
| IO Green | `IO Green` `IO_Green` `solar` |
| Mining Safety Services | `Mining Safety Services` `MSS` |
| Pencox Auto Air | `Pencox` `auto air` `aircon` |
| Ritz International | `Ritz International` `diesel` `fuel` |
| Salaria Mining Services | `Salaria` `mine planning` `SAMREC` |
| Salaria Safety Services | `Salaria Safety` |
| Treadstone / Logistics | `Treadstone` `haulage` `bulk transport` |
| Tread Stone CPM | `Tread Stone CPM` `CPM` `Treadstone CPM` |
| Vcom | `Vcom` `aerial fibre` `FNO` `VEA` |
| Vera-Commodities | `Vera-Commodities` `Vera Commodities` `minerals trading` |
| Veralift | `Veralift` `crane` |
| Veralogix Diesel | `Veralogix Diesel` `diesel supply` |
| Veralogix Drilling & Blasting | `drilling blasting` `Veralogix D&B` |
| Veralogix Mining | `Veralogix Mining` `contract mining` |
| Veralogix Plant | `Woestalleen` `Veralogix Plant` `DMS` `washing` |
| Veralogix Projects | `Veralogix Projects` |
| Veralogix Properties | `Veralogix Properties` `Laver Street` |
| Veralogix Rentals | `Veralogix Rentals` `fleet` `excavator` |
| Veralogix Holdings | `Veralogix Holdings` `group structure` |
| Veramani | `Veramani` `IT` |
| YAL.ai | `YAL.ai` `YAL` `anti-phishing` `cyber` |

---

## Prompt A — Company profile from Drive (all companies)

```text
Using ONLY information found in my Google Drive (and any files I attach), build a factual company profile for:

{{DISPLAY_NAME}} (company_id: {{COMPANY_ID}})
Parent group: Veralogix Group (Middelburg, Mpumalanga, South Africa unless Drive says otherwise).

Rules:
- Prefer primary documents (letterheads, CIPC docs, quotes, websites drafts, presentations).
- If a field is unknown, use null or [] — NEVER invent registration numbers, BBBEE levels, or client names.
- Quote short evidence snippets and name the Drive file for each non-null field.

Return JSON:
{
  "company_id": "{{COMPANY_ID}}",
  "display_name": "",
  "trading_names": [],
  "parent_group": "",
  "industry_vertical": "",
  "description": "",
  "services": [],
  "products": [],
  "website": null,
  "email": null,
  "phone": null,
  "physical_address": null,
  "operating_regions": [],
  "primary_commodities_served": [],
  "key_clients_public": [],
  "fleet_or_assets_summary": null,
  "b_bbee_level": null,
  "cipc_registration_number": null,
  "psira_or_other_licences": [],
  "cidb_grade": null,
  "employees_approx": null,
  "relationship_notes": "how this entity relates to sister companies if mentioned",
  "open_questions": [],
  "sources": [{"file":"", "field":"", "snippet":""}],
  "confidence": "high|medium|low",
  "last_updated": "YYYY-MM-DD"
}
```

---

## Prompt B — Universal market intelligence (template)

Use when a company-specific prompt is not listed, or as a refresh wrapper:

```text
You are a market intelligence researcher for a South African industrial group (Veralogix / Geologix Vanguard).

COMPANY: {{DISPLAY_NAME}}
VERTICAL: {{VERTICAL}}
KNOWN CONTEXT (from Drive / internal docs — treat as seed, verify publicly):
{{CONTEXT_BULLETS}}

Research PUBLIC South African sources and return JSON with keys:
{
  "competitors": [ {"name":"","website":"","overlap":"","regions":"","notes":""} ],
  "tender_landscape": { "portals":[], "typical_buyers":[], "required_registrations":[], "notes":"" },
  "regulatory_watchlist": [ {"body":"","obligation":"","monitor_url":""} ],
  "opportunity_signals": [ {"signal":"","source":"","url":"","urgency":"immediate|this_week|this_month"} ],
  "key_terminology": [],
  "sister_company_synergies": [ {"sister":"","joint_opportunity":""} ],
  "sources": [],
  "generated_at": "YYYY-MM-DD",
  "limitations": []
}

Constraints: South Africa focus; cite URLs; mark uncertain items; no fabricated CIPC/BBBEE data.
```

---

# Company prompts — P0 MVP

## 1. Salaria Mining Services — `salaria-mining-services` — MVP · COMPLETE (refresh + Drive profile)

**Save to:** `Companys Information/Salaria/Mining Services/`  
**Also merge into:** `.../knowledge-base/companies/salaria-mining-services/profile/`  
**Local extras:** `Geologix Vanguard/Salaria Mining Services/*`

```text
You are a market intelligence researcher. Use my Google Drive files about Salaria Mining Services PLUS public SA sources.

COMPANY CONTEXT (verify/correct from Drive):
Salaria Mining Services provides mineral resource management and reporting, mine plan drafting, rock engineering, geotechnical analysis, reserve statements, feasibility studies, and exploration services in South Africa.

TASKS:
A) From Drive: fill company_profile fields (CIPC, address, services list, key people titles only if public/internal docs allow, regions).
B) From public web: refresh competitors, tenders, regulators, signal sources, terminology.

Return ONE JSON object:
{
  "company_profile": { ... same schema as Prompt A ... },
  "competitors": [],
  "tender_landscape": {},
  "regulatory_watchlist": [],
  "signal_sources": [],
  "key_terminology": [],
  "drive_file_index": [],
  "generated_at": ""
}
```

---

## 2. Veralogix Rentals — `veralogix-rentals` — MVP · COMPLETE (refresh)

**Save to:** `Companys Information/Veralogix Group/Veralogix Rentals/`  
**Local extras:** `Geologix Vanguard/Veralogix Rentals/*`

```text
Market intelligence refresh for Veralogix Rentals (SA heavy mining equipment rental; fleet often cited 320+ units: excavators, dozers, loaders, ADTs, specialised vehicles).

1) From my Google Drive: extract exact fleet lists, rate cards if present, depot locations, client sectors, BBBEE/CIPC if documented.
2) Public research JSON keys: competitors, demand_signal_sources, tender_landscape, equipment_demand_by_sector (coal/chrome/iron ore/PGM/gold), regulatory_requirements.
3) Flag anything in Drive that contradicts the public description.

Return JSON with company_profile + those keys + sources[].
```

---

## 3. IO Green — `io-green` — MVP · PROMPT_ONLY (needs `market_intelligence.json`)

**Save to:** `Companys Information/Energy & Engineering/IO Green/market_intelligence.json`  
**Local extras:** `Geologix Vanguard/IO_Green/doc_8f86fe.md`

```text
Build complete market_intelligence.json for IO Green (SA solar supply/install + electrical supply/install for industrial, commercial, mining).

Use Drive + the existing IO Green research docs if found + public sources.

JSON keys required:
competitors, market_opportunity_signals, tender_landscape, energy_market_context, competitive_positioning,
company_profile (Prompt A schema), sources, generated_at

Also list CIDB / DOL / ECB requirements and Section 12B relevance for industrial solar clients.
```

---

# Company prompts — P1 EMPTY / high gap

## 4. Aiguille Security — `aiguille-security` — EMPTY · HIGH PRIORITY

**Save to:** `Companys Information/Aiguille/Security/`  
**Note:** Large `Q/` sync may contain ops docs — use Prompt 0 first; skip SENSITIVE content.

```text
You are a market intelligence researcher for Aiguille Security, a South African security company in the Veralogix Group (Mpumalanga / mining-industrial focus likely).

FROM GOOGLE DRIVE: determine exact services (armed response, guarding, CCTV, mining site security, investigations), PSIRA status, operating areas, and any tender history. Do not invent licence numbers.

PUBLIC RESEARCH — return JSON:
{
  "company_profile": {},
  "competitors": [ {"name":"","website":"","services":"","regions":"","mining_focus":true} ],
  "regulatory_watchlist": [ {"body":"PSIRA|SAPS|...","obligation":"","url":""} ],
  "tender_landscape": { "portals":[], "mining_house_security_rfps":[], "typical_requirements":[] },
  "opportunity_signals": [],
  "key_terminology": [],
  "sources": [],
  "generated_at": ""
}
```

---

## 5. Aiguille Tools & Edges — `aiguille-tools-edges` — EMPTY · confirm scope

**Registry note:** tools/hardware supply? Confirm scope.

```text
Research Aiguille Tools & Edges (South Africa, Veralogix/Aiguille group). First use Drive to discover whether they supply mining GET (ground engaging tools), industrial cutting edges, tooling, or something else.

Return JSON:
company_profile, product_categories, competitors, tender_landscape, OEM_brands_common_in_SA_mining, opportunity_signals, open_questions, sources, generated_at

If Drive is empty, state confidence=low and list what a human must confirm.
```

---

## 6. CG Transport — `cg-transport` — EMPTY

```text
Research CG Transport (Pty) Ltd — South African logistics company linked to Veralogix / Treadstone group.

Drive first: confirm commodity vs general freight, routes, fleet type, depots.
Then public JSON: competitors, tender_landscape, regulatory_watchlist (RTMS, Cross-Border, DoT), opportunity_signals (mining haulage, Transnet disruptions), sister_synergies (Treadstone, Rentals, Vera-Commodities), sources, company_profile, generated_at
```

---

## 7. CG Auto Transport — `cg-auto-transport` — EMPTY · confirm vs CG Transport

```text
Clarify and research CG Auto Transport (SA). Registry asks: auto/vehicle transport vs bulk commodity transport?

From Drive: prove whether distinct from CG Transport.
JSON: company_profile, service_scope, competitors (car carriers / dealer logistics), tender_landscape, opportunity_signals, distinction_from_cg_transport, sources, generated_at
```

---

## 8. Tread Stone CPM — `treadstone-cpm` — EMPTY · acronym unconfirmed

```text
Research Tread Stone CPM (South Africa, logistics vertical under Veralogix). Registry note: CPM acronym unconfirmed.

1) Search Drive for expansions of "CPM" (e.g. Contract Project Management, Coal Processing Management, etc.).
2) If still unknown, list top 5 plausible expansions with evidence scores.
3) Market intel JSON once scope is best-guess: competitors, buyers, tenders, signals, open_questions, company_profile, sources, generated_at
```

---

## 9. Veralogix Diesel — `veralogix-diesel` — EMPTY · confirm vs Ritz

```text
Research Veralogix Diesel (SA fuel/diesel supply under Veralogix). Confirm relationship to Ritz International (diesel trading) from Drive.

JSON keys: company_profile, relationship_to_ritz_international, competitors, tender_landscape (mining diesel supply, municipal fuel), regulatory_watchlist (NERSA wholesale, customs if import), opportunity_signals (load-shedding genset diesel demand, mining production), sources, generated_at
```

---

## 10. Veralogix Drilling & Blasting — `veralogix-drilling-blasting` — EMPTY

```text
Research Veralogix Drilling & Blasting (SA mining services).

Drive: equipment, explosives partnerships, regions, mine sites served.
Public JSON: competitors, tender_landscape, regulatory_watchlist (Explosives Act, DMRE, MHSA), opportunity_signals (new pits, strip ratios, contractor changeouts), key_terminology, sources, company_profile, generated_at
```

---

## 11. Veralogix Mining (Pty) Ltd — `veralogix-mining` — EMPTY · confirm scope

```text
Research Veralogix Mining (Pty) Ltd. Registry: confirm exact service scope (contract mining vs holding vs owner-operator).

Drive + Veralogix Group report (search Drive for Veralogix Group Holdings Middelburg).
JSON: company_profile, confirmed_scope, competitors, commodities, regions, tender_landscape, synergies_with_rentals_plant_salaria, open_questions, sources, generated_at
```

---

## 12. Alpha Industries SA — `alpha-industries-sa` — EMPTY · vs Alpha Technical Solutions

```text
Research Alpha Industries SA and its relationship to Alpha Technical Solutions (crushing/screening/plant).

Drive: are they same trading entity, sister, or brand split?
JSON: company_profile, relationship_to_alpha_technical_solutions, competitors, tender_landscape, opportunity_signals, sources, generated_at
```

---

## 13. Salaria Safety Services — `salaria-safety-services` — EMPTY · vs Mining Safety Services

```text
Research Salaria Safety Services. Registry asks: distinct from Mining Safety Services (MSS)?

Drive: prove overlap or separation (training vs audits vs PPE vs emergency response).
JSON: company_profile, distinction_from_mining_safety_services, competitors, regulatory_watchlist, tender_landscape, sources, generated_at
```

---

## 14. YAL.ai — `yal-ai` — EMPTY · product/SaaS schema

```text
Research YAL.ai (AI anti-phishing / cybersecurity product under Veralogix technology vertical).

This is PRODUCT/SaaS intelligence, not classic mining services.

JSON keys:
company_profile,
product_overview,
target_segments (mining/industrial/enterprise SA),
competitors_sa_and_global,
pricing_signals_if_public,
procurement_channels (SITA, SOE cyber tenders, private RFPs),
regulatory (POPIA, cybercrime act),
gtm_opportunity_signals,
sources, generated_at
```

---

## 15. Veralogix Projects (Pty) Ltd — `veralogix-projects` — corporate vehicle

```text
From Drive only: what does Veralogix Projects (Pty) Ltd do? Project delivery arm vs shell?

Return company_profile + intelligence_profile_recommended (true/false) + evidence sources. If purely corporate vehicle, list documents that prove it and skip deep competitor research.
```

---

## 16. Veralogix Properties (Pty) Ltd — `veralogix-properties` — corporate vehicle

```text
From Drive: property holdings, addresses (e.g. 3A Laver Street Middelburg), leases, related entities.

JSON: company_profile, property_list, intelligence_value (low/medium), sources. No competitor deep-dive unless properties are commercial parks marketed externally.
```

---

## 17. Veralogix Holdings — `veralogix-holdings` — corporate vehicle

```text
Build a GROUP STRUCTURE brief from Drive + any Veralogix Group research reports.

JSON:
{
  "holding_profile": {},
  "subsidiary_map": [{"company":"","role":"","evidence_file":""}],
  "hq": {},
  "open_registry_questions": ["CPM acronym","Vcom vs Bioniq","Alpha Industries vs Technical","Salaria Safety vs MSS","Diesel vs Ritz"],
  "sources": [],
  "generated_at": ""
}
```

---

# Company prompts — P2 / P3 (have intel — Drive enrich + refresh)

For each COMPLETE company below: run **Prompt 0 + Prompt A**, then a short refresh.

## 18. Veramani (IT) — `veramani` — PROMPT_ONLY

**Save:** `Companys Information/Veramani/IT Division/market_intelligence.json`

```text
Normalize Veramani IT intelligence into market_intelligence.json.
Context: IT holding / software, web, connectivity for mining & industrial SA.
Keys: company_profile, competitors, demand_signals, tender_landscape, seo_opportunities, technology_trends, relationship_to_bioniq_vcom_yal, sources, generated_at
Use Drive folder Research/Veramani* if present.
```

---

## 19–32. COMPLETE entities — short refresh pack

Run this once per company (replace names). Existing `market_intelligence.json` may exist — ask Gemini to **merge, not wipe**.

| # | Company | company_id | Folder under Companys Information |
| --- | --- | --- | --- |
| 19 | Alpha Technical Solutions | alpha-technical-solutions | `Veralogix Group/Alpha/Technical Solutions/` |
| 20 | Coal Processors International | coal-processors-international | `Veralogix Group/Coal Processors International/` |
| 21 | Endeto Project Services | endeto-project-services | `Veralogix Group/Endeto Project Services/` |
| 22 | Veralogix Plant (Woestalleen) | veralogix-plant | `Veralogix Group/Veralogix Plant (Woestalleen)/` |
| 23 | Veralift | veralift | `Veralogix Group/Veralift/` |
| 24 | Treadstone Logistics | treadstone | `Treadstone/Logistics/` |
| 25 | Vera-Commodities | vera-commodities | `Commodities & Trading/Vera-Commodities/` |
| 26 | Ritz International | ritz-international | `Commodities & Trading/Ritz International/` |
| 27 | Mining Safety Services | mining-safety-services | `Salaria/Mining Safety Services/` |
| 28 | Pencox Auto Air | pencox-auto-air | `Equipment & Fleet/Pencox Auto Air/` |
| 29 | Bioniq | bioniq | `Veramani/Bioniq (ISP)/` |
| 30 | Vcom | vcom | `Veramani/Vcom/` |

**Refresh prompt:**

```text
Company: {{DISPLAY_NAME}} ({{COMPANY_ID}}), Veralogix Group, South Africa.

1) Search my Google Drive for newer facts (fleet, licences, clients, addresses).
2) Update company_profile (Prompt A schema) with evidence.
3) Refresh market intelligence sections appropriate to this business (competitors, tenders, regulation, opportunity signals).
4) Return JSON with: company_profile, market_intelligence, what_changed, sources, generated_at.
5) Do not delete valid prior intel — mark superseded claims in what_changed.
```

**Extra for Bioniq/Vcom:**

```text
Also answer explicitly: how do Bioniq (ISP/hotspots) and Vcom (aerial fibre FNO) relate commercially (sister, supplier, competitor, shared clients)? Evidence from Drive first.
```

---

# Cross-portfolio prompts (Gemini)

## CP-1 — Fill empty company_profile stubs

```text
I have ~27 Veralogix operating companies whose company_profile.json fields are mostly empty (description, website, regions, CIPC, BBBEE). Using Google Drive across the whole Geologix/Veralogix corpus, produce a CSV-like JSON array:

[{"company_id":"","display_name":"","description":"","website":null,"operating_regions":[],"confidence":"","best_source_file":""}]

Only include fields you can evidence. Skip TBD pharma.
```

## CP-2 — Resolve open registry questions

```text
Using Google Drive evidence, answer these open questions from company_registry.json:
1) What does Tread Stone CPM stand for / do?
2) Exact relationship Vcom vs Bioniq?
3) Scope of Aiguille Tools & Edges?
4) Alpha Industries SA vs Alpha Technical Solutions?
5) Salaria Safety Services vs Mining Safety Services?
6) Veralogix Diesel vs Ritz International?

Return JSON keyed by question with answer, confidence, evidence_files[].
```

## CP-3 — Signal routing validation (PROMPT B)

```text
Given Veralogix companies [paste list], validate and improve signal routing for these 10 signals:
[paste CROSS-PORTFOLIO/PROMPT B.md signals 1–10]

For each signal return affected_companies, opportunity_per_company, urgency, recommended_action_48h, drive_evidence_if_any.
JSON only.
```

---

## Tracking checklist

| company_id | Prompt 0 | Profile A | Market intel | Saved to Companys Information | Saved to KB profile |
| --- | --- | --- | --- | --- | --- |
| salaria-mining-services | ☐ | ☐ | ☐ | ☐ | ☐ |
| veralogix-rentals | ☐ | ☐ | ☐ | ☐ | ☐ |
| io-green | ☐ | ☐ | ☐ | ☐ | ☐ |
| aiguille-security | ☐ | ☐ | ☐ | ☐ | ☐ |
| aiguille-tools-edges | ☐ | ☐ | ☐ | ☐ | ☐ |
| cg-transport | ☐ | ☐ | ☐ | ☐ | ☐ |
| cg-auto-transport | ☐ | ☐ | ☐ | ☐ | ☐ |
| treadstone-cpm | ☐ | ☐ | ☐ | ☐ | ☐ |
| veralogix-diesel | ☐ | ☐ | ☐ | ☐ | ☐ |
| veralogix-drilling-blasting | ☐ | ☐ | ☐ | ☐ | ☐ |
| veralogix-mining | ☐ | ☐ | ☐ | ☐ | ☐ |
| alpha-industries-sa | ☐ | ☐ | ☐ | ☐ | ☐ |
| salaria-safety-services | ☐ | ☐ | ☐ | ☐ | ☐ |
| yal-ai | ☐ | ☐ | ☐ | ☐ | ☐ |
| veramani | ☐ | ☐ | ☐ | ☐ | ☐ |
| veralogix-projects | ☐ | ☐ | — | ☐ | ☐ |
| veralogix-properties | ☐ | ☐ | — | ☐ | ☐ |
| veralogix-holdings | ☐ | ☐ | CP-1/CP-2 | ☐ | ☐ |
| (COMPLETE set 19–30) | ☐ | ☐ | refresh ☐ | ☐ | ☐ |
| tbd-pharma | BLOCKED | BLOCKED | BLOCKED | — | — |

---

## After Gemini returns JSON

1. Validate JSON parses.  
2. Drop into the company folder as `market_intelligence.json` (and keep a dated copy if replacing).  
3. For EMPTY companies, also create `Prompt.md` by adapting the research task text above (so Cursor agents stay consistent).  
4. Update `.project-intel/docs/component-catalog.md` status COMPLETE when both Prompt + market intel exist.  
5. Never commit `K/Q/C/D` sync dumps or sensitive paths Gemini flagged.

---

*Generated by ProjectIntel from registry + Companys Information coverage scan + Geologix Vanguard parent-folder discovery (2026-07-13).*
