# @famagas_: estratégia de crescimento orgânico

Documento-mestre. **Toda tarefa que cria conteúdo para o @famagas_ lê este arquivo inteiro antes.** A análise semanal atualiza as regras e o "Diário de testes" no fim.

## 1. Metas do Peterson (10/11/2026)
- **500.000 visualizações por mês** no Instagram, em poucos meses.
- **Passar de 100.000 seguidores.**
- **Sinais de sucesso que mais importam:** (1) pessoas comentando a palavra da chamada (CANAL, OFERTA, RECEITA...), (2) pessoas entrando no canal "Achadinhos e Ofertas FamaGás" no WhatsApp, (3) compartilhamentos e salvamentos.
- **Meta nova (Peterson, 23/11/2026): R$ 3.000 por mês de comissão de afiliado** (Mercado Livre, etiqueta famagaszap; TikTok Shop se valer a pena) com as ofertas do canal "Achadinhos e Ofertas FamaGás", e mais seguidores no canal. O Instagram é a porta de entrada do canal.
- **Verba de anúncio: R$ 10 por dia** (Peterson, 23/11/2026), para seguidores e engajamento nas cidades com loja.
- Propósito: mais clientes, mais satisfeitos e mais fiéis; a FamaGás lembrada na hora de pedir o gás.
- O Claude é o especialista de marketing: analisa a cada 7 dias, decide e executa as mudanças sozinho.

| Prazo | Views/mês | Seguidores | Comentários com palavra/semana | Sinal de saúde |
|---|---|---|---|---|
| 30 dias | 40 mil | +1.000 | 30 | 1 Reels acima de 5 mil views |
| 60 dias | 150 mil | +5.000 | 120 | 1 Reels acima de 30 mil views |
| 90 dias | 500 mil | +15.000 | 400 | 3 a 5 Reels acima de 50 mil views/mês |
| 12 meses | 500 mil+ estável | 100 mil | | |

Honestidade: 100 mil seguidores só com orgânico leva tempo; a análise semanal diz se o ritmo está no caminho e quando vale somar anúncio aos Reels campeões.

## 2. Diagnóstico de 10/11/2026 (linha de base)
- De 03 a 10/11 saíram por dia 1 carrossel de receita (10h30), 1 carrossel do canal (20h) e 2 stories (8h30 e 17h), todos imagem parada.
- Impressão do Peterson: poucas interações, pouco engajamento, pouca chance de viralizar. **Os números por post ainda não eram medidos**; a coleta entra no ar com o Publish do site de 10/11 (`metricas/relatorio.json`). A 1ª análise registra aqui a linha de base real.
- Causas prováveis (as mesmas vistas no @appdonagas): só imagem estática (quem leva conteúdo a não seguidores é o Reels); 4 peças por dia com pouca resposta ensinam o algoritmo que a conta não prende; todo post pede a mesma coisa ("Comente CANAL"); capas que explicam em vez de provocar; todas as peças com a mesma cara.

## 3. Princípios
1. **Reels diário com o mascote animado é o motor de alcance.** Carrossel é o motor de salvamento. Story é relacionamento.
2. **80/20:** 80% entretém, ensina ou faz economizar; 20% chama para o canal ou para a FamaGás.
3. **Cada peça tem UM objetivo de sinal** (compartilhar, salvar ou comentar) e o CTA serve a ele.
4. **Gancho nos 2 primeiros segundos:** texto gigante na tela + movimento + frase que abre curiosidade.
5. **Teste sempre, decida com número.** Toda semana 3 hipóteses; o que vence vira padrão, o que perde sai.

## 4. Público e tom
Famílias e donas de casa das cidades onde a FamaGás tem loja (interior e Grande SP, litoral, Vitória da Conquista-BA). Tom de vizinho de confiança, bem-humorado, que entende de cozinha: frases curtas, linguagem do dia a dia. Assinatura: "Há 40 anos cuidando da sua casa". O mascote é o herói da cozinha (botijão de capa).

## 5. Pilares (rodízio; nenhum mais de 2 vezes seguidas)
| Pilar | Sinal | Exemplos |
|---|---|---|
| A. Humor do dia a dia | Compartilhar | o gás que acaba no domingo; tipos de pessoa quando o gás acaba |
| B. Economia de gás | Salvar | chama amarela; tampa na panela; panela de pressão |
| C. Mitos, verdades e segurança | Comentar/salvar | botijão deitado; validade da mangueira; por que o gás tem cheiro |
| D. Receitas baratas e rápidas | Comentar RECEITA | uma panela só; sem forno; janta de 20 minutos |
| E. FamaGás de verdade | Seguir | 40 anos; frota; lojas; equipe |
| F. Canal de ofertas (máx. 1 a cada 5) | Comentar palavra | achadinhos da semana |

## 6. Formatos de Reels (campo `formato` do roteiro; a análise compara)
`alerta` ("você está perdendo gás"), `mito`, `lista` (3 jeitos), `receita`, `humor`, `canal`, `curiosidade`, `pergunta`. **Desde o lote 3: Reels curtos, narração de 25 a 32 palavras (12 a 16 segundos no total), 3 cenas de 4 a 5 s.** Legenda na tela sempre. Final com CTA único. Ideias a testar: POV, erro x acerto, loop (o fim emenda no começo), pergunta polêmica.

## 7. Palavras de chamada (teste A/B pedido pelo Peterson)
O robô responde no direct a: **CANAL, OFERTA, OFERTAS, ACHADINHO(S), PROMO, PROMOÇÃO** (link do canal) e **RECEITA(S)** (receita + canal). O relatório mostra quantas pessoas comentaram cada palavra em cada post.
- Varie a palavra entre os posts (campo `palavra` do roteiro) e compare. Palavra com mais comentários por mil views vira a principal.
- Palavra só em posts onde há bônus real. No máximo 1 em cada 2 Reels pede palavra; os outros pedem compartilhar, salvar ou opinião.
- **Situação em 19/11:** nenhuma palavra venceu ainda (7 Reels, 1 comentário com palavra). **CANAL segue como principal** (7 comentários nos carrosséis de 03 a 07/11) e **RECEITA é a desafiante**. ACHADINHOS e OFERTA ficam fora dos roteiros novos até o Reels de 23/11 (OFERTA) ser medido.
- Entradas no canal: o WhatsApp não informa por API. A análise semanal anota o número de seguidores do canal (visto no WhatsApp do Mac Mini, quando disponível) e compara com a semana anterior.

## 8. Regras de conteúdo
- Informação técnica só quando for certa. Segurança: só orientação geral + "em caso de cheiro forte de gás, saia do local e ligue 193". **Nunca instrução de instalação** (trocar regulador, apertar conexão etc.).
- P13 = cozinha de casa; P20 = empilhadeira; P45 = comércio/condomínio. Preço só se confirmado; nunca prometer prazo de entrega.
- Cidades só as que têm loja (famagas.com.br/unidades). Sem loja em Sumaré e Sarapuí. Telefone/WhatsApp: 0800 010 9669.
- Humor respeitoso, sem estereótipo. Nunca foto de pessoa famosa. Não citar concorrentes.
- Nada que possa parecer spam para a Meta: sem sorteio fora das regras, sem pedir "marque 10 amigos", sem compra de seguidores, sem automação fora da API oficial.

## 9. Regras visuais
- Cores e fontes da marca; **logo sempre o arquivo oficial**; todo fundo com textura; nada de espaço vazio.
- **Mascote sempre inteiro** (nunca recorte com mão, braço ou pé cortado), nunca espelhado, nunca "falando".
- Gancho não pode cobrir o rosto do mascote; texto fora das áreas do Instagram (250 px no topo, 340 px na base).
- Revisão visual de TODAS as peças antes de publicar.

## 10. Cadência
- **Desde 19/11 (decisão da análise):** só **1 Reels por dia**. Os carrosséis e stories do site acabaram em 18/11 e **não foram renovados**: na semana de 11 a 17/11 os 14 carrosséis fizeram em média 83 views, 0 compartilhamento e 1 salvamento no total; publicar 4 peças fracas por dia ensina o Instagram que a conta não prende.
- Horário: padrão 18h30; em teste 12h00 (ciclo 3).
- Carrossel só volta se for peça forte e isolada (ex.: receita popular com custo, como o escondidinho de 13/11, 366 views) e depois que os Reels passarem de 500 views de média.

## 11. Sistema
- Tudo fica na pasta `famagas-oficina/` do repositório `petersongal/donagas-conteudo` (que já tem a chave da fal.ai). Reels: `reels/roteiros/*.json` → workflow "Oficina FamaGás" → `posts/<id>/` + `agenda.json` → publicador do site posta. Ver `reels/LEIA-ME.md`.
- **Fotos reais** (pedido do Peterson, 10/11): cada Reels deve mostrar o assunto com pelo menos 1 foto real de banco gratuito, sempre revisada antes de usar.
- Números: `metricas/relatorio.json` (a cada 3 h): views, alcance, salvos, compartilhamentos, comentários, curtidas, tempo médio assistido (Reels), seguidores por dia, palavras comentadas por post e por dia.
- Carrosséis e stories atuais ficam no repositório do site (`src/data/instagram-agenda.json` + `public/instagram/`) e dependem de Publish.

## 12. Tráfego pago
Só depois de 5 criativos campeões no orgânico (pelo menos 3 Reels com compartilhamentos + salvamentos ≥ 3x a média). A análise semanal avisa quando chegar a hora e sugere verba e cidades.

---

## Diário de testes

### Ciclo 1: 12/11 a 18/11/2026
- Hipótese 1: Reels com mascote animado alcança pelo menos 5x mais views que carrossel.
- Hipótese 2: palavras diferentes (CANAL x OFERTA x RECEITA x ACHADINHOS) geram quantidades diferentes de comentário; descobrir a melhor.
- Hipótese 3: Reels que abre com cena completa do mascote (tipo "foto") segura mais que o que abre com o mascote recortado no palco.
- **Linha de base real (medida em 12/11, 06h50):** 18 carrosséis publicados de 03 a 10/11 = 2.477 visualizações no total; média por post de **138 visualizações**, 57 de alcance, 5,1 curtidas, 1,5 comentário, 0,1 salvamento e 0,3 compartilhamento. Por tipo: posts fixos 329 views (o "Prazer, FamaGás" foi o melhor da conta: 602 views, 28 curtidas, 8 comentários, 4 compartilhamentos), receita 106, canal 92. Tendência de queda: os carrosséis de 08 a 11/11 ficaram entre 21 e 87 views. Seguidores: 3.028 (parado). Comentários com palavra: CANAL 7 e RECEITA 3 de 03 a 07/11; nenhum de 08 a 11/11.
- **Situação em 12/11 (1 dia de Reels; NÃO é análise, a semana fecha em 17/11):** 1º Reels ("Chama amarela", 11/11 18h35) em 12 horas: 282 views, 214 de alcance (quase 4x o alcance médio de um carrossel), 3 compartilhamentos, 8 curtidas, 1 comentário, 0 salvamento, tempo médio assistido 3,5 s de 18,8 s. Os carrosséis do mesmo dia fizeram 45 e 21 views. As 3 hipóteses seguem **inconclusivas** (1 Reels só); o julgamento é em 19/11 com os 7 Reels.
- Ponto de atenção para 19/11: tempo médio de 3,5 s é baixo; se repetir nos outros Reels, mexer nos 3 primeiros segundos (abertura e gancho).

### Lote 2 (18 a 24/11), preparado em 12/11 para não faltar Reels
Feito antes do fechamento do ciclo 1 porque os roteiros acabavam em 17/11 e a próxima análise é só em 19/11. Mantém as regras atuais e já monta os testes do ciclo 2:
- Hipótese A (abertura): Reels que abre com **foto real** (18, 19 e 21/11) segura mais tempo que o que abre com o mascote no palco (20 e 24/11) ou com cena do mascote (22 e 23/11). Medida: tempo médio assistido.
- Hipótese B (pilar E): um Reels "Prazer, FamaGás" (22/11) repete o resultado do melhor carrossel da conta e traz seguidores.
- Hipótese C (palavras, 2ª rodada com os contextos trocados): OFERTA no Reels do canal (23/11) contra ACHADINHOS (17/11); CANAL em dica de economia (21/11) contra OFERTA (15/11); RECEITA de novo (19/11).
- Regras novas de produção (valem daqui em diante): (1) a soma das durações das cenas fica perto do tamanho da voz (17 a 18 s) e nenhum cartão de texto passa de 7 s na tela; (2) Reels de receita só com receita que existe em famagas.com.br/receitas, porque o robô responde RECEITA com esse link; (3) toda foto real escolhida entra em `gerador/assets/fotos/creditos.json` (fonte e licença); (4) a narração não começa com palavra muito comprida (ex.: "aposentadoria"), porque a legenda vira uma caixa de 2 linhas em cima do rosto do mascote.
- Fotos reais: a busca passou a pedir primeiro bancos atuais (Flickr, StockSnap, Rawpixel, só CC0/domínio público). De 66 candidatas novas, 4 aprovadas: `agua-fervendo.jpg`, `fogao-desligado.jpg`, `chaleira-fogao.jpg`, `pizza-fatia.jpg`. Voz conferida nos 7 (similaridade 0,86 a 1,0; 2 refeitos). Seis dos 7 Reels do lote 2 têm foto real; o do dia 22 (FamaGás de verdade) não tem, porque precisa de foto real da própria FamaGás (loja, caminhão, equipe). Não achei foto boa de botijão brasileiro nem de panelas.

### Ciclo 2: análise de 19/11/2026 (fecha o ciclo 1: 7 Reels de 11 a 17/11)
**Números (relatório do site, coleta de 19/11 06h45):**
- Semana de 11 a 17/11: **2.428 visualizações** em 21 peças (7 Reels = 1.263; 7 carrosséis de receita = 763; 7 do canal = 402). No mês (03 a 18/11): 5.330. **Projeção do mês: cerca de 10 mil views**, contra 40 mil da meta de 30 dias e 500 mil da meta final. Estamos muito abaixo.
- Seguidores: 3.028 → 3.037 (+9 em 8 dias; +7 só em 18 e 19/11).
- Comentários com palavra: **1** na semana (RECEITA, no Reels do macarrão). CANAL, OFERTA e ACHADINHOS: zero. Canal do WhatsApp: não medido.
- Reels, um a um (views / alcance / compart. / tempo médio): chama amarela 492 / 359 / 3 / 3,2 s · botijão deitado 190 / 145 / 1 / 4,5 s · macarrão 89 / 51 / 0 / 6,3 s · gás acaba no domingo 204 / 163 / 0 / 5,3 s · 3 jeitos 186 / 142 / 0 / 5,1 s · mangueira 64 / 39 / 0 / 5,5 s · achadinhos 38 / 20 / 0 / 8,6 s. Média 180 views, 131 de alcance, tempo médio 5,5 s de ~19 s. **Nenhum salvamento em nenhum Reels.** Tendência de queda ao longo da semana.
- Top 3: Reels chama amarela (492), carrossel do escondidinho (366, 20 curtidas), Reels gás acaba no domingo (204). Pior: carrossel do canal de 18/11 (19 views); entre os Reels, achadinhos (38).

**Julgamento das hipóteses do ciclo 1:**
1. Reels alcança 5x mais views que carrossel: **PERDEU.** Reels 180 de média contra 83 dos carrosséis da mesma semana = 2,2x em views e 3,5x em alcance (131 x 37). Reels é melhor, mas não é o salto esperado.
2. Palavras geram quantidades diferentes de comentário: **INCONCLUSIVO.** Só 1 comentário com palavra em 7 Reels; com 40 a 500 views por Reels não dá para comparar palavras.
3. Abrir com cena completa do mascote segura mais que mascote no palco: **INCONCLUSIVO.** Cena: 5,8 s de tempo médio e 201 views (4 Reels); palco: 5,1 s e 153 views (3 Reels). Diferença pequena e amostra pequena.

**Leitura honesta:** o problema não é a palavra nem a abertura; é a distribuição. Os Reels quase não saem da bolha dos seguidores (alcance de 20 a 360 pessoas numa conta de 3 mil) e quem vê assiste só 5 dos 19 segundos. Os Reels com menos views têm tempo médio maior porque só os seguidores fiéis viram. O único Reels com foto real (chama amarela) foi o de mais views; os 6 seguintes eram só mascote e cartão.

**Mudanças executadas em 19/11:**
- Cadência: só 1 Reels por dia (seção 10). Carrosséis e stories diários não foram renovados.
- Reels mais curtos (seção 6): narração de 25 a 32 palavras, 12 a 16 s no total, para subir a parte assistida.
- Reels do formato `canal` (pilar F) fora do lote 3: foi o pior da semana (38 views). Volta só se o de 23/11 (OFERTA) passar da média.
- Dois formatos novos: `curiosidade` ("por que se chama P13?") e `pergunta` que divide ("arroz: lava ou não lava?"), feitos para compartilhar e comentar.
- Fotos reais novas aprovadas (de 47 candidatas): `pao-de-queijo`, `tampa-panela`, `arroz`, `bolo-caseiro`, `panela-pressao`. Ainda sem foto boa de botijão brasileiro nem de feijão.

**Em andamento (lote 2, 18 a 24/11, julgado em 26/11):** hipóteses A (abrir com foto real), B (Reels "Prazer, FamaGás" traz seguidores) e C (palavras em contexto trocado). Primeiro sinal: o Reels de 18/11 (abre com foto real) fez 131 views e 117 de alcance em 15 horas.

**3 hipóteses novas (lote 3, 25/11 a 01/12, julgadas em 03/12):**
- D (duração): Reels curtos (12 a 16 s) têm parte assistida acima de 40% (hoje 29%) e média de views maior que a dos lotes 1 e 2.
- E (horário): Reels ao meio-dia (26, 28 e 30/11) alcança mais gente que às 18h30 (25, 27, 29/11 e 01/12).
- F (formato): `pergunta` e `curiosidade` (28 e 30/11) trazem mais comentários e compartilhamentos que `alerta` de economia.
- Aviso: com 100 a 500 views por Reels os testes têm muito ruído; só vira regra o que ganhar com folga (30% ou mais).

**Anúncio:** ainda não. Nenhum Reels campeão (zero salvamento; 4 compartilhamentos na semana inteira). Reavaliar em 26/11. Se até 03/12 a média não passar de 500 views por Reels, o orgânico sozinho não chega nem perto de 500 mil por mês nesta conta, e a recomendação passa a ser impulsionar com verba pequena o melhor Reels de cada semana nas cidades com loja.

### Mudança de rumo de 23/11/2026 (pedido do Peterson: "resolva, 100% autônomo")
**Números com 12 Reels no ar (23/11):** média ~190 views. Os 2 campeões são verdade que assusta ou surpreende sobre o gás: "Chama amarela? Você está perdendo gás" (497) e "O gás não tem cheiro" (489, maior alcance: 434). Humor fica no meio (156 a 209). Receita (91 e 78), canal (50) e "Prazer, FamaGás" (59) foram os piores. Seguidores parados em ~3.037.
**Regras novas (valem a partir do lote 3):**
- 5 de cada 7 Reels: verdade surpreendente, mito ou alerta sobre gás e economia, sempre com a perda ou o perigo no gancho ("você está perdendo", "não faça"). 2 de cada 7: humor do dia a dia. Receita e Reels "do canal" saem dos Reels (receita continua no robô do direct).
- Fazer "parte 2" de todo Reels que passar de 2x a média.
- Foto real com **movimento de verdade**: cena `{"tipo":"real", "imagem":..., "anima":"<movimento em inglês>"}` anima a foto aprovada com a IA de vídeo da fal.ai (vapor, chama, fervura; sem pessoas). Sem a chave ou se falhar, volta para a câmera viva. Conferir os quadros depois do workflow.
- **Não fazemos react nem corte de vídeo de outras pessoas ou de famosos**: é conteúdo de terceiros (direito autoral) e o Instagram derruba o alcance de conteúdo não original e pode bloquear a conta. Vídeo gravado pelo Peterson na FamaGás entra quando ele puder.
- Lote 3 refeito: o Reels do pão de queijo virou "Cheiro de gás? Não acenda a luz" (parte 2 do campeão). Todos os 7 com foto real animada.
**Anúncio (R$ 10/dia):** impulsionar 1 Reels por semana, sempre o de mais views da semana anterior, por 7 dias, objetivo "mais visitas ao perfil", público local (raio em volta das cidades com loja), 18 a 65 anos. 1ª escolha: "O gás não tem cheiro" (20/11). A conta de anúncio precisa ser ligada pelo Peterson (Turbinar no app do Instagram ou conector de anúncios da Meta).
**Hipóteses novas (julgadas em 03/12, junto com D, E e F):**
- G: foto real animada segura mais tempo assistido que a foto parada (comparar com os lotes 1 e 2).
- H: o Reels impulsionado traz pelo menos 100 seguidores na semana (R$ 70).
- I: a parte 2 de um campeão ("não acenda a luz") passa de 2x a média.
**Afiliados (meta R$ 3.000/mês):** com comissão média de uns 6% a 10% no Mercado Livre, R$ 3.000 pedem cerca de R$ 30 a 50 mil vendidos por mês pelos links. Isso só vem com canal grande (milhares de seguidores ativos) e ofertas boas todo dia. Ordem: (1) Instagram leva gente ao canal (palavra CANAL só no fim dos Reels de economia e no robô do direct); (2) canal com 3 ofertas por dia de casa/cozinha (curadoria semanal das terças); (3) medir seguidores do canal e comissão toda semana; (4) TikTok (repostar os mesmos Reels e depois TikTok Shop) quando o Peterson criar a conta.

