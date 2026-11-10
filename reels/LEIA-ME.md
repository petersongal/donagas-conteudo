# Reels do @appdonagas — como funciona

**Decisão (10/11/2026):** os Reels são feitos com o **mascote oficial animado por IA**, não com avatar humano.
Motivos: o mascote já é a cara da marca (ninguém confunde com outra empresa), combina com o tom bem-humorado,
não cai no "vale da estranheza" de um humano falso e não entra na regra do Instagram de 2026 que limita o alcance
de contas com pessoas geradas por IA sem rótulo.

**Plataforma:** fal.ai (créditos pré-pagos, sem mensalidade, uma chave para vários modelos).
- Vídeo: Kling 2.6 Pro, imagem → vídeo, sem áudio (US$ 0,07/s). Trocável pela variável MODELO_VIDEO.
- Voz: ElevenLabs v4 Turbo em português (US$ 0,04 por 1.000 caracteres), voz "Brian" (variável VOZ).
- Custo típico: 2 cenas de IA de 5 s + voz ≈ US$ 0,72 por Reels (≈ US$ 22/mês com 1 Reels por dia).

## Fluxo
1. A tarefa semanal (ou a análise de 5 dias) escreve `reels/roteiros/<id>.json` e dá push.
2. O GitHub Actions (`.github/workflows/reels.yml`) roda `reels/fabrica.py`: quadros da marca → IA anima o mascote →
   voz com tempos por palavra → ffmpeg monta 1080x1920 com gancho na tela, legendas animadas e cartão final → capa.
3. O vídeo vai para `posts/<id>/reel.mp4` + `capa.jpg` e entra no `agenda.json` como `tipo: "reels"`.
4. O publicador do app posta como Reels (compartilhado no feed). Métricas aparecem no Admin › Instagram.

Sem o segredo `FAL_KEY` no repositório, a fábrica roda em modo teste (sem IA, sem voz) e não agenda nada.

## Formato do roteiro
```json
{
 "id": "2026-11-20-reels-tema-curto",          // a-z, 0-9 e hífen; começa com a data
 "quando": "2026-11-20T19:00:00-03:00",         // se passar do horário, vai para o dia seguinte
 "pilar": "C", "objetivo": "comentar", "cta": "texto curto", "abordagem": "Reels: ...", "lote": "semanaN",
 "legenda": "gancho na 1ª linha...\n\nCTA\n\n#hashtags",
 "gancho": "Texto curto na tela nos 2,6 s iniciais, [destaque] entre colchetes",
 "voz": "Narração em português falado, 25 a 45 palavras (12 a 18 s). Frases curtas. Começa pelo gancho.",
 "cenas": [
  {"tipo": "ia", "mascote": "mascote-pensando.png", "fundo": "marinho", "dur": 5,
   "movimento": "em inglês: o que o mascote faz (gesto, expressão) + câmera; uma ação só"},
  {"tipo": "texto", "titulo": "[MITO!] frase curta", "sub": "complemento", "fundo": "claro", "emoji": "❌", "dur": 4},
  {"tipo": "ia", "mascote": "mascote-joia.png", "fundo": "rosa", "dur": 5, "movimento": "..."}
 ],
 "final": {"titulo": "CTA com [destaque]", "sub": "complemento curto", "mascote": "mascote-celular.png"}
}
```
Regras: no máximo 2 cenas "ia" por Reels (custo); poses disponíveis em `gerador/assets/mascote-*.png`
(nunca `mascote-senhora.png`); `movimento` simples (um gesto) para a IA não deformar o personagem;
nenhum texto pedido à IA (texto é sempre colocado pela fábrica). **O mascote NÃO fala** (decisão do Peterson, 10/11: a boca não sincroniza com a voz):
o `movimento` descreve só expressões e gestos — pode abrir a boca para reagir (cara de surpresa, sorrisão, risada) e
segurar a expressão, mas nunca mexer a boca como quem fala (sobrancelha, olhar, sorriso, aceno de cabeça, joinha);
nunca escreva "talking", "says" ou "explains". A fábrica já reforça isso no prompt e no negative prompt. Mesmas regras de conteúdo da ESTRATEGIA-CRESCIMENTO.md.

Conferência: depois que a fábrica roda, baixar `posts/<id>/reel.mp4`, extrair quadros (ffmpeg -ss) e olhar com Read.
Se o mascote deformou, marcar `"aprovado": false` no item da agenda e refazer o roteiro com outro movimento.
