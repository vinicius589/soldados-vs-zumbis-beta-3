# Beta 4 — fichas de tropas para definir

Este é o documento de trabalho usado para aprovar, retirar, acrescentar e
balancear as tropas antes da produção dos sprites. O elenco oficial de nomes e
armas continua registrado em `ELENCO_FUTURO_BETA4.md`.

## Como responder

Não é necessário preencher tudo de uma vez. Basta informar o código da ficha e
o que já estiver decidido. Exemplos:

- `C1: mantém; 180 de vida; 24 de dano; habilidade Tiro de Xerife...`
- `D5: trocar a MG3 por M249.`
- `A8: retirar o Barco de Patrulha.`
- `Adicionar na cidade: nome, arma e função...`

Campos não informados permanecem **a definir**. Nada será inventado ou tratado
como aprovado sem ser identificado como proposta.

## Rodada aprovada — básicos e regra dos automáticos

As relações abaixo foram aprovadas pelo usuário. Os números são a primeira
implementação experimental para teste e continuam ajustáveis.

- Os básicos C1, D1 e A1 alcançam **exatamente dois blocos à frente**.
- Um básico não atira se houver outra defesa entre ele e o alvo na mesma linha.
- C2, D2 e A2 podem atirar através de aliados, têm mais munição e maior cadência.
- Os automáticos têm apenas um pequeno ganho de vida, nunca uma diferença de
  escala visual ou uma resistência desproporcional.
- Em compensação, os automáticos levam mais tempo para recarregar.
- C1, D1 e A1 têm a passiva **Recarga Ágil** e a limitação **Linha Limpa**.
- C2, D2 e A2 têm a passiva **Fogo por Cobertura**, que ignora o bloqueio de
  linha causado por aliados. Passivas não usam cooldown separado.

| Código | Situação | Vida | Dano por bala | Intervalo | Munição | Recarga | Alcance | Regra especial |
|---|---|---:|---:|---:|---:|---:|---:|---|
| C1 | Em teste no jogo | 100 | 22 | 0,82 s | 7 | 2,0 s | 2 | Linha Limpa |
| D1 | Em teste no jogo | 102 | 26 | 0,94 s | 6 | 2,2 s | 2 | Linha Limpa |
| A1 | Em teste no jogo | 101 | 14 | 0,68 s | 15 | 1,8 s | 2 | Linha Limpa; somente terra |
| C2 | Proposta para aprovação | 108 | 8 | 0,34 s | 30 | 3,4 s | 4 | Fogo por Cobertura |
| D2 | Proposta para aprovação | 110 | 15 | 0,46 s | 24 | 3,7 s | 4 | Fogo por Cobertura |
| A2 | Proposta para aprovação | 109 | 12 | 0,39 s | 30 | 3,6 s | 4 | Fogo por Cobertura; somente terra |

Os três automáticos permanecem fora da seleção até a aprovação dos números e
da arte isolada. A diferença máxima proposta de vida entre básico e automático
é de nove pontos, conforme o pedido de ser apenas “um pouquinho maior”.

## Campos de cada ficha

### Primeira rodada — identidade e função

1. **Situação:** manter, retirar, substituir ou ainda decidir.
2. **Nome da carta.**
3. **Arma/equipamento.**
4. **Vida** — ou estrutura, para veículos.
5. **Dano** — por bala, golpe, jato, granada ou explosão.
6. **Habilidade principal** — o que faz, em quem funciona e por quanto tempo.

### Segunda rodada — balanceamento

7. **Cadência/intervalo:** tempo entre ataques ou quantidade de tiros por rajada.
8. **Munição:** número de tiros antes da recarga; use “infinita” somente quando
   realmente não houver recarga.
9. **Recarga:** duração da animação e do bloqueio de ataque.
10. **Alcance:** em espaços do tabuleiro ou curta/média/longa distância.
11. **Custo:** suprimentos necessários para posicionar a carta.
12. **Cooldown:** espera para reutilizar a habilidade, separado da recarga.
13. **Área e alvo:** um inimigo, linha, cone, raio, grupo, terrestre ou aquático.
14. **Efeito:** empurrão, atordoamento, queimadura, veneno, lentidão etc.
15. **Fraqueza/limite:** aquilo que impede a carta de resolver tudo sozinha.

### Terceira rodada — animação

16. **Idle:** movimento enquanto espera.
17. **Ataque:** movimento da arma e do corpo.
18. **Recarga/preparo:** sequência visível quadro a quadro.
19. **Dano:** reação ao golpe sem alterar a escala do personagem.
20. **Habilidade:** sequência especial e efeitos visuais próprios.

## Cidade — Nova York

| Código | Carta | Arma/equipamento | Situação | Vida | Dano | Habilidade | Cooldown |
|---|---|---|---|---:|---:|---|---:|
| C1 | Xerife de Rua | Desert Eagle | A definir | — | — | — | — |
| C2 | Agente Tático da SWAT | MP5 | A definir | — | — | — | — |
| C3 | Atirador de Precisão | AWM | A definir | — | — | — | — |
| C4 | Operador de Rádio | Rádio tático | A definir | — | — | — | — |
| C5 | Agente de Entrada | SPAS-12 | A definir | — | — | — | — |
| C6 | Especialista Antipraga | Pulverizador químico | A definir | — | — | — | — |
| C7 | Lançador de Foguetes | RPG-7 | A definir | — | — | — | — |
| C8 | Escudeiro da Tropa de Choque | Escudo e cassetete | A definir | — | — | — | — |

### Observações da cidade

- Tropa de Choque: C5, C7 e C8.
- Identidade visual: polícia dos Estados Unidos, Xerife e SWAT.
- O Especialista Antipraga deve usar químicos contra infectados, mas dano,
  efeito e duração ainda não foram aprovados.

## Deserto — Egito

| Código | Carta | Arma/equipamento | Situação | Vida | Dano | Habilidade | Cooldown |
|---|---|---|---|---:|---:|---|---:|
| D1 | Pistoleiro do Deserto | Magnum .357 | A definir | — | — | — | — |
| D2 | Fuzileiro do Deserto | SCAR | A definir | — | — | — | — |
| D3 | Atirador do Horizonte | Dragunov SVD | A definir | — | — | — | — |
| D4 | Operador de Rádio | Rádio militar de longo alcance | A definir | — | — | — | — |
| D5 | Tenente Artilheiro | MG3, provisória | A definir | — | — | — | — |
| D6 | Incinerador do Deserto | Lança-chamas | A definir | — | — | — | — |
| D7 | Nômade do Morteiro | Morteiro portátil | A definir | — | — | — | — |
| D8 | Homem-Bomba | Carga explosiva corporal | A definir | — | — | — | — |

### Observações do deserto

- D3 foi registrado como Dragunov SVD a partir da referência “Dragon 9SVD”.
- D5 ainda pode trocar a MG3 pela M249 antes da produção do sprite.
- D6 é a unidade exclusiva de fogo do deserto.
- D8 precisa definir raio, dano, momento de detonação e se desaparece mesmo
  quando a explosão não derrota nenhum zumbi.

## Cachoeira — Minas Gerais

### Tropas humanas da Marinha do Brasil

| Código | Carta | Arma/equipamento | Situação | Vida | Dano | Habilidade | Cooldown |
|---|---|---|---|---:|---:|---|---:|
| A1 | Marinheiro | Glock 19 em 9×19 mm | A definir | — | — | — | — |
| A2 | Fuzileiro da Marinha | M16 | A definir | — | — | — | — |
| A3 | Atirador de Precisão | TRG-42 | A definir | — | — | — | — |
| A4 | Operador de Rádio | Rádio naval | A definir | — | — | — | — |
| A5 | Bombeiro Hidráulico | Lançador de água pressurizada | A definir | — | — | — | — |
| A6 | Granadeiro | M32 MGL | A definir | — | — | — | — |
| A7 | Homem-Bomba | Carga de demolição | Imóvel; explosão imediata no contato | 142 | 188 | 0 | — |

### Unidades mecânicas

| Código | Carta | Arma/equipamento | Situação | Estrutura | Dano | Habilidade | Cooldown |
|---|---|---|---|---:|---:|---|---:|
| A8 | Barco de Patrulha | Armamento naval leve | A definir | — | — | — | — |
| A9 | Submarino Tático | Armamento submerso | A definir | — | — | — | — |

### Observações da cachoeira

- A1 usa Glock 19, escolha provisória entre as opções de pistola 9 mm.
- A5 precisa definir força do empurrão, duração da lentidão e interação com
  zumbis aquáticos.
- A7 precisa definir quantidade de minas, tempo de preparo, raio e reposição.
- A8 e A9 precisam confirmar se ocupam cartas normais ou um grupo mecânico
  separado no menu.

## Novos personagens propostos

Use esta área somente quando uma carta nova for sugerida. Uma proposta não entra
automaticamente no elenco oficial.

| Mapa | Nome proposto | Arma/equipamento | Função | Entrou no elenco? |
|---|---|---|---|---|
| — | — | — | — | Não decidido |

## Ordem sugerida para aprovação

1. C1, D1 e A1 — os três defensores básicos.
2. C2, D2 e A2 — os três fuzileiros/automáticos.
3. C3, D3 e A3 — os três atiradores de precisão.
4. C4, D4 e A4 — os três operadores de rádio.
5. C5, D5 e A5 — espingarda, metralhadora pesada e água.
6. C6, D6 e A6 — químico, fogo e granadas.
7. C7, D7 e A7 — foguete, morteiro e minas.
8. C8 e D8 — tanques/sacrifício.
9. A8 e A9 — barco e submarino.

Essa ordem permite comparar funções equivalentes entre os mapas sem transformar
os três elencos em cópias uns dos outros.
