"""Cria um ZIP jogavel sem as Alfas, Betas antigas e material de producao."""

from __future__ import annotations

import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


GAME_DIR = Path(__file__).resolve().parents[1]
REPO_DIR = GAME_DIR.parents[1]
ASSET_DIRS = (
    "assets",
    "CENARIOS_BETA4_CONCEITOS",
    "PIXEL_ART_SPRITES_BETA4",
    "PROTOTIPO_CARTA_CAMPO",
)
MEDIA_SUFFIXES = {".png", ".wav"}


def main(output: Path) -> None:
    launcher = REPO_DIR / "JOGAR_AGORA_WINDOWS.exe"
    if not launcher.is_file():
        raise FileNotFoundError(launcher)

    media = sorted(
        path
        for name in ASSET_DIRS
        for path in (GAME_DIR / name).rglob("*")
        if path.is_file() and path.suffix.lower() in MEDIA_SUFFIXES
    )
    if len(media) < 500:
        raise RuntimeError(f"Pacote incompleto: apenas {len(media)} imagens/sons")
    for path in media:
        with path.open("rb") as handle:
            if handle.read(32).startswith(b"version https://git-lfs"):
                raise RuntimeError(f"Arquivo LFS nao baixado: {path}")

    output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(output, "w", compression=ZIP_DEFLATED, compresslevel=6) as archive:
        archive.write(launcher, "JOGAR_AGORA_WINDOWS.exe")
        archive.writestr(
            "LEIA_ME_PRIMEIRO.txt",
            "Soldados vs Zumbis - Beta 4 para Windows 10/11\n\n"
            "1. Extraia o ZIP inteiro (nao execute de dentro do ZIP).\n"
            "2. Abra JOGAR_AGORA_WINDOWS.exe nesta pasta.\n"
            "3. Nao mova somente o EXE: a pasta betas/beta-4 guarda as artes e sons.\n\n"
            "Nao exige Python nem download adicional. O EXE nao tem assinatura digital;\n"
            "o Windows pode pedir confirmacao ao abrir.\n",
        )
        for path in media:
            archive.write(path, path.relative_to(REPO_DIR).as_posix())
    print(f"{output} - {len(media)} imagens/sons - {output.stat().st_size / 1_000_000:.1f} MB")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Uso: python empacotar_windows.py CAMINHO_DO_ZIP")
    main(Path(sys.argv[1]).resolve())
