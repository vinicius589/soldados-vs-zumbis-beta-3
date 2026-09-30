"""Encontra as artes compartilhadas pelo jogo-fonte e pelos executaveis nativos."""

from pathlib import Path
import sys


def game_root() -> Path:
    source = Path(__file__).resolve().parent
    if not getattr(sys, "frozen", False):
        return source

    executable = Path(sys.executable).resolve()
    for parent in executable.parents:
        candidate = parent / "betas" / "beta-4"
        if (candidate / "assets" / "v7").is_dir():
            return candidate

    bundled = Path(getattr(sys, "_MEIPASS", source))
    if (bundled / "assets" / "v7").is_dir():
        return bundled
    raise FileNotFoundError(
        "Artes da Beta 4 nao encontradas. Extraia o ZIP completo antes de abrir o jogo."
    )
