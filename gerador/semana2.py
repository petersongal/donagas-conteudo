"""Lote 2 — Instagram @appdonagas: 13/11 a 19/11/2026.
Por dia: 3 carrosséis no feed (09h30, 13h00, 19h30) + 1 story (08h30). 21 carrosséis + 7 stories.
Regras: nunca citar a FamaGás; sem instrução de instalação; sem preço (ou 'pode variar por região'); sem prometer tempo de entrega; sem citar cidades.
"""
import json, sys
from pathlib import Path
from semana1 import m, CEL, TAGS, CTA_TXT
from arte import capa, passo, lista, tela_app, cta, story, render

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "/home/claude/donagas-conteudo")
L = lambda t: t + CTA_TXT + TAGS
C = lambda n: (lambda: cta(m("mascote-celular.png"), pagina=f"{n}/{n}"))

P = [
 # ---- 13/11
 dict(id="do-cep-a-porta", abord="Passo a passo do app: do CEP à porta", leg="Do CEP até a sua porta, veja o caminho do pedido no app 📲",
  s=[lambda: capa("Do CEP\n[até a sua porta]", "O caminho do pedido, passo a passo.", m("mascote-celular.png"), selo="PASSO A PASSO", pagina="1/4"),
     lambda: passo("1", "Digite o CEP", "O app mostra as revendas que atendem o seu endereço.", CEL(360), pagina="2/4"),
     lambda: tela_app("Escolha [a oferta]", "Compare marca e preço. Os valores podem variar por região.", pagina="3/4"),
     C(4)]),
 dict(id="receita-farofa", abord="Receita: farofa de frigideira", leg="Farofa crocante de frigideira, pronta em poucos minutos 🥄",
  s=[lambda: capa("Farofa crocante\n[de frigideira]", "Três passos para acompanhar o almoço.", m("mascote-chef.png"), selo="RECEITA RÁPIDA", pagina="1/3"),
     lambda: lista("Como fazer", ["Doure alho e cebola na manteiga", "Junte a farinha aos poucos, mexendo sempre", "Desligue quando estiver douradinha e solta"], pagina="2/3", mascote=m("mascote-chef.png")),
     C(3)]),
 dict(id="faq-botijao-vazio", abord="FAQ: preciso devolver o botijão vazio?", leg="Preciso devolver o botijão vazio? Depende do tipo de pedido 🤔",
  s=[lambda: capa("Preciso devolver\n[o botijão vazio?]", "Depende do pedido que você escolhe.", m("mascote-pensando.png"), selo="PERGUNTAS FREQUENTES", pagina="1/3"),
     lambda: lista("Entenda", ["Na troca: o entregador leva o vazio e deixa o cheio", "No completo: você recebe o botijão cheio e fica com ele", "No app você escolhe com um toque"], pagina="2/3"),
     C(3)]),
 # ---- 14/11
 dict(id="sexta-confira-gas", abord="Antes do fim de semana: confira o gás", leg="Fim de semana chegando? Dê uma olhada no gás antes 👀",
  s=[lambda: capa("Fim de semana\n[chegando?]", "Confira o gás antes que a cozinha encha.", m("mascote-joia.png"), pagina="1/3"),
     lambda: lista("Antes de começar", ["Veja há quantos dias foi a última troca", "Pense nas refeições que vêm pela frente", "Na dúvida, peça antes pelo app"], pagina="2/3", mascote=m("mascote-pensando.png")),
     C(3)]),
 dict(id="receita-sopa", abord="Receita: sopa de legumes", leg="Sopa de legumes quentinha para a noite 🥕",
  s=[lambda: capa("Sopa de legumes\n[quentinha]", "Simples, nutritiva e feita numa panela só.", m("mascote-chef.png"), selo="RECEITA RÁPIDA", pagina="1/4"),
     lambda: lista("Ingredientes", ["Cenoura, batata e abobrinha em cubos", "Cebola e alho", "Sal e cheiro-verde a gosto"], pagina="2/4"),
     lambda: lista("Modo de fazer", ["Refogue a cebola e o alho", "Junte os legumes e cubra com água", "Tampe e cozinhe em fogo médio até amolecer"], pagina="3/4", mascote=m("mascote-chef.png")),
     C(4)]),
 dict(id="faq-avaliacoes", abord="FAQ: dá para ver a avaliação da revenda?", leg="Dá para ver a avaliação da revenda antes de pedir? Dá sim ⭐",
  s=[lambda: capa("Veja a nota\n[antes de pedir]", "Avaliações ajudam na escolha.", m("mascote-pensando.png"), selo="PERGUNTAS FREQUENTES", pagina="1/3"),
     lambda: passo("✓", "Ordene pela melhor avaliação", "No app você ordena as ofertas e escolhe a revenda que mais agrada.", "", pagina="2/3", chips=("Ordene por avaliação", "Compare marca e preço")),
     C(3)]),
 # ---- 15/11
 dict(id="domingo-panelao", abord="Almoço de domingo", leg="Domingo de panelão e mesa cheia 💗 Deixe o gás em dia.",
  s=[lambda: capa("Domingo de\n[mesa cheia]", "Panelão no fogo, gás garantido.", m("mascote-chef.png"), pagina="1/3"),
     lambda: lista("Para o almoço render", ["Tampe as panelas grandes", "Use fogo baixo depois de ferver", "Prepare o que der com antecedência"], pagina="2/3"),
     C(3)]),
 dict(id="pix-cartao-dinheiro", abord="Pix, cartão ou dinheiro: como escolher na entrega", leg="Pix, cartão ou dinheiro? Você escolhe na hora da entrega 💳",
  s=[lambda: capa("Pix, cartão\n[ou dinheiro?]", "Você decide na hora da entrega.", m("mascote-maquininha.png"), selo="PAGUE NA ENTREGA", pagina="1/3"),
     lambda: lista("Como funciona", ["Escolha a forma de pagamento no pedido", "Pague só quando o gás chegar", "Dinheiro? Avise se precisa de troco"], pagina="2/3"),
     C(3)]),
 dict(id="preco-ou-prazo", abord="Menor preço ou menor prazo?", leg="Menor preço ou menor prazo? No app você escolhe o que pesa mais ⚖️",
  s=[lambda: capa("Menor preço\n[ou menor prazo?]", "Você decide o que pesa mais hoje.", m("mascote-pensando.png"), pagina="1/4"),
     lambda: passo("1", "Quer economizar?", "Ordene por menor preço e veja as ofertas mais em conta da sua região.", "", pagina="2/4", chips=("Ordene por menor preço",)),
     lambda: passo("2", "Tem pressa?", "Ordene por menor tempo e confira o prazo informado por cada revenda.", "", pagina="3/4", chips=("Ordene por menor tempo",)),
     C(4)]),
 # ---- 16/11
 dict(id="receita-panqueca", abord="Receita: panqueca de frigideira", leg="Panqueca simples para o jantar 🥞",
  s=[lambda: capa("Panqueca simples\n[de frigideira]", "Massa fácil e recheio do seu jeito.", m("mascote-chef.png"), selo="RECEITA RÁPIDA", pagina="1/3"),
     lambda: lista("Massa", ["Bata 1 ovo, 1 copo de leite e 1 de farinha", "Junte uma pitada de sal", "Doure uma concha por vez na frigideira"], pagina="2/3", mascote=m("mascote-chef.png")),
     C(3)]),
 dict(id="cheiro-de-gas", abord="Sentiu cheiro de gás: orientação geral", leg="Sentiu cheiro de gás? Mantenha a calma e siga estas orientações. Emergência: 193 🛡️",
  s=[lambda: capa("Sentiu\n[cheiro de gás?]", "Orientações gerais para agir com calma.", m("mascote-joia.png"), selo="SEGURANÇA", pagina="1/3"),
     lambda: lista("O que fazer", ["Não acenda luz, fósforo ou isqueiro", "Abra portas e janelas", "Saia do local e ligue 193 (Bombeiros)"], pagina="2/3"),
     C(3)]),
 dict(id="finalize-pedido", abord="Finalizar o pedido: nome e celular", leg="Finalizar o pedido é rápido: só nome e celular 📱",
  s=[lambda: capa("Finalize\n[seu pedido]", "Só nome e celular no final.", m("mascote-celular.png"), selo="PASSO A PASSO", pagina="1/3"),
     lambda: passo("✓", "Sem burocracia", "Você vê as ofertas antes. Nome e celular só na hora de confirmar.", CEL(360), pagina="2/3"),
     C(3)]),
 # ---- 17/11
 dict(id="panela-certa", abord="Economia: panela do tamanho certo", leg="Panela do tamanho certo ajuda o gás a render 🍲",
  s=[lambda: capa("A panela certa\n[faz o gás render]", "Pequenos ajustes, menos desperdício.", m("mascote-chef.png"), selo="ECONOMIA", pagina="1/3"),
     lambda: lista("Combine panela e boca", ["Panela pequena na boca pequena", "A chama não deve passar do fundo", "Tampe sempre que der"], pagina="2/3"),
     C(3)]),
 dict(id="pedir-outro-endereco", abord="Pedir para outro endereço", leg="Vai mandar gás para a casa da mãe? Dá para pedir para outro endereço 🏠",
  s=[lambda: capa("Gás para outro\n[endereço]", "Casa da mãe, da avó ou do filho.", m("mascote-celular.png"), pagina="1/3"),
     lambda: passo("✓", "Informe o CEP de lá", "O app mostra as revendas que atendem aquele endereço.", "", pagina="2/3", chips=("Digite o CEP do destino", "Pague na entrega")),
     C(3)]),
 dict(id="receita-cuscuz", abord="Receita: cuscuz no café da manhã", leg="Cuscuz quentinho no café da manhã ☕",
  s=[lambda: capa("Cuscuz quentinho\n[no café]", "Prático para começar bem o dia.", m("mascote-chef.png"), selo="RECEITA RÁPIDA", pagina="1/3"),
     lambda: lista("Passo a passo", ["Hidrate a flocão com água e sal", "Deixe descansar por alguns minutos", "Cozinhe no vapor até ficar macio"], pagina="2/3", mascote=m("mascote-chef.png")),
     C(3)]),
 # ---- 18/11
 dict(id="hora-de-pedir", abord="Hora de pedir de novo", leg="Já faz um tempo da última troca? Talvez seja hora de pedir de novo 🔁",
  s=[lambda: capa("Será que é\n[hora de pedir?]", "Use o histórico para decidir.", m("mascote-pensando.png"), pagina="1/3"),
     lambda: lista("No app você", ["Vê o último pedido que fez", "Repete com um toque", "Acompanha o status até a entrega"], pagina="2/3", mascote=m("mascote-celular.png")),
     C(3)]),
 dict(id="uso-do-forno", abord="Economia: uso do forno", leg="Forno aceso pede planejamento: aproveite cada fornada 🔥",
  s=[lambda: capa("Forno aceso?\n[aproveite bem]", "Planeje e economize gás.", m("mascote-chef.png"), selo="ECONOMIA", pagina="1/3"),
     lambda: lista("Boas práticas", ["Pré-aqueça só o necessário", "Asse mais de uma coisa por fornada", "Evite abrir a porta sem necessidade"], pagina="2/3"),
     C(3)]),
 dict(id="faq-aviso-pedido", abord="FAQ: serei avisado do pedido?", leg="Serei avisado sobre o meu pedido? Acompanhe pelo app 🔔",
  s=[lambda: capa("Serei avisado\n[do pedido?]", "Você acompanha tudo pelo app.", m("mascote-correndo.png"), selo="PERGUNTAS FREQUENTES", pagina="1/3"),
     lambda: lista("Pelo app", ["Veja o status do pedido", "Receba avisos no celular", "Fale com a revenda se precisar"], pagina="2/3", mascote=m("mascote-celular.png")),
     C(3)]),
 # ---- 19/11
 dict(id="casa-nova", abord="Casa nova: botijão completo", leg="Mudança de casa? Peça o botijão completo e comece sem susto 📦",
  s=[lambda: capa("Casa nova?\n[peça o completo]", "Sem botijão, sem problema.", m("mascote-joia.png"), pagina="1/3"),
     lambda: lista("Para começar", ["Escolha botijão completo no pedido", "Informe o CEP do novo endereço", "Pague só na entrega"], pagina="2/3"),
     C(3)]),
 dict(id="receita-legumes", abord="Receita: legumes salteados", leg="Legumes salteados em poucos minutos 🥦",
  s=[lambda: capa("Legumes\n[salteados]", "Colorido, rápido e leve.", m("mascote-chef.png"), selo="RECEITA RÁPIDA", pagina="1/3"),
     lambda: lista("Como fazer", ["Corte tudo em pedaços parecidos", "Salteie em fogo alto por poucos minutos", "Tempere no final e sirva"], pagina="2/3", mascote=m("mascote-chef.png")),
     C(3)]),
 dict(id="compare-sem-pressa", abord="Compare sem pressa", leg="Antes de confirmar, dê uma olhada em todas as ofertas 🔍",
  s=[lambda: capa("Compare\n[sem pressa]", "Veja todas as ofertas antes de confirmar.", m("mascote-pensando.png"), pagina="1/4"),
     lambda: lista("O que olhar", ["Marca do botijão", "Preço, que pode variar por região", "Prazo informado pela revenda", "Avaliação de outros clientes"], pagina="2/4"),
     lambda: tela_app("Tudo [na tela]", "Veja as ofertas do seu endereço e escolha com calma.", pagina="3/4"),
     C(4)]),
]
assert len(P) == 21

STORIES = [
 ("2026-11-13T08:30:00-03:00", "Sexta! Gás [em dia?]", "Confira antes do fim de semana.", "mascote-joia.png", "marinho"),
 ("2026-11-14T08:30:00-03:00", "Sábado de [cozinha cheia]", "Peça pelo app e pague na entrega.", "mascote-chef.png", "rosa"),
 ("2026-11-15T08:30:00-03:00", "Domingo de [almoço em família]", "Gás garantido na sua porta.", "mascote-correndo.png", "marinho"),
 ("2026-11-16T08:30:00-03:00", "Segunda com [gás em dia]", "Peça em poucos toques pelo app.", "mascote-celular.png", "rosa"),
 ("2026-11-17T08:30:00-03:00", "Pix, cartão ou [dinheiro]", "Você paga só na entrega.", "mascote-maquininha.png", "marinho"),
 ("2026-11-18T08:30:00-03:00", "Já anotou a [data da troca?]", "Assim você sabe quando pedir.", "mascote-pensando.png", "rosa"),
 ("2026-11-19T08:30:00-03:00", "Gás de cozinha [na sua porta]", "Baixe grátis: App Store e Google Play.", "mascote-correndo.png", "marinho"),
]

DIAS = [f"2026-11-{d}" for d in range(13, 20)]
jobs, novos, k = [], [], 0
for d in DIAS:
    for hhmm in ("09:30", "13:00", "19:30"):
        p = P[k]; k += 1
        pid = f"{d}-feed-{p['id']}"
        imgs = []
        for i, fn in enumerate(p["s"], 1):
            rel = f"posts/{pid}/{i}.jpg"
            jobs.append((fn(), str(OUT / rel), 1080, 1350)); imgs.append(rel)
        novos.append({"id": pid, "tipo": "carrossel", "abordagem": p["abord"], "legenda": L(p["leg"]), "imagens": imgs, "agendado_para": f"{d}T{hhmm}:00-03:00", "aprovado": True})
for quando, titulo, texto, masc, fundo in STORIES:
    sid = quando[:10] + "-story-0830"
    rel = f"posts/{sid}/1.jpg"
    jobs.append((story(titulo, texto, m(masc), fundo), str(OUT / rel), 1080, 1920))
    novos.append({"id": sid, "tipo": "story", "abordagem": "story: " + titulo.replace("[", "").replace("]", ""), "legenda": "", "imagens": [rel], "agendado_para": quando, "aprovado": True})
render(jobs)
path = OUT / "agenda.json"
ag = json.loads(path.read_text())
ids = {a["id"] for a in novos}
out = [a for a in ag if a["id"] not in ids] + novos
out.sort(key=lambda a: a["agendado_para"])
path.write_text(json.dumps(out, ensure_ascii=False, indent=1))
print(len(jobs), "imagens;", len(out), "itens")
