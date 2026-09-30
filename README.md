# Soldados vs Zumbis — versões do jogo

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
alphas/           código e arte das quatro etapas de referência/correção
betas/            Beta 1, 2, 3 e 4; cada uma abre por seu executar.bat
material-bruto/   textos originais, propostas e explicação do que eles são
README.md         este guia
```

Cada versão tem seu próprio `README.md`, `requirements.txt`, `main.py` e
`executar.bat`. Também tem `NOTAS_DA_VERSAO.md`, que resume as mudanças
encontradas nos arquivos **daquela** versão. As pastas são independentes:
uma Beta não busca imagens ou código dentro de outra Beta ou de uma Alfa.
Arquivos grandes de arte e áudio usam Git LFS.

## Como abrir uma Beta

1. Instale Python 3 e Git LFS. Depois de clonar o repositório, execute
   `git lfs pull` para baixar a arte e o áudio completos.
2. Abra `betas/beta-1/`, `beta-2/`, `beta-3/` ou `beta-4/`.
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

O critério pedido pelo autor é: **Beta** marca uma versão com conteúdo ou
funções acrescentados; **Alfa** registra a base inicial ou uma etapa de
correções. Isso organiza a consulta, mas não apaga as misturas reais dos
pacotes antigos: algumas Betas também corrigiram bugs, e a revisão depois
da Beta 3 já tinha parte do conteúdo da Beta 4. As notas apontam essas
ressalvas em vez de inventar uma cronologia perfeita.

| Ordem | Etapa | O que mudou e por que a pasta existe |
|---:|---|---|
| 1 | [Alfa inicial](alphas/alfa-inicial/) | Primeira base preservada: três regiões e campanha de 15 ondas. Serve para comparação. Não há versão anterior disponível que comprove correções específicas nela. |
| 2 | [Beta 1](betas/beta-1/) | Acrescentou abertura, carregamento prévio de recursos e consulta de soldados e zumbis no menu. É jogável sem depender da Alfa. |
| 3 | [Alfa após Beta 1](alphas/alfa-pos-beta-1/) | A reconstrução v7.1 reposicionou Cidade e Praia sobre terreno jogável e corrigiu um travamento ligado a efeitos de projéteis. A mudança de base foi maior que um patch pequeno. |
| 4 | [Beta 2](betas/beta-2/) | Reuniu faixas e contenções por cenário, interface/pausa e evolução visual N1→N2 com Sargento de Promoção. Ainda usa campanha de 15 ondas. |
| 5 | [Alfa após Beta 2](alphas/alfa-pos-beta-2/) | Separou as minas de objetos indevidos, restringiu minas de pressão ao terreno correto e reduziu a parede de dificuldade de chefes e resistentes. |
| 6 | [Beta 3](betas/beta-3/) | Ampliou recursos regionais, armas de água/veneno/fogo e a escolha de Fácil, Médio ou Difícil; também consolidou correções de animação e cartas. |
| 7 | [Alfa após Beta 3](alphas/alfa-pos-beta-3/) | Guarda o snapshot de revisão anterior ao fechamento atual. Embora aqui sirva como referência de correções, o arquivo original dizia “Beta 4” e já tinha adições; não é prova de uma fase só corretiva. |
| 8 | [Beta 4](betas/beta-4/) | Versão atual com 12 ondas, quatro faixas, 24 cartas regionais (oito por mapa), áudio, controles e sistema de animações/counters integrado. É a pasta para a equipe continuar o trabalho. |

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
pastas também passaram em suas checagens básicas de inicialização. Isso
confirma que o pacote carrega; **não comprova** que todas as ondas são
vencíveis nem que cada animação foi aprovada visualmente. Os pontos de
revisão para a equipe estão em
[`material-bruto/textos/PENDENCIAS_PARA_EQUIPE.md`](material-bruto/textos/PENDENCIAS_PARA_EQUIPE.md).
