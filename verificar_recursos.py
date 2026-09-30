"""Impede que os lancadores abram um ZIP do GitHub sem os arquivos Git LFS."""

from pathlib import Path
import sys


EXTENSOES = {".png", ".jpg", ".jpeg", ".gif", ".wav", ".ogg"}
ASSINATURA_LFS = b"version https://git-lfs.github.com/spec/v1"


def encontrar_atalhos(pasta: Path) -> list[Path]:
    atalhos = []
    for caminho in pasta.rglob("*"):
        if not caminho.is_file() or caminho.suffix.lower() not in EXTENSOES:
            continue
        with caminho.open("rb") as arquivo:
            if arquivo.read(len(ASSINATURA_LFS)) == ASSINATURA_LFS:
                atalhos.append(caminho)
    return atalhos


def main() -> int:
    pasta = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    atalhos = encontrar_atalhos(pasta)
    if not atalhos:
        return 0

    print("\nERRO: este pacote nao contem as imagens e os sons completos.")
    print(f"Foram encontrados {len(atalhos)} arquivos que sao apenas atalhos do Git LFS.")
    print(f"Exemplo: {atalhos[0].relative_to(pasta)}")
    print("Baixe 'soldados-vs-zumbis-pacote-completo.zip' em:")
    print("https://github.com/vinicius589/soldados-vs-zumbis-beta-3/releases/tag/pacote-completo-2026-09-30")
    print("O botao 'Code > Download ZIP' nao serve para jogar este projeto.\n")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
