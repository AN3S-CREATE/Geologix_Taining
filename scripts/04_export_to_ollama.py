"""Phase 5: Register merged models with Ollama using Modelfiles."""
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODELS = ROOT / "models"

CHECKS = [
    ("geologix-general-merged", "Geologix.modelfile", "geologix"),
    ("geologix-legal-merged", "GeologixLegal.modelfile", "geologix-legal"),
]


def require_ollama() -> None:
    if shutil.which("ollama") is None:
        print("ERROR: ollama not found on PATH. Install Ollama and restart it first.")
        sys.exit(1)


def merged_looks_ready(path: Path) -> bool:
    if not path.is_dir():
        return False
    # Ignore placeholder .gitkeep-only folders
    return any(p.name != ".gitkeep" for p in path.iterdir())


def main() -> None:
    require_ollama()
    print("=" * 50)
    print("📦  EXPORT: Register Geologix models in Ollama")
    print("=" * 50)

    for folder, modelfile, name in CHECKS:
        merged = MODELS / folder
        mf = MODELS / modelfile
        if not merged_looks_ready(merged):
            print(f"SKIP {name}: missing merged weights at {merged}")
            print("       Train first (02_train_geologix.py / 03_train_geologix_legal.py).")
            continue
        if not mf.is_file():
            print(f"SKIP {name}: missing {mf}")
            continue

        print(f"\nCreating Ollama model: {name}")
        result = subprocess.run(
            ["ollama", "create", name, "-f", str(mf)],
            cwd=str(MODELS),
            check=False,
        )
        if result.returncode != 0:
            print(f"FAILED: ollama create {name}")
            sys.exit(result.returncode)
        print(f"✅ Registered: {name}")

    print("\nCurrent Ollama models:")
    subprocess.run(["ollama", "list"], check=False)


if __name__ == "__main__":
    main()
