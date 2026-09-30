#!/usr/bin/env bash
set -euo pipefail

project_dir="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
game_dir="$project_dir/betas/beta-4"
environment_dir="$project_dir/.venv-beta4"

python_cmd=""
for candidate in python3.14 python3.13 python3.12 python3; do
    if command -v "$candidate" >/dev/null 2>&1 &&
        "$candidate" -c 'import sys; raise SystemExit(sys.version_info < (3, 12))' >/dev/null 2>&1; then
        python_cmd="$candidate"
        break
    fi
done
if [ -z "$python_cmd" ]; then
    echo "Python 3.12 ou mais recente nao foi encontrado. Instale-o e tente novamente." >&2
    exit 1
fi

cd "$project_dir"
"$python_cmd" verificar_recursos.py "$game_dir"

if [ ! -x "$environment_dir/bin/python" ] ||
    ! "$environment_dir/bin/python" -m pip --version >/dev/null 2>&1; then
    echo "Preparando o ambiente da Beta 4 (somente na primeira abertura)..."
    if ! "$python_cmd" -m venv "$environment_dir"; then
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
