"""Lote 3 — @appdonagas no estilo da ESTRATEGIA-CRESCIMENTO.md (refeito em 10/11/2026).
Substitui o que estava agendado de 10/11 19h30 a 19/11.
Cadência (decisão do Peterson, 10/11): 2 carrosséis por dia (11h30 e 19h30) + 1 story (08h30).
Pilares: A humor/identificação · B economia · C mitos e verdades · D receitas · E gente de verdade · F app (máx. 1 em 5).
"""
import json, sys
from pathlib import Path
from arte import render
from arte2 import (capa_manchete, capa_reacao, rehook, ideia, erro_acerto,
                   lista_grande, tela, cta_sinal, story_v2)

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "/home/claude/donagas-conteudo")

H_ECO = "#economiadomestica #gasdecozinha #dicasdecasa #cozinhapratica"
H_HUM = "#humor #donadecasa #gasdecozinha #vidadecasa"
H_REC = "#receitafacil #receitabarata #jantarrapido #cozinhapratica"
H_MIT = "#mitoouverdade #gasdecozinha #segurancaemcasa #botijao"
H_APP = "#appdonagas #gasdecozinha #entregadegas #botijao"
APP_TXT = "💬 Comente APP que eu te mando o link para baixar no direct."


def post(pid, quando, pilar, layout, objetivo, cta, abord, legenda, slides):
    n = len(slides)
    return dict(pid=pid, quando=quando, pilar=pilar, layout=layout, objetivo=objetivo, cta=cta,
                abord=abord, legenda=legenda, slides=[(lambda f=f, i=i: f(f"{i}/{n}")) for i, f in enumerate(slides, 1)])


P = []

# ---------------------------------------------------------------- 10/11 19h30 · A
P.append(post("tipos-quando-o-gas-acaba", "2026-11-10T19:30", "A", "mascote", "compartilhar", "Marca quem é o nº 3",
  "Humor: tipos de pessoa quando o gás acaba",
  "Toda casa tem pelo menos um desses quando o gás acaba 😂\n\nDesliza e descobre qual é o seu. Eu confesso: já fui o nº 3.\n\n👉 Marca aqui quem é o nº 3 da sua casa.\n\n" + H_HUM,
  [lambda p: capa_reacao("Tipos de pessoa quando o [gás acaba]", "Eu já fui o nº 3 😅", "mascote-pensando.png", p),
   lambda p: rehook("Você é qual? Seja sincero 👀", p, "🤔"),
   lambda p: ideia("1", "O que balança o botijão", "Sacode, escuta o barulhinho e jura que dá pra mais uma semana.", p, mascote="mascote-pensando.png"),
   lambda p: ideia("2", "O que nega até o fim", "\"Deve ser o acendedor.\" Troca a pilha, testa três vezes... e nada.", p, "marinho", mascote="mascote-joia.png"),
   lambda p: ideia("3", "O do arroz pela metade", "Só descobre quando a panela já está no fogo e a visita, no portão.", p, mascote="mascote-chef.png"),
   lambda p: ideia("4", "O que pede antes de acabar", "Anota a data da troca e pede com calma. Esse é raro, mas existe! 🏆", p, "marinho", mascote="mascote-celular.png"),
   lambda p: cta_sinal("compartilhar", "Marca quem é o [nº 3] da sua casa 😂", "Manda pra família e descobre quem se identifica.", "mascote-correndo.png", p)]))

# ---------------------------------------------------------------- 11/11 11h30 · B
P.append(post("feijao-gastando-gas", "2026-11-11T11:30", "B", "manchete", "salvar", "Salva pra não esquecer",
  "Economia: feijão gastando gás à toa",
  "Seu feijão pode estar gastando gás à toa 🫘\n\nSão 4 hábitos simples que fazem o fogo ficar menos tempo ligado. O nº 2 quase todo mundo erra.\n\n🔖 Salva pra lembrar no próximo feijão e manda pra quem cozinha na sua casa.\n\n" + H_ECO,
  [lambda p: capa_manchete("Seu feijão está [gastando gás] à toa", "ECONOMIA", p, "4 hábitos que fazem o gás render mais", "🫘"),
   lambda p: rehook("O erro nº 2 quase todo mundo comete", p, "😬", "mascote-pensando.png"),
   lambda p: ideia("1", "Deixe de molho antes", "Algumas horas na água antes de cozinhar: o feijão amolece mais rápido e o fogo fica menos tempo ligado.", p, mascote="mascote-chef.png"),
   lambda p: ideia("2", "Abaixe o fogo quando a pressão pegar", "Começou a chiar? Fogo baixo. O chiado constante já basta para cozinhar.", p, "marinho", mascote="mascote-joia.png"),
   lambda p: ideia("3", "Use a panela de pressão", "Feijão, carne e grão-de-bico cozinham em bem menos tempo do que na panela comum.", p, mascote="mascote-chef.png"),
   lambda p: ideia("4", "Faça mais e congele", "Cozinhe uma panelada e congele em porções. Uma vez no fogo vale por vários dias.", p, "marinho", mascote="mascote-correndo.png"),
   lambda p: lista_grande("Resumo para salvar", ["Feijão de molho antes", "Fogo baixo quando a pressão pegar", "Prefira a panela de pressão", "Cozinhe mais e congele"], p, selo="🔖 Salva esse post"),
   lambda p: cta_sinal("salvar", "[Salva] pra lembrar no próximo feijão", "E manda pra quem cozinha na sua casa.", "mascote-chef.png", p)]))

# ---------------------------------------------------------------- 11/11 19h30 · C
P.append(post("botijao-deitado-mito", "2026-11-11T19:30", "C", "mascote", "comentar", "Qual você achava verdade?",
  "Mitos e verdades: botijão deitado",
  "Botijão deitado rende mais? 🤔\n\nTem muita coisa sobre gás de cozinha que a gente ouve desde criança e nem sempre é verdade. Separei 3 mitos e verdades.\n\n💬 Comenta o número do que você achava que era verdade.\n\n" + H_MIT,
  [lambda p: capa_reacao("Botijão deitado [rende mais?]", "Minha tia jura que sim 🤔", "mascote-pensando.png", p, "rosa"),
   lambda p: rehook("A resposta surpreende muita gente", p, "😮", "mascote-joia.png"),
   lambda p: erro_acerto("1. Botijão deitado", "Deitar o botijão faz o gás render mais", "O botijão fica sempre em pé. Deitado não rende mais e não é seguro.", p),
   lambda p: erro_acerto("2. O cheiro do gás", "O gás de cozinha tem cheiro natural", "Ele quase não tem cheiro. Recebe um aditivo de propósito para você perceber um vazamento.", p, "MITO", "VERDADE", "mascote-joia.png"),
   lambda p: erro_acerto("3. Chama amarela", "Chama amarela é normal", "A chama boa é azul. Amarelada pede limpeza do queimador ou avaliação de um técnico.", p, "MITO", "VERDADE", "mascote-pensando.png"),
   lambda p: cta_sinal("comentar", "Qual você achava que era [verdade]?", "Comenta o número: 1, 2 ou 3 👇", "mascote-pensando.png", p)]))

# ---------------------------------------------------------------- 12/11 11h30 · D
P.append(post("macarrao-alho-oleo", "2026-11-12T11:30", "D", "manchete", "salvar", "Salva a receita",
  "Receita: macarrão alho e óleo em 15 minutos",
  "Janta pronta em 15 minutos com 5 ingredientes 🍝\n\nMacarrão alho e óleo: barato, rápido e uma panela só para o macarrão.\n\n🔖 Salva para aquele dia corrido e manda pra quem vive dizendo que não sabe cozinhar 😄\n\n" + H_REC,
  [lambda p: capa_manchete("Janta pronta em [15 minutos]", "RECEITA BARATA", p, "Macarrão alho e óleo com 5 ingredientes", "🍝"),
   lambda p: rehook("Você provavelmente já tem tudo em casa", p, "🧄", "mascote-chef.png"),
   lambda p: lista_grande("Ingredientes", ["Macarrão espaguete", "4 dentes de alho fatiados", "Azeite ou óleo", "Sal e pimenta-do-reino", "Cheiro-verde (opcional)"], p),
   lambda p: lista_grande("Modo de fazer", ["Cozinhe o macarrão na água com sal, com a panela tampada até ferver", "Doure o alho no azeite em fogo baixo", "Misture o macarrão escorrido, tempere e sirva"], p, "marinho"),
   lambda p: ideia("💡", "Dica que economiza gás", "Tampe a panela para a água ferver mais rápido e só destampe na hora de colocar o macarrão.", p, mascote="mascote-chef.png"),
   lambda p: cta_sinal("salvar", "[Salva] para o dia corrido", "E manda pra quem diz que não sabe cozinhar 😄", "mascote-chef.png", p)]))

# ---------------------------------------------------------------- 12/11 19h30 · F
P.append(post("visita-chegando-sem-gas", "2026-11-12T19:30", "F", "mascote", "clique", "Comente APP",
  "App: acabou o gás com visita chegando",
  "Acabou o gás e a visita já está chegando? 😱\n\nRespira. Dá pra resolver pelo celular, sem ligar para ninguém e pagando só na entrega.\n\n" + APP_TXT + "\n\n" + H_APP,
  [lambda p: capa_reacao("Acabou o gás e a [visita está chegando]", "E agora?! 😱", "mascote-correndo.png", p),
   lambda p: rehook("Calma. Dá pra resolver em 3 toques", p, "😮‍💨", "mascote-celular.png"),
   lambda p: ideia("1", "Abra o app e digite o CEP", "Aparecem as revendas que entregam no seu endereço.", p, mascote="mascote-celular.png"),
   lambda p: tela("2. Compare [tudo]", "Marca, preço da sua região e prazo de cada revenda, na mesma tela.", p),
   lambda p: ideia("3", "Pague só na entrega", "Pix, cartão ou dinheiro, na hora que o gás chegar.", p, "marinho", mascote="mascote-maquininha.png"),
   lambda p: cta_sinal("app", "", "Baixe grátis: App Store e Google Play.", "mascote-celular.png", p)]))

# ---------------------------------------------------------------- 13/11 11h30 · A
P.append(post("5-fases-sem-gas", "2026-11-13T11:30", "A", "manchete", "compartilhar", "Marca quem já passou pela fase 3",
  "Humor: as 5 fases de quem fica sem gás",
  "As 5 fases de quem fica sem gás 😂\n\nDa negação à aceitação, todo mundo já passou por pelo menos três.\n\n👉 Marca quem já ficou preso na fase 3.\n\n" + H_HUM,
  [lambda p: capa_manchete("As 5 fases de quem [fica sem gás]", "SEXTA-FEIRA", p, "Você já passou por quantas?", "😩"),
   lambda p: ideia("1", "Negação", "\"Deve ser o acendedor.\" Troca a pilha e tenta de novo.", p, mascote="mascote-pensando.png"),
   lambda p: ideia("2", "Raiva", "\"Logo hoje?! Com o feijão no fogo?!\"", p, "marinho", mascote="mascote-joia.png"),
   lambda p: ideia("3", "Barganha", "\"Será que dá pra terminar no micro-ondas?\"", p, mascote="mascote-pensando.png"),
   lambda p: ideia("4", "Tristeza", "Olhar para o arroz pela metade em silêncio.", p, "marinho", mascote="mascote-chef.png"),
   lambda p: ideia("5", "Aceitação", "Pede o gás pelo celular, paga na entrega e promete pedir antes da próxima vez.", p, mascote="mascote-celular.png"),
   lambda p: cta_sinal("compartilhar", "Marca quem travou na [fase 3] 😂", "Manda no grupo da família.", "mascote-correndo.png", p)]))

# ---------------------------------------------------------------- 13/11 19h30 · B
P.append(post("7-habitos-gas-render", "2026-11-13T19:30", "B", "mascote", "salvar", "Salva o post",
  "Economia: 7 hábitos para o gás render",
  "7 hábitos que fazem o botijão durar mais 🔥\n\nNenhum deles custa nada. O nº 5 pouca gente faz.\n\n🔖 Salva e confere quantos você já faz.\n\n" + H_ECO,
  [lambda p: capa_reacao("7 hábitos que fazem o [gás durar mais]", "O nº 5 pouca gente faz 👀", "mascote-chef.png", p, "rosa"),
   lambda p: lista_grande("Na hora de cozinhar", ["Tampe a panela", "A chama não passa do fundo", "Panela de pressão para grãos e carnes"], p),
   lambda p: lista_grande("Antes e depois", ["Descongele antes de ir ao fogo", "Desligue minutos antes: o calor termina o preparo", "Fundo da panela limpo esquenta melhor", "No forno, asse dois pratos juntos"], p, "marinho", inicio=4),
   lambda p: ideia("5", "Por que funciona?", "Panela tampada e quente segue cozinhando por alguns minutos, mesmo com o fogo desligado.", p, mascote="mascote-chef.png"),
   lambda p: cta_sinal("salvar", "[Salva] e confere quantos você já faz", "Conta nos comentários: de 0 a 7?", "mascote-joia.png", p)]))

# ---------------------------------------------------------------- 14/11 11h30 · C
P.append(post("por-que-gas-tem-cheiro", "2026-11-14T11:30", "C", "manchete", "comentar", "Você sabia? SIM ou NÃO",
  "Curiosidade: por que o gás tem cheiro",
  "O gás de cozinha quase não tem cheiro. Então de onde vem aquele cheiro forte? 👃\n\nÉ um alarme colocado de propósito. Desliza para entender.\n\n💬 Você sabia? Comenta SIM ou NÃO.\n\n" + H_MIT,
  [lambda p: capa_manchete("O gás de cozinha [não tem cheiro]", "VOCÊ SABIA?", p, "Então que cheiro é esse?", "👃"),
   lambda p: rehook("Então por que você sente aquele cheiro forte?", p, "🤔", "mascote-pensando.png"),
   lambda p: ideia("1", "É um aditivo", "As distribuidoras colocam uma substância de cheiro forte no gás, de propósito.", p, mascote="mascote-pensando.png"),
   lambda p: ideia("2", "É um alarme", "Sem esse cheiro, um vazamento passaria despercebido. Com ele, você percebe na hora.", p, "marinho", mascote="mascote-joia.png"),
   lambda p: lista_grande("Sentiu o cheiro?", ["Não acenda luz, fósforo ou isqueiro", "Abra portas e janelas", "Saia do local e ligue 193"], p, selo="🚒 Emergência: 193"),
   lambda p: cta_sinal("comentar", "Você [sabia]?", "Comenta SIM ou NÃO e manda pra quem também não sabia.", "mascote-pensando.png", p)]))

# ---------------------------------------------------------------- 14/11 19h30 · D
P.append(post("crepioca-5-minutos", "2026-11-14T19:30", "D", "mascote", "salvar", "Salva a receita",
  "Receita: crepioca em 5 minutos",
  "Lanche quentinho em 5 minutos, numa frigideira só 🍳\n\nCrepioca: ovo, tapioca e o recheio que tiver em casa.\n\n🔖 Salva e me conta qual recheio você usaria.\n\n" + H_REC,
  [lambda p: capa_reacao("Lanche pronto em [5 minutos]", "Só ovo e tapioca 😋", "mascote-chef.png", p),
   lambda p: lista_grande("Ingredientes", ["1 ovo", "2 colheres de goma de tapioca", "1 pitada de sal", "Recheio: queijo, tomate, frango..."], p),
   lambda p: lista_grande("Modo de fazer", ["Bata o ovo com a tapioca e o sal", "Despeje na frigideira untada, fogo baixo e tampada", "Vire, recheie, dobre e sirva"], p, "marinho"),
   lambda p: ideia("💡", "Dica de economia", "Frigideira tampada cozinha por cima e por baixo ao mesmo tempo: menos tempo de fogo.", p, mascote="mascote-chef.png"),
   lambda p: cta_sinal("salvar", "[Salva] e conta qual recheio você usaria", "Queijo? Frango? Banana com canela?", "mascote-chef.png", p)]))

# ---------------------------------------------------------------- 15/11 11h30 · A
P.append(post("quem-cozinha-lava-louca", "2026-11-15T11:30", "A", "manchete", "comentar", "Time A ou Time B",
  "Debate: quem cozinha lava a louça?",
  "Regra da casa: quem cozinha não lava a louça. Concorda? 🍽️\n\nDomingo é dia de panelão e de pia cheia. Veja os dois lados e escolha o seu time.\n\n💬 Time A ou Time B? Comenta aí.\n\n" + H_HUM,
  [lambda p: capa_manchete("Quem cozinha [não lava] a louça", "DOMINGO", p, "Concorda? Time A ou Time B?", "🍽️"),
   lambda p: rehook("Antes de responder, veja os dois lados", p, "⚖️", "mascote-pensando.png"),
   lambda p: ideia("A", "Time quem cozinha descansa", "Quem passou a manhã no fogão já fez a parte mais difícil.", p, mascote="mascote-chef.png"),
   lambda p: ideia("B", "Time cada um lava o seu", "Quem sujou, lava. E quem cozinha suja tudo, né? 😅", p, "marinho", mascote="mascote-joia.png"),
   lambda p: cta_sinal("comentar", "Time [A] ou Time [B]?", "Comenta aí e marca quem vai lavar a louça hoje.", "mascote-correndo.png", p)]))

# ---------------------------------------------------------------- 15/11 19h30 · B
P.append(post("pressao-x-panela-comum", "2026-11-15T19:30", "B", "mascote", "salvar", "Salva o post",
  "Economia: panela de pressão x panela comum",
  "Panela de pressão ou panela comum: qual gasta menos gás? 🍲\n\nPara grãos e carnes, a diferença é grande. Para outras coisas, nem tanto.\n\n🔖 Salva e manda pra quem não larga a panela comum.\n\n" + H_ECO,
  [lambda p: capa_reacao("Pressão ou panela comum: qual [gasta menos?]", "Aposto que você erra o nº 3 😏", "mascote-chef.png", p, "rosa"),
   lambda p: erro_acerto("1. Feijão e grão-de-bico", "Na panela comum, horas no fogo", "Na pressão, cozinha em bem menos tempo", p, "PANELA COMUM", "PRESSÃO", "mascote-chef.png"),
   lambda p: erro_acerto("2. Carnes duras", "Músculo e acém demoram muito na panela comum", "Na pressão ficam macios bem mais rápido", p, "PANELA COMUM", "PRESSÃO", "mascote-joia.png"),
   lambda p: erro_acerto("3. Arroz e legumes", "Precisam de pressão para economizar", "Cozinham rápido na panela comum tampada", p, "MITO", "VERDADE", "mascote-pensando.png"),
   lambda p: ideia("💡", "Segurança em dia", "Confira sempre a válvula e a borracha da sua panela de pressão antes de usar.", p, "marinho", mascote="mascote-joia.png"),
   lambda p: cta_sinal("salvar", "[Salva] pra escolher a panela certa", "E manda pra quem não larga a panela comum.", "mascote-chef.png", p)]))

# ---------------------------------------------------------------- 16/11 11h30 · F
P.append(post("veja-antes-de-pedir", "2026-11-16T11:30", "F", "mascote", "clique", "Comente APP",
  "App: o que você vê antes de pedir o gás",
  "3 coisas que você pode ver ANTES de pedir o gás 👀\n\nMarca, preço da sua região e prazo de cada revenda. Sem ligar, sem esperar na linha.\n\n" + APP_TXT + "\n\n" + H_APP,
  [lambda p: capa_reacao("3 coisas para ver [antes de pedir] o gás", "A nº 2 muda tudo 💸", "mascote-celular.png", p),
   lambda p: ideia("1", "A marca", "Escolha a marca que você prefere entre as ofertas do seu endereço.", p, mascote="mascote-pensando.png"),
   lambda p: ideia("2", "O preço da sua região", "Compare as ofertas lado a lado. Os valores podem variar por região.", p, "marinho", mascote="mascote-maquininha.png"),
   lambda p: tela("3. O [prazo]", "Veja o prazo informado por cada revenda e escolha.", p),
   lambda p: cta_sinal("app", "", "Baixe grátis e pague só na entrega.", "mascote-celular.png", p)]))

# ---------------------------------------------------------------- 16/11 19h30 · D
P.append(post("arroz-com-sobras", "2026-11-16T19:30", "D", "manchete", "salvar", "Salva a receita",
  "Receita: arroz de sobras numa panela só",
  "Sobrou arroz? Vira janta em 15 minutos 🍚\n\nArroz mexido com o que tiver na geladeira: legumes, ovo, frango desfiado. Nada se perde.\n\n🔖 Salva e manda pra quem odeia desperdiçar comida.\n\n" + H_REC,
  [lambda p: capa_manchete("Sobrou arroz? Vira [janta]", "RECEITA SEM DESPERDÍCIO", p, "Pronto em 15 minutos, numa panela só", "🍚"),
   lambda p: lista_grande("O que usar", ["Arroz que sobrou", "1 ou 2 ovos", "Legumes picados (cenoura, ervilha, milho)", "Frango ou carne que sobrou (opcional)"], p),
   lambda p: lista_grande("Modo de fazer", ["Refogue alho e cebola", "Junte os legumes e o que sobrou", "Coloque o arroz e os ovos, mexendo até firmar"], p, "marinho"),
   lambda p: ideia("💡", "Por que economiza", "Comida já cozida só precisa esquentar: poucos minutos de fogo e zero desperdício.", p, mascote="mascote-chef.png"),
   lambda p: cta_sinal("salvar", "[Salva] pra não jogar comida fora", "E manda pra quem odeia desperdício.", "mascote-chef.png", p)]))

# ---------------------------------------------------------------- 17/11 11h30 · C
P.append(post("sinais-gas-acabando", "2026-11-17T11:30", "C", "mascote", "comentar", "Qual sinal você usa?",
  "Curiosidade: sinais de que o gás está acabando",
  "4 sinais de que o gás está acabando ⏳\n\nPerceber antes evita aquele susto no meio do almoço.\n\n💬 Qual sinal você usa? Comenta o número.\n\n" + H_MIT,
  [lambda p: capa_reacao("4 sinais de que o [gás está acabando]", "O nº 4 evita o susto 😅", "mascote-pensando.png", p, "rosa"),
   lambda p: ideia("1", "A chama fica mais fraca", "Mesmo no máximo, ela parece baixa.", p, mascote="mascote-pensando.png"),
   lambda p: ideia("2", "A comida demora mais", "A água leva mais tempo para ferver do que o normal.", p, "marinho", mascote="mascote-chef.png"),
   lambda p: ideia("3", "Faz tempo da última troca", "Se você anotou a data, já sabe quando costuma acabar.", p, mascote="mascote-joia.png"),
   lambda p: ideia("4", "Peça antes do fim", "Percebeu os sinais? Peça com calma, sem esperar acabar.", p, "marinho", mascote="mascote-celular.png"),
   lambda p: cta_sinal("comentar", "Qual sinal [você usa]?", "Comenta o número: 1, 2, 3 ou 4 👇", "mascote-pensando.png", p)]))

# ---------------------------------------------------------------- 17/11 19h30 · A
P.append(post("so-quem-ficou-sem-gas", "2026-11-17T19:30", "A", "manchete", "compartilhar", "Manda pra quem sempre deixa acabar",
  "Humor: coisas que só quem ficou sem gás entende",
  "Coisas que só quem já ficou sem gás entende 😂\n\nSe você nunca passou por isso, parabéns. Se passou, já sabe.\n\n👉 Manda pra quem sempre deixa o gás acabar.\n\n" + H_HUM,
  [lambda p: capa_manchete("Só quem já [ficou sem gás] entende", "IDENTIFICA?", p, "Quantas dessas já aconteceram com você?", "😂"),
   lambda p: ideia("1", "Pedir fogo na vizinha", "\"Posso terminar o arroz aí rapidinho?\"", p, mascote="mascote-joia.png"),
   lambda p: ideia("2", "Janta de pão com ovo...", "...sem o ovo, porque não tem como fritar.", p, "marinho", mascote="mascote-pensando.png"),
   lambda p: ideia("3", "Esquentar água na chaleira", "Café resolvido. E o almoço?", p, mascote="mascote-chef.png"),
   lambda p: ideia("4", "A promessa de sempre", "\"Da próxima vez eu peço antes.\" (spoiler: não pede)", p, "marinho", mascote="mascote-correndo.png"),
   lambda p: cta_sinal("compartilhar", "Manda pra quem [sempre deixa acabar] 😂", "Quantas dessas já aconteceram com você?", "mascote-correndo.png", p)]))

# ---------------------------------------------------------------- 18/11 11h30 · B
P.append(post("forno-5-truques", "2026-11-18T11:30", "B", "manchete", "salvar", "Salva o post",
  "Economia: 5 truques do forno",
  "O forno é um dos maiores gastos de gás da cozinha 🔥\n\n5 truques simples para assar gastando menos. O nº 1 todo mundo faz errado.\n\n🔖 Salva para o próximo bolo.\n\n" + H_ECO,
  [lambda p: capa_manchete("5 truques para o forno [gastar menos]", "ECONOMIA", p, "O nº 1 todo mundo faz errado", "🔥"),
   lambda p: ideia("1", "Não abra a porta toda hora", "Cada espiada deixa o calor escapar e o forno precisa esquentar de novo.", p, mascote="mascote-pensando.png"),
   lambda p: ideia("2", "Asse dois pratos juntos", "Aproveite o forno quente: bolo e assado na mesma fornada.", p, "marinho", mascote="mascote-chef.png"),
   lambda p: lista_grande("E mais 3", ["Preaqueça só o tempo da receita", "Desligue alguns minutos antes do fim", "Use forma do tamanho certo"], p, inicio=3),
   lambda p: cta_sinal("salvar", "[Salva] para o próximo bolo", "E manda pra quem vive com o forno ligado.", "mascote-chef.png", p)]))

# ---------------------------------------------------------------- 18/11 19h30 · F
P.append(post("gas-casa-da-mae", "2026-11-18T19:30", "F", "mascote", "compartilhar", "Manda pra sua mãe",
  "App: mandar gás para a casa da mãe",
  "Dá para mandar gás para a casa da sua mãe sem sair de casa 💗\n\nNo app você pede para outro endereço: informa o CEP de lá e o pagamento é na entrega.\n\n👉 Manda esse post pra sua mãe (ou pro seu irmão que nunca lembra).\n\n" + APP_TXT + "\n\n" + H_APP,
  [lambda p: capa_reacao("Gás na casa da mãe [sem sair de casa]", "Filho que é filho pede pelo app 💗", "mascote-celular.png", p, "rosa"),
   lambda p: ideia("1", "Digite o CEP de lá", "O app mostra as revendas que atendem o endereço da sua mãe.", p, mascote="mascote-celular.png"),
   lambda p: ideia("2", "Escolha a oferta", "Compare marca, preço da região e prazo antes de pedir.", p, "marinho", mascote="mascote-pensando.png"),
   lambda p: ideia("3", "Pagamento na entrega", "Pix, cartão ou dinheiro, direto com quem entrega.", p, mascote="mascote-maquininha.png"),
   lambda p: cta_sinal("compartilhar", "Manda isso pra [sua mãe] 💗", "E comente APP para receber o link no direct.", "mascote-correndo.png", p)]))

# ---------------------------------------------------------------- 19/11 11h30 · C
P.append(post("mito-verdade-cozinha", "2026-11-19T11:30", "C", "manchete", "comentar", "Quantas você acertou?",
  "Mitos e verdades da cozinha",
  "Mito ou verdade da cozinha: quantas você acerta? 🧂\n\nTeste rápido com 3 perguntas. Responde antes de deslizar!\n\n💬 Comenta quantas você acertou: 0, 1, 2 ou 3.\n\n" + H_MIT,
  [lambda p: capa_manchete("Mito ou verdade: [quantas você acerta?]", "TESTE RÁPIDO", p, "Responde antes de deslizar!", "🧂"),
   lambda p: erro_acerto("1. Sal faz a água ferver mais rápido", "Sal acelera a fervura", "Quase não muda nada. Pode salgar quando quiser.", p, mascote="mascote-pensando.png"),
   lambda p: erro_acerto("2. Tampar a panela economiza", "Tanto faz tampar ou não", "Tampada, a água ferve mais rápido e o gás rende mais.", p, mascote="mascote-chef.png"),
   lambda p: erro_acerto("3. Descongelar no fogo", "Descongelar na panela é mais prático e não muda nada", "Descongelar antes na geladeira gasta bem menos gás.", p, mascote="mascote-joia.png"),
   lambda p: cta_sinal("comentar", "Quantas você [acertou]?", "Comenta: 0, 1, 2 ou 3 👇", "mascote-pensando.png", p)]))

# ---------------------------------------------------------------- 19/11 19h30 · D
P.append(post("3-jantas-baratas", "2026-11-19T19:30", "D", "mascote", "salvar", "Salva as 3 jantas",
  "Receitas: 3 jantas baratas numa panela só",
  "3 jantas baratas, cada uma numa panela só 🍲\n\nMenos louça, menos gás e comida gostosa na mesa.\n\n🔖 Salva para a semana e conta qual você faz primeiro.\n\n" + H_REC,
  [lambda p: capa_reacao("3 jantas baratas [numa panela só]", "Menos louça, menos gás 🙌", "mascote-chef.png", p),
   lambda p: lista_grande("1. Macarrão com sardinha", ["Refogue alho, cebola e tomate", "Junte a sardinha e o macarrão cozido", "Finalize com cheiro-verde"], p),
   lambda p: lista_grande("2. Sopa de feijão com macarrão", ["Bata o feijão que sobrou com água", "Ferva e junte macarrão de sopa", "Tempere e sirva quentinho"], p, "marinho"),
   lambda p: lista_grande("3. Arroz com ovo e legumes", ["Refogue os legumes picados", "Junte o arroz pronto", "Quebre os ovos e mexa até firmar"], p),
   lambda p: cta_sinal("salvar", "[Salva] as 3 jantas da semana", "Conta qual você faz primeiro: 1, 2 ou 3?", "mascote-chef.png", p)]))

assert len(P) == 19, len(P)

# ---------------------------------------------------------------- stories 08h30
STORIES = [
 ("2026-11-11", "Você [balança o botijão] pra ver se tem gás?", "Todo mundo já fez isso 😅", "mascote-pensando.png", "marinho", "Responda [SIM] ou [NÃO] 💬", "", "comentar"),
 ("2026-11-12", "O que vai ter de [janta hoje?]", "Hoje tem receita de 15 minutos no feed 🍝", "mascote-chef.png", "rosa", "Me conta aqui 💬", "", "comentar"),
 ("2026-11-13", "Sexta! O gás [aguenta o fim de semana?]", "Peça pelo celular e pague só na entrega.", "mascote-correndo.png", "marinho", "Responda [APP] a este story 💬", "e receba o link do app no direct", "clique"),
 ("2026-11-14", "O gás de cozinha [tem cheiro?]", "A resposta sai hoje no feed 👀", "mascote-pensando.png", "rosa", "Responda [SIM] ou [NÃO] 💬", "", "comentar"),
 ("2026-11-15", "Quem cozinha [lava a louça?]", "Domingo de debate na cozinha 🍽️", "mascote-joia.png", "marinho", "Responda: time [A] ou time [B] 💬", "", "comentar"),
 ("2026-11-16", "Segunda com o [gás em dia?]", "Compare marca, preço e prazo antes de pedir.", "mascote-celular.png", "rosa", "Responda [APP] a este story 💬", "e receba o link do app no direct", "clique"),
 ("2026-11-17", "Como você sabe que o [gás está acabando?]", "Hoje tem os 4 sinais no feed ⏳", "mascote-pensando.png", "marinho", "Me conta aqui 💬", "", "comentar"),
 ("2026-11-18", "Forno [ligado hoje?]", "O que vai assar? Bolo, frango, pão?", "mascote-chef.png", "rosa", "Me conta aqui 💬", "", "comentar"),
 ("2026-11-19", "Gás na casa da [mãe?]", "Dá pra pedir para outro endereço pelo app 💗", "mascote-celular.png", "marinho", "Responda [APP] a este story 💬", "e receba o link do app no direct", "clique"),
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
                      "pilar": p["pilar"], "layout": p["layout"], "objetivo": p["objetivo"], "cta": p["cta"], "lote": "semana3-estrategia"})
    for d, titulo, texto, masc, fundo, cta_txt, cta_sub, obj in STORIES:
        sid = f"{d}-story-0830-v2"
        rel = f"posts/{sid}/1.jpg"
        jobs.append((story_v2(titulo, texto, masc, fundo, cta_txt, cta_sub), str(OUT / rel), 1080, 1920))
        novos.append({"id": sid, "tipo": "story", "abordagem": "story: " + titulo.replace("[", "").replace("]", ""), "legenda": "",
                      "imagens": [rel], "agendado_para": f"{d}T08:30:00-03:00", "aprovado": True,
                      "pilar": "story", "layout": "story", "objetivo": obj, "cta": cta_txt.replace("[", "").replace("]", ""), "lote": "semana3-estrategia"})
    render(jobs)
    print(len(jobs), "imagens")
    (OUT / "gerador" / "semana3_novos.json").write_text(json.dumps(novos, ensure_ascii=False, indent=1))
