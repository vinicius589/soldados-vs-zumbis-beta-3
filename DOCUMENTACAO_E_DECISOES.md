# Guia das informações entregues à equipe

Esta página distingue **o que está implementado** de propostas, protótipos e
revisões históricas. A autoridade para o comportamento da Beta 4 é o código de
[`betas/beta-4/`](betas/beta-4/), conferido pelos testes, e seu
[`README.md`](betas/beta-4/README.md). A raiz mantém um espelho de
compatibilidade. Se outro documento
contradiz esses dois, ele registra uma etapa anterior ou uma ideia ainda não
aprovada; não deve ser tratado como ordem de implementação.

## Versões e critérios

- [`alphas/README.md`](alphas/README.md) e [`betas/README.md`](betas/README.md):
  sequência dos marcos, localização do código e execução de cada Beta.
- [`HISTORICO_DE_VERSOES_PRE_GITHUB.md`](HISTORICO_DE_VERSOES_PRE_GITHUB.md):
  levantamento realizado antes da publicação. Chamar uma versão de **Beta**
  significa que o marco acrescentou conteúdo; chamar de **Alfa** significa
  que a etapa concentrou correções. O rótulo não substitui um changelog
  retroativo que não existia na época.
- [`REVISAO_PRE_GITHUB.md`](REVISAO_PRE_GITHUB.md): fotografia da revisão
  anterior à publicação, não uma declaração de aprovação de todos os visuais.

## Produção Beta 4

- [`README.md`](README.md): instalação, elenco ativo, controles, ondas,
  regras de combate e dificuldade em vigor.
- [`ASSET_MANIFEST.md`](ASSET_MANIFEST.md): inventário e ligação das artes.
- [`ANIMATION_REVIEW.md`](ANIMATION_REVIEW.md): problemas de animação
  investigados e critérios de revisão.
- [`REFERENCIAS_VISUAIS_ARMAS_BETA4.md`](REFERENCIAS_VISUAIS_ARMAS_BETA4.md):
  referências para armas, projéteis e efeitos; cada equipamento requer
  identidade própria, mesmo quando um exemplo de alinhamento já foi aprovado.
- [`assets/audio_sources_cc0/SOURCES.md`](assets/audio_sources_cc0/SOURCES.md):
  origem e licenças das fontes usadas no áudio derivado da versão atual.
- [`PENDENCIAS_PARA_EQUIPE.md`](PENDENCIAS_PARA_EQUIPE.md): questões em aberto,
  risco visual, balanceamento não validado por jogadas completas e protocolo
  de contribuição.
- [`PROXIMAS_DECISOES.md`](PROXIMAS_DECISOES.md): escolhas futuras propostas,
  explicitamente ainda não aprovadas.

## Ideias e decisões anteriores

Os documentos `BETA4_*.md`, `ELENCO_FUTURO_BETA4.md`,
`AMEACAS_BETA4_PROPOSTA.md` e `PROMPT*.md` preservam elenco planejado, fichas,
ameaças sugeridas, história e instruções de produção de arte. Há neles
alternativas descartadas, nomes anteriores e parâmetros de equilíbrio antigos.
São referências de intenção e debate, não uma segunda especificação vigente.
Os experimentos visuais e seus relatórios permanecem em
`CENARIOS_BETA4_CONCEITOS/`, `PIXEL_ART_SPRITES_BETA4/` e nos dois diretórios
`PROTOTIPO_*`. Apenas os recursos necessários para executar ou reproduzir os
testes e ferramentas acompanham a entrega; arquivos rejeitados, caches e
capturas temporárias permanecem fora do repositório.

## Critérios a manter no trabalho seguinte

1. A arte deve ser legível como jogo 16 bits, sem aparência 3D fotográfica;
   o realismo pedido é o da **ação**: passos alternados, postura, recuo,
   recarga, mordida e efeitos conectados ao corpo ou equipamento.
2. Quadro a quadro, o mesmo ator mantém identidade, escala e pivô. Não pode
   haver membros cortados, restos do quadro anterior, fundo verde residual ou
   animação invertida. Os zumbis avançam rumo aos defensores, à esquerda.
3. Disparo, água, chama, gás, torpedo e habilidades começam no ponto de origem
   correto. A potência visual não justifica efeitos gigantes ou balas fora do
   cano. Cada arma tem comportamento próprio.
4. Cada faixa é independente; projéteis, efeitos e inimigos permanecem nela,
   salvo mecânica explicitamente reservada a chefes.
5. A versão atual usa oito cartas fixas por mapa, quatro faixas e doze ondas.
   Mudanças de elenco, seleção, economia ou progressão exigem nova decisão do
   autor, não inferência de um documento antigo.

As amostras prontas para discussão estão em `visual_qa_beta4/entrega/`.
Nenhuma imagem estática isolada prova que a transição em tempo real foi aprovada.
