# Soldados vs Zumbis — proposta de ameaças

Esta lista é uma proposta de design e **não ativa zumbis novos nas hordas**.
Ela fecha exatamente 18 zumbis comuns, 6 sub-bosses e 3 bosses.

## Fundamento da lore

A Hélix-13 combinava energia nuclear, pesquisa farmacêutica e engenharia
biológica. A explosão de Nova York espalhou o primeiro composto. Parte dele foi
levada por uma equipe da empresa à escavação Khepra, no Egito, onde reanimou
corpos preservados e alterou objetos funerários. Outro lote foi descartado
clandestinamente em Minas Gerais, chegou à cachoeira e contaminou banhistas,
equipes de resgate, fauna e vegetação aquática.

Cada mapa possui seis comuns: Normal, Corredor e Rastejante formam a base
compartilhada; os outros três expressam profissão, história e terreno locais.

## 18 zumbis comuns

| Região | Ameaças | Papel tático e justificativa |
|---|---|---|
| Nova York | Infectado Urbano, Corredor da Hélix, Rastejador do Metrô | Base equilibrada, pressão veloz sem stagger e tanque lento. São as vítimas diretas da explosão e da evacuação. |
| Nova York | Policial Infectado | Colete absorve os primeiros tiros; representa a primeira linha abandonada pela Hélix. |
| Nova York | Cientista da Hélix | Libera nuvem corrosiva com meia vida; carrega o próprio composto do acidente. |
| Nova York | Técnico da Subestação | Pulso elétrico atrasa uma recarga; traz a infraestrutura destruída para o combate. |
| Egito | Desperto de Khepra, Corredor das Dunas, Rastejador da Cripta | Base regional, corrida constante e corpo funerário resistente. |
| Egito | Arqueiro da Necrópole | Ataque remoto fraco; obriga o jogador a ter precisão sem transformar todo zumbi em tanque. |
| Egito | Hospedeiro de Escaravelhos | Libera enxame curto ao morrer; nasce da fauna alterada dentro das múmias. |
| Egito | Saqueador Canópico | Procura e rouba suprimentos; conecta o perigo à escavação e à economia da partida. |
| Cachoeira | Afogado da Cachoeira, Corredor da Margem, Rastejador do Barranco | Base regional, pressão terrestre rápida e ameaça lenta de mordida pesada. |
| Cachoeira | Surfista Infectado | Usa os canais e desacelera em terra; respeita a geografia da água. |
| Cachoeira | Mergulhador Afogado | Fica submerso e emerge perto da defesa aquática; deriva das equipes de resgate. |
| Cachoeira | Pescador da Praga | Rede reduz temporariamente a cadência; transforma uma profissão local em controle tático. |

## 6 sub-bosses

| Região | Sub-boss | Comportamento, habilidade e contraponto |
|---|---|---|
| Nova York | Demolidor do Metrô | Marretada em área contra casas próximas. Lento e vulnerável a corrosão e fogo concentrado. |
| Nova York | Bruto da Quarentena | Armadura frontal e função de tanque. RPG, SPAS-12 próxima e antipraga quebram as placas. |
| Egito | Guardião do Sarcófago | Escudo ritual e golpe de empurrão. Fogo e morteiro destroem sua formação. |
| Egito | Sacerdote da Praga | Fortalece infectados próximos e fica na retaguarda. Deve virar prioridade do sniper. |
| Cachoeira | Baiacu Mutante | Infla e espalha espinhos ao morrer, somente na própria faixa. Exige distância e espaçamento. |
| Cachoeira | Salva-Vidas Colossal | Alterna água e margem e prepara uma investida. Água pressurizada interrompe a preparação. |

## 3 bosses

### Diretor Zero da Hélix — Nova York

O executivo que autorizou o descarte usou em si o protótipo de sobrevivência da
empresa. Alterna blindagem, convocação de funcionários infectados e sobrecarga
do traje. Sua chegada ativa chuva tóxica; durante a sobrecarga o núcleo fica
exposto, criando uma janela clara de dano em vez de uma esponja de vida.

### Faraó Khepra Reanimado — Egito

O soberano da câmara real despertou quando a contaminação alcançou a pirâmide.
Comanda três fases, acende as piras, cria tempestade de areia que reduz alcance
e pode reanimar um zumbi comum. O intervalo entre decretos é sua vulnerabilidade.

### Colosso do Véu Verde — Cachoeira

Massa de algas, lixo, peixes e corpos formada no ponto mais contaminado. Alterna
água e margem sem teleportar. Regenera na água e causa um tremor na cachoeira;
na margem perde regeneração e fica exposto a explosivos.

## Princípios de balanceamento

- Comuns alteram uma regra por vez e continuam legíveis em grupo.
- Sub-bosses combinam resistência com uma habilidade que exige mudança tática.
- Bosses mudam cenário e ritmo, mas sempre exibem uma janela de vulnerabilidade.
- Nenhuma ameaça troca de faixa sem uma animação e uma justificativa territorial.
- Invocação, roubo, corrosão e controle possuem limite para não remover o
  controle do jogador.

Os dados completos de lore, comportamento, habilidade e contraponto estão em
`beta4_threat_proposals.py`, com validação automática das quantidades.
