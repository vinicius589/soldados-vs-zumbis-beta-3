# Soldados vs Zumbis — Elenco e balanceamento proposto da Beta 4

> **Documento histórico.** Os nomes e as fichas das tropas foram substituídos
> em 13/09/2026 por `ELENCO_FUTURO_BETA4.md`. Este arquivo não deve controlar
> novos sprites, cartas ou balanceamento.

## Situação deste documento

Esta é a proposta de elenco para aprovação antes da produção dos próximos
sprites. Não existe mais Nível 1, Nível 2 ou Nível 3: cada carta representa um
personagem completo, com função própria. Os números abaixo são a base da
dificuldade **Média**, antes dos multiplicadores de onda e dificuldade.

As armas recarregam automaticamente quando a munição termina. A recarga tem
animação completa e o personagem não ataca durante esse período. Um alvo só é
atacado depois de entrar na quantidade de espaços indicada pelo alcance.

## Identidade dos três mapas

### 1. Nova York — Zona Hélix

- País: Estados Unidos.
- Campo: quatro faixas de rua alinhadas entre a base militar e a cidade contaminada.
- Uniformes: azul-marinho, preto, cinza e detalhes laranja de emergência.
- Identificação: bandeira dos Estados Unidos no braço dos militares.
- Ameaça: radiação, ácido, mutações do Projeto Lázaro e tropas infectadas.
- Animações de fundo propostas: dois militares conversando na base; mecânico
  conferindo caixas; holofote varrendo a rua; bandeira tremulando; cabeça de
  infectado aparecendo parcialmente atrás da barricada; chuva tóxica rara.
- Não usar: onda do mar, água de trincheira, píer, caverna, névoa ou relâmpago
  genérico sem relação com uma habilidade.

### 2. Egito — Necrópole de Khepra

- País: Egito.
- Campo: quatro caminhos de areia compactada diante de uma base militar egípcia.
- Uniformes: bege, cáqui, marrom e placas modernas contra areia.
- Identificação: bandeira do Egito no braço; a força fictícia do jogo se chama
  **Força-Tarefa Khepra**, uma unidade egípcia de contenção arqueológica.
- Ameaça: múmias, maldições, magia funerária e resíduos do Agente R-13.
- Animações de fundo propostas: dois soldados estudando um mapa; antena girando;
  bandeira tremulando; pequenos redemoinhos de areia; olhos de uma estátua
  acendendo; escaravelhos atravessando a entrada de uma tumba.

### 3. Minas Gerais — Cachoeira do Véu Verde

- País: Brasil; estado de Minas Gerais.
- Campo: margens de pedra e terra intercaladas com canais rasos alimentados por
  uma cachoeira. Não existe oceano, praia extensa, onda marítima ou píer.
- Uniformes: verde-oliva, azul de resgate, amarelo e detalhes vermelhos.
- Identificação: bandeira do Brasil em um braço e emblema regional triangular
  vermelho de Minas Gerais no outro.
- Ameaça: água doce contaminada, banhistas, pescadores, animais anfíbios e
  resíduos do Grupo Hélix trazidos pelo rio.
- Animações de fundo propostas: queda contínua da cachoeira; espuma seguindo o
  curso da água; agentes da Defesa Civil conversando; bandeira tremulando;
  sombra de criatura sob a água; peixe contaminado saltando raramente; gotas
  tóxicas escorrendo de um contêiner preso nas pedras.

## Tropas — Nova York

| Personagem | História curta | Vida | Dano base | Alcance | Habilidade | Munição | Recarga |
|---|---|---:|---:|---:|---|---:|---:|
| Marcus Reed — Guarda de Rua | Patrulheiro que encontrou o primeiro infectado antes do bloqueio militar. | 320 | 16 por bala | 3 | **Saque rápido:** ganha 25% de cadência durante 4 s quando o primeiro inimigo entra no alcance. Recarga interna: 14 s. | 24 | 3,2 s |
| Elena Brooks — Agente Tática | Liderou a retirada de civis pela Quinta Avenida e decidiu ficar na zona de exclusão. | 390 | 26 por bala | 4 | **Rajada de contenção:** três acertos seguidos reduzem a velocidade do alvo em 18% por 2 s. | 30 | 4,2 s |
| Darius Cole — Breacher Urbano | Especialista em entradas forçadas que transformou equipamento policial em defesa de rua. | 460 | 18 × 5 projéteis | 2 | **Impacto próximo:** o disparo empurra inimigos leves dentro do primeiro espaço. | 6 | 5,8 s |
| Owen Hayes — Artilheiro de Contenção | Veterano responsável por segurar o portão principal da base Hélix. | 530 | 19 por bala | 5 | **Fogo sustentado:** a cadência cresce por até 4 s no mesmo alvo; então a arma precisa resfriar por 2 s. | 80 | 8,5 s |
| Miguel Torres — Granadeiro Metropolitano | Ex-bombeiro militar que usa munição de contenção retirada de um depósito do Grupo Hélix. | 370 | 145 em área | 4 | **Carga de ruptura:** reduz a armadura atingida em 15% por 6 s. | 6 | 7,5 s |
| Abigail “Rook” Carter — Fogueteira de Resposta | Operadora antiblindado convocada quando os primeiros brutos romperam as barricadas. | 350 | 360 em área | 6 | **Ruptura pesada:** causa 35% a mais contra armadura e placas de boss; forte intervalo entre disparos. | 3 | 11 s |
| Henry Park — Operador de Morteiro | Calculista da defesa que adaptou marcações urbanas para bombardear sem atingir a base. | 340 | 220 em área | 3–6 | **Tiro marcado:** prioriza o quadrado com mais inimigos; não atira a menos de 3 espaços. | 4 | 9 s |
| Naomi Blake — Atiradora de Precisão | Cobria a evacuação do alto de um hospital quando a cidade foi isolada. | 300 | 270 | Linha inteira | **Alvo prioritário:** causa 420 contra inimigo especial após 1,2 s de mira. | 5 | 6,8 s |
| Chloe Bennett — Operadora de Drone | Engenheira de voo da Guarda Nacional que pilota um drone armado recuperado intacto. | 350 | 22 por tiro | 5 | **Varredura aérea:** o drone marca um alvo por 6 s; ele recebe 12% a mais de todos os danos. | 36 de bateria | 8 s |
| Dra. Maya Chen — Especialista Antipraga | Pesquisadora que denunciou o Projeto Lázaro e criou um neutralizante contra o R-13. | 410 | 12 inicial + 14/s por 4 s | 3 | **Antídoto corrosivo:** envenena zumbis e reduz cura/reanimação recebida em 50% por 6 s. | 60 de fluido | 8,5 s |
| Daniel Price — Operador de Rádio | Manteve a frequência militar funcionando depois da queda das redes da cidade. | 310 | — | — | **Ponte aérea:** entrega 50 suprimentos a cada 28 s; a transmissão visível dura 4 s e pode ser interrompida. | — | 28 s |
| Jordan King — Escudeiro de Choque | Policial de controle de distúrbios que virou a última barreira viva do portão. | 950 | 45 corpo a corpo | 1 | **Bloqueio balístico:** reduz 55% do dano frontal; após quatro bloqueios, atordoa o alvo por 1 s. | — | 1,4 s entre golpes |

## Inimigos — Nova York

| Inimigo | História curta | Vida | Dano | Habilidade |
|---|---|---:|---:|---|
| Civil Irradiado | Morador alcançado pela nuvem da Meia-Noite Verde. | 180 | 25 | Unidade básica, lenta e previsível. |
| Turista Perdido | Visitante contaminado enquanto tentava abandonar a cidade. | 220 | 24 | A mochila absorve o primeiro projétil recebido e então cai visualmente. |
| Corredor Entregador | Ciclista infectado com músculos superestimulados pelo R-13. | 140 | 42 | Dá um avanço curto na própria linha quando entra a 4 espaços de uma tropa. |
| Cientista Contaminado | Pesquisador do Grupo Hélix que carregava amostras durante a explosão. | 210 | 20 | Arremessa uma ampola a até 3 espaços; a poça causa 8 de dano/s por 4 s. Cooldown: 13 s. |
| Policial Infectado | Agente que morreu tentando manter uma rota de evacuação aberta. | 430 | 30 | Colete reduz em 35% os primeiros 220 pontos de dano frontal. |
| Operário Blindado | Trabalhador fundido a placas e equipamento de manutenção do reator. | 570 | 46 | Possui duas placas de 120 de vida que quebram em estágios visíveis. |
| Cuspidor Nuclear | Mutação cujo estômago produz ácido radioativo. | 280 | 24 + 10/s por 4 s | Cuspe a até 3 espaços aplica corrosão, aumentando a recarga da vítima em 15% por 5 s. Cooldown: 12 s. |
| Gritador de Sirene | Infectado fundido a um sistema portátil de alerta. | 250 | 20 | Acelera aliados próximos em 15% durante 6 s. Cooldown: 16 s; não acumula. |
| Divisor Tóxico | Corpo inchado por resíduos concentrados do laboratório. | 660 | 42 | Ao morrer, causa 90 em área e solta dois fragmentos com 90 de vida; só acontece uma vez. |
| Parasita de Laboratório | Protótipo do Projeto Lázaro criado para controlar músculos de um hospedeiro. | 320 | 16 | Imobiliza o ataque de uma tropa por no máximo 3 s. Cooldown: 14 s; permanece na mesma linha. |

### Bosses — Nova York

| Onda | Boss | Vida | Dano | Poder de chegada | Habilidade repetível |
|---:|---|---:|---:|---|---|
| 5 | Demolidor do Martelo | 5.200 | 80 | Atrasa todos os soldados por 5 s uma única vez. | Golpeia somente a própria linha, causando 70 e atordoando por 2 s. Cooldown: 15 s. |
| 10 | Cuspidor Alfa | 8.300 | 62 | Cria por 5 s uma nuvem tóxica apenas na linha em que entrou. | Dispara três ácidos com 0,35 s entre eles e depois fica 11 s sem usar o poder. |
| 15 | Colosso do Reator | 12.800 | 105 | Entra com três placas de 600 de vida, cada uma claramente visível. | Ao perder uma placa, emite uma onda de 55 de dano na própria linha e fica vulnerável por 3 s. |

## Tropas — Egito

| Personagem | História curta | Vida | Dano base | Alcance | Habilidade | Munição | Recarga |
|---|---|---:|---:|---:|---|---:|---:|
| Youssef Nassar — Patrulheiro do Deserto | Foi o primeiro soldado egípcio a chegar à Expedição Khepra depois do pedido de socorro. | 330 | 20 | 3 | **Troca rápida:** muda de alvo sem perder a cadência acumulada. | 20 | 3,4 s |
| Layla Hassan — Fuzileira de Expedição | Escolta militar que sobreviveu ao despertar da primeira tumba. | 390 | 28 | 4 | **Mecânica selada:** areia e maldições comuns não aumentam sua primeira recarga. | 30 | 4,5 s |
| Omar Farouk — Escopeteiro de Ruínas | Especialista moderno em combate fechado dentro de corredores arqueológicos. | 450 | 20 × 5 | 2 | **Interceptação:** causa 40% a mais contra inimigos no quadro em que emergem do solo. | 7 | 6 s |
| Samir Dawoud — Artilheiro de Duna | Defendeu o acampamento usando uma metralhadora montada em apoio portátil. | 510 | 20 | 5 | **Mira estabilizada:** após 2 s no mesmo alvo, ganha 20% de precisão e 15% de cadência. | 70 | 8 s |
| Noura Khalil — Incineradora do Deserto | Usa fogo controlado para impedir que tecidos mumificados se regenerem. | 400 | 10 + 15/s por 4 s | 3 | **Queimadura reveladora:** impede camuflagem e revela escavadores na própria linha. | 70 de combustível | 9 s |
| Karim Mansour — Demolidor de Tumbas | Abre passagens soterradas e transformou cargas de escavação em munição. | 370 | 170 em área | 4 | **Quebra-selo:** remove 25% da proteção de escudos e barreiras mágicas. | 5 | 8 s |
| Farid Rahman — Morteirista Nômade | Calcula a trajetória usando marcos no deserto quando instrumentos eletrônicos falham. | 340 | 240 em área | 3–6 | **Impacto de areia:** alvos atingidos perdem 12% de velocidade por 3 s. | 4 | 9,5 s |
| Salma El-Sayed — Atiradora do Horizonte | Vigia as dunas e interrompe sacerdotes antes de completarem rituais. | 300 | 285 | Linha inteira | **Interrupção:** acerto em conjurador atrasa a habilidade dele em 4 s. Cooldown: 12 s. | 5 | 7 s |
| Tarek Amin — Operador Escaravelho | Pilota um drone moderno batizado pelo formato, sem usar magia antiga. | 350 | 24 | 5 | **Scanner de solo:** marca escavadores e sandstalkers por 7 s. | 32 de bateria | 8,5 s |
| Amira Zaki — Escudeira Balística | Protege arqueólogos com escudo moderno resistente ao calor e aos impactos. | 980 | 44 | 1 | **Cobertura:** reduz em 25% o dano recebido pela tropa imediatamente atrás. | — | 1,5 s entre golpes |
| Hadi Mostafa — Radioperador de Longo Alcance | Mantém contato com Cairo por uma antena militar via satélite. | 310 | — | — | **Comboio aéreo:** entrega 52 suprimentos a cada 30 s e não é silenciado por tempestade de areia. | — | 30 s |
| Dra. Nadia Fawzi — Arqueóloga Tática | Descobriu que o mineral de Khepra reagia ao R-13 e decidiu ajudar a conter o desastre. | 320 | 22 | 3 | **Leitura de selo:** marca um inimigo amaldiçoado; ele perde 20% de defesa por 8 s. Cooldown: 15 s. | 12 | 3,2 s |

## Inimigos — Egito

| Inimigo | História curta | Vida | Dano | Habilidade |
|---|---|---:|---:|---|
| Múmia Operária | Trabalhador de uma necrópole despertado pelo vazamento. | 200 | 28 | Unidade básica resistente ao primeiro efeito de lentidão. |
| Corredor Chacal | Guerreiro magro cuja máscara ritual se fundiu ao rosto. | 150 | 44 | Arranque curto na própria linha; não troca de faixa. |
| Escavador da Expedição | Arqueólogo infectado que ainda carrega a picareta. | 270 | 50 | Cava com animação visível, avança exatamente um espaço ocupado e emerge; nunca teleporta e nunca muda de linha. Cooldown: 16 s. |
| Ladrão de Suprimentos | Saqueador reanimado atraído pelo equipamento da base. | 190 | 18 | Ao alcançar a zona de carga rouba 25 suprimentos; fica vulnerável por 2 s durante o roubo. |
| Acólito das Cinzas | Sacerdote menor despertado com fragmentos de magia funerária. | 240 | 22 | Maldição aumenta em 20% a próxima recarga de uma tropa. Cooldown: 14 s. |
| Curandeiro Funerário | Embalsamador que conserva corpos até depois da morte. | 270 | 18 | Cura 120 de um aliado a cada 12 s; uma única vez pode reviver um comum com 40% da vida. |
| Sentinela do Sarcófago | Guerreiro antigo preso ao próprio escudo cerimonial. | 680 | 36 | Escudo de 350 de vida reduz 45% do dano frontal até quebrar. |
| Sandstalker | Predador preservado na areia pela energia de Khepra. | 250 | 40 | Fica camuflado até entrar a 3 espaços, mas fogo ou scanner o revelam. |
| Hospedeiro de Escaravelhos | Múmia vazia controlada por um enxame. | 350 | 32 | Ao morrer, libera três escaravelhos de 45 de vida e 12 de dano. |
| Bruto Embalsamado | Guardião enorme reforçado por resina e placas funerárias. | 920 | 62 | Resiste a empurrão e atordoa a tropa atingida por 1,2 s. Cooldown: 11 s. |

### Bosses — Egito

| Onda | Boss | Vida | Dano | Poder de chegada | Habilidade repetível |
|---:|---|---:|---:|---|---|
| 5 | Guardião da Esfinge | 5.500 | 82 | Invoca duas Sentinelas com 70% da vida normal. | Muralha de areia reduz projéteis recebidos em 35% durante 4 s. Cooldown: 16 s. |
| 10 | Arquimago de Khepra | 8.000 | 68 | Concede somente um bônus — velocidade, força ou proteção — à escolta inicial. | Troca de encantamento a cada 14 s; os bônus nunca acumulam. |
| 15 | Faraó Necromante | 12.500 | 100 | Entra com quatro múmias básicas, distribuídas apenas na própria linha. | Em 66% e 33% da vida, tenta reviver um especial com 35% da vida; a conjuração dura 3 s e pode ser interrompida. |

## Tropas — Minas Gerais

| Personagem | História curta | Vida | Dano base | Alcance | Habilidade | Munição | Recarga |
|---|---|---:|---:|---:|---|---:|---:|
| Lucas Andrade — Guarda da Serra | Policial da pequena cidade próxima que isolou a estrada da cachoeira. | 340 | 18 | 3 | **Proteção local:** ganha 15% de cadência quando um inimigo pisa na metade aliada da linha. | 24 | 3,4 s |
| Ana Silva — Fuzileira Brasileira | Militar enviada para proteger moradores e impedir o Grupo Hélix de recuperar amostras. | 400 | 29 | 4 | **Rajada disciplinada:** a terceira bala da rajada causa 20% a mais. | 30 | 4,4 s |
| João Nogueira — Atirador de Bote | Guia de rafting e reservista que conhece cada correnteza da região. | 380 | 25 | 4 | **Posição fluvial:** só pode ser colocado na água; recebe 25% menos dano de respingos e ondas. | 24 | 4,8 s |
| Renata Alves — Bombeira Hidráulica | Bombeira militar que adaptou uma bomba de alta pressão para contenção. | 440 | 14 por pulso | 3 | **Jato pressurizado:** aplica Encharcado, reduzindo a velocidade em 22% por 3 s, e empurra alvos leves. | 65 de água pressurizada | 7,5 s |
| Paulo Mendes — Artilheiro Fluvial | Opera uma arma estabilizada montada sobre plataforma de resgate. | 520 | 20 | 5 | **Base oscilante:** ganha precisão após 1,5 s parado; a animação acompanha a flutuação. | 75 | 8,2 s |
| Camila Rocha — Mergulhadora de Combate | Especialista do Corpo de Bombeiros que investigou os contêineres submersos. | 430 | 95 por arpão | 3 | **Mergulho tático:** fica submersa por 2 s durante a recarga e não recebe ataques à distância. | 6 arpões | 6,5 s |
| Beatriz Lima — Operadora de Drone Florestal | Mapeava incêndios e passou a rastrear criaturas entre mata, pedra e água. | 360 | 23 | 5 | **Rastreamento térmico:** revela submersos e aumenta em 12% o dano que eles recebem por 6 s. | 34 de bateria | 8 s |
| Rafael Costa — Lançador de Profundidade | Mergulhador da Marinha que adaptou cargas leves para não destruir a cachoeira. | 380 | 190 em área | 4 | **Detonação submersa:** 35% a mais contra inimigos aquáticos; só mira quadrados de água. | 5 | 8,8 s |
| Thiago Barros — Operador de Sonar | Técnico ambiental que detectou o primeiro cardume mutante sob a espuma. | 330 | — | Linha inteira | **Pulso de sonar:** revela todos os submersos da própria linha e dá 15% de precisão às tropas por 7 s. Cooldown: 18 s. | — | 18 s |
| Júlia Moreira — Socorrista de Resgate | Integrante da Defesa Civil que permaneceu para retirar sobreviventes e manter a linha ativa. | 360 | — | 2 | **Estabilização:** recupera 140 de vida e 20% da munição de uma tropa; usa apenas uma carga a cada 24 s. | 3 cargas | 24 s por carga |
| Gabriel Freitas — Morteirista da Margem | Militar treinado em terreno montanhoso que usa marcações nas pedras. | 350 | 225 em área | 3–6 | **Impacto de espuma:** inimigos aquáticos atingidos ficam visíveis por 5 s. | 4 | 9,2 s |
| Marcos Vieira — Rádio da Defesa Civil | Radioamador mineiro que conectou quartéis, bombeiros e moradores quando as torres caíram. | 320 | — | — | **Rede comunitária:** entrega 48 suprimentos a cada 27 s; uma antena claramente animada indica a transmissão. | — | 27 s |

## Inimigos — Minas Gerais

| Inimigo | História curta | Vida | Dano | Habilidade |
|---|---|---:|---:|---|
| Afogado da Cachoeira | Banhista contaminado pela primeira descarga do R-13. | 190 | 26 | Inimigo básico; anda na margem ou nada somente na linha em que nasceu. |
| Remador Infectado | Praticante de rafting preso a um caiaque danificado. | 170 | 40 | Avança rapidamente na água; o caiaque absorve 90 de dano e depois quebra. |
| Zumbi de Boia | Turista com boia presa ao corpo. | 330 | 24 | Muito lento; a boia absorve os primeiros 140 de dano. |
| Mergulhador do Poço | Mergulhador com roupa rasgada e arpão enferrujado. | 290 | 32 | Atira um arpão a 3 espaços e submerge por 2 s durante a recarga. Cooldown: 12 s. |
| Baiacu do R-13 | Peixe de água doce transformado em criatura inchada e espinhosa. | 510 | 46 | Infla por 1 s antes de avançar; ao morrer causa 65 na própria linha. |
| Nadador Feral | Banhista transformado em mutante anfíbio. | 180 | 38 | Dá uma arrancada submersa de um espaço, sempre na mesma linha. Cooldown: 15 s. |
| Pescador Tóxico | Pescador contaminado com rede e galões presos ao corpo. | 310 | 26 | Rede aumenta em 20% a próxima recarga da tropa atingida. Cooldown: 14 s. |
| Salva-Vidas Gritador | Funcionário da área recreativa com apito fundido à garganta. | 270 | 26 | Acelera somente aliados aquáticos próximos em 15% por 6 s. Cooldown: 16 s. |
| Bruto do Lodo | Mutante coberto por pedra, barro, raízes e conchas de água doce. | 930 | 58 | Reduz dano frontal em 25%; o golpe cria respingo que reduz precisão em 12% por 3 s. |
| Anfíbio de Esgoto | Criatura de pele lisa vinda do sistema de drenagem do Grupo Hélix. | 250 | 42 | Salta exatamente uma tropa na própria linha uma única vez; nunca troca de faixa. |

### Bosses — Minas Gerais

| Onda | Boss | Vida | Dano | Poder de chegada | Habilidade repetível |
|---:|---|---:|---:|---|---|
| 5 | Barqueiro Afogado | 5.300 | 78 | Chama dois Mergulhadores do Poço com 70% da vida. | Âncora prende uma unidade por 2,5 s. Cooldown: 15 s. |
| 10 | Baiacu Colossal | 8.100 | 72 | Infla e recebe 30% menos dano frontal durante 4 s. | Rompe um galão e contamina apenas o quadrado aquático atual por 5 s. Cooldown: 14 s. |
| 15 | Leviatã do Véu Verde | 12.900 | 108 | A cachoeira muda de cor e uma corrente desloca embarcações um espaço sem destruí-las. | Alterna jato, golpe físico e arremesso de detritos; há 5 s de intervalo visual entre ataques e 14 s antes de repetir o mesmo poder. |

## Regras de animação ligadas às fichas

1. Todo personagem armado terá `idle`, `ataque`, `recarga`, `dano` e `morte`.
2. Pernas, braços, armas, carregadores e equipamentos mudam de pose entre os
   quadros; mover a imagem inteira não conta como caminhada.
3. Zumbis terão `andar/nadar`, `morder/golpear`, `habilidade`, `dano` e `morte`.
4. Escavador mostra entrada na areia, túnel avançando um espaço e saída; nunca
   fica apenas invisível e nunca teleporta.
5. Bosses terão entrada, idle, deslocamento, golpe básico, poder de chegada,
   habilidade repetível, reação a dano, transição e morte.
6. Todos permanecem centralizados pela posição dos pés ou pelo ponto de contato
   com a água. O pivô não muda entre os quadros.
7. O contorno verde-chroma não pode sobreviver no arquivo usado pelo jogo.
8. Tropas, armas, projéteis e veículos defensivos apontam e atacam da esquerda
   para a direita. Zumbis e bosses surgem à direita, caminham, nadam, atacam e
   caem da direita para a esquerda. Nenhuma sequência pode inverter o lado do
   rosto, da arma ou do movimento entre quadros.
9. Cada quadro possui área própria e margem transparente: braços, armas,
   projéteis, sombras e partes da morte não podem invadir o quadro vizinho.

## Decisão ainda aberta

Os nomes, histórias, números e habilidades acima são uma primeira proposta de
produção. Depois da aprovação do elenco, cada personagem será transformado em
uma ficha visual e em um sprite sheet próprio. Só então o balanceamento será
testado em ondas completas; nenhum valor desta tabela deve ser considerado
definitivo antes desse teste jogável.
