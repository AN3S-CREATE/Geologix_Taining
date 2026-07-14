"""
P0–P3 scaffolding: ingest Veralogix company information into Geologix AI context pack.

Source: data/veralogix_companys_information/
Output: data/company_context/
"""
from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "veralogix_companys_information"
OUT = ROOT / "data" / "company_context"

SKIP_DIRS = {
    ".git",
    ".index",
    ".claude",
    ".project-intel",
    ".vscode",
    "_research_archive",
}

PROCESS_TYPES = [
    {
        "id": "PROC-ID",
        "name": "Identity / introduction",
        "purpose": "Introduce Geologix AI or a subsidiary in Group voice",
    },
    {
        "id": "PROC-ROUTE",
        "name": "Single-subsidiary routing",
        "purpose": "Send a query to the correct company and explain why",
    },
    {
        "id": "PROC-XPORT",
        "name": "Cross-portfolio coordination",
        "purpose": "Expand a market/ops trigger into a multi-entity action chain",
    },
    {
        "id": "PROC-SOP",
        "name": "Operating procedure",
        "purpose": "Describe standard response or escalation (non-confidential)",
    },
    {
        "id": "PROC-OFFER",
        "name": "Capability brief",
        "purpose": "Explain what the subsidiary sells or delivers",
    },
    {
        "id": "PROC-RISK",
        "name": "Risk & compliance handoff",
        "purpose": "Flag MHSA / POPIA / environmental / security handoffs",
    },
]


def load_json(path: Path):
    with path.open(encoding="utf-8-sig") as f:
        return json.load(f)


def extract_company_context_block(prompt_md: str) -> str:
    """Pull COMPANY CONTEXT section from Prompt.md research briefs."""
    if not prompt_md:
        return ""
    match = re.search(
        r"COMPANY CONTEXT:\s*(.*?)(?:\n\s*RESEARCH TASK|\n\s*SUBSIDIARY MAP:|\Z)",
        prompt_md,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if match:
        return re.sub(r"\s+", " ", match.group(1)).strip()
    # Fallback: first non-empty paragraph after the opener
    lines = [ln.strip() for ln in prompt_md.splitlines() if ln.strip()]
    return " ".join(lines[1:4])[:800] if len(lines) > 1 else ""


def readiness_bucket(status: str) -> str:
    status = (status or "unknown").lower()
    if status in {"complete", "complete_chunked"}:
        return "layer_b_and_c"
    if status in {"prompt_plus_docs", "chunked_from_docs"}:
        return "layer_a_and_c_review_b"
    if status in {"prompt_only"}:
        return "layer_a_stub"
    return "review"


def collect_companies(portfolio: dict) -> list[dict]:
    by_folder = {c["folder"]: c for c in portfolio.get("companies", [])}
    companies = []

    for folder in sorted(p.name for p in SOURCE.iterdir() if p.is_dir()):
        if folder in SKIP_DIRS or folder == "CROSS-PORTFOLIO":
            continue
        company_dir = SOURCE / folder
        index_path = company_dir / "index.json"
        prompt_path = company_dir / "Prompt.md"
        mi_path = company_dir / "market_intelligence.json"
        manifest_path = company_dir / "chunks_manifest.json"

        portfolio_row = by_folder.get(folder, {})
        index = load_json(index_path) if index_path.exists() else {}
        prompt_text = prompt_path.read_text(encoding="utf-8", errors="replace") if prompt_path.exists() else ""

        chunk_count = 0
        if manifest_path.exists():
            try:
                manifest = load_json(manifest_path)
                if isinstance(manifest, dict):
                    chunk_count = len(manifest.get("chunks") or manifest.get("files") or [])
                elif isinstance(manifest, list):
                    chunk_count = len(manifest)
            except json.JSONDecodeError:
                chunk_count = 0

        sectional = sorted(
            p.name
            for p in company_dir.glob("*.json")
            if re.match(r"^\d{2}_", p.name) or p.name.startswith("doc")
        )

        data_status = (
            index.get("data_status")
            or portfolio_row.get("data_status")
            or ("complete" if mi_path.exists() else "prompt_only")
        )

        record = {
            "folder": folder,
            "display_name": index.get("display_name") or portfolio_row.get("display_name") or folder,
            "group": index.get("group") or portfolio_row.get("group") or "Unassigned",
            "sector": index.get("sector") or portfolio_row.get("sector") or "",
            "hq": index.get("hq") or portfolio_row.get("hq") or "",
            "description": index.get("description") or "",
            "company_context": extract_company_context_block(prompt_text),
            "related_companies": index.get("related_companies") or [],
            "data_status": data_status,
            "readiness": readiness_bucket(data_status),
            "has_prompt": prompt_path.exists(),
            "has_index": index_path.exists(),
            "has_market_intelligence": mi_path.exists(),
            "chunk_files_count": chunk_count or index.get("file_summary", {}).get("chunk_files_count", 0),
            "sectional_json_files": sectional,
            "ai_read_order": index.get("ai_read_order")
            or [
                "1. index.json",
                "2. chunks_manifest.json / market_intelligence.json",
                "3. sectional / doc chunk JSON",
                "4. Prompt.md",
            ],
            "source_path": str(company_dir.relative_to(ROOT)).replace("\\", "/"),
        }
        companies.append(record)

    return companies


def build_identity(companies: list[dict], portfolio: dict, group_index: dict) -> dict:
    groups: dict[str, list[str]] = {}
    for c in companies:
        groups.setdefault(c["group"], []).append(c["display_name"])

    return {
        "assistant_name": "Geologix AI",
        "owner": "Veralogix Group (Geologix Vanguard portfolio)",
        "role": (
            "Unified internal intelligence system for Veralogix Group and affiliated "
            "portfolio companies. Routes queries, coordinates cross-subsidiary work, "
            "and answers from company knowledge with source attribution when retrieved."
        ),
        "hq": group_index.get("hq") or "Middelburg, Mpumalanga, South Africa",
        "holding_vehicle": "Veralogix Mining (Pty) Ltd",
        "portfolio_label": portfolio.get("portfolio", "Geologix Vanguard — Veralogix Group Portfolio"),
        "company_count": len(companies),
        "groups": {g: sorted(names) for g, names in sorted(groups.items())},
        "operating_principles": [
            "Modular, scalable, and ROI-driven",
            "Route to the correct subsidiary; never answer in isolation when dependencies exist",
            "Cite sources when using retrieved market or company intelligence",
            "Strategic decisions remain with human leadership",
            "Keep confidential live matters out of fine-tuned weights; use RAG for current memory",
        ],
        "voice": (
            "Professional South African mining-services Group voice: clear, operational, "
            "coordination-aware, and concise. Prefer subsidiary names as used in the registry."
        ),
        "system_prompt_draft": (
            "You are Geologix AI, the unified internal intelligence system for Veralogix Group "
            f"and the Geologix Vanguard portfolio ({len(companies)} companies). "
            "Headquarters: Middelburg, Mpumalanga, South Africa. "
            "Holding vehicle: Veralogix Mining (Pty) Ltd. "
            "You route queries to the correct subsidiary expertise, surface cross-portfolio "
            "dependencies, and remain modular, scalable, and ROI-driven. "
            "Cite sources when available. Strategic decisions remain with human leadership."
        ),
        "as_of": str(date.today()),
    }


def build_xport_process_templates(triggers: list[dict]) -> list[dict]:
    templates = []
    for t in triggers:
        event = t.get("event", "").strip()
        companies = t.get("triggered_companies") or []
        if not event or not companies:
            continue
        lead = companies[0]
        support = companies[1:]
        templates.append(
            {
                "process_id": "PROC-XPORT",
                "event": event,
                "lead_subsidiary": lead,
                "supporting_subsidiaries": support,
                "instruction_template": (
                    f"Route this Group opportunity/event and list required subsidiary coordination: '{event}'."
                ),
                "output_guidance": (
                    f"Lead: {lead}. Engage: {', '.join(companies)}. "
                    "Explain why each is triggered and recommend a joint planning window."
                ),
                "status": "template_ready_for_human_or_generator_fill",
            }
        )
    return templates


def build_route_templates(companies: list[dict]) -> list[dict]:
    templates = []
    for c in companies:
        if c["readiness"] == "layer_a_stub":
            continue
        templates.append(
            {
                "process_id": "PROC-ROUTE",
                "company": c["display_name"],
                "group": c["group"],
                "sector": c["sector"],
                "instruction_template": (
                    f"A user asks for help related to {c['sector']}. "
                    f"Route to the correct Veralogix portfolio company and explain the handoff."
                ),
                "output_guidance": (
                    f"Primary: {c['display_name']} ({c['group']}). "
                    f"Sector: {c['sector']}. HQ: {c['hq'] or 'South Africa'}. "
                    f"Related: {', '.join(c['related_companies'][:5]) or 'see registry'}."
                ),
                "readiness": c["readiness"],
                "status": "template_ready_for_human_or_generator_fill",
            }
        )
    return templates


def main() -> None:
    if not SOURCE.exists():
        raise SystemExit(f"Missing source folder: {SOURCE}")

    OUT.mkdir(parents=True, exist_ok=True)

    portfolio = load_json(SOURCE / "portfolio_index.json")
    companies = collect_companies(portfolio)

    group_index = {}
    group_index_path = SOURCE / "Veralogix Group" / "index.json"
    if group_index_path.exists():
        group_index = load_json(group_index_path)

    identity = build_identity(companies, portfolio, group_index)

    cross_path = SOURCE / "CROSS-PORTFOLIO" / "index.json"
    cross = load_json(cross_path) if cross_path.exists() else {}
    triggers = cross.get("cross_portfolio_triggers") or []

    xport_templates = build_xport_process_templates(triggers)
    route_templates = build_route_templates(companies)

    registry = {
        "as_of": str(date.today()),
        "source": "data/veralogix_companys_information",
        "portfolio": portfolio.get("portfolio"),
        "company_count": len(companies),
        "companies": companies,
    }

    triggers_out = {
        "as_of": str(date.today()),
        "source": "data/veralogix_companys_information/CROSS-PORTFOLIO/index.json",
        "description": cross.get("description"),
        "purpose": cross.get("purpose"),
        "triggers": triggers,
        "process_templates": xport_templates,
    }

    readiness_counts: dict[str, int] = {}
    for c in companies:
        readiness_counts[c["readiness"]] = readiness_counts.get(c["readiness"], 0) + 1

    manifest = {
        "as_of": str(date.today()),
        "assistant": "Geologix AI",
        "process_doc": "docs/geologix-ai-company-context-process.md",
        "ingest_script": "scripts/00_ingest_company_context.py",
        "layers": {
            "A_identity": "data/company_context/geologix_identity.json",
            "B_soul_seed": "data/geologix-core-training.json (curated) → merge to data/geologix_core_training.json",
            "C_rag_source": "data/veralogix_companys_information/** (not vaulted in this phase)",
        },
        "process_types": PROCESS_TYPES,
        "readiness_counts": readiness_counts,
        "counts": {
            "companies_in_registry": len(companies),
            "portfolio_index_rows": len(portfolio.get("companies", [])),
            "cross_portfolio_triggers": len(triggers),
            "proc_xport_templates": len(xport_templates),
            "proc_route_templates": len(route_templates),
        },
        "next_steps": [
            "Review geologix_identity.json and update models/Geologix.modelfile SYSTEM block",
            "Fill PROC-ROUTE / PROC-XPORT templates into Alpaca pairs",
            "Append reviewed pairs into data/geologix_core_training.json",
            "Later: build company RAG vault (P4) separate from legal vault",
        ],
    }

    process_queue = {
        "as_of": str(date.today()),
        "description": "Learning/training process queue derived from company information pack",
        "process_types": PROCESS_TYPES,
        "identity_process": {
            "process_id": "PROC-ID",
            "instruction_template": (
                "As Geologix AI, introduce yourself to a new Group executive and explain "
                "how you serve the Veralogix / Geologix Vanguard portfolio."
            ),
            "uses": "geologix_identity.json",
        },
        "route_templates": route_templates,
        "cross_portfolio_templates": xport_templates,
    }

    outputs = {
        "company_registry.json": registry,
        "geologix_identity.json": identity,
        "cross_portfolio_triggers.json": triggers_out,
        "training_process_manifest.json": manifest,
        "learning_process_queue.json": process_queue,
    }

    for name, payload in outputs.items():
        path = OUT / name
        with path.open("w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print(f"Wrote {path.relative_to(ROOT)} ({_count_hint(payload)})")

    print("\nIngest complete.")
    print(f"Companies: {len(companies)}")
    print(f"Readiness: {readiness_counts}")
    print(f"XPORT templates: {len(xport_templates)} | ROUTE templates: {len(route_templates)}")


def _count_hint(payload) -> str:
    if isinstance(payload, dict):
        if "companies" in payload and isinstance(payload["companies"], list):
            return f"{len(payload['companies'])} companies"
        if "triggers" in payload and isinstance(payload["triggers"], list):
            return f"{len(payload['triggers'])} triggers"
        if "route_templates" in payload:
            return (
                f"{len(payload.get('route_templates', []))} route + "
                f"{len(payload.get('cross_portfolio_templates', []))} xport templates"
            )
    return "ok"


if __name__ == "__main__":
    main()
