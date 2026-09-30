# Prompt final — soldados armados da Beta 4

Modo usado: geração de imagem com a ferramenta integrada do Codex, produzindo
PNG raster transparente. Nenhum sprite antigo foi usado como arte final.

## Estrutura comum

Crie uma sprite sheet 16-bit pixel art de produção para um tower defense 2D
lateral. Use exatamente 8 colunas por 5 linhas, totalizando 40 células iguais e
separadas. Mostre o mesmo personagem inteiro em todas as células, sempre virado
para a direita, com proporção corporal, tamanho da cabeça, escala da arma, centro
do corpo e linha dos pés rigorosamente constantes.

- Linha 1: caminhada com pernas e braços alternados.
- Linha 2: espera com respiração discreta e pés apoiados.
- Linha 3: disparo ou ação própria da arma, com recuo físico legível.
- Linha 4: recarga completa e lenta: retirar munição usada, descartá-la para
  baixo ao lado da bota, buscar a nova munição no colete e encaixá-la na arma.
- Linha 5: reação corporal ao dano e recuperação, com pés no chão.

O cano deve ficar à frente das mãos e apontar horizontalmente para a direita.
Clarão, cápsula e fumaça devem ser pequenos, nascer na arma e permanecer dentro
da mesma célula. Não desenhe projétil viajando, trilha, explosão distante, texto,
símbolo de impacto, sangue, sombra externa, grade, fundo verde ou checkerboard.
Fundo totalmente transparente. Não recorte pés, mãos, arma ou equipamento; não
misture pixels de uma célula na seguinte.

## Variações de equipamento

- Nova York: Xerife/Desert Eagle; SWAT/MP5; precisão/AWM;
  entrada/SPAS-12; antipraga/pulverizador; foguetes/RPG-7.
- Egito: Pistoleiro/Magnum .357; Fuzileiro/SCAR; horizonte/Dragunov SVD;
  artilheiro/MG3; incinerador/lança-chamas; nômade/morteiro portátil.
- Minas Gerais: Marinheiro/Glock 19; Fuzileiro/M16; precisão/TRG-42;
  bombeiro hidráulico; granadeiro/M32 MGL; Homem-Bomba/carga de demolição.

Para o RPG-7, não desenhe foguete em voo: apenas ignição compacta no cano e
pequeno sopro traseiro. Para o pulverizador e o bombeiro, o jato longo pertence
ao VFX do jogo; a folha recebe somente névoa compacta no bocal. Para o morteiro,
mostre o operador ajoelhado colocando o obus no tubo. Para o Homem-Bomba, a
ação é firmar os pés, proteger o detonador e acionar a carga; a explosão pertence
ao VFX separado e nunca é desenhada dentro da folha corporal.

## Contrato usado pelo jogo

As linhas são carregadas nesta ordem fixa: `move`, `idle`, `shoot`, `reload`,
`hit`. A troca de quadros é controlada por delta time; a recarga desacelera a
folha inteira até coincidir com o tempo real definido na ficha da arma.
