# Projeto Soldados vs Zumbis — jogar e consultar as versões

## Jogar agora — Windows 10/11

1. Clique no botão verde **Code → Download ZIP** nesta página.
2. Extraia **o ZIP inteiro** pelo Windows, 7-Zip ou WinRAR. Não abra o jogo de dentro do ZIP.
3. Na pasta extraída, dê dois cliques em **`JOGAR_AGORA_WINDOWS.exe`**. Não é necessário instalar Python ou bibliotecas, nem baixar as artes na primeira abertura.

O executável é da **Beta 4** e procura as imagens e os sons em `betas/beta-4/` dentro da mesma pasta extraída. Não mova apenas o `.exe` para a área de trabalho. O jogo salva o progresso na pasta de dados local do usuário, não dentro do ZIP. O executável não é assinado digitalmente; o Windows pode mostrar um aviso de segurança. Confira que o arquivo veio deste repositório antes de permitir a abertura. A inicialização e o carregamento de recursos foram testados no Windows 11; Windows 10 ainda precisa de confirmação em outro computador.

O GitHub está configurado para **incluir os arquivos Git LFS no Download ZIP**, por isso esse download será grande. O uso desses arquivos consome a franquia de tráfego Git LFS do proprietário do repositório; em caso de limite atingido, use o [pacote da Beta 4 nos Releases](https://github.com/vinicius589/soldados-vs-zumbis-beta-3/releases/download/historico-corrigido-2026-09-30/soldados-vs-zumbis-beta-4-jogar.zip) como alternativa, observando que esse pacote histórico exige Python.

### macOS e Linux

O código está disponível nas mesmas pastas, mas **não há executável nativo pronto** para esses sistemas. Instale Python 3.12 ou mais recente, extraia o ZIP completo e use `bash jogar-beta-4-macos.command` no Terminal do macOS ou `bash jogar-beta-4.sh` no terminal Linux, a partir da raiz do projeto. Esses iniciadores instalam as bibliotecas na primeira execução; pode ser necessário instalar `python3-venv` no Linux. O código é multiplataforma, mas a execução gráfica ainda precisa ser testada nesses sistemas.

Para comparar as versões antigas e consultar as Alfas, use as pastas `alphas/` e `betas/` ou a [página de versões e downloads](https://github.com/vinicius589/soldados-vs-zumbis-beta-3/releases/tag/historico-corrigido-2026-09-30).

Este repositório guarda o jogo **e a evolução dele**, sem espalhar código,
sprites, prompts e relatórios pela página inicial. Para comparar versões
antigas, entre em [`betas/`](betas/) e escolha uma versão. Se quer entender o que foi
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

## Arquivos e versões anteriores

O **Code → Download ZIP** agora deve incluir as artes reais de todas as pastas,
pois a opção de inclusão de Git LFS foi ativada no repositório. Para consultar
versões antigas, abra o `executar.bat` na pasta da versão desejada, após
instalar Python. O [pacote histórico completo](https://github.com/vinicius589/soldados-vs-zumbis-beta-3/releases/download/historico-corrigido-2026-09-30/soldados-vs-zumbis-pacote-jogavel.zip)
e os textos brutos continuam disponíveis nos Releases. A Beta 1 original não
foi localizada; sua pasta é apenas documental.

## Como abrir uma Beta

1. Instale Python 3.12 ou mais recente e extraia o ZIP completo. Se preferir
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
