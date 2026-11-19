"""Lote 4 — @appdonagas, semana 20/11 a 26/11/2026 (fechamento de 19/11).
Cadência: 1 Reels 19h00 (fábrica) + 1 carrossel 11h30 + 1 story 08h30. Carrosséis com 8 a 9 slides (hipótese 3).
Aprendizado do ciclo 2: Reels de economia/receita com pergunta rendem mais; CTA de opinião não gerou comentário.
"""
import json, sys
from pathlib import Path
from arte import render
from arte2 import (capa_manchete, capa_reacao, rehook, ideia, erro_acerto,
                   lista_grande, tela, cta_sinal, story_v2)

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "/home/claude/donagas-conteudo")
H_ECO = "#economiadomestica #gasdecozinha #dicasdecasa #cozinhapratica"
H_HUM = "#humor #donadecasa #gasdecozinha #vidadecasa"
H_REC = "#receitafacil #receitabarata #cozinhapratica #dicasdecasa"
H_MIT = "#mitoouverdade #gasdecozinha #seguranca #cozinhapratica"
H_APP = "#appdonagas #gasdecozinha #entregadegas #botijao"
APP_TXT = "💬 Comente APP que eu te mando o link para baixar no direct."


def post(pid, quando, pilar, layout, objetivo, cta, abord, legenda, slides):
    n = len(slides)
    return dict(pid=pid, quando=quando, pilar=pilar, layout=layout, objetivo=objetivo, cta=cta,
                abord=abord, legenda=legenda, slides=[(lambda f=f, i=i: f(f"{i}/{n}")) for i, f in enumerate(slides, 1)])

P = []

# 20/11 · D · manchete
P.append(post("5-marmitas-1-domingo", "2026-11-20T11:30", "D", "manchete", "salvar", "Salva o plano",
  "Receita: 5 marmitas em um dia",
  "5 marmitas prontas em um dia só 🍱\n\nCozinhar tudo de uma vez deixa o fogo menos tempo ligado e a semana mais tranquila.\n\n🔖 Salva o plano e manda pra quem vive sem tempo de cozinhar.\n\n" + H_REC,
  [lambda p: capa_manchete("5 marmitas em [um dia só]", "PLANO DA SEMANA", p, "Barato, simples e sem desperdício", "🍱"),
   lambda p: rehook("O segredo é cozinhar tudo de uma vez", p, "🤫", "mascote-chef.png"),
   lambda p: ideia("1", "Arroz e feijão em panelão", "Faça para a semana toda. Uma panela cheia no fogo gasta menos que várias panelas pequenas.", p, mascote="mascote-chef.png"),
   lambda p: ideia("2", "Uma proteína, duas versões", "Frango cozido e desfiado vira recheio num dia e mistura com legumes no outro.", p, "marinho", mascote="mascote-joia.png"),
   lambda p: ideia("3", "Legumes juntos", "Cenoura, chuchu e abobrinha cozinham no mesmo tempo de fogo. Uma panela só.", p, mascote="mascote-chef.png"),
   lambda p: ideia("4", "Esfrie e guarde em potes", "Deixe esfriar um pouco, guarde em potes e congele o que não for comer em poucos dias.", p, "marinho", mascote="mascote-pensando.png"),
   lambda p: lista_grande("Resumo para salvar", ["Arroz e feijão em panelão", "Frango desfiado em 2 versões", "Legumes na mesma panela", "Potes e freezer"], p, "marinho", selo="🔖 Salva esse plano"),
   lambda p: cta_sinal("salvar", "[Salva] o plano da semana", "E manda pra quem vive sem tempo.", "mascote-chef.png", p)]))

# 21/11 · B · mascote
P.append(post("9-coisas-gastam-gas", "2026-11-21T11:30", "B", "mascote", "salvar", "Salva e confere quantas você faz",
  "Economia: 9 coisas que gastam gás sem você perceber",
  "9 coisas que gastam gás sem você perceber 🔥\n\nTem hábito aí que quase todo mundo tem. Desliza e confere quantos são seus.\n\n🔖 Salva e manda pra quem cozinha na sua casa.\n\n" + H_ECO,
  [lambda p: capa_reacao("9 coisas que [gastam gás] sem você perceber", "Eu fazia 5 delas 😬", "mascote-pensando.png", p, "rosa"),
   lambda p: rehook("Conta quantas você faz. Sem mentir 👀", p, "🤥", "mascote-chef.png"),
   lambda p: lista_grande("Na panela", ["Panela sem tampa", "Chama maior que o fundo da panela", "Fogo alto depois que ferveu"], p),
   lambda p: lista_grande("Antes de cozinhar", ["Descongelar a comida no fogo", "Panela grande para pouca comida", "Ferver mais água do que vai usar"], p, "marinho", inicio=4),
   lambda p: lista_grande("E também", ["Fundo da panela sujo de fuligem", "Abrir a porta do forno toda hora", "Fogo ligado esperando a panela"], p, inicio=7),
   lambda p: erro_acerto("O nº 2 engana", "Chama grande cozinha mais rápido", "Se passar do fundo da panela, o calor escapa pelos lados e esquenta só a cozinha.", p, mascote="mascote-chef.png"),
   lambda p: ideia("💡", "Comece pelo mais fácil", "Panela com tampa já faz diferença no mesmo dia. Depois ajuste o resto.", p, "marinho", mascote="mascote-joia.png"),
   lambda p: cta_sinal("salvar", "[Salva] e conta: quantas você faz?", "De 0 a 9. Manda pra quem cozinha aí.", "mascote-chef.png", p)]))

# 22/11 · A · manchete
P.append(post("frases-de-mae-na-cozinha", "2026-11-22T11:30", "A", "manchete", "compartilhar", "Manda pra sua mãe",
  "Humor: frases de mãe na cozinha",
  "Frases que toda mãe diz na cozinha 😂\n\nTem alguma que você já ouviu mil vezes?\n\n👉 Manda pra sua mãe (ela vai rir).\n\n" + H_HUM,
  [lambda p: capa_manchete("Frases de mãe [na cozinha]", "DOMINGO", p, "Qual você já ouviu mil vezes?", "👩‍🍳"),
   lambda p: rehook("Domingo cheira a panela no fogo 🍲", p, "😂", "mascote-chef.png"),
   lambda p: ideia("1", "\"Não mexe nessa panela!\"", "Mesmo que seja só uma olhadinha. Mesmo que você tenha só 40 anos.", p, mascote="mascote-chef.png"),
   lambda p: ideia("2", "\"Já vai sair, tá quase!\"", "Traduzindo: ainda faltam 40 minutos.", p, "marinho", mascote="mascote-pensando.png"),
   lambda p: ideia("3", "\"Olha o fogo!\"", "Dita da sala, de olhos fechados, com precisão de radar.", p, mascote="mascote-joia.png"),
   lambda p: ideia("4", "\"Tampa essa panela!\"", "E ela está certa: com tampa, o gás rende mais.", p, "marinho", mascote="mascote-chef.png"),
   lambda p: ideia("5", "\"Quem vai lavar a louça?\"", "Pergunta retórica. A resposta sempre foi você.", p, mascote="mascote-correndo.png"),
   lambda p: ideia("6", "\"Vem comer que esfria!\"", "Dita três vezes. Na quarta vem com o nome inteiro.", p, "marinho", mascote="mascote-joia.png"),
   lambda p: cta_sinal("compartilhar", "Manda pra [sua mãe] 😂", "E conta qual frase ela mais diz.", "mascote-correndo.png", p)]))

# 23/11 · F · mascote
P.append(post("repita-o-ultimo-pedido", "2026-11-23T11:30", "F", "mascote", "clique", "Comente APP",
  "App: repetir o último pedido",
  "Pediu o gás e gostou? Da próxima vez é mais fácil 😉\n\nNo App Dona Gás você pode repetir o último pedido, conferir a oferta e pagar só na entrega.\n\n" + APP_TXT + "\n\n" + H_APP,
  [lambda p: capa_reacao("Gostou do último pedido? [Repita]", "Sem começar do zero 😉", "mascote-celular.png", p),
   lambda p: rehook("Menos toques, mais sossego", p, "😌", "mascote-celular.png"),
   lambda p: ideia("1", "Peça pelo app", "Digite o CEP, compare as ofertas e escolha a que você prefere.", p, mascote="mascote-celular.png"),
   lambda p: ideia("2", "Gostou? Repita o pedido", "Na próxima vez, abra o app e repita o último pedido.", p, "marinho", mascote="mascote-joia.png"),
   lambda p: ideia("3", "Confira antes de confirmar", "Endereço e oferta da sua região: dê uma olhada rápida e confirme.", p, mascote="mascote-pensando.png"),
   lambda p: ideia("4", "Pague só na entrega", "Pix, cartão ou dinheiro, na hora que o gás chegar.", p, "marinho", mascote="mascote-maquininha.png"),
   lambda p: tela("Tudo na [mesma tela]", "Marca, preço da sua região e pagamento na entrega.", p),
   lambda p: cta_sinal("app", "", "Baixe grátis: App Store e Google Play.", "mascote-celular.png", p)]))

# 24/11 · C · manchete
P.append(post("descongelar-carne", "2026-11-24T11:30", "C", "manchete", "salvar", "Salva pra descongelar do jeito certo",
  "Segurança na cozinha: descongelar carne",
  "Como descongelar carne do jeito certo 🥩\n\n3 jeitos seguros e 1 que muita gente faz errado. O certo também gasta menos gás.\n\n🔖 Salva pra próxima vez que tirar a carne do freezer.\n\n" + H_MIT,
  [lambda p: capa_manchete("Descongelar carne: [3 jeitos certos]", "SEGURANÇA NA COZINHA", p, "E 1 que quase todo mundo erra", "🥩"),
   lambda p: rehook("O erro é o mais comum da cozinha", p, "😬", "mascote-pensando.png"),
   lambda p: erro_acerto("O jeito errado", "Deixar a carne na bancada a noite toda", "Fora da geladeira, as bactérias se multiplicam. Descongele de forma segura.", p, mascote="mascote-pensando.png"),
   lambda p: ideia("1", "Na geladeira", "O jeito mais seguro. Tire do freezer na véspera e deixe de um dia para o outro.", p, mascote="mascote-chef.png"),
   lambda p: ideia("2", "Em água fria", "Dentro de saco fechado, trocando a água de vez em quando. Cozinhe logo depois.", p, "marinho", mascote="mascote-joia.png"),
   lambda p: ideia("3", "No micro-ondas", "Use a função descongelar e leve a carne ao fogo logo em seguida.", p, mascote="mascote-chef.png"),
   lambda p: ideia("💡", "E o gás com isso?", "Carne descongelada cozinha mais rápido. O fogo fica menos tempo ligado.", p, "marinho", mascote="mascote-joia.png"),
   lambda p: lista_grande("Resumo para salvar", ["Geladeira, de véspera", "Água fria em saco fechado", "Micro-ondas e direto ao fogo", "Nunca na bancada"], p, selo="🔖 Salva esse post"),
   lambda p: cta_sinal("salvar", "[Salva] pra descongelar do jeito certo", "E manda pra quem deixa a carne na pia.", "mascote-chef.png", p)]))

# 25/11 · B · mascote
P.append(post("cozinhar-pra-muita-gente", "2026-11-25T11:30", "B", "mascote", "salvar", "Salva o post",
  "Economia: cozinhar para muita gente gastando menos gás",
  "Cozinhando para muita gente? 🍲\n\nFamília grande, visita ou festa: 5 jeitos de gastar menos gás sem trabalhar mais.\n\n🔖 Salva pro próximo almoço grande e manda pra quem sempre cozinha pra todo mundo.\n\n" + H_ECO,
  [lambda p: capa_reacao("Cozinhando pra [muita gente?]", "Gaste menos gás 🔥", "mascote-chef.png", p, "rosa"),
   lambda p: rehook("Panela cheia, fogão ligado, gás indo embora", p, "😅", "mascote-pensando.png"),
   lambda p: ideia("1", "Panelão no lugar de várias", "Uma panela grande e cheia no fogo gasta menos que três pequenas.", p, mascote="mascote-chef.png"),
   lambda p: ideia("2", "Pressão para feijão e carne", "A panela de pressão encurta bastante o tempo de fogo.", p, "marinho", mascote="mascote-joia.png"),
   lambda p: ideia("3", "Adiante o que der", "Pique legumes e descongele a carne de véspera. Menos tempo no fogo no dia.", p, mascote="mascote-pensando.png"),
   lambda p: ideia("4", "Aproveite o forno quente", "Se for assar, coloque dois pratos juntos na mesma fornada.", p, "marinho", mascote="mascote-chef.png"),
   lambda p: ideia("5", "Desligue um pouco antes", "O calor da panela tampada termina o cozimento.", p, mascote="mascote-joia.png"),
   lambda p: lista_grande("Resumo para salvar", ["Panelão no lugar de várias", "Pressão para feijão e carne", "Adiante o preparo", "Forno cheio, não vazio"], p, "marinho", selo="🔖 Salva esse post"),
   lambda p: cta_sinal("salvar", "[Salva] pro próximo almoço grande", "E manda pra quem cozinha pra todo mundo.", "mascote-chef.png", p)]))

# 26/11 · D · manchete
P.append(post("lanche-da-tarde-5-ideias", "2026-11-26T11:30", "D", "manchete", "salvar", "Salva as 5 ideias",
  "Receitas: 5 lanches da tarde com o que tem em casa",
  "Lanche da tarde sem gastar muito e sem complicar 🥪\n\n5 ideias com o que quase toda casa tem.\n\n🔖 Salva e conta qual você faz primeiro.\n\n" + H_REC,
  [lambda p: capa_manchete("Lanche da tarde [sem complicar]", "5 IDEIAS BARATAS", p, "Com o que você já tem em casa", "🥪"),
   lambda p: rehook("A nº 3 vira o lanche favorito da casa", p, "😋", "mascote-chef.png"),
   lambda p: ideia("1", "Bolinho de chuva", "Farinha, ovo, leite, açúcar e fermento. Frite colheradas e passe na canela.", p, mascote="mascote-chef.png"),
   lambda p: ideia("2", "Misto quente de frigideira", "Pão, queijo e presunto. Frigideira tampada, fogo baixo, dois minutos de cada lado.", p, "marinho", mascote="mascote-joia.png"),
   lambda p: ideia("3", "Mingau de aveia", "Aveia, leite e canela. Mexa em fogo baixo até engrossar.", p, mascote="mascote-chef.png"),
   lambda p: ideia("4", "Ovo mexido no pão", "Rápido, barato e pronto em poucos minutos.", p, "marinho", mascote="mascote-joia.png"),
   lambda p: ideia("5", "Banana com canela", "Banana na frigideira com um fio de mel e canela. Sobremesa em 5 minutos.", p, mascote="mascote-chef.png"),
   lambda p: lista_grande("Resumo para salvar", ["Bolinho de chuva", "Misto de frigideira", "Mingau de aveia", "Ovo mexido no pão", "Banana com canela"], p, "marinho", selo="🔖 Salva as 5 ideias"),
   lambda p: cta_sinal("salvar", "[Salva] e conta qual você faz primeiro", "Manda pra quem sempre pergunta o que comer.", "mascote-chef.png", p)]))

assert len(P) == 7

STORIES = [
 ("2026-11-20", "Depois que ferve, [fogo alto ou baixo?]", "Hoje tem dica no Reels das 19h 🔥", "mascote-pensando.png", "marinho", "Responda [ALTO] ou [BAIXO] 💬", "", "comentar"),
 ("2026-11-21", "Quantas coisas [gastam gás] sem você perceber?", "Hoje tem lista de 9 no feed 👀", "mascote-chef.png", "rosa", "Me conta aqui 💬", "", "comentar"),
 ("2026-11-22", "Qual frase sua mãe [mais diz] na cozinha?", "Hoje tem as 6 mais famosas no feed 😂", "mascote-joia.png", "marinho", "Me conta aqui 💬", "", "comentar"),
 ("2026-11-23", "Quanto tempo [dura] seu botijão?", "Anote a data da troca e descubra 📅", "mascote-pensando.png", "rosa", "Responda: [SEMANAS] ou [MESES] 💬", "", "comentar"),
 ("2026-11-24", "A carne de hoje já [saiu do freezer?]", "No feed: 3 jeitos seguros de descongelar 🥩", "mascote-chef.png", "marinho", "Responda [SIM] ou [NÃO] 💬", "", "comentar"),
 ("2026-11-25", "Cuscuz [hoje]?", "Receita de 10 minutos no Reels das 19h 🌽", "mascote-chef.png", "rosa", "Me conta aqui 💬", "", "comentar"),
 ("2026-11-26", "Ceia de fim de ano: [quem cozinha] na sua casa?", "Hoje tem dica no Reels das 19h 🎄", "mascote-pensando.png", "marinho", "Me conta aqui 💬", "", "comentar"),
]

if __name__ == "__main__":
    jobs, novos = [], []
    for p in P:
        d = p["quando"][:10]
        pid = f"{d}-feed-{p['pid']}"
        imgs = []
        for i, fn in enumerate(p["slides"], 1):
            rel = f"posts/{pid}/{i}.jpg"
            jobs.append((fn(), str(OUT / rel), 1080, 1350)); imgs.append(rel)
        novos.append({"id": pid, "tipo": "carrossel", "abordagem": p["abord"], "legenda": p["legenda"], "imagens": imgs,
                      "agendado_para": p["quando"] + ":00-03:00", "aprovado": True,
                      "pilar": p["pilar"], "layout": p["layout"], "objetivo": p["objetivo"], "cta": p["cta"], "lote": "semana4"})
    for d, titulo, texto, masc, fundo, cta_txt, cta_sub, obj in STORIES:
        sid = f"{d}-story-0830-v2"
        rel = f"posts/{sid}/1.jpg"
        jobs.append((story_v2(titulo, texto, masc, fundo, cta_txt, cta_sub), str(OUT / rel), 1080, 1920))
        novos.append({"id": sid, "tipo": "story", "abordagem": "story: " + titulo.replace("[", "").replace("]", ""), "legenda": "",
                      "imagens": [rel], "agendado_para": f"{d}T08:30:00-03:00", "aprovado": True,
                      "pilar": "story", "layout": "story", "objetivo": obj, "cta": cta_txt.replace("[", "").replace("]", ""), "lote": "semana4"})
    render(jobs)
    print(len(jobs), "imagens")
    (OUT / "gerador" / "semana4_novos.json").write_text(json.dumps(novos, ensure_ascii=False, indent=1))
