# Referências visuais das armas — Beta 4

Este arquivo registra por que os disparos, recuos, recargas e projéteis não
usam a animação da SWAT como molde universal. A SWAT é somente a referência
aprovada de contato entre cano, clarão e projétil.

## Critérios usados no jogo

- O clarão nasce na boca do cano e tem tamanho próprio para cada família.
- O projétil começa depois do clarão; ele não fica colado na arma nem aparece
  debaixo do personagem.
- Pistolas 9 mm, submetralhadoras 9 mm, fuzis 5,56, armas 7,62/.338,
  escopetas, granadas, foguetes e torpedos usam silhuetas e ritmos diferentes.
- O projétil visível é uma leitura artística na escala do cenário. Ele não
  representa o diâmetro real em pixels, mas preserva a hierarquia relativa.
- Recuo e recarga permanecem desenhados nas folhas próprias de cada unidade;
  o código não desloca toda a imagem de forma genérica por cima delas.

## Fontes primárias consultadas

### Pistolas

- Glock G19 Gen5 MOS: 9 x 19 mm, carregador padrão de 15 cartuchos e cano de
  102 mm. Fonte: https://us.glock.com/en/products/law-enforcement/pistols/g19-gen5-mos
- Desert Eagle: pistola semiautomática operada a gás, disponível em calibres
  maiores do que a Glock. Fontes e manuais do fabricante:
  https://www.magnumresearch.com/brochures-manuals/

Aplicação: a Glock recebe clarão e recuo menores; a Desert Eagle tem impulso
mais pesado, mas a bala continua pequena no cenário.

### Submetralhadora e fuzis

- HK MP5: 9 x 19 mm, carregador de 15/30 cartuchos, cadência nominal de
  800 disparos por minuto e ejeção à direita.
  Fonte: https://www.heckler-koch.com/en/Products/Military%20and%20Law%20Enforcement/Submachine%20guns/MP5
- FN SCAR-L Mk2: 5,56 x 45 mm NATO, canos de 10 ou 14,5 polegadas,
  operação a gás e carregador de 30 cartuchos.
  Fonte: https://fnherstal.com/en/defence/portable-weapons/fn-scar-l-mk2/
- Colt M16A4: 5,56 x 45 mm NATO e cano de 20 polegadas.
  Fonte: https://www.colt.com/wp-content/uploads/2024/09/24-COLT-2263-COLLATERAL-MLE_Catalog-web-FINAL.pdf

Aplicação: a MP5 usa rajada visual curta e controlada; SCAR e M16 têm clarão
um pouco maior e recuo de fuzil, com diferenças de postura e comprimento.

### Precisão

- SAKO TRG 22/42: rifle de precisão de ação por ferrolho. O manual identifica
  ferrolho, alavanca, porta de ejeção e carregador como partes separadas.
  Fonte: https://media.sako.global/image/upload/v1691732877/TRG_22_42_A1_instruction_manual_v1.9_gc6vrx.pdf

Aplicação: o TRG não reutiliza o ciclo rápido da MP5; o disparo é seguido pela
operação do ferrolho antes do próximo tiro.

## Armas e dispositivos especiais

- SPAS-12: o Agente de Entrada usa dispersão curta de chumbos e recuo de
  ombro; não recebe projétil de pistola.
- MG3/M249: o Tenente Artilheiro usa rajada sustentada, clarão moderado e
  alimentação própria da metralhadora.
- M32/MGL e lançador químico: usam granadas visíveis em arco, sem clarão de
  fuzil e sem feixe contínuo.
- RPG-7: usa um foguete único e separado; não é bala ampliada.
- Morteiro: o projétil nasce no tubo e sobe em arco.
- Barco: usa munição naval curta.
- Submarino: lança somente torpedo para a frente; não possui animação de bala.
- Bombeiro: mantém o corpo e o tempo aprovados; o jato nasce na mangueira.
- Incinerador: a chama cresce em três estágios e é redesenhada a cada quadro,
  sem reaproveitar o traço da água.

## Regra de validação

Toda nova prévia deve mostrar, dentro do cenário, pelo menos: entrada,
disparo, recarga e dano. Para armas contínuas ou lançadores, deve também
mostrar oito quadros consecutivos do efeito para revelar corte, sobreposição,
mudança de escala ou origem incorreta.
