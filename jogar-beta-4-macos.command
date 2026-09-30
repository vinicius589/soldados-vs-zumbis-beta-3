#!/bin/bash
project_dir="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
/bin/bash "$project_dir/jogar-beta-4.sh" "$@"
status=$?
if [ "$status" -ne 0 ] && [ -t 0 ]; then
    printf '\nA Beta 4 nao iniciou. Pressione Enter para fechar esta janela.'
    read -r _
fi
exit "$status"
