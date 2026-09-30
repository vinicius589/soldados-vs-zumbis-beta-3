# Soldados vs Zumbis — versões do jogo

## Baixar e jogar a Beta 4

**[BAIXAR SÓ A BETA 4 PARA JOGAR (ZIP)](https://github.com/vinicius589/soldados-vs-zumbis-beta-3/releases/download/historico-corrigido-2026-09-30/soldados-vs-zumbis-beta-4-jogar.zip)** — arquivo publicado na [página de versões e downloads](https://github.com/vinicius589/soldados-vs-zumbis-beta-3/releases/tag/historico-corrigido-2026-09-30), visível para qualquer pessoa. Para consultar todas as Alfas e Betas, há também o [pacote histórico completo](https://github.com/vinicius589/soldados-vs-zumbis-beta-3/releases/download/historico-corrigido-2026-09-30/soldados-vs-zumbis-pacote-jogavel.zip). Extraia o ZIP inteiro antes de abrir o jogo. Não baixe pelo botão verde **Code → Download ZIP**: esse ZIP automático não contém todas as imagens e sons.

| Sistema | Como abrir depois de extrair |
|---|---|
| Windows 10/11 | Instale Python 3.12 ou mais recente; dê dois cliques em `JOGAR_BETA_4.bat`. |
| macOS | Instale Python 3.12 ou mais recente; abra `jogar-beta-4-macos.command`. Se o macOS não permitir abrir pelo Finder, use `bash jogar-beta-4-macos.command` no Terminal, dentro da pasta extraída. |
| Linux | Instale Python 3.12 ou mais recente; no terminal da pasta extraída, execute `bash jogar-beta-4.sh`. Algumas distribuições também exigem o pacote `python3-venv`. |

Os lançadores preparam as bibliotecas automaticamente na primeira abertura, com acesso à internet. O Windows foi testado. A sintaxe dos iniciadores Linux/macOS foi conferida, mas a abertura gráfica nesses sistemas ainda precisa ser confirmada em computadores reais. Não há executável independente de Python para os três sistemas.

Este repositório guarda o jogo **e a evolução dele**, sem espalhar código,
sprites, prompts e relatórios pela página inicial. Se você só quer jogar,
entre em [`betas/`](betas/) e escolha uma versão. Se quer entender o que foi
corrigido entre elas, consulte [`alphas/`](alphas/). Os textos de planejamento
e registros antigos estão separados em [`material-bruto/`](material-bruto/).

## O que é o jogo atual?

*Soldados vs Zumbis* é um jogo de defesa por faixas feito em Python/Pygame.
Você posiciona tropas, gasta suprimentos e impede que os infectados cruzem o
mapa. A **Beta 4** é a versão de trabalho mais recente: tem os cenários de
Nova York (polícia), Egito (militares) e Cachoeira em Minas Gerais (Marinha),
com quatro faixas e oito cartas próprias em cada mapa. Cada campanha tem
12 ondas: duas comuns, uma de subchefe e uma de chefe, repetidas três vezes.
As versões antigas podem ter **15 ondas, cartas e regras diferentes**. Não
copie o `main.py` de uma pasta para outra esperando que as artes coincidam.

## Onde está cada coisa?

```text
alphas/           cinco etapas de criação de sprites e revisão
betas/            Beta 1 documentada; Betas 2, 3 e 4 executáveis
material-bruto/   textos originais, propostas e explicação do que eles são
README.md         este guia
```

Cada versão **preservada** tem seu próprio `README.md`, `requirements.txt`,
`main.py` e `executar.bat`. Também tem `NOTAS_DA_VERSAO.md`, que resume as
mudanças encontradas nos arquivos **daquela** versão. A Beta 1 é a única
exceção: seu código original não foi localizado e não há executável na
pasta. As pastas jogáveis são independentes:
uma Beta não busca imagens ou código dentro de outra Beta ou de uma Alfa.
Arquivos grandes de arte e áudio usam Git LFS.

## Baixar o jogo com as imagens completas

Use o **pacote histórico completo vinculado no começo desta página**. Para jogar uma versão
antiga, extraia o pacote e abra o `executar.bat` da Alfa ou Beta desejada no Windows.
As referências de produção ficam no download separado
**soldados-vs-zumbis-material-bruto.zip**, na mesma página.

**Não use “Code → Download ZIP” nem “Source code (zip)” para jogar.** Esses
arquivos automáticos do GitHub contêm apenas referências de poucos bytes no
lugar das imagens e dos sons guardados em Git LFS. Isso causa o erro
`Unsupported image format` na Beta 4 e na Alfa da Beta 4 e faz as demais
versões mostrarem figuras provisórias (como círculos vermelhos). O pacote
acima inclui os arquivos reais de todas as versões.

## Como abrir uma Beta

1. Instale Python 3.12 ou mais recente e extraia o pacote completo indicado acima. Se preferir
   clonar o repositório como desenvolvedor, instale Git LFS e execute
   `git lfs pull` depois do clone para baixar a arte e o áudio completos.
2. Abra `betas/beta-2/`, `beta-3/` ou `beta-4/`. A Beta 1 original não está
   disponível para execução porque seu arquivo não foi localizado.
3. No Windows, dê dois cliques no **`executar.bat` dentro da pasta escolhida**.
   Não use um lançador de outra versão.

Se preferir o terminal, entre na pasta da Beta e rode:

```powershell
python -m pip install -r requirements.txt
python main.py
```

A Beta 4 usa renderização por CPU/RAM como padrão; uma placa de vídeo
dedicada não é exigida. O áudio e os controles de teclado podem ser ajustados
no menu do jogo. Para as regras e comandos próprios da versão atual, leia
[`betas/beta-4/README.md`](betas/beta-4/README.md).

## Por que há Alfas e Betas separadas?

Esta classificação foi corrigida conforme a identificação feita pelo autor
em 30/09/2026. **Beta** é o marco de conteúdo aprovado; **Alfa** é a etapa de
criação ou correção ligada à respectiva Beta. Os números internos `v6`, `v7.4`
e `v7.5` identificam pacotes técnicos e não determinam o nome histórico da
Beta. A primeira Beta tinha personagens e faixas desenhados com formas
simples, sem sprites; seu arquivo original não está neste acervo. Não foi
substituído por uma recriação apresentada como autêntica.

| Etapa identificada | Arquivo preservado | Papel no acervo |
|---|---|---|
| [Beta 1](betas/beta-1/) | Original não localizado | Primeiro jogo de desenhos simples descrito pelo autor. A pasta contém apenas esta informação, sem código inventado. |
| [Alfa inicial](alphas/alfa-inicial/) | Executável | Início do trabalho com sprites após a Beta 1. É a primeira base com arte preservada, não o primeiro jogo. |
| [Beta 2](betas/beta-2/) | Executável | Antiga pasta chamada “Beta 1”: abertura, carregamento de recursos e consulta de personagens no menu. |
| [Alfa da Beta 2](alphas/alfa-beta-2/) | Executável | Revisão v7.1 das arenas e da estabilidade dos efeitos. |
| [Alfa da Beta 3 — v7.4](alphas/alfa-beta-3-v7-4/) | Executável | Antiga pasta chamada “Beta 2”: evolução N1/N2, Sargento, contenções e interface. Classificada pelo autor como Alfa de correção da Beta 3. |
| [Alfa da Beta 3 — v7.5](alphas/alfa-beta-3-v7-5/) | Executável | Minas isoladas e redução de dificuldade excessiva. |
| [Beta 3](betas/beta-3/) | Executável | Recursos regionais e modos de dificuldade. |
| [Alfa da Beta 4](alphas/alfa-beta-4/) | Executável | Revisão de animações, controles, áudio e balanceamento antes da Beta 4. |
| [Beta 4](betas/beta-4/) | Executável | Campanha de 12 ondas, quatro faixas, oito cartas por mapa, áudio e animações integradas. |

Para detalhes de uma etapa, abra **`NOTAS_DA_VERSAO.md` na própria pasta**.
As Alfas também mantêm código executável para comparação, mas não são a
linha em que a equipe deve desenvolver novas funções.

## O que é “material bruto”?

[`material-bruto/`](material-bruto/) guarda os textos originais de elenco,
história, prompts de arte, relatórios de revisão, planejamento e dúvidas.
Eles explicam como o projeto chegou aqui; **não são uma segunda lista de
requisitos atuais**. Alguns falam em cartas descartadas, seleção de três
cartas, 15 ondas ou números de suprimentos antigos. A explicação por tipo
de documento e as perguntas ainda abertas estão no README daquela pasta.

## Situação da entrega

Em 30/09/2026, `betas/beta-4/` passou em **122 testes automatizados** e na
checagem de inicialização numa cópia limpa do repositório. As outras sete
pastas executáveis também passaram em suas checagens básicas de inicialização. Isso
confirma que o pacote carrega; **não comprova** que todas as ondas são
vencíveis nem que cada animação foi aprovada visualmente. Os pontos de
revisão para a equipe estão em
[`material-bruto/textos/PENDENCIAS_PARA_EQUIPE.md`](material-bruto/textos/PENDENCIAS_PARA_EQUIPE.md).
