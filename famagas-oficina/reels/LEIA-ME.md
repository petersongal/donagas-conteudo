# Reels do @famagas_: como funciona

Mesma fábrica do @appdonagas, com a marca FamaGás (azul #185EA7, amarelo #F8D527, azul-noite #0B2E57; títulos em Barlow Condensed itálico; logo oficial).

## Fluxo
1. A tarefa semanal escreve `reels/roteiros/<id>.json` e dá push.
2. O GitHub Actions (`.github/workflows/reels.yml`) roda `reels/fabrica.py`: quadros da marca → mascote animado → voz em português
   com tempos por palavra (conferida por outra IA) → ffmpeg monta 1080x1920 com gancho na tela, legendas, trilha e cartão final → capa.
3. O vídeo vai para `posts/<id>/reel.mp4` + `capa.jpg` e entra no `agenda.json` como `tipo: "reels"`.
4. O publicador do site (famagas.com.br) posta como Reels e coleta os números.

Sem o segredo `FAL_KEY` no repositório, a fábrica roda em modo teste (sem voz) e não agenda nada.
Custo com a chave: só voz + conferência + trilha (centavos de dólar por Reels). O mascote é animado sem IA.

## O mascote NÃO fala
Regra do Peterson: a boca não sincroniza com a voz, então o mascote nunca mexe a boca como quem fala.
Ele se mexe de corpo inteiro: entra pulando, balança, respira, chega mais perto e troca de pose; nas cenas "foto" a câmera se aproxima e desliza.
`reels/config.json` → `"animacao_mascote": "poses"`. Voltar para IA de vídeo (Kling) só com aprovação do Peterson e conferindo a boca quadro a quadro.
Nunca espelhar o mascote (o logo fica ao contrário).

## Cenas disponíveis
- `{"tipo": "ia", "mascote": "mascote-cafe.png", "fundo": "azul|noite|amarelo|creme", "dur": 5}`: mascote recortado no palco da marca.
  Poses em `gerador/assets/mascote-*.png`. Hoje só existe `mascote-cafe.png`. Os recortes oficiais (joia, chef, panela de pressão, empilhadeira)
  estão no design system (https://claude.ai/artifact/EQVoBmuyv9h56Nkovgcjbu) e precisam ser copiados para cá: sempre mascote inteiro,
  nunca recorte com mão, braço ou pé cortado. Com mais poses, a fábrica troca de pose sozinha no meio da cena.
- `{"tipo": "foto", "imagem": "cena-chef.jpg|cena-panela.jpg|cena-aquecedor.jpg|cena-empilhadeira.jpg", "dur": 5}`: cena completa do mascote com câmera viva.
- `{"tipo": "texto", "titulo": "[destaque] frase curta", "sub": "...", "fundo": "creme|amarelo|noite|azul", "emoji": "🔥", "dur": 4}`.

## Formato do roteiro
```json
{
 "id": "2026-11-20-reels-tema-curto",        // a-z, 0-9 e hífen; começa com a data
 "quando": "2026-11-20T18:30:00-03:00",       // se já passou, vai para o dia seguinte no mesmo horário
 "pilar": "B", "formato": "alerta", "objetivo": "salvar", "cta": "texto curto", "palavra": "CANAL",   // palavra do robô usada (ou null)
 "abordagem": "Reels: ...", "lote": "reels-semanaN",
 "legenda": "gancho na 1ª linha...\n\nCTA\n\n#hashtags",
 "gancho": "Até ~30 letras, [destaque] entre colchetes (2 linhas na tela)",
 "voz": "Narração falada, 25 a 45 palavras. Frases curtas. Começa pelo gancho.",
 "cenas": [ ...3 cenas, alternando tipos... ],
 "final": {"titulo": "CTA com [destaque]", "sub": "complemento curto", "mascote": "mascote-cafe.png"}
}
```
Palavras que o robô responde: CANAL, OFERTA(S), ACHADINHO(S), PROMO, PROMOÇÃO → link do canal; RECEITA(S) → receita + canal.
Palavra nova precisa entrar em `IG_PALAVRAS` (`src/lib/instagram-bot.ts` do site) e de um Publish.

## Conferência obrigatória
Depois que a fábrica roda: baixar `posts/<id>/reel.mp4`, extrair quadros (`ffmpeg -ss`) e olhar com Read (gancho sem cobrir o rosto,
legendas sem sobreposição, mascote inteiro). `posts/<id>/verificacao.json` precisa ter similaridade ≥ 0,85; se a voz trocar uma palavra, reescreva a frase.
Problema → `"aprovado": false` no item da agenda e refazer.

## Voz e trilha
Voz "Liam" (ElevenLabs v4 Turbo, português). Trilha padrão `reels/musica/opcao-1-pagode-leve.mp3` (instrumental, pagode leve com cavaquinho),
gerada na 1ª execução com a chave; alternativa `opcao-2-forro-alegre.mp3`. Troca em `reels/config.json`.

## Fotos reais (pedido do Peterson, 10/11)
Ele quer fotos reais nos Reels para mostrar o assunto (chama, fogão, panela...), de bancos públicos e gratuitos.
- Cena: `{"tipo": "real", "imagem": "chama-azul.jpg", "reserva": "cena-panela.jpg", "dur": 4}` (arquivo em `gerador/assets/fotos/`; se faltar, entra a cena reserva do mascote).
- A sessão do Claude não alcança os bancos de imagem; quem baixa é o GitHub Actions (`reels/fotos.py`, temas em `reels/fotos/pedido.json`):
  Openverse e Wikimedia Commons, só CC0/domínio público, para `gerador/assets/fotos/candidatas/<tema>/` com `creditos.json`.
- **Toda candidata é olhada (Read) antes de usar**; a escolhida é copiada para `gerador/assets/fotos/<nome>.jpg`. Em 10/11, de 32 candidatas só as de chama azul serviam
  (domínio público traz muita foto de arquivo antiga). Download do Unsplash por ID falhou sem chave.
- Para fotos melhores (Pexels/Pixabay/Unsplash) é preciso uma chave gratuita de API como segredo do repositório (ex.: `PEXELS_KEY`) e acrescentar a fonte em `fotos.py`.
- Nunca foto de pessoa famosa, marca concorrente ou criança identificável.
