"""Lote 1 — Instagram @appdonagas: 05/11 a 12/11/2026.
Por dia: 1 carrossel no feed (11h30) + 2 stories (8h30 e 18h30). Hoje (05/11): carrossel 17h30 + story 19h.
Gera posts/<id>/<n>.jpg e agenda.json no repositório donagas-conteudo.
Regras: nunca citar a FamaGás; nada de instruções de instalação (registro, mangueira, regulador);
preço só real da região (aqui não citamos valores); segurança só com orientações gerais oficiais.
"""
import json, sys
from pathlib import Path
from arte import A, b64, capa, passo, lista, tela_app, cta, story, render

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "/home/claude/donagas-conteudo")


def m(nome):
    return nome if (A / nome).exists() else "mascote-joia.png"


CEL = lambda w=400, r=-5, b=140: f'<div class="celular" style="width:{w}px;right:70px;bottom:{b}px;transform:rotate({r}deg)"><img src="{b64(A / "tela-inicio.png")}"></div>'
TAGS = "\n\n#gasdecozinha #botijao #entregadegas #gas #appdonagas"
CTA_TXT = "\n\n💬 Comente APP que eu te mando o link para baixar no direct."

FEED = [
    dict(id="2026-11-05-feed-3-toques", quando="2026-11-05T17:30:00-03:00", abordagem="Acabou o gás? Peça em 3 toques",
         legenda="Acabou o gás bem na hora do almoço? 😅 Com o App Dona Gás você pede em 3 toques: informa o CEP, escolhe a oferta da sua região e confirma. Pagamento só na entrega: Pix, cartão ou dinheiro." + CTA_TXT + TAGS,
         slides=[lambda: capa("Acabou o gás?\n[Peça em 3 toques]", "Sem ligar, sem esperar na linha. Você escolhe e a gente leva.", m("mascote-celular.png"), selo="APP GRÁTIS", pagina="1/5"),
                 lambda: passo("1", "Informe o CEP", "Ou toque em \"Usar minha localização\". O app mostra só as revendas que entregam no seu endereço.", CEL(), pagina="2/5", chips=("Sem cadastro para ver preços",)),
                 lambda: passo("2", "Escolha a oferta", "Compare marcas, preço e tempo de entrega. Escolha troca (você devolve o vazio) ou botijão completo.", "", pagina="3/5", chips=("Entrega já inclusa no preço", "Ordene por menor preço", "Ordene por menor tempo")),
                 lambda: passo("3", "Confirme e pronto", "Seu nome e celular só na hora de finalizar. Você paga quando o gás chegar.", "", pagina="4/5", chips=("Pix", "Cartão na maquininha", "Dinheiro")),
                 lambda: cta(m("mascote-celular.png"), pagina="5/5")]),
    dict(id="2026-11-06-feed-pague-na-entrega", quando="2026-11-06T11:30:00-03:00", abordagem="Pague só na entrega",
         legenda="Aqui você só paga quando o gás chega na sua porta. ✅ Pix, cartão na maquininha ou dinheiro: você escolhe na hora." + CTA_TXT + TAGS,
         slides=[lambda: capa("Você só paga\n[quando o gás chega]", "Nada de pagar antes. Escolha Pix, cartão ou dinheiro na entrega.", m("mascote-maquininha.png"), selo="SEM SURPRESA", pagina="1/4"),
                 lambda: lista("Formas de pagamento", ["Pix na hora da entrega", "Cartão de crédito ou débito na maquininha", "Dinheiro (avise se precisa de troco)"], pagina="2/4", mascote=m("mascote-joia.png")),
                 lambda: tela_app("Preço claro [antes de pedir]", "A entrega já está incluída no preço que aparece no app.", pagina="3/4"),
                 lambda: cta(m("mascote-celular.png"), pagina="4/4")]),
    dict(id="2026-11-07-feed-compare-precos", quando="2026-11-07T11:30:00-03:00", abordagem="Compare preços antes de pedir",
         legenda="Antes de pedir, compare! 🔍 No App Dona Gás você vê as marcas, o preço e o prazo das revendas que atendem o seu endereço — tudo na mesma tela." + CTA_TXT + TAGS,
         slides=[lambda: capa("Compare preços\n[antes de pedir]", "Marcas, preço e prazo das revendas da sua região, lado a lado.", m("mascote-pensando.png"), pagina="1/4"),
                 lambda: lista("Do seu jeito", ["Ordene por menor preço", "Ordene por menor tempo de entrega", "Ordene pela melhor avaliação", "Filtre pela marca que você prefere"], pagina="2/4"),
                 lambda: tela_app("Tudo na [mesma tela]", "Os preços e prazos mudam por região: o app mostra os do seu endereço.", pagina="3/4"),
                 lambda: cta(m("mascote-celular.png"), pagina="4/4")]),
    dict(id="2026-11-08-feed-troca-ou-completo", quando="2026-11-08T11:30:00-03:00", abordagem="Troca ou botijão completo",
         legenda="Troca ou botijão completo: qual escolher? 🤔 Se você já tem um botijão vazio, peça a troca. Se não tem, peça o completo. No app você escolhe com um toque." + CTA_TXT + TAGS,
         slides=[lambda: capa("Troca ou\n[botijão completo?]", "Entenda a diferença e peça o certo pelo app.", m("mascote-pensando.png"), pagina="1/4"),
                 lambda: passo("1", "Troca", "Você já tem um botijão vazio: o entregador leva o vazio e deixa o cheio. É o pedido mais comum.", "", pagina="2/4", chips=("Tem botijão vazio em casa?", "Peça a troca")),
                 lambda: passo("2", "Botijão completo", "Você ainda não tem botijão (mudança, casa nova): recebe o botijão cheio e fica com ele.", "", pagina="3/4", chips=("Não tem botijão?", "Peça o completo")),
                 lambda: cta(m("mascote-correndo.png"), pagina="4/4")]),
    dict(id="2026-11-09-feed-economia", quando="2026-11-09T11:30:00-03:00", abordagem="Dicas de economia de gás",
         legenda="5 dicas simples para o seu gás render mais na cozinha 🍳 Salva esse post e manda para quem cozinha aí na sua casa!" + CTA_TXT + TAGS,
         slides=[lambda: capa("5 dicas para o\n[gás render mais]", "Pequenos hábitos na cozinha que fazem diferença no mês.", m("mascote-chef.png"), pagina="1/3"),
                 lambda: lista("Na cozinha", ["Tampe a panela: cozinha mais rápido", "Chama só no fundo da panela, sem passar das bordas", "Use a panela de pressão para feijão e carnes", "Descongele os alimentos antes de cozinhar", "Desligue alguns minutos antes: o calor termina o preparo"], pagina="2/3"),
                 lambda: cta(m("mascote-celular.png"), pagina="3/3")]),
    dict(id="2026-11-10-feed-quanto-dura", quando="2026-11-10T11:30:00-03:00", abordagem="Quanto dura um botijão P13",
         legenda="Quanto tempo dura um botijão P13? Depende de quantas pessoas moram na casa e de quanto se cozinha. Uma dica: anote a data da troca para saber o seu ritmo. E quando acabar, é só repetir o último pedido no app. 😉" + CTA_TXT + TAGS,
         slides=[lambda: capa("Quanto dura um\n[botijão P13?]", "Depende do seu dia a dia. Veja como saber o seu ritmo.", m("mascote-pensando.png"), pagina="1/4"),
                 lambda: lista("Depende de", ["Quantas pessoas moram na casa", "Quantas refeições são feitas no fogão", "Uso do forno e de panelas grandes"], pagina="2/4", mascote=m("mascote-chef.png")),
                 lambda: passo("✓", "Anote a data da troca", "Assim você descobre quanto tempo o botijão dura na sua casa. Quando acabar, repita o último pedido com um toque no app.", CEL(), pagina="3/4"),
                 lambda: cta(m("mascote-celular.png"), pagina="4/4")]),
    dict(id="2026-11-11-feed-seguranca", quando="2026-11-11T11:30:00-03:00", abordagem="Segurança com o botijão",
         legenda="Segurança em primeiro lugar 🛡️ Cuidados simples com o botijão de gás em casa. Em caso de emergência, ligue 193 (Bombeiros)." + CTA_TXT + TAGS,
         slides=[lambda: capa("Cuidados com o\n[botijão em casa]", "Orientações simples para a sua família ficar tranquila.", m("mascote-joia.png"), pagina="1/3"),
                 lambda: lista("Fique atento", ["Mantenha o botijão em pé e em local ventilado", "Confira o lacre na hora da entrega", "Sentiu cheiro de gás? Não acenda luz nem fósforo", "Abra portas e janelas e saia do local", "Emergência: ligue 193 (Bombeiros)"], pagina="2/3"),
                 lambda: cta(m("mascote-celular.png"), pagina="3/3")]),
    dict(id="2026-11-12-feed-repita-pedido", quando="2026-11-12T11:30:00-03:00", abordagem="Repita o último pedido",
         legenda="Já pediu uma vez? Então ficou ainda mais fácil: no App Dona Gás você repete o último pedido com um toque. 🔁 Seus endereços ficam salvos e você acompanha o status pelo app." + CTA_TXT + TAGS,
         slides=[lambda: capa("Repita o pedido\n[com um toque]", "Endereço salvo, oferta favorita e status do pedido no celular.", m("mascote-celular.png"), pagina="1/3"),
                 lambda: lista("Mais praticidade", ["Repita o último pedido com um toque", "Seus endereços ficam salvos", "Acompanhe o status do pedido", "Aviso no celular quando sai para entrega"], pagina="2/3", mascote=m("mascote-correndo.png")),
                 lambda: cta(m("mascote-celular.png"), pagina="3/3")]),
]

STORIES = [
    ("2026-11-05T19:00:00-03:00", "Gás acabou no meio do almoço? [Relaxa.]", "Pelo App Dona Gás você pede em poucos toques e paga só na entrega.", "mascote-joia.png", "marinho"),
    ("2026-11-06T08:30:00-03:00", "Bom dia! Já [baixou o app?]", "Gás de cozinha na sua porta, com preço da sua região.", "mascote-celular.png", "rosa"),
    ("2026-11-06T18:30:00-03:00", "Pix, cartão ou dinheiro: [na entrega]", "Você só paga quando o gás chegar.", "mascote-maquininha.png", "marinho"),
    ("2026-11-07T08:30:00-03:00", "Compare antes de [pedir]", "Marcas, preço e prazo lado a lado no app.", "mascote-pensando.png", "rosa"),
    ("2026-11-07T18:30:00-03:00", "Entrega rápida [na sua porta]", "Veja o prazo da revenda antes de confirmar.", "mascote-correndo.png", "marinho"),
    ("2026-11-08T08:30:00-03:00", "Tem botijão vazio? [Peça a troca]", "Não tem? Peça o completo. Tudo pelo app.", "mascote-joia.png", "rosa"),
    ("2026-11-08T18:30:00-03:00", "Sábado de [cozinha cheia?]", "Deixe o gás garantido para o fim de semana.", "mascote-chef.png", "marinho"),
    ("2026-11-09T08:30:00-03:00", "Domingo é dia de [almoço em família]", "O gás acabou? Pede pelo app e pronto.", "mascote-senhora.png", "rosa"),
    ("2026-11-09T18:30:00-03:00", "Dica: tampe a [panela]", "Cozinha mais rápido e o gás rende mais.", "mascote-chef.png", "marinho"),
    ("2026-11-10T08:30:00-03:00", "Segunda começou [sem gás?]", "Peça em 3 toques e pague na entrega.", "mascote-celular.png", "rosa"),
    ("2026-11-10T18:30:00-03:00", "Anote a [data da troca]", "Assim você sabe quanto o seu botijão dura.", "mascote-pensando.png", "marinho"),
    ("2026-11-11T08:30:00-03:00", "Confira o [lacre]", "Botijão lacrado é segurança para a sua família.", "mascote-joia.png", "rosa"),
    ("2026-11-11T18:30:00-03:00", "Entrega já [inclusa no preço]", "O valor que você vê no app é o que você paga.", "mascote-correndo.png", "marinho"),
    ("2026-11-12T08:30:00-03:00", "Repita o pedido [com um toque]", "Seus endereços ficam salvos no app.", "mascote-celular.png", "rosa"),
    ("2026-11-12T18:30:00-03:00", "Gás de cozinha [na sua porta]", "Baixe grátis: App Store e Google Play.", "mascote-joia.png", "marinho"),
]


def build():
    jobs, agenda = [], []
    for p in FEED:
        imgs = []
        for i, fn in enumerate(p["slides"], 1):
            rel = f"posts/{p['id']}/{i}.jpg"
            jobs.append((fn(), str(OUT / rel), 1080, 1350))
            imgs.append(rel)
        agenda.append({"id": p["id"], "tipo": "carrossel", "abordagem": p["abordagem"], "legenda": p["legenda"], "imagens": imgs, "agendado_para": p["quando"], "aprovado": True})
    for quando, titulo, texto, masc, fundo in STORIES:
        sid = quando[:10] + "-story-" + quando[11:13] + quando[14:16]
        rel = f"posts/{sid}/1.jpg"
        jobs.append((story(titulo, texto, m(masc), fundo), str(OUT / rel), 1080, 1920))
        agenda.append({"id": sid, "tipo": "story", "abordagem": "story: " + titulo.replace("[", "").replace("]", ""), "legenda": "", "imagens": [rel], "agendado_para": quando, "aprovado": True})
    render(jobs)
    path = OUT / "agenda.json"
    atual = json.loads(path.read_text()) if path.exists() else []
    ids = {a["id"] for a in agenda}
    novo = [a for a in atual if a["id"] not in ids] + agenda
    novo.sort(key=lambda a: a["agendado_para"])
    path.write_text(json.dumps(novo, ensure_ascii=False, indent=1))
    print(len(jobs), "imagens;", len(novo), "itens na agenda")


if __name__ == "__main__":
    build()
