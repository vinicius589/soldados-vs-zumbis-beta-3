#!/usr/bin/env bash
set -euo pipefail

project_dir="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
game_dir="$project_dir/betas/beta-4"
environment_dir="$project_dir/.venv-beta4"

if ! command -v python3 >/dev/null 2>&1; then
    echo "Python 3.12 ou mais recente nao foi encontrado. Instale-o e tente novamente." >&2
    exit 1
fi

if ! python3 -c 'import sys; raise SystemExit(sys.version_info < (3, 12))'; then
    echo "Este pacote precisa de Python 3.12 ou mais recente." >&2
    exit 1
fi

cd "$project_dir"
python3 verificar_recursos.py "$game_dir"

if [ ! -x "$environment_dir/bin/python" ]; then
    echo "Preparando o ambiente da Beta 4 (somente na primeira abertura)..."
    if ! python3 -m venv "$environment_dir"; then
        echo "Nao foi possivel criar o ambiente Python. No Linux, verifique se python3-venv esta instalado." >&2
        exit 1
    fi
fi

if ! "$environment_dir/bin/python" -c 'import pygame, numpy, OpenGL, PIL' >/dev/null 2>&1; then
    echo "Instalando as bibliotecas da Beta 4 (conexao com a internet necessaria)..."
    "$environment_dir/bin/python" -m pip install --disable-pip-version-check -r "$game_dir/requirements.txt"
fi

cd "$game_dir"
if [ "${1:-}" = "--verificar" ]; then
    exec "$environment_dir/bin/python" smoke_test.py
fi
exec "$environment_dir/bin/python" main.py "$@"
