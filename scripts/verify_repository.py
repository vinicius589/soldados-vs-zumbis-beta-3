"""Verificações rápidas de higiene e estrutura do repositório."""
from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = (
    "README.md",
    "LICENSE",
    "pyproject.toml",
    "run.py",
    "src/main.py",
    "tests/conftest.py",
    ".github/workflows/ci.yml",
    ".github/workflows/release.yml",
)
FORBIDDEN_PARTS = {"__pycache__", ".pytest_cache", ".ruff_cache", ".venv"}
FORBIDDEN_SUFFIXES = {".pyc", ".pyo"}


def tracked_files() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files"], cwd=ROOT, check=True, capture_output=True, text=True
    )
    return result.stdout.splitlines()


def main() -> None:
    missing = [path for path in REQUIRED if not (ROOT / path).is_file()]
    tracked = tracked_files()
    dirty = [
        path
        for path in tracked
        if any(part in Path(path).parts for part in FORBIDDEN_PARTS)
        or Path(path).suffix.lower() in FORBIDDEN_SUFFIXES
    ]
    if missing or dirty:
        if missing:
            print("Arquivos obrigatórios ausentes:")
            print("\n".join(f"- {path}" for path in missing))
        if dirty:
            print("Arquivos gerados indevidos versionados:")
            print("\n".join(f"- {path}" for path in dirty))
        raise SystemExit(1)
    print(f"estrutura válida: {len(tracked)} arquivos versionados")


if __name__ == "__main__":
    main()
