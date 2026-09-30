# Soldados vs Zumbis — Beta 4

Este repositório abre diretamente na versão jogável atual. É um jogo de defesa por faixas: escolha tropas, administre suprimentos e detenha os infectados em Nova York, no Deserto e na Cachoeira de Minas Gerais. Cada mapa tem oito cartas e uma campanha de 12 ondas (duas comuns, uma de subchefe e uma de chefe, por ciclo).

## Jogar no Windows 10/11

1. No botão verde **Code**, escolha **Download ZIP**.
2. Aguarde o download completo e **extraia o ZIP inteiro** pelo Explorador do Windows, 7-Zip ou WinRAR. O pacote é grande porque já contém as imagens e os sons; não há outro download de recursos.
3. Abra a pasta extraída e dê dois cliques em **`JOGAR_AGORA_WINDOWS.exe`**, que está nesta mesma pasta do README. Não precisa instalar Python.

Não execute o jogo de dentro do ZIP e não mova o `.exe` sozinho: as pastas de arte e áudio precisam ficar ao lado dele. O executável não é assinado digitalmente; se o Windows pedir confirmação, confira que o arquivo veio deste repositório. Ele foi testado no Windows 11; o Windows 10 ainda precisa de teste em outra máquina.

## Jogar pelo código no macOS ou Linux

Não há executável nativo pronto para esses sistemas. Com Python 3.12 ou mais recente instalado, abra o terminal **na pasta extraída**, ao lado de `main.py`, e rode:

```bash
python3 -m pip install -r requirements.txt
python3 main.py
```

As mesmas instruções servem para quem prefere rodar o código no Windows, substituindo `python3` por `py` quando necessário. macOS e Linux ainda precisam de teste gráfico em computadores reais; o código e os recursos estão no ZIP, mas não prometemos execução com um clique nessas plataformas.

## O que vem no ZIP

`main.py` e os demais `.py` são o jogo; `assets/`, `CENARIOS_BETA4_CONCEITOS/`, `PIXEL_ART_SPRITES_BETA4/` e `PROTOTIPO_CARTA_CAMPO/` guardam os recursos que ele usa. `requirements.txt` lista as bibliotecas para rodar pelo código. O jogo usa CPU e memória como caminho padrão, sem exigir placa de vídeo dedicada.

O botão **Code → Download ZIP** entrega **somente a Beta 4 atual**, pronta para abrir no Windows após extrair. Ele não mistura outras Alfas/Betas nem pede para localizar arquivos em outra pasta.

## Versões anteriores e colaboração

As versões de referência, Alfas de correção, Betas anteriores e textos de desenvolvimento estão nos [Releases](https://github.com/vinicius589/soldados-vs-zumbis-beta-3/releases), separados do download principal. O [pacote histórico completo](https://github.com/vinicius589/soldados-vs-zumbis-beta-3/releases/tag/historico-corrigido-2026-09-30) é para consulta e pode exigir Python. A Beta 1 original, feita com desenhos simples, não foi localizada; não apresentamos uma recriação como se fosse o arquivo autêntico.

A Beta 4 é a base para a equipe continuar o projeto. As Alfas registram correções entre marcos de conteúdo, enquanto as Betas marcam as versões ampliadas. Ainda há espaço para refinar arte, som e balanceamento com testes dos colegas e do professor; apontem o mapa, a onda, a unidade e, se possível, uma captura quando acharem um defeito.
