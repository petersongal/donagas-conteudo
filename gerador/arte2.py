"""Layouts novos (estratégia de crescimento, 10/11/2026) — ver ESTRATEGIA-CRESCIMENTO.md.

Três famílias de capa em rodízio:
- capa_manchete: fundo claro, título enorme, sem mascote (interrompe o padrão do feed).
- capa_reacao:   mascote reagindo com balão de fala, título no topo.
- (foto real:    quando houver fotos em assets/fotos/)
Miolo: rehook (slide 2), ideia (1 ideia por slide, número gigante), erro_acerto, lista_grande.
Fim: cta_sinal (compartilhar / salvar / comentar / app).
Story: story_v2 com CTA livre.
Todos 1080x1350 (story 1080x1920).
"""
from arte import A, b64, doc, esc, chama_bg, marca, LOGO

MARINHO, ROSA, ROSA_F = "#171276", "#FF47A3", "#C2186B"

EXTRA = """
<style>
.kicker{position:absolute;left:70px;display:inline-flex;align-items:center;gap:12px;border-radius:999px;padding:12px 28px;font-weight:900;font-size:30px;letter-spacing:1px}
.desliza{position:absolute;right:70px;bottom:130px;display:flex;align-items:center;gap:14px;font-weight:900;font-size:36px}
.desliza b{display:flex;align-items:center;justify-content:center;width:84px;height:84px;border-radius:50%;font-size:46px}
.balao{position:absolute;background:#fff;color:#171276;border-radius:46px;padding:34px 40px;font-weight:900;font-size:46px;line-height:1.15;box-shadow:0 20px 50px rgba(0,0,0,.25)}
.balao:after{content:"";position:absolute;width:0;height:0;border:28px solid transparent}
.gigante{position:absolute;font-weight:900;line-height:.8;letter-spacing:-8px}
.ea{border-radius:40px;padding:40px 46px;display:flex;gap:30px;align-items:flex-start}
.ea .ic{flex:none;width:92px;height:92px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:54px;font-weight:900}
.ea .t{font-size:30px;font-weight:900;letter-spacing:2px;margin-bottom:10px}
.ea .d{font-size:44px;font-weight:900;line-height:1.15}
.li{display:flex;gap:30px;align-items:center;margin-bottom:36px}
.li .n{flex:none;width:100px;height:100px;border-radius:28px;background:#FF47A3;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:48px;box-shadow:0 8px 0 #C2186B}
.li .x{font-size:42px;font-weight:800;line-height:1.18}
</style>
"""


def _d(w, h, body, cls):
    return doc(w, h, EXTRA + body, cls)


def _pag(p, cor):
    return f'<div class="setas" style="right:70px;top:78px;color:{cor}">{p}</div>'


def _rod(cor, txt="@appdonagas"):
    return f'<div class="rodape" style="bottom:46px;color:{cor}"><span>{txt}</span><span>app.donagas.com.br</span></div>'


def _fs(t, grande, medio, pequeno, lim1=24, lim2=40):
    n = len(t.replace("[", "").replace("]", ""))
    return grande if n <= lim1 else (medio if n <= lim2 else pequeno)


# ---------------------------------------------------------------- capas
def capa_manchete(titulo, kicker="", pagina="1/7", sub="", emoji=""):
    fs = _fs(titulo, 150, 124, 104)
    body = f"""
    {chama_bg(640, 760, 620, 14)}
    <div class="brilho" style="width:620px;height:620px;background:#FF47A3;opacity:.18;left:-220px;top:-200px"></div>
    {marca(70, 64, "#171276", marinho=True)}
    {_pag(pagina + ' ➜', ROSA_F)}
    {f'<div class="kicker" style="top:200px;background:#171276;color:#fff">{esc(kicker)}</div>' if kicker else ''}
    <h1 style="position:absolute;left:70px;top:{300 if kicker else 220}px;width:940px;font-size:{fs}px;color:#171276;line-height:.98">{esc(titulo)}</h1>
    {f'<div style="position:absolute;left:70px;bottom:230px;width:600px;background:#fff;border-radius:40px;padding:34px 40px;box-shadow:0 18px 50px rgba(23,18,118,.14);font-size:42px;font-weight:900;line-height:1.2;color:#171276">{esc(sub)}</div>' if sub else ''}
    {f'<div style="position:absolute;right:90px;bottom:300px;font-size:230px;line-height:1;transform:rotate(8deg);filter:drop-shadow(0 20px 30px rgba(23,18,118,.25))">{emoji}</div>' if emoji else ''}
    <div class="desliza" style="color:#171276">desliza <b style="background:#FF47A3;color:#fff">➜</b></div>
    {_rod("#171276")}
    """
    return _d(1080, 1350, body, "claro tx-pontos")


def capa_reacao(titulo, balao, mascote, pagina="1/7", fundo="marinho"):
    m = b64(A / mascote)
    fs = _fs(titulo, 104, 90, 78, 22, 36)
    cor_em = ROSA if fundo == "marinho" else MARINHO
    cls = "marinho tx-listras" if fundo == "marinho" else "rosa tx-listras"
    palco = "palco" if fundo == "marinho" else "palco rosa-p"
    body = f"""
    <div class="brilho" style="width:700px;height:700px;background:{'#FF47A3' if fundo=='marinho' else '#fff'};opacity:.3;left:-200px;bottom:-150px"></div>
    {chama_bg(760, 900, 460, 14)}
    {marca(70, 64, marinho=(fundo != 'marinho'))}
    {_pag(pagina + ' ➜', '#FFB3D9' if fundo=='marinho' else MARINHO)}
    <h1 style="position:absolute;left:70px;top:190px;width:940px;font-size:{fs}px;line-height:1.0">{esc(titulo).replace('<em>', f'<em style="color:{cor_em}">')}</h1>
    <div class="{palco}" style="width:520px;height:520px;left:-40px;bottom:120px"></div>
    <img class="mascote" src="{m}" style="height:720px;left:20px;bottom:110px">
    <div class="balao" style="right:60px;bottom:470px;width:470px">{esc(balao)}</div>
    <div class="desliza" style="color:#fff">desliza <b style="background:#fff;color:{MARINHO if fundo=='marinho' else ROSA}">➜</b></div>
    {_rod('#fff')}
    """
    return _d(1080, 1350, body, cls)


# ---------------------------------------------------------------- miolo
def rehook(texto, pagina="2/7", emoji="👀", mascote="mascote-pensando.png"):
    fs = _fs(texto, 116, 96, 82, 26, 46)
    mm = b64(A / mascote)
    body = f"""
    <div class="brilho" style="width:800px;height:800px;background:#FF47A3;opacity:.35;right:-260px;bottom:-200px"></div>
    {chama_bg(-140, 840, 560, -16)}
    {marca(70, 64)}
    {_pag(pagina + ' ➜', '#FFB3D9')}
    <div style="position:absolute;left:70px;top:230px;font-size:150px">{emoji}</div>
    <h1 style="position:absolute;left:70px;top:440px;width:940px;font-size:{fs}px">{esc(texto)}</h1>
    <img class="mascote" src="{mm}" style="height:430px;left:70px;bottom:110px">
    <div class="desliza" style="color:#fff">continua <b style="background:#FF47A3;color:#fff">➜</b></div>
    {_rod('#fff')}
    """
    return _d(1080, 1350, body, "marinho tx-listras")


def ideia(numero, titulo, texto, pagina, fundo="claro", mascote="mascote-joia.png"):
    escuro = fundo == "marinho"
    cor = "#fff" if escuro else MARINHO
    cor_t = "#E9E6FF" if escuro else "#3a3580"
    cls = "marinho tx-listras" if escuro else "claro tx-pontos"
    fs = _fs(titulo, 92, 80, 68, 20, 36)
    body = f"""
    {chama_bg(720, 960, 460, 12)}
    {marca(70, 64, cor, marinho=not escuro)}
    {_pag(pagina + ' ➜', '#FFB3D9' if escuro else ROSA_F)}
    <div class="gigante" style="left:56px;top:170px;font-size:300px;color:{ROSA}">{numero}</div>
    <h1 style="position:absolute;left:70px;top:470px;width:940px;font-size:{fs}px;color:{cor}">{esc(titulo)}</h1>
    <div style="position:absolute;left:70px;top:{760 if len(titulo) > 16 else 650}px;width:620px;background:{'rgba(255,255,255,.1)' if escuro else '#fff'};border-radius:40px;padding:36px 40px;box-shadow:0 18px 50px rgba(23,18,118,.12);font-size:42px;font-weight:800;line-height:1.25;color:{cor_t}">{esc(texto)}</div>
    <img class="mascote" src="{b64(A / mascote)}" style="height:500px;right:20px;bottom:100px">
    {_rod(cor)}
    """
    return _d(1080, 1350, body, cls)


def erro_acerto(titulo, erro, acerto, pagina, rot_e="MITO", rot_a="VERDADE", mascote="mascote-pensando.png"):
    body = f"""
    {chama_bg(-120, 1000, 420, -12)}
    {marca(70, 64, MARINHO, marinho=True)}
    {_pag(pagina + ' ➜', ROSA_F)}
    <h1 style="position:absolute;left:70px;top:190px;width:940px;font-size:{_fs(titulo, 84, 72, 62, 22, 38)}px;color:#171276">{esc(titulo)}</h1>
    <div style="position:absolute;left:70px;right:70px;top:{450 if len(titulo) > 22 else 380}px">
      <div class="ea" style="background:#FFE3F1;color:#C2186B;margin-bottom:34px">
        <div class="ic" style="background:#C2186B;color:#fff">✕</div>
        <div><div class="t">{rot_e}</div><div class="d" style="color:#7a0e45">{esc(erro)}</div></div>
      </div>
      <div class="ea" style="background:#171276;color:#fff">
        <div class="ic" style="background:#FF47A3;color:#fff">✓</div>
        <div><div class="t" style="color:#FFB3D9">{rot_a}</div><div class="d">{esc(acerto)}</div></div>
      </div>
    </div>
    <img class="mascote" src="{b64(A / mascote)}" style="height:400px;right:40px;bottom:100px">
    {_rod(MARINHO)}
    """
    return _d(1080, 1350, body, "claro tx-pontos")


def lista_grande(titulo, itens, pagina, fundo="claro", inicio=1, selo=""):
    escuro = fundo == "marinho"
    cor = "#fff" if escuro else MARINHO
    cls = "marinho tx-listras" if escuro else "claro tx-pontos"
    fs_i = 48 if len(itens) <= 4 else 42
    li = "".join(f'<div class="li"><div class="n">{i}</div><div class="x" style="color:{cor};font-size:{fs_i}px">{esc(t)}</div></div>'
                 for i, t in enumerate(itens, inicio))
    body = f"""
    {chama_bg(760, 980, 420, 12)}
    {marca(70, 64, cor, marinho=not escuro)}
    {_pag(pagina + ' ➜', '#FFB3D9' if escuro else ROSA_F)}
    <h1 style="position:absolute;left:70px;top:190px;width:940px;font-size:{_fs(titulo, 84, 72, 62, 22, 38)}px;color:{cor}">{esc(titulo)}</h1>
    <div style="position:absolute;left:70px;width:940px;top:{440 if len(titulo) > 22 else 370}px">{li}</div>
    {f'<div class="pill rosa" style="position:absolute;left:70px;bottom:130px;font-size:34px">{esc(selo)}</div>' if selo else ''}
    {_rod(cor)}
    """
    return _d(1080, 1350, body, cls)


def tela(titulo, texto, pagina):
    t = b64(A / "tela-inicio.png")
    body = f"""
    {chama_bg(-140, 760, 520, -16)}
    {marca(70, 64, marinho=True)}
    {_pag(pagina + ' ➜', MARINHO)}
    <h1 style="position:absolute;left:70px;top:190px;width:500px;font-size:{_fs(titulo, 80, 70, 60, 16, 30)}px">{esc(titulo)}</h1>
    <p style="position:absolute;left:70px;top:560px;width:460px;font-size:40px;font-weight:800;line-height:1.26;color:#fff">{esc(texto)}</p>
    <div class="celular" style="width:450px;right:60px;top:180px;transform:rotate(4deg)"><img src="{t}"></div>
    {_rod('#fff', 'Tela real do App Dona Gás')}
    """
    return _d(1080, 1350, body, "rosa tx-pontos-b")


# ---------------------------------------------------------------- fim
CTA_ICONE = {"compartilhar": "📤", "salvar": "🔖", "comentar": "💬", "app": "📲"}


def cta_sinal(tipo, titulo, sub, mascote, pagina):
    if tipo == "app":
        titulo = titulo or "Comente [APP] e receba o link no direct"
    from PIL import Image
    im = Image.open(A / mascote)
    ratio = im.width / im.height
    alt = 780 if ratio < 0.6 else 620
    larg = int(alt * ratio)
    tw = min(560, 1080 + 10 - larg - 70 - 40)
    m = b64(A / mascote)
    body = f"""
    <div class="brilho" style="width:700px;height:700px;background:#fff;opacity:.3;left:-200px;top:-200px"></div>
    {chama_bg(700, 880, 500, 16)}
    {marca(70, 64, marinho=True)}
    {_pag(pagina, MARINHO)}
    <div style="position:absolute;left:70px;top:190px;font-size:120px">{CTA_ICONE[tipo]}</div>
    <h1 style="position:absolute;left:70px;top:350px;width:{tw}px;font-size:{_fs(titulo, 88, 76, 66, 22, 40) if tw >= 520 else _fs(titulo, 76, 66, 58, 22, 40)}px;line-height:1.05">{esc(titulo).replace('<em>', '<em style="font-style:normal;white-space:nowrap;color:#fff;background:#171276;border-radius:20px;padding:0 16px">')}</h1>
    <p style="position:absolute;left:70px;top:{820 if len(titulo) > 30 else 760}px;width:{min(480, tw)}px;font-size:38px;font-weight:800;line-height:1.26">{esc(sub)}</p>
    <div class="palco" style="width:520px;height:520px;right:-70px;bottom:130px"></div>
    <img class="mascote" src="{m}" style="height:{alt}px;right:-10px;bottom:110px">
    {_rod('#fff', 'Siga @appdonagas')}
    """
    return _d(1080, 1350, body, "rosa tx-listras")


# ---------------------------------------------------------------- story
def story_v2(titulo, texto, mascote, fundo, cta_txt, cta_sub=""):
    from PIL import Image
    if mascote == "mascote-senhora.png":
        mascote = "mascote-joia.png"
    im = Image.open(A / mascote)
    alt = 680
    larg = int(alt * im.width / im.height)
    m = b64(A / mascote)
    cls = "marinho tx-listras" if fundo == "marinho" else "rosa tx-listras"
    palco = "palco" if fundo == "marinho" else "palco rosa-p"
    em_cor = ROSA if fundo == "marinho" else MARINHO
    pw = max(380, min(500, 1080 - 60 - larg - 110))
    body = f"""
    <div class="brilho" style="width:800px;height:800px;background:{'#FF47A3' if fundo=='marinho' else '#fff'};opacity:.3;right:-250px;top:700px"></div>
    {chama_bg(-160, 1240, 560, -16)}{chama_bg(780, 220, 360, 12)}
    {marca(80, 270, marinho=(fundo != 'marinho'))}
    <h1 style="position:absolute;left:80px;top:390px;width:920px;font-size:{_fs(titulo, 110, 96, 84, 22, 40)}px;line-height:1.02">{esc(titulo).replace('<em>', f'<em style="color:{em_cor}">')}</h1>
    <p style="position:absolute;left:80px;top:860px;width:{pw}px;font-size:46px;font-weight:800;line-height:1.28">{esc(texto)}</p>
    <div class="{palco}" style="width:600px;height:600px;right:-70px;bottom:540px"></div>
    <img class="mascote" src="{m}" style="height:{alt}px;right:60px;bottom:520px">
    <div style="position:absolute;left:80px;right:80px;bottom:340px;background:#fff;color:#171276;border-radius:40px;padding:30px 40px;font-weight:900;font-size:44px;text-align:center;box-shadow:0 20px 40px rgba(0,0,0,.25)">
      {esc(cta_txt).replace('<em>', '<em style="font-style:normal;background:#FF47A3;color:#fff;border-radius:18px;padding:0 16px">')}{f'<br><span style="font-size:32px;font-weight:800;color:#3a3580">{esc(cta_sub)}</span>' if cta_sub else ''}
    </div>
    """
    return _d(1080, 1920, body, cls)
