# Soldados vs Zumbis — fichas das tropas Beta 4 V3

> **Documento histórico.** O elenco de tropas foi substituído em 13/09/2026
> pelo documento canônico `ELENCO_FUTURO_BETA4.md`. Os números abaixo não devem
> controlar novos sprites ou cartas até que o novo elenco seja balanceado.

## Regras desta revisão

- O nome principal de cada carta é uma **classe**: Guarda de Rua, Agente
  Tática, Operadora de Drone etc. Não é o nome civil de uma pessoa.
- Não existem níveis N1, N2 ou N3 e não existe evolução de nível.
- Engenheiros e médicos foram retirados do elenco.
- Todas as armas com munição recarregam automaticamente quando chegam a zero.
- Durante a recarga, a tropa faz a animação completa e não ataca.
- O cooldown abaixo pertence à habilidade; ele não substitui o tempo de
  recarga da arma.
- “Passiva” significa que a habilidade funciona por condição e não pode ser
  acionada repetidamente.
- Estes são os valores-base da dificuldade **Média**, antes dos
  multiplicadores de onda e dificuldade.

## Nova York — Zona Hélix

Uniformes azul-marinho, preto e laranja de emergência, com bandeira dos
Estados Unidos no braço. Este mapa combate civis contaminados, mutações
radioativas e criaturas tóxicas surgidas após a explosão do Grupo Hélix.

| Carta | História | Vida | Dano | Alcance | Habilidade | Munição | Recarga | Cooldown |
|---|---|---:|---:|---:|---|---:|---:|---:|
| Guarda de Rua | Patrulhava o primeiro bloqueio e foi a primeira defesa organizada contra os infectados. | 320 | 16 por bala | 3 espaços | **Saque rápido:** ganha 25% de cadência por 4 s quando o primeiro inimigo entra no alcance. | 24 | 3,2 s | 14 s |
| Agente Tática | Liderou a retirada de civis e domina rajadas curtas de contenção. | 390 | 26 por bala | 4 espaços | **Contenção:** três acertos consecutivos reduzem a velocidade do alvo em 18% por 2 s. | 30 | 4,2 s | Passiva |
| Breacher Urbano | Especialista policial de entradas forçadas, equipado com escopeta militar compacta. | 460 | 18 × 5 chumbos | 2 espaços | **Impacto próximo:** empurra um inimigo leve que estiver no primeiro espaço. | 6 | 5,8 s | 5 s |
| Artilheiro de Contenção | Mantém corredores inteiros sob fogo de metralhadora pesada. | 530 | 19 por bala | 5 espaços | **Fogo sustentado:** a cadência cresce durante 4 s no mesmo alvo; depois a arma resfria. | 80 | 8,5 s | 2 s de resfriamento |
| Granadeiro Metropolitano | Usa um lançador de granadas retirado do depósito de emergência da cidade. | 370 | 145 em área | 4 espaços | **Carga de ruptura:** reduz a armadura dos atingidos em 15% por 6 s. | 6 | 7,5 s | 12 s |
| Fogueteira de Resposta | Convocada para deter brutos que romperam as barricadas do reator. | 350 | 360 em área | 6 espaços | **Ruptura pesada:** o próximo foguete causa 35% a mais contra armadura e bosses. | 3 | 11 s | 15 s |
| Operador de Morteiro | Calcula trajetórias sobre os prédios sem atingir a base aliada. | 340 | 220 em área | 3 a 6 espaços | **Tiro marcado:** escolhe o quadrado com mais inimigos e nunca atira abaixo do alcance mínimo. | 4 bombas | 9 s | Passiva |
| Atiradora de Precisão | Cobria a evacuação de um hospital quando a cidade foi isolada. | 300 | 270; 420 em especial | Linha inteira | **Alvo prioritário:** após 1,2 s de mira, causa 420 em um inimigo especial. | 5 | 6,8 s | 10 s |
| Operadora de Drone | Pilota um drone armado recuperado da Guarda Nacional. Operadora e drone apontam para a direita. | 350 | 22 por tiro | 5 espaços | **Varredura aérea:** marca um alvo por 6 s; ele recebe 12% a mais de todo dano. | 36 de bateria | 8 s | 18 s |
| Especialista Antipraga | Ex-pesquisadora do Grupo Hélix, usa neutralizante tóxico contra as mutações. | 410 | 12 + 14/s por 4 s | 3 espaços | **Veneno corrosivo:** aplica Envenenado e reduz cura/reanimação em 50% por 6 s. Não usa fogo. | 60 de fluido | 8,5 s | 14 s |
| Operador de Rádio | Reativou uma frequência militar depois da queda das redes da cidade. | 310 | — | — | **Ponte aérea:** entrega 50 suprimentos após uma transmissão visível de 4 s. | — | — | 28 s |
| Escudeiro de Choque | Policial de controle de distúrbios que segura a linha com escudo e cassetete. | 950 | 45 corpo a corpo | 1 espaço | **Contra-choque:** reduz 55% do dano frontal e, após quatro bloqueios, atordoa por 1 s. | — | 1,4 s entre golpes | 6 s |

## Egito — Necrópole de Khepra

Uniformes militares modernos de deserto, com bandeira do Egito. Não há
armaduras medievais nas tropas. O lança-chamas é exclusivo deste mapa porque
o fogo impede a regeneração das múmias e revela criaturas enterradas.

| Carta | História | Vida | Dano | Alcance | Habilidade | Munição | Recarga | Cooldown |
|---|---|---:|---:|---:|---|---:|---:|---:|
| Patrulheiro do Deserto | Foi a primeira patrulha da Força-Tarefa Khepra a responder ao pedido da expedição. | 330 | 20 por bala | 3 espaços | **Troca rápida:** muda de alvo sem perder a cadência acumulada. | 20 | 3,4 s | Passiva |
| Fuzileira de Expedição | Sobreviveu ao despertar da tumba e escolta arqueólogos militares. | 390 | 28 por bala | 4 espaços | **Mecânica selada:** areia e maldição comum não aumentam a primeira recarga. | 30 | 4,5 s | Uma vez ao ser colocada |
| Escopeteiro de Ruínas | Especialista moderno em combate fechado dentro de corredores arqueológicos. | 450 | 20 × 5 chumbos | 2 espaços | **Interceptação:** causa 40% a mais contra inimigos no quadro em que emergem. | 7 | 6 s | Passiva |
| Artilheiro de Duna | Defende o acampamento com metralhadora em apoio portátil. | 510 | 20 por bala | 5 espaços | **Mira estabilizada:** após 2 s no mesmo alvo, recebe 20% de precisão e 15% de cadência. | 70 | 8 s | Passiva |
| Incineradora do Deserto | Usa chama controlada para impedir a regeneração de tecidos mumificados. | 400 | 10 + 18/s por 4 s | 3 espaços | **Queimadura reveladora:** aplica Queimadura e revela escavadores na própria linha. | 70 de combustível | 9 s | 8 s |
| Demolidor de Tumbas | Adaptou cargas de escavação para romper barreiras mágicas. | 370 | 170 em área | 4 espaços | **Quebra-selo:** remove 25% da proteção de escudos e barreiras. | 5 | 8 s | 12 s |
| Morteirista Nômade | Calcula a trajetória por marcos do terreno quando os instrumentos falham. | 340 | 240 em área | 3 a 6 espaços | **Impacto de areia:** atingidos perdem 12% de velocidade por 3 s. | 4 bombas | 9,5 s | Passiva |
| Atiradora do Horizonte | Interrompe sacerdotes antes que concluam rituais. | 300 | 285 por tiro | Linha inteira | **Interrupção:** um acerto em conjurador atrasa a habilidade dele em 4 s. | 5 | 7 s | 12 s |
| Operador Escaravelho | Pilota um drone moderno batizado pelo formato, sem magia antiga. | 350 | 24 por tiro | 5 espaços | **Scanner de solo:** revela escavadores e sandstalkers durante 7 s. | 32 de bateria | 8,5 s | 16 s |
| Escudeira Balística | Protege a expedição com escudo moderno resistente a calor e impacto. | 980 | 44 corpo a corpo | 1 espaço | **Cobertura:** reduz em 25% o dano sofrido pela tropa imediatamente atrás. | — | 1,5 s entre golpes | Passiva |
| Radioperador de Longo Alcance | Mantém o contato com Cairo por antena militar via satélite. | 310 | — | — | **Comboio aéreo:** entrega 52 suprimentos e não é silenciado por tempestade de areia. | — | — | 30 s |
| Arqueóloga Tática | Decifrou a reação do mineral de Khepra ao resíduo radioativo do Grupo Hélix. | 320 | 22 por disparo | 3 espaços | **Leitura de selo:** reduz em 20% a defesa de um inimigo amaldiçoado por 8 s. | 12 | 3,2 s | 15 s |

## Minas Gerais — Cachoeira do Véu Verde

Uniformes verde-oliva e laranja de resgate, com bandeira do Brasil e emblema
regional de Minas Gerais. O mapa mistura duas margens de terra e duas linhas
de água contaminada. Não há lança-chamas: a ferramenta equivalente é o jato
de água pressurizada.

| Carta | História | Vida | Dano | Alcance | Habilidade | Munição | Recarga | Cooldown |
|---|---|---:|---:|---:|---|---:|---:|---:|
| Guarda da Serra | Policial local que isolou a estrada da cachoeira durante a primeira contaminação. | 340 | 18 por bala | 3 espaços | **Proteção local:** ganha 15% de cadência quando o inimigo entra na metade aliada. | 24 | 3,4 s | 12 s |
| Fuzileira Brasileira | Militar enviada para impedir o Grupo Hélix de recuperar amostras do rio. | 400 | 29 por bala | 4 espaços | **Rajada disciplinada:** a terceira bala de cada rajada causa 20% a mais. | 30 | 4,4 s | Passiva |
| Atirador de Bote | Guia de rafting e reservista que conhece cada correnteza da região. | 380 | 25 por bala | 4 espaços | **Posição fluvial:** só entra na água e recebe 25% menos dano de ondas e respingos. | 24 | 4,8 s | Passiva |
| Bombeira Hidráulica | Adaptou uma bomba de alta pressão para conter mutantes aquáticos. | 440 | 14 por pulso | 3 espaços | **Jato pressurizado:** aplica Encharcado, reduz a velocidade em 22% por 3 s e empurra leves. | 65 de água | 7,5 s | 6 s |
| Artilheiro Fluvial | Opera arma estabilizada em plataforma de resgate. | 520 | 20 por bala | 5 espaços | **Base oscilante:** após 1,5 s parado, ganha precisão mesmo com a flutuação. | 75 | 8,2 s | Passiva |
| Mergulhadora de Combate | Investigou contêineres submersos antes que a área fosse evacuada. | 430 | 95 por arpão | 3 espaços | **Mergulho tático:** durante a recarga, fica submersa por 2 s e evita ataques à distância. | 6 arpões | 6,5 s | Passiva |
| Operadora de Drone Florestal | Antes mapeava incêndios; agora rastreia criaturas entre mata, rocha e água. | 360 | 23 por tiro | 5 espaços | **Rastreamento térmico:** revela submersos e aumenta em 12% o dano recebido por 6 s. | 34 de bateria | 8 s | 16 s |
| Lançador de Profundidade | Adaptou cargas leves para eliminar monstros sem destruir a cachoeira. | 380 | 190 em área | 4 espaços | **Detonação submersa:** causa 35% a mais contra inimigos aquáticos. | 5 cargas | 8,8 s | 10 s |
| Operador de Sonar | Técnico ambiental que detectou o primeiro cardume mutante sob a espuma. | 330 | — | Linha inteira | **Pulso de sonar:** revela submersos e dá 15% de precisão às tropas da linha por 7 s. | — | — | 18 s |
| Batedora da Mata | Agente ambiental treinada para seguir rastros na vegetação fechada e nas pedras. | 355 | 34 por disparo | 4 espaços | **Sinalização de trilha:** revela e marca um inimigo camuflado; ele recebe 10% a mais de dano por 5 s. | 18 | 4,1 s | 14 s |
| Morteirista da Margem | Usa marcações naturais nas pedras para atingir aglomerações sem acertar a base. | 350 | 225 em área | 3 a 6 espaços | **Impacto de espuma:** inimigos aquáticos atingidos ficam visíveis por 5 s. | 4 bombas | 9,2 s | Passiva |
| Rádio da Defesa Civil | Conectou quartéis, bombeiros e moradores quando as torres da região caíram. | 320 | — | — | **Rede comunitária:** entrega 48 suprimentos; a antena animada denuncia a transmissão. | — | — | 27 s |

## Defesas de emergência das linhas

Estas defesas não ocupam uma vaga de tropa e só disparam quando um inimigo
ultrapassa o último ponto de contenção:

| Região | Defesa | Funcionamento |
|---|---|---|
| Nova York | Trator de contenção | Sai da base, mantém o centro exato da pista e elimina todos os inimigos daquela linha. |
| Egito | Drone de saturação | Cruza a linha da esquerda para a direita, com hélices e disparos animados, eliminando a fileira. |
| Minas Gerais | Mina aquática | Existe somente nas linhas 2 e 3, arma em oito quadros e propaga explosões por toda a linha de água. |
