"""Lote 5 — @appdonagas, semana 27/11 a 03/12/2026 (fechamento de 26/11), tema "Gás sem susto".
Cadência: 1 Reels 19h00 (fábrica) + 1 carrossel 11h30 + 1 story 08h30. Carrosséis com 8 a 9 slides (hipótese 3).
Aprendizado do ciclo 3: verdade/alerta sobre gás com perda ou perigo no gancho; receita e humor rendem pouco; "Comente APP" foi o único CTA com comentário.
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

# 27/11 · C · manchete
P.append(post("chama-azul-ou-amarela", "2026-11-27T11:30", "C", "manchete", "salvar", "Salva pra conferir seu fogão",
  "Curiosidade: o que a cor da chama diz",
  "Chama azul ou amarela? 🔥\n\nA cor da chama do fogão conta se está tudo bem. Desliza e confere.\n\n🔖 Salva pra conferir seu fogão hoje.\n\n" + H_MIT,
  [lambda p: capa_manchete("Chama azul ou [amarela?]", "FOGÃO", p, "O que a cor da chama diz", "🔥"),
   lambda p: rehook("A cor entrega se o fogão está bem", p, "👀", "mascote-pensando.png"),
   lambda p: ideia("🔵", "Chama azul", "É a chama normal: firme, regular e sem fumaça. Está tudo certo.", p, mascote="mascote-joia.png"),
   lambda p: ideia("🟠", "Amarela ou laranja", "Pode ser sujeira na boca do fogão. Não ignore e confira.", p, "marinho", mascote="mascote-pensando.png"),
   lambda p: ideia("⚫", "Fundo da panela preto", "Fuligem é sinal de chama ruim. Vale limpar a boca do fogão.", p, mascote="mascote-chef.png"),
   lambda p: ideia("🧽", "Limpe com o fogão frio", "Fogão apagado e frio: escove os furinhos da boca e seque bem.", p, "marinho", mascote="mascote-chef.png"),
   lambda p: ideia("🔧", "Continuou amarela?", "Chame um técnico. Não mexa em mangueira nem regulador por conta própria.", p, mascote="mascote-pensando.png"),
   lambda p: lista_grande("Resumo para salvar", ["Azul e firme: normal", "Amarela ou laranja: atenção", "Fuligem: limpe a boca", "Persistiu? Chame técnico"], p, "marinho", selo="🔖 Salva esse post"),
   lambda p: cta_sinal("salvar", "[Salva] pra conferir seu fogão", "E manda pra quem vive com a panela preta.", "mascote-chef.png", p)]))

# 28/11 · F · mascote
P.append(post("baixe-antes-de-acabar", "2026-11-28T11:30", "F", "mascote", "clique", "Comente APP",
  "App: baixar antes de o gás acabar",
  "Gás acaba sempre na hora errada 😅\n\nBaixe o App Dona Gás agora, com calma, e deixe tudo pronto: endereço salvo, ofertas da sua região e pagamento só na entrega.\n\n" + APP_TXT + "\n\n" + H_APP,
  [lambda p: capa_reacao("Baixe o app [antes] de o gás acabar", "Fica pronto pra quando precisar 😉", "mascote-celular.png", p),
   lambda p: rehook("Gás acaba sempre na hora errada", p, "😅", "mascote-pensando.png"),
   lambda p: ideia("1", "Baixe com calma", "Hoje você está sem pressa. Instale o App Dona Gás e crie sua conta.", p, mascote="mascote-celular.png"),
   lambda p: ideia("2", "Salve seu endereço", "Na hora do aperto, é só confirmar.", p, "marinho", mascote="mascote-joia.png"),
   lambda p: ideia("3", "Compare as ofertas", "Veja marca e oferta da sua região antes de decidir.", p, mascote="mascote-pensando.png"),
   lambda p: ideia("4", "Pague só na entrega", "Pix, cartão ou dinheiro, quando o gás chegar.", p, "marinho", mascote="mascote-maquininha.png"),
   lambda p: ideia("5", "Da próxima vez, repita", "Gostou do pedido? Repita em poucos toques.", p, mascote="mascote-celular.png"),
   lambda p: tela("Tudo na [mesma tela]", "Ofertas da sua região e pagamento na entrega.", p),
   lambda p: cta_sinal("app", "", "Baixe grátis: App Store e Google Play.", "mascote-celular.png", p)]))

# 29/11 · A · manchete
P.append(post("quem-cozinha-em-casa", "2026-11-29T11:30", "A", "manchete", "compartilhar", "Manda pra quem cozinha aí",
  "Humor: sinais de que é você quem cozinha em casa",
  "Você é quem cozinha na sua casa se... 😂\n\nDesliza e conta quantas você marcou.\n\n👉 Manda pra quem cozinha aí.\n\n" + H_HUM,
  [lambda p: capa_manchete("Você é quem [cozinha] na sua casa se...", "DOMINGO", p, "Quantas você marca?", "🍳"),
   lambda p: rehook("Spoiler: quem cozinha reconhece todas", p, "😂", "mascote-chef.png"),
   lambda p: ideia("1", "Sabe de cabeça o que falta", "Arroz, óleo, sal. A lista está na sua cabeça.", p, mascote="mascote-pensando.png"),
   lambda p: ideia("2", "Esquenta o almoço 3 vezes", "Porque ninguém chegou na hora que disse.", p, "marinho", mascote="mascote-chef.png"),
   lambda p: ideia("3", "Ouve \"o que tem pra comer?\"", "De quem acabou de abrir a geladeira. Com a porta aberta.", p, mascote="mascote-joia.png"),
   lambda p: ideia("4", "Sente o cheiro e já sabe", "Feijão no fogo? Sabe até quanto falta pra ficar pronto.", p, "marinho", mascote="mascote-chef.png"),
   lambda p: ideia("5", "Diz \"já vai\"", "E ainda faltam 20 minutos. Todo mundo sabe.", p, mascote="mascote-correndo.png"),
   lambda p: ideia("6", "Desconfia do fogão", "Quando ele faz clique, clique e não acende.", p, "marinho", mascote="mascote-pensando.png"),
   lambda p: cta_sinal("compartilhar", "Manda pra [quem cozinha] aí 😂", "E conta quantas você marcou.", "mascote-chef.png", p)]))

# 30/11 · C · mascote
P.append(post("cheirou-gas-o-que-fazer", "2026-11-30T11:30", "C", "mascote", "salvar", "Salva e mostra pra sua família",
  "Segurança: cheirou gás, o que fazer",
  "Cheirou gás? Calma e siga estes passos 🙏\n\nTodo mundo em casa precisa saber. Em caso de emergência, ligue 193 (Bombeiros).\n\n🔖 Salva e mostra pra sua família.\n\n" + H_MIT,
  [lambda p: capa_reacao("Cheirou gás? [O que fazer]", "Calma. Salva esse post 🙏", "mascote-pensando.png", p, "marinho"),
   lambda p: rehook("Guarda isso: pode ser importante", p, "⚠️", "mascote-pensando.png"),
   lambda p: ideia("1", "Não acenda nada", "Nada de fósforo, isqueiro ou vela. E não mexa em interruptores.", p, mascote="mascote-pensando.png"),
   lambda p: ideia("2", "Abra portas e janelas", "Deixe o ar circular para o gás sair.", p, "marinho", mascote="mascote-joia.png"),
   lambda p: ideia("3", "Saia do local", "Leve todo mundo para fora. Crianças e animais primeiro.", p, mascote="mascote-correndo.png"),
   lambda p: ideia("4", "Ligue 193", "Bombeiros. Ligue de fora de casa e siga as orientações.", p, "marinho", mascote="mascote-celular.png"),
   lambda p: erro_acerto("O erro mais perigoso", "Procurar o vazamento com fogo", "Nunca. O cheiro é o aviso: saia e ligue 193.", p, mascote="mascote-pensando.png"),
   lambda p: lista_grande("Resumo para salvar", ["Não acenda nada", "Abra portas e janelas", "Saia do local", "Ligue 193"], p, "marinho", selo="🔖 Salva esse post"),
   lambda p: cta_sinal("salvar", "[Salva] e mostra pra sua família", "Todo mundo em casa precisa saber.", "mascote-joia.png", p)]))

# 01/12 · B · manchete
P.append(post("sobras-guarde-certo", "2026-12-01T11:30", "B", "manchete", "salvar", "Salva o post",
  "Economia: guardar sobras do jeito certo",
  "Sobrou comida? Guarde do jeito certo 🥘\n\nMenos desperdício, menos fogo ligado e mais dinheiro no bolso.\n\n🔖 Salva pra próxima vez que sobrar.\n\n" + H_ECO,
  [lambda p: capa_manchete("Sobras de comida: [guarde certo]", "ECONOMIA DE CASA", p, "Menos desperdício, menos fogo", "🥘"),
   lambda p: rehook("O erro nº 1 estraga a comida e o bolso", p, "😬", "mascote-pensando.png"),
   lambda p: ideia("1", "Esfrie rápido", "Não deixe a comida mais de 2 horas fora da geladeira.", p, mascote="mascote-chef.png"),
   lambda p: ideia("2", "Use potes pequenos", "Porções menores esfriam mais rápido e você só esquenta o que vai comer.", p, "marinho", mascote="mascote-joia.png"),
   lambda p: ideia("3", "Escreva a data", "Um pedaço de fita e uma caneta resolvem. Você sabe o que é de quando.", p, mascote="mascote-pensando.png"),
   lambda p: ideia("4", "Coma em até 3 dias", "Passou disso, melhor descartar. Sem arriscar.", p, "marinho", mascote="mascote-chef.png"),
   lambda p: ideia("5", "Esquente só o que for comer", "Menos fogo ligado e menos desperdício.", p, mascote="mascote-joia.png"),
   lambda p: lista_grande("Resumo para salvar", ["Esfrie em até 2 horas", "Potes pequenos", "Escreva a data", "Coma em até 3 dias"], p, "marinho", selo="🔖 Salva esse post"),
   lambda p: cta_sinal("salvar", "[Salva] pra próxima vez que sobrar", "E manda pra quem joga comida fora.", "mascote-chef.png", p)]))

# 02/12 · D · manchete
P.append(post("sobremesa-sem-fogao", "2026-12-02T11:30", "D", "manchete", "salvar", "Salva as 3 ideias",
  "Receitas: 3 sobremesas geladas sem ligar o fogão",
  "Sobremesa de fim de ano sem ligar o fogão 🍮\n\n3 ideias que ficam prontas na geladeira e deixam o fogão livre pro prato principal.\n\n🔖 Salva e conta qual você faz primeiro.\n\n" + H_REC,
  [lambda p: capa_manchete("Sobremesa de fim de ano [sem fogão]", "3 IDEIAS GELADAS", p, "Prontas na geladeira", "🍮"),
   lambda p: rehook("A nº 2 some da travessa primeiro", p, "😋", "mascote-chef.png"),
   lambda p: ideia("1", "Mousse de maracujá", "Bata leite condensado, creme de leite e suco concentrado de maracujá. Geladeira por 3 horas.", p, mascote="mascote-chef.png"),
   lambda p: ideia("2", "Pavê de bolacha", "Camadas de bolacha molhada no leite e creme de leite com leite condensado. Geladeira por 4 horas.", p, "marinho", mascote="mascote-joia.png"),
   lambda p: ideia("3", "Salada de frutas gelada", "Frutas picadas, suco de laranja e açúcar a gosto. Geladeira antes de servir.", p, mascote="mascote-chef.png"),
   lambda p: ideia("💡", "E o gás com isso?", "Sobremesa gelada deixa o fogão livre para o prato principal.", p, "marinho", mascote="mascote-joia.png"),
   lambda p: lista_grande("Resumo para salvar", ["Mousse de maracujá", "Pavê de bolacha", "Salada de frutas gelada"], p, selo="🔖 Salva as 3 ideias"),
   lambda p: cta_sinal("salvar", "[Salva] e conta qual você faz primeiro", "Manda pra quem faz a sobremesa da ceia.", "mascote-chef.png", p)]))

# 03/12 · C · mascote
P.append(post("botijao-em-casa-5-cuidados", "2026-12-03T11:30", "C", "mascote", "salvar", "Salva pra conferir hoje",
  "Segurança: 5 cuidados com o botijão em casa",
  "Botijão em casa: 5 cuidados que valem ouro 🛡️\n\nSão simples e protegem a sua família. Confere quantos você já faz.\n\n🔖 Salva pra conferir hoje.\n\n" + H_MIT,
  [lambda p: capa_reacao("Botijão em casa: [5 cuidados]", "Salva pra conferir hoje 👇", "mascote-joia.png", p, "rosa"),
   lambda p: rehook("O nº 4 muita gente esquece", p, "🤔", "mascote-pensando.png"),
   lambda p: ideia("1", "Sempre em pé", "O botijão deve ficar em pé, nunca deitado.", p, mascote="mascote-joia.png"),
   lambda p: ideia("2", "Lugar ventilado", "Evite cantos fechados. O ar precisa circular.", p, "marinho", mascote="mascote-pensando.png"),
   lambda p: ideia("3", "Longe do calor", "Longe de sol forte e de superfícies quentes.", p, mascote="mascote-chef.png"),
   lambda p: ideia("4", "Longe das crianças", "Fora do alcance de crianças e de curiosos.", p, "marinho", mascote="mascote-pensando.png"),
   lambda p: ideia("5", "Sem arrastar nem derrubar", "Ele é pesado. Peça ajuda para carregar.", p, mascote="mascote-joia.png"),
   lambda p: lista_grande("Resumo para salvar", ["Em pé", "Lugar ventilado", "Longe do calor", "Longe das crianças", "Sem arrastar"], p, "marinho", selo="🔖 Salva esse post"),
   lambda p: cta_sinal("salvar", "[Salva] pra conferir hoje", "E manda pra quem tem botijão em casa.", "mascote-joia.png", p)]))

assert len(P) == 7

STORIES = [
 ("2026-11-27", "Acenda o [fósforo] antes de abrir o gás", "Reels hoje às 19h: o erro mais comum 🔥", "mascote-chef.png", "marinho", "Reels hoje às [19h] ▶️", "", "assistir"),
 ("2026-11-28", "Fogão fazendo [clique, clique] e nada?", "Reels hoje às 19h pra você rir 😂", "mascote-pensando.png", "rosa", "Reels hoje às [19h] ▶️", "", "assistir"),
 ("2026-11-29", "Botijão cheio pesa [mais de 25 kg]", "Reels hoje às 19h explica por quê 💪", "mascote-joia.png", "marinho", "Reels hoje às [19h] ▶️", "", "assistir"),
 ("2026-11-30", "Botijão [suando] por fora é normal?", "Reels hoje às 19h: a resposta 💧", "mascote-pensando.png", "rosa", "Reels hoje às [19h] ▶️", "", "assistir"),
 ("2026-12-01", "Panela pequena na [boca grande]?", "Reels hoje às 19h: o calor que escapa 🔥", "mascote-chef.png", "marinho", "Reels hoje às [19h] ▶️", "", "assistir"),
 ("2026-12-02", "Olhou o [lacre] do botijão?", "Reels hoje às 19h: o que conferir na entrega 👀", "mascote-joia.png", "rosa", "Reels hoje às [19h] ▶️", "", "assistir"),
 ("2026-12-03", "Acabou o gás? [3 toques]", "Reels hoje às 19h: peça pelo app 📲", "mascote-celular.png", "marinho", "Reels hoje às [19h] ▶️", "", "assistir"),
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
                      "pilar": p["pilar"], "layout": p["layout"], "objetivo": p["objetivo"], "cta": p["cta"], "lote": "semana5"})
    for d, titulo, texto, masc, fundo, cta_txt, cta_sub, obj in STORIES:
        sid = f"{d}-story-0830-v2"
        rel = f"posts/{sid}/1.jpg"
        jobs.append((story_v2(titulo, texto, masc, fundo, cta_txt, cta_sub), str(OUT / rel), 1080, 1920))
        novos.append({"id": sid, "tipo": "story", "abordagem": "story: " + titulo.replace("[", "").replace("]", ""), "legenda": "",
                      "imagens": [rel], "agendado_para": f"{d}T08:30:00-03:00", "aprovado": True,
                      "pilar": "story", "layout": "story", "objetivo": obj, "cta": cta_txt.replace("[", "").replace("]", ""), "lote": "semana5"})
    render(jobs)
    print(len(jobs), "imagens")
    (OUT / "gerador" / "semana5_novos.json").write_text(json.dumps(novos, ensure_ascii=False, indent=1))
