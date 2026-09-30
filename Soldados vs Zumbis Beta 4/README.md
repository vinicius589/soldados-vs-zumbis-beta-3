# Soldados vs Zumbis Beta 4

Esta pasta contém a versão atual do jogo, as imagens e os sons usados por ela.
**Extraia a pasta inteira antes de jogar.** Não mova somente o executável.

## Windows 10/11

Dê dois cliques em `JOGAR_AGORA_WINDOWS.exe`. Não precisa instalar Python.
O executável não tem assinatura digital, então o Windows pode pedir uma
confirmação de segurança. Verifique que o arquivo veio deste repositório.

## macOS e Linux

Não há executável nativo para esses sistemas. Instale Python 3.12 ou mais
recente, abra um terminal nesta pasta e execute:

```bash
python3 -m pip install -r requirements.txt
python3 main.py
```

Em algumas distribuições Linux, instale também o suporte a `venv`/`pip` do
sistema. A abertura gráfica nesses sistemas ainda precisa de teste em máquinas
reais.

## Arquivos principais

- `main.py` e os outros arquivos `.py`: código do jogo.
- `assets/`, `CENARIOS_BETA4_CONCEITOS/`, `PIXEL_ART_SPRITES_BETA4/` e
  `PROTOTIPO_CARTA_CAMPO/`: imagens e sons necessários.
- `requirements.txt`: bibliotecas para executar pelo código-fonte.

O progresso do executável Windows é salvo na pasta de dados do usuário.
