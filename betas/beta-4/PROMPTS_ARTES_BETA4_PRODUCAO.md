# Registro das artes novas — Beta 4

Modo usado: gerador de imagens integrado do Codex, sem fallback externo. As seis folhas foram geradas do zero e depois copiadas para `assets/beta4_producao`.

Regras comuns de todos os pedidos: pixel art 16-bit original, visão lateral-isométrica de jogo dos anos 90, grade regular de oito colunas, fundo realmente transparente, corpo inteiro, pés na mesma linha, escala corporal constante, nenhum membro ou efeito invadindo a célula vizinha, nenhuma parte cortada e nenhuma reutilização de personagens comerciais ou sprites antigos do projeto.

## Defensores — grade 8 x 5

Ordem das linhas: caminhada, espera/mira, disparo, recarga e dano.

### Cidade — Xerife de Rua

> Create an original 16-bit pixel-art 8-by-5 sprite sheet of a United States county sheriff for a side-isometric tower-defense game. Tan sheriff shirt, dark navy tactical trousers, black protective vest, gold star badge, service pistol, believable police silhouette. Eight coherent frames per row: walking right, guarded idle, firing right with recoil and muzzle flash, physical magazine reload, and taking damage. Transparent background, constant body size and foot baseline, complete uncropped figure in every cell, no frame invasion, no text, no existing game character.

### Deserto — Operador do Sa'ka

> Create an original 16-bit pixel-art 8-by-5 sprite sheet of an Egyptian Armed Forces Sa'ka special-operations rifleman for a side-isometric tower-defense game. Arid digital camouflage, practical scarf, helmet and goggles, Egyptian red-white-black shoulder patch, modern service rifle. Eight coherent frames per row: walking right, aiming idle, firing right, removing and inserting a magazine, and taking damage. Transparent background, constant proportions and foot baseline, no medieval or fantasy armor, no cropped equipment, no adjacent-frame overlap, no text.

### Cachoeira — Fuzileiro Naval

> Create an original 16-bit pixel-art 8-by-5 sprite sheet of a Brazilian Navy amphibious marine for a side-isometric tower-defense game. Dark navy and jungle-green tactical uniform, blue beret or naval helmet, Brazilian flag patch, compact carbine, rescue hook and waterproof pack. Eight coherent frames per row: walking right, ready idle, firing right, visible magazine reload, and taking damage. Transparent background, vivid readable colors, stable scale and foot baseline, full body in every cell, no frame invasion, no text.

## Zumbis — grade 8 x 4

Ordem das linhas: caminhada, espera/ameaça, mordida e dano.

### Cidade — Infectado Urbano

> Create an original 16-bit pixel-art 8-by-4 sprite sheet of a radioactive former office worker zombie from a quarantined New York district. Torn suit, toxic wounds, asymmetrical limp, readable hands and jaw. It travels and attacks toward the left. Rows: eight-frame limping walk, threatening idle, physical bite lunge with both arms remaining visible, and damage recoil. Transparent background, stable height and foot baseline, complete uncropped anatomy, no frame invasion, no text, no existing game character.

### Deserto — Desperto de Khepra

> Create an original 16-bit pixel-art 8-by-4 sprite sheet of an ancient Egyptian mummy reanimated by radioactive contamination. Weathered linen, small turquoise funerary details, toxic green eyes, no magical portal or scenery. It travels and attacks toward the left. Rows: uneven walk, threatening idle, bite-and-grab lunge, and damage recoil with dust. Transparent background, fixed body scale and feet, every limb inside its own cell, no text or existing game character.

### Cachoeira — Afogado do Véu Verde

> Create an original 16-bit pixel-art 8-by-4 sprite sheet of a drowned former waterfall rescue worker zombie from Minas Gerais, Brazil. Torn orange rescue vest, soaked dark clothing, algae and contaminated water details. It travels and attacks toward the left. Rows: heavy wet walk, swaying idle, bite lunge with both hands visible, and damage recoil with contained splash. Transparent background, vivid colors, constant size and baseline, full body in every cell, no frame invasion, no text.

## Arquivos finais

- `assets/beta4_producao/guarda_rua_8x5_v1.png`
- `assets/beta4_producao/sentinela_dunas_8x5_v1.png`
- `assets/beta4_producao/patrulheiro_cachoeira_8x5_v1.png`
- `assets/beta4_producao/infectado_urbano_8x4_v1.png`
- `assets/beta4_producao/desperto_khepra_8x4_v1.png`
- `assets/beta4_producao/afogado_veu_verde_8x4_v1.png`

## Personagem ambiental — comando da cidade

Modo usado: gerador de imagens integrado do Codex, sem fallback externo. A folha
foi normalizada após a geração para oito células independentes, removendo invasão
entre quadros sem alterar o desenho das poses.

### Tenente policial com apito — grade 8 x 1

> Create one original horizontal eight-frame 16-bit pixel-art sprite sheet of a high-ranking New York police lieutenant performing a whistle-command animation. Dark navy police uniform, peaked police cap, badge and restrained lieutenant insignia; recognizably police, never an army general. Frames: authoritative idle, reach for whistle, raise it, place it at the mouth, whistle with physical reaction, sustain the whistle, lower it and return to idle. Side-isometric view facing right, true transparent background, constant body size and foot baseline, full head/hands/feet, no weapon, no salute, no frame invasion, no text or watermark.

Arquivo final:

- `CENARIOS_BETA4_CONCEITOS/animacao_ambiental/tenente_policia_apito_1x8_v1.png`

## Marinha do Brasil — revisão orientada pela referência do usuário

Modo usado: gerador de imagens integrado do Codex, sem fallback externo. A
imagem enviada foi usada somente como referência de uniforme. Foram ignorados
os textos, marcações vermelhas e todos os modelos não escolhidos. O fundo
xadrez rasterizado foi removido e as duas folhas foram reempacotadas com alfa
real, pivô comum nos pés e margem independente em cada célula.

### Marinheiro praça — grade 8 x 5

> Create one original 16-bit pixel-art 8-by-5 sprite sheet of a lower-ranking Brazilian Navy sailor using only the selected dark-blue enlisted sailor uniform and small white sailor cap from the reference. Preserve the sailor collar, Brazilian flag patch and recognizable praça identity while adding a compact naval carbine. Rows: walking right, ready idle, firing right, physical magazine reload and taking damage. True transparent background, stable body size and feet, full figure and weapon, no frame invasion, no officer cap, camouflage, beige, green or white gala uniform, text or watermark.

### Oficial da Marinha — grade 8 x 1

> Create one original 16-bit pixel-art eight-frame sheet of a senior Brazilian Navy officer using only the selected dark navy-blue officer uniform family from the reference. Peaked naval cap, restrained gold insignia and Brazilian flag patch. Sequence: attention, raise the right hand, complete salute, hold, lower and return to attention. Transparent background, stable proportions and feet, no weapon, no army, police, beige, green, diving or white gala uniform, no frame invasion, text or watermark.

Arquivos finais:

- `assets/beta4_producao/marinheiro_praca_8x5_v2.png`
- `CENARIOS_BETA4_CONCEITOS/animacao_ambiental/oficial_marinha_brasil_saudacao_1x8_v2.png`
