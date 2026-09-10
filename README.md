# Soldados vs Zumbis — Beta 4

Este é um tower defense militar original feito com **Pygame e PyOpenGL**. A Beta 4 reorganiza o projeto em torno de quatro rotas físicas, animação por estados, recarga própria das armas e três regiões completas de 15 ondas: Cidade, Deserto e Praia.

Os projetos locais fornecidos foram usados somente como estudo de arquitetura. A entrega não contém código, arte, som nem arquivo extraído desses exemplos ou de jogos comerciais. As técnicas reaplicadas em código próprio incluem: sequências separadas por ação, relógio de animação independente do FPS, ponto de contato no quadro correto, recorte por alfa, preservação do apoio dos pés ao trocar de pose, grupos lógicos por faixa e efeitos que terminam sem repetir.

Os três campos foram reconstruídos para a mesma geometria jogável. Cidade tem quatro avenidas, Deserto tem quatro trilhas e Praia tem a composição **areia–água–água–areia**. Personagens, zumbis, chefes, projéteis e contenções usam a mesma linha central de sua rota; ninguém nasce ou deriva no céu, no horizonte ou fora do canal.

Cada rota começa com uma contenção temática de uso único. A Cidade usa a bomba urbana, o Deserto usa a carga das dunas, e a Praia usa cargas costeiras nas duas rotas de areia e boias-bomba nas duas rotas de água. As minas escolhidas por carta continuam sendo objetos diferentes dessas contenções.

## Beta 4

Esta entrega fecha a revisão visual e técnica da **Beta 4**, sem criar uma nova camada de conteúdo. Ela corrige a apresentação e a regra dos movimentos especiais, confere a curva dos três modos e torna toda a lista regional realmente encontrável em uma campanha de 15 ondas.

- O compositor híbrido usa Pygame para regras, entrada, áudio, textos e superfícies; o PyOpenGL mantém as texturas na GPU, aplica iluminação/cor e desenha cada ator em uma malha subdividida.
- NumPy fornece ao PyOpenGL o manipulador de arrays nativo no Python 3.14, evitando o aviso e a conversão lenta da primeira abertura.
- Caminhada não é mais a imagem inteira balançando: as metades inferiores avançam em oposição, o tronco contrabalança e ataque, dano, stun, habilidade, **recarga**, salto, escavação, queda e carrinhos usam poses próprias calculadas pelo shader.
- Pés, rodas e cascos usam uma âncora imutável no centro da faixa pintada. A animação altera a malha acima dela, nunca a linha lógica do personagem.
- As quatro faixas têm limites próprios em Cidade, Deserto e Praia. A profundidade reduz discretamente atores das pistas traseiras e aumenta os da frente; na Praia a variação é menor porque a câmera é quase ortográfica.
- O HUD e os efeitos ficam em uma camada independente e sempre nítida, acima dos atores deformados.
- Se a máquina não oferecer um contexto OpenGL compatível, o jogo entra sozinho no modo Pygame. Para forçar esse modo, defina `SVZ_RENDERER=software` antes de abrir.

- A tela de carregamento usa **exatamente** a ilustração de referência enviada para esta beta como fundo, pré-carregada antes do menu; o arquivo não foi redesenhado nem substituído.
- O **Saltador** recebeu um retrato original sem pilar, ponte ou cenário embutido. No jogo, ele percorre um arco de salto visível e ultrapassa somente a primeira defesa bloqueadora.
- O **Rastejante urbano** agora tem uma silhueta própria, baixa e sem pernas funcionais; ele não reutiliza mais a arte nem a leitura visual do Corredor.
- A Cidade substitui o fogo por **Pulverizador de Veneno N1 → Canhão de Veneno N2**, com duas artes originais próprias. O estado **Envenenado** dura 4,2 segundos, causa dano periódico e reduz o avanço em 12%. O **Lança-Chamas** fica exclusivo do Deserto, recebeu mais dano e aplica **Queimadura** com duração finita.
- O **Escavador** não teleporta mais nem causa uma pancada grátis ao atravessar. Ele abaixa, enterra o corpo, atravessa somente a primeira defesa e emerge logo atrás dela — uma única travessia por inimigo, com quadros próprios para entrada, túnel e saída.
- A **Praia foi refeita do zero**: novo cenário, novo atlas costeiro N1, novo atlas N2 e novo atlas de infectados. As quatro bandas pintadas são remapeadas para os mesmos limites usados por clique, colisão, personagem e carga.
- Mecânico e Engenheiro deixaram de existir no elenco. Toda arma esvaziada entra numa recarga automática própria de **8 a 15 segundos**, conforme a família; a unidade baixa a arma, fica incapaz de atirar, mostra o progresso e só volta ao combate com o carregador completo.
- A diretoria de ondas usa uma regra auditável: começa com o invasor-base, acrescenta ameaças em ordem e libera **100% do elenco de Cidade, Deserto ou Praia na onda 15**. Nenhum personagem regional fica cadastrado sem poder entrar em jogo.
- Fácil, Médio e Difícil continuam limitando cartas e regulando vida, dano, quantidade, intervalo, escolta e frequência dos poderes de maneira verificável: Fácil < Médio < Difícil. O Fácil permaneceu intacto; o Médio recebeu só uma pressão extra, enquanto o Difícil passou a ser o modo veterano, ainda vencível sem stun infinito ou paredes impossíveis de vida.

### O que foi reaprendido dos projetos de estudo

Foram inspecionados os exemplos locais de tower defense, plataforma, luta, survival e tiro fornecidos durante o desenvolvimento. A leitura foi feita como referência técnica, sem importar os arquivos deles:

- dos clones de tower defense: grupos por rota, busca de alvo somente na mesma faixa, conjuntos distintos de caminhar/atacar/morrer e disparo liberado no quadro de contato;
- dos projetos de plataforma e luta: colisão separada do recorte visual, âncora inferior preservada, estado de ação com começo/fim e efeito de uso único;
- dos projetos de tiro: arma em estados de repouso/disparo, projétil raster rotacionado pela trajetória, recuo temporizado e som ligado ao evento de disparo;
- padrões frágeis foram deliberadamente descartados: dano na entrada da pose, temporizador dependente do FPS, troca de imagem que desloca os pés, fallback colorido visível, projéteis geométricos e ativos comerciais de terceiros.

## Executar

No Windows, extraia o arquivo ZIP e dê duplo clique em executar.bat.

Ou abra um terminal dentro da pasta do jogo:

~~~powershell
python -m pip install -r requirements.txt
python main.py
~~~

Requer Python 3.10 ou superior, pygame-ce==2.5.8, PyOpenGL==3.1.10 e numpy==2.5.3. O `executar.bat` verifica e instala essas dependências na primeira abertura.

## Controles

- Clique em **Jogar Campanha**, escolha **Fácil**, **Médio** ou **Difícil** e então abra o mapa.
- Escolha livremente Cidade, Deserto ou Praia e monte uma equipe de 8 cartas.
- Clique numa carta e depois no terreno para posicionar a defesa.
- Teclas 1 a 8: selecionam as cartas da missão.
- Tecla E ou botão **N3**: ativa o Núcleo de Ascensão; depois clique numa defesa.
- Clique em **REMOVER** (ou pressione **R**) e depois em uma defesa para recolhê-la. São devolvidos 35% dos suprimentos; clique novamente em REMOVER para desligar a ferramenta.
- Clique em **PAUSA** (ou pressione **P**) para congelar inimigos, recargas, projéteis, cronômetros e ondas. Use o mesmo botão ou P para continuar.
- Clique em **PRÓXIMA** (ou pressione **Espaço** durante o intervalo) para iniciar a próxima onda antes da contagem terminar.
- Clique em **MENU** durante uma missão, ou pressione **Esc**, para voltar diretamente à tela inicial. Sair assim não marca vitória nem derrota.
- Clique no **Ladrão de Suprimentos** marcado com “CLIQUE” para recuperar a carga.
- Cada faixa começa com uma **Bomba de Contenção**. Quando o primeiro infectado cruza a linha final daquela faixa, ela percorre a linha uma única vez e elimina os invasores que encontrar. Cidade: carrinho urbano; Deserto: carga das dunas; Praia: carrinhos costeiros na areia e boia-bomba no canal. Quando a contenção já foi gasta, um invasor que escapar naquela faixa causa a derrota.

As faces das cartas exibem custo e estatísticas objetivas (dano, munição, tempo de recarga, vida ou suprimento). Passe o mouse sobre uma carta para ver o nome temático e a habilidade completa, sem duplicar essa descrição no tabuleiro. Na missão, clicar em uma carta confirma brevemente o nome e o Nível escolhidos; a moldura dourada, a arte e a defesa posicionada usam a mesma chave de carta.

## Modos de dificuldade

| Modo | Cartas disponíveis | Preparação | Hordas e chefes |
| --- | --- | --- | --- |
| **Fácil** | Apenas cartas **N2** | 390 suprimentos e **3 Núcleos de Ascensão** já disponíveis para usar | Inimigos comuns têm 20% mais vida e dano; chefes têm 15% mais vida e dano. Hordas 15% maiores, escoltas 20% maiores, entradas 10% mais rápidas e poderes 15% mais frequentes. O arsenal N2 e os Núcleos mantêm o modo acessível, mas não existe botão nem atalho para remover tropas posicionadas. |
| **Médio** | Cartas **N1 e N2** | 128 suprimentos e nenhum Núcleo inicial | Inimigos comuns têm 36% mais vida e dano; chefes têm 24% mais vida e dano. Hordas 24% maiores, escoltas 36% maiores, entradas 23% mais rápidas e poderes 14% mais frequentes. É um desafio central exigente, mas ainda permite montar respostas com N1 e N2. |
| **Difícil** | Apenas cartas **N1** | 105 suprimentos para exigir uma formação mais consciente | Zumbis comuns têm 66% mais vida e 58% mais dano; chefes têm 62% mais vida e 50% mais dano, com horda 39% maior, escoltas 54% maiores, entradas 32% mais rápidas e poderes 16% mais frequentes. É a modalidade veterana, ainda vencível com munição, suportes e posicionamento. |

O Nível 3 não vira uma carta de seleção: ele é aplicado no campo por Núcleos. No Fácil, os três Núcleos iniciais equivalem aos upgrades N3 já liberados para a primeira missão; nos outros modos, eles continuam sendo conquistados ao derrotar chefes.

Todas as cartas, em todos os mapas e modos, têm **10 segundos de recarga depois de serem posicionadas**. Enquanto a carta recarrega, ela fica escurecida e exibe na própria interface quantos segundos ainda faltam.

## Estrutura da campanha

Há três regiões disponíveis desde o início. Cada uma é uma rota completa de 15 ondas:

| Região | Terreno e identidade | Pressão inimiga |
| --- | --- | --- |
| Cidade Quarentenada | Avenida de asfalto integrada à cidade em ruínas | Tóxicos, blindados, policiais infectados, escudos e corredores |
| Deserto das Ruínas | Estrada de terra, pirâmides e tempestade de areia | Escavadores, ladrão mágico, curandeiro mortal, parasita e necromante |
| Praia de Maré Morta | Uma faixa de areia, duas faixas centrais de água e uma faixa final de areia | Surfistas, boias, mergulhadores, caçadores e maré infectada |

Cada região possui **15 ondas**. Os chefes aparecem nas ondas **5, 10 e 15**, sempre com uma escolta e um alerta vermelho central de chegada. A progressão começa apenas com o inimigo-base, com pouca vida, pouco dano e intervalos maiores. A cada onda, a diretoria adiciona counters novos, aumenta a vida e o dano e reduz o intervalo de chegada; as últimas ondas trazem quase todo o elenco regional junto de grupos maiores. Recompensas de ondas, rádio e chefes foram reduzidas para que a economia não transforme o final em uma vitória automática.

A curva é intencionalmente **fácil no começo e média–difícil no final**: a última parte reúne mais inimigos, vida e dano maiores, além dos chefes, mas mantém vida, escolta e intervalos em faixas vencíveis sem depender obrigatoriamente da contenção de última linha.

Todo chefe possui duas camadas claras: uma **entrada especial**, usada uma única vez, e uma **habilidade recorrente localizada**, com recarga longa. A v7.5 diminui o teto de vida e dano de todos os chefes e reduz uma unidade da escolta em cada marco, preservando a necessidade de montar uma linha funcional sem transformar o carrinho-bomba na única forma de vencer. Exemplo: o Bruto Demolidor da Cidade paralisa os militares por 3 segundos ao entrar; depois, só o Martelo da faixa onde ele está interrompe os tiros por 1,2 segundo, com 18 segundos de intervalo. Assim o chefe exige reação, mas nunca cria uma cadeia infinita de atordoamento.

## Regras principais

### Alcance real

Uma defesa só ataca quando o alvo entra na sua faixa de alcance. Escopetas resolvem o curto alcance; rifles e snipers cobrem a pista; granadas, morteiros e armas especiais lidam com grupos de formas diferentes.

### Munição e recarga própria

Armas continuam com carregadores finitos, mas não dependem mais de uma unidade externa. Quando a munição chega a zero, a tropa interrompe o tiro e inicia automaticamente uma recarga completa. Rifles N2 levam 8 segundos; espingardas, jatos e armas de embarcação ficam na faixa intermediária; sniper, granadas, morteiro e torpedo podem chegar a 15 segundos. O progresso aparece no campo e o shader OpenGL anima a troca de carregador/câmara sem soltar os pés, rodas ou casco do terreno.

O **Rádio** continua existindo somente para gerar suprimentos. Não entrega munição e não encurta a recarga das armas.

### Núcleo de Ascensão: Nível 3 temporário

O chefe derrotado entrega um **Núcleo de Ascensão** (máximo de 3 guardados). Use-o em uma defesa já posicionada para ativar temporariamente seu Nível 3, limpar seus debuffs e completar sua munição.

Exemplos:

- Rifleiros cobrem a linha e acertam uma pequena área no fim do tiro.
- Escopetas ganham impacto maior em grupo.
- Snipers recebem dano de execução.
- Bombardeiros podem disparar uma bazuca que rasga a linha.
- Morteiros soltam bombas extras; o lança-chamas do Deserto intensifica a Queimadura, o Canhão de Veneno urbano amplia a nuvem tóxica e o Canhão de Maré segura inimigos encharcados na Praia.
- A ascensão completa imediatamente a munição e cancela uma recarga que esteja em andamento.
- Barreiras passam a disparar e explodem ao cair.
- Minas limpam a linha inteira.

O Núcleo não altera a carta de forma permanente: ele é uma decisão de emergência ou de virada de onda.

### Evolução Nível 1 → Nível 2

As cartas N1 e N2 estão disponíveis para a seleção. Elas não compartilham mais o mesmo retrato: cada cenário tem uniforme, silhueta e equipamento próprios para cada nível. A v7.8 valida essa identidade por carta e a v7.9 também a limita à região correta: uma N2 não pode carregar a arte, a habilidade ou o terreno de uma classe vizinha. Na tela **Soldados**, cada par aparece literalmente em duas faixas, com a carta N1 em cima e a respectiva N2 logo abaixo.

- **Sargento de Promoção**: carta especial exclusiva do modo **Difícil**, que custa 135 suprimentos. Ao sobreviver por 90 segundos, procura uma defesa N1 num raio de três blocos e nas faixas vizinhas e a promove permanentemente para a carta N2 correspondente. Não aparece no Fácil nem no Médio.
- A promoção preserva uma parte proporcional de vida e munição, remove atordoamento/corrosão e reinicia os tempos de ataque com a ficha nova.
- O Sargento promove uma defesa por ciclo. Se não houver uma N1 próxima ao terminar o cronômetro, ele aguarda 8 segundos e verifica de novo; não desperdiça um ciclo completo.
- O Sargento não dá N3. O Nível 3 continua sendo um efeito separado, temporário e obtido somente de chefes derrotados.

### Água

Atirador de Lancha, Lancha Patrulha, Submarino e Bomba de Água aparecem **somente** na seleção e nas fichas de soldados da **Praia de Maré Morta**. Eles só são posicionáveis no **canal central** desse mapa. Cidade e Deserto não mostram itens marítimos na montagem de equipe. Tropas de terra não são colocadas dentro da água. Pelo mesmo motivo, Boia, Surfista, Salva-Vidas, Mergulhador, Caçador da Costa, Cuspidor de Sal, Gritador de Maré e Nadador **nascem somente no canal**; Cowboy e Saltador são as ameaças costeiras terrestres.

As cartas **Mina de Areia** e **Mina Segura** são terrestres: ficam apenas nas duas faixas secas da Praia. Elas têm sprites próprios, sem suprimentos, caixas ou ponte. A **Bomba de Água** é a alternativa naval e usa uma mina marítima independente, apenas nas duas faixas do canal.

O **Atirador de Lancha N1** também é aquático: é uma carta de rifle de três blocos, com 10 disparos, montada em um pequeno barco. Ele só entra no canal e pode ser promovido pelo Sargento para a **Lancha Patrulha N2**.

O **Lançador de Água N1** e o **Canhão de Maré N2** são cartas terrestres exclusivas da Praia: ficam nas duas faixas de areia, não no canal. Em vez de fogo, seus jatos de alta pressão atingem uma área curta, removem a queima e aplicam **Encharcado** por 2,4 segundos (3,6 s enquanto estiverem em N3), reduzindo em 32% a velocidade do zumbi. Eles têm dano menor que o lança-chamas, portanto servem para controlar avanço e abrir espaço, não para derreter uma horda sozinhos.

### Armas elementais por região

- **Cidade:** Pulverizador de Veneno N1 e Canhão de Veneno N2. Aplicam **Envenenado** por 4,2 segundos, com dano periódico, fluxo químico rasterizado e 12% de redução de velocidade.
- **Deserto:** Lança-Chamas de Mão N1 e Lança-Chamas N2. São as únicas cartas incendiárias; agora causam 14 e 20 de dano-base e aplicam **Queimadura**.
- **Praia:** Lançador de Água N1 e Canhão de Maré N2. Aplicam **Encharcado**, não fogo nem veneno.

## Elenco e contrapontos

Cada região oferece mais de dez cartas temáticas. As roupas e silhuetas são próprias de Cidade, Deserto e Praia.

- **Rifles:** Recruta e Soldado controlam alvos simples; a ascensão libera o Fuzileiro.
- **Espingardas:** seguram corredores e saltadores perto da linha.
- **Snipers:** lidam com blindados e subchefes, mas exigem munição e proteção.
- **Explosivos:** quebram escudos e grupos; as granadas básicas podem acertar aliados próximos.
- **Elementais e morteiro:** Cidade usa veneno, Deserto usa fogo e Praia usa água; o morteiro continua como impacto explosivo de arco.
- **Rádio:** sustenta a economia. A munição pertence a cada arma; não existem mais cartas de Mecânico, Engenheiro ou Médico.
- **Contenção e minas:** compram tempo contra investidas, mas os saltadores conseguem ultrapassar a primeira linha. Carrinhos de contenção continuam separados visual e mecanicamente das minas que o jogador posiciona como carta.

Os zumbis possuem habilidades efetivas durante a batalha:

- Corredor e Surfista fazem dash inicial.
- Policial, Militar e Cowboy atiram de longe.
- Porta-Escudo e Salva-Vidas reduzem disparos frontais, mas fogo e veneno em área ajudam a quebrar a formação.
- Cuspidor Ácido e Cuspidor de Sal corroem armas e ferem à distância.
- Gritadores aceleram hordas.
- Escavador cava em três etapas visíveis e passa apenas pela primeira tropa bloqueadora.
- Ladrão rouba suprimentos e pode ser clicado.
- Curandeiro recupera aliados e pode reanimar um infectado.
- Parasita e Mutantes atordoam ou desabilitam as defesas.
- Chefes aplicam eventos de campo, invocam aliados, aceleram a horda, soltam névoa ácida, ondas ou abalos.

## Animações e efeitos

Zumbis e tropas usam uma **máquina de estados de animação**. Zumbis caminham, travam antes de morder, avançam no golpe, reagem ao dano, oscilam quando atordoados, fazem pose de habilidade, saltam em arco, entram/atravessam/saem da escavação e continuam caindo por alguns quadros ao morrer. Tropas entram em campo, atacam com recuo e clarão na arma, reagem a impacto, recarregam, operam rádio e promovem aliados. Os relógios de recarga, salto, stun e escavação acumulam `dt` em vez de reiniciar a pose a cada quadro.

Os tiros também foram redesenhados em movimento. Balas, cartuchos, munição pesada, granadas, obuses, foguetes, torpedos, ácido, munição infectada, micromíssil e arpão são sprites próprios; fogo, água e veneno usam folhas de matéria com quatro fases; impacto balístico, explosão, abalo, magia e maré têm sequências independentes. O dano de mordida e golpe só acontece no ponto de contato da animação, e não quando o inimigo apenas começa a pose.

O cenário não usa quadrados verdes coloridos: a área de posicionamento acompanha o cenário pintado. Uma borda fina só aparece sob o mouse para indicar o ponto de instalação; na Praia, a água recebe um brilho discreto.

## Tela de carregamento

Antes de liberar o menu, o jogo abre uma tela de carregamento real e coloca em memória **47 recursos**: a ilustração enviada para o carregamento, menu, três cenários de quatro rotas, nove atlases, cartas individuais, contenções, minas, três folhas de oito poses, três folhas de ações completas dos chefes e quatro folhas de efeitos/projéteis. Em seguida, os recortes de ator são enviados antecipadamente à GPU; a partida não precisa ler arquivos nem criar texturas pesadas no meio de uma onda.

## Arquivos

- main.py — jogo completo.
- opengl_presenter.py — compositor, shaders, malha de atores e cache de texturas na GPU.
- smoke_test.py — verificações automatizadas sem janela visível.
- assets/v7/ — artes originais desta reconstrução.
- ASSET_MANIFEST.md — inventário e direção das artes originais.
- requirements.txt — dependência.
- executar.bat — atalho de execução no Windows.
- campanha_v7.json — criado automaticamente para guardar melhores ondas e regiões concluídas; pode ser apagado para reiniciar esse histórico.

## Verificação técnica

~~~powershell
python -m py_compile main.py opengl_presenter.py smoke_test.py
python smoke_test.py
~~~

O teste usa SDL_VIDEODRIVER=dummy, portanto não abre uma janela gráfica.
