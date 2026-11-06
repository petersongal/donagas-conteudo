"""Lote 1b: reforço para 3 carrosséis/dia (09h30, 13h00, 19h30) e 1 story/dia (08h30). 06/11 a 12/11/2026."""
import json, sys
from pathlib import Path
from semana1 import m, CEL, TAGS, CTA_TXT
from arte import capa, passo, lista, tela_app, cta, story, render

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "/home/claude/donagas-conteudo")
L = lambda t: t + CTA_TXT + TAGS

NEW = [
 dict(id="receita-arroz", abord="Receita: arroz soltinho", leg="Arroz soltinho sem segredo 🍚 Salva essa dica para o almoço de hoje!",
  s=[lambda: capa("Arroz soltinho\n[sem segredo]", "Três passos simples para acertar todo dia.", m("mascote-chef.png"), selo="RECEITA RÁPIDA", pagina="1/4"),
     lambda: lista("Antes de cozinhar", ["Lave o arroz até a água sair mais clara", "Refogue o arroz no alho e no óleo", "Use o dobro de água fervente em relação ao arroz"], pagina="2/4"),
     lambda: lista("Na panela", ["Tampe e deixe em fogo baixo", "Não mexa depois que a água secar", "Desligue e deixe descansar tampado por 5 minutos"], pagina="3/4", mascote=m("mascote-chef.png")),
     lambda: cta(m("mascote-celular.png"), pagina="4/4")]),
 dict(id="receita-feijao", abord="Receita: feijão na pressão", leg="Feijão na panela de pressão rende e economiza gás 🫘 Veja o passo a passo.",
  s=[lambda: capa("Feijão na pressão\n[e economia de gás]", "Cozinha mais rápido e gasta menos.", m("mascote-chef.png"), selo="RECEITA RÁPIDA", pagina="1/4"),
     lambda: lista("Preparo", ["Deixe o feijão de molho de um dia para o outro", "Escorra e use água nova na panela", "Tempere com alho, cebola e louro"], pagina="2/4"),
     lambda: passo("✓", "Dica de ouro", "Conte o tempo só depois que a panela pegar pressão e abaixe o fogo. Assim o gás rende mais.", "", pagina="3/4", chips=("Fogo baixo depois da pressão", "Panela bem fechada")),
     lambda: cta(m("mascote-celular.png"), pagina="4/4")]),
 dict(id="receita-macarrao", abord="Receita: macarrão de uma panela", leg="Macarrão em uma panela só: menos louça e menos gás 🍝",
  s=[lambda: capa("Macarrão em\n[uma panela só]", "Menos louça, menos tempo de fogão.", m("mascote-chef.png"), selo="RECEITA RÁPIDA", pagina="1/3"),
     lambda: lista("Como fazer", ["Coloque macarrão, água e tempero juntos na panela", "Leve ao fogo com a panela tampada", "Mexa de vez em quando até o molho encorpar"], pagina="2/3", mascote=m("mascote-chef.png")),
     lambda: cta(m("mascote-celular.png"), pagina="3/3")]),
 dict(id="receita-ovos", abord="Receita: ovos mexidos cremosos", leg="Ovos mexidos cremosos em poucos minutos 🍳",
  s=[lambda: capa("Ovos mexidos\n[bem cremosos]", "Um truque simples muda tudo.", m("mascote-chef.png"), selo="RECEITA RÁPIDA", pagina="1/3"),
     lambda: lista("O truque", ["Fogo baixo o tempo todo", "Mexa devagar com a colher", "Tire do fogo antes de secar: ele termina de cozinhar na panela"], pagina="2/3"),
     lambda: cta(m("mascote-celular.png"), pagina="3/3")]),
 dict(id="faq-cadastro", abord="FAQ: preciso criar conta?", leg="Preciso criar conta para pedir? Veja como funciona 👇",
  s=[lambda: capa("Preciso criar\n[conta para pedir?]", "A resposta é rápida.", m("mascote-pensando.png"), selo="PERGUNTAS FREQUENTES", pagina="1/3"),
     lambda: passo("✓", "Ver preços é livre", "Informe o CEP e veja as ofertas da região. Nome e celular só no fim do pedido.", CEL(360), pagina="2/3"),
     lambda: cta(m("mascote-celular.png"), pagina="3/3")]),
 dict(id="faq-marca", abord="FAQ: posso escolher a marca?", leg="Posso escolher a marca do meu gás? Pode sim 😉",
  s=[lambda: capa("Posso escolher\n[a marca?]", "Pode! E ainda compara preço.", m("mascote-pensando.png"), selo="PERGUNTAS FREQUENTES", pagina="1/3"),
     lambda: lista("No app você", ["Vê as marcas disponíveis no seu endereço", "Compara preço e prazo lado a lado", "Escolhe a oferta que cabe no seu bolso"], pagina="2/3"),
     lambda: cta(m("mascote-celular.png"), pagina="3/3")]),
 dict(id="faq-entrega-inclusa", abord="FAQ: a entrega está inclusa?", leg="A entrega está inclusa no preço? No app, sim: o valor que você vê já considera a entrega 🛵",
  s=[lambda: capa("A entrega está\n[inclusa?]", "O valor do app é o que você paga.", m("mascote-correndo.png"), selo="PERGUNTAS FREQUENTES", pagina="1/3"),
     lambda: lista("Sem surpresa", ["Entrega já inclusa no preço que aparece", "Você paga só quando o gás chega", "Pix, cartão na maquininha ou dinheiro"], pagina="2/3", mascote=m("mascote-maquininha.png")),
     lambda: cta(m("mascote-celular.png"), pagina="3/3")]),
 dict(id="passo-baixar", abord="Passo a passo: baixe o app", leg="Baixar o App Dona Gás é grátis e leva um minuto 📲",
  s=[lambda: capa("Baixe o app\n[em um minuto]", "Grátis para iPhone e Android.", m("mascote-celular.png"), selo="PASSO A PASSO", pagina="1/4"),
     lambda: passo("1", "Abra a loja", "No iPhone, abra a App Store. No Android, abra o Google Play.", "", pagina="2/4"),
     lambda: passo("2", "Busque Dona Gás", "Procure por Dona Gás, toque em baixar e abra o app.", CEL(360), pagina="3/4"),
     lambda: cta(m("mascote-celular.png"), pagina="4/4")]),
 dict(id="passo-acompanhar", abord="Passo a passo: acompanhe o pedido", leg="Depois de pedir, acompanhe tudo pelo app 📦",
  s=[lambda: capa("Acompanhe\n[seu pedido]", "Você sabe em que etapa ele está.", m("mascote-correndo.png"), selo="PASSO A PASSO", pagina="1/3"),
     lambda: lista("No app", ["Veja o status do pedido", "Receba aviso no celular quando sair para entrega", "Fale com a revenda se precisar"], pagina="2/3"),
     lambda: cta(m("mascote-celular.png"), pagina="3/3")]),
 dict(id="passo-enderecos", abord="Passo a passo: salve seus endereços", leg="Salve seus endereços e peça ainda mais rápido 🏠",
  s=[lambda: capa("Salve seus\n[endereços]", "Casa, trabalho, casa da mãe.", m("mascote-celular.png"), selo="PASSO A PASSO", pagina="1/3"),
     lambda: lista("Vantagens", ["Seu endereço fica salvo para o próximo pedido", "Peça de novo com um toque", "Menos digitação, mais rapidez"], pagina="2/3", mascote=m("mascote-joia.png")),
     lambda: cta(m("mascote-celular.png"), pagina="3/3")]),
 dict(id="antes-de-acabar", abord="Confira o gás antes de receber visita", leg="Vai receber visita ou viajar? Confira o gás antes 👀",
  s=[lambda: capa("Visita chegando?\n[confira o gás]", "Evite o aperto na hora do almoço.", m("mascote-pensando.png"), pagina="1/3"),
     lambda: lista("Faça assim", ["Anote a data da última troca", "Confira se o botijão ainda dura o fim de semana", "Peça pelo app antes de acabar"], pagina="2/3"),
     lambda: cta(m("mascote-celular.png"), pagina="3/3")]),
 dict(id="almoco-familia", abord="Almoço em família com gás garantido", leg="Almoço em família pede cozinha tranquila 💗 Deixe o gás garantido.",
  s=[lambda: capa("Almoço em família\n[sem susto]", "Gás garantido para a mesa cheia.", m("mascote-joia.png"), pagina="1/3"),
     lambda: passo("✓", "Peça com antecedência", "Compare as ofertas da sua região e escolha a que cabe no seu bolso. Pague só na entrega.", "", pagina="2/3", chips=("Troca ou botijão completo", "Pix, cartão ou dinheiro")),
     lambda: cta(m("mascote-celular.png"), pagina="3/3")]),
 dict(id="cozinha-segura", abord="Cozinha segura", leg="Pequenos cuidados deixam a cozinha mais segura 🛡️ Em emergência, ligue 193.",
  s=[lambda: capa("Cozinha mais\n[segura]", "Cuidados simples do dia a dia.", m("mascote-joia.png"), selo="DICAS", pagina="1/3"),
     lambda: lista("No fogão", ["Cabo da panela virado para dentro", "Nunca deixe a panela no fogo sozinha", "Crianças longe do fogão aceso", "Emergência: ligue 193 (Bombeiros)"], pagina="2/3"),
     lambda: cta(m("mascote-celular.png"), pagina="3/3")]),
 dict(id="economize-comparando", abord="Economize comparando", leg="Antes de pedir, compare: o melhor preço pode estar em outra marca 🔍",
  s=[lambda: capa("Compare e\n[economize]", "O melhor preço pode estar em outra marca.", m("mascote-pensando.png"), pagina="1/3"),
     lambda: tela_app("Preços lado a [lado]", "Ordene por menor preço ou menor prazo e escolha a oferta ideal.", pagina="2/3"),
     lambda: cta(m("mascote-celular.png"), pagina="3/3")]),
]
assert len(NEW) == 14
DIAS = ["2026-11-06", "2026-11-07", "2026-11-08", "2026-11-09", "2026-11-10", "2026-11-11", "2026-11-12"]

jobs, novos = [], []
k = 0
for d in DIAS:
    for hhmm in ("09:30", "19:30"):
        p = NEW[k]; k += 1
        pid = f"{d}-feed-{p['id']}"
        imgs = []
        for i, fn in enumerate(p["s"], 1):
            rel = f"posts/{pid}/{i}.jpg"
            jobs.append((fn(), str(OUT / rel), 1080, 1350)); imgs.append(rel)
        novos.append({"id": pid, "tipo": "carrossel", "abordagem": p["abord"], "legenda": L(p["leg"]), "imagens": imgs, "agendado_para": f"{d}T{hhmm}:00-03:00", "aprovado": True})
render(jobs)

path = OUT / "agenda.json"
ag = json.loads(path.read_text())
out = []
for a in ag:
    d, h = a["agendado_para"][:10], a["agendado_para"][11:16]
    if a["tipo"] == "story" and h == "18:30" and d in DIAS:
        continue                       # 1 story a cada 24 h: mantém só o das 8h30
    if a["tipo"] == "carrossel" and h == "11:30" and d in DIAS:
        a["agendado_para"] = f"{d}T13:00:00-03:00"
    out.append(a)
ids = {a["id"] for a in novos}
out = [a for a in out if a["id"] not in ids] + novos
out.sort(key=lambda a: a["agendado_para"])
path.write_text(json.dumps(out, ensure_ascii=False, indent=1))
print(len(jobs), "imagens;", len(out), "itens")
