"""Gerador de artes do Instagram do App Dona Gás (@appdonagas).

Padrão visual (design system Dona Gás):
- Cores: rosa #FF47A3, rosa forte #C2186B, marinho #171276, marinho noite #0D0A4A, rosa claro #FFE3F1, branco.
- Fonte: Nunito (900 títulos, 800 destaques, 700 texto).
- Todo fundo leva textura discreta (chamas/listras) — nada de fundo liso e vazio.
- Mascote oficial (3D, boné e roupa rosa) ocupa ≥ 1/3 da arte quando aparece.
- Rodapé: logo Dona Gás + "app.donagas.com.br". Nunca citar a FamaGás.
Feed 1080x1350 · Story 1080x1920 (área segura: 250 px no topo, 340 px na base).
"""
import asyncio, base64, html, os
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).parent
A = ROOT / "assets"
FONTS = ROOT / "node_modules/@fontsource/nunito/files"


def b64(path: Path) -> str:
    ext = path.suffix.lower().lstrip(".")
    mime = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg", "webp": "image/webp", "woff2": "font/woff2"}[ext]
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()


FONT_CSS = "".join(
    f"@font-face{{font-family:'Nunito';font-weight:{w};src:url('{b64(FONTS / f'nunito-latin-{w}-normal.woff2')}') format('woff2')}}"
    for w in (700, 800, 900)
)

LOGO = b64(A / "logo-icone.png")
LOGO_M = b64(A / "logo-icone-marinho.png")

BASE_CSS = FONT_CSS + """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:100%;height:100%}
body{font-family:'Nunito',sans-serif;-webkit-font-smoothing:antialiased}
.c{position:relative;overflow:hidden;width:__W__;height:__H__}
.marinho{background:#171276;color:#fff}
.rosa{background:#FF47A3;color:#fff}
.claro{background:#FFF1F8;color:#171276}
/* texturas */
.tx-listras::before{content:"";position:absolute;inset:-20%;background:repeating-linear-gradient(-35deg,rgba(255,255,255,.055) 0 26px,transparent 26px 70px);pointer-events:none}
.tx-pontos::before{content:"";position:absolute;inset:0;background-image:radial-gradient(rgba(23,18,118,.14) 2.6px,transparent 3px);background-size:34px 34px;pointer-events:none}
.tx-pontos-b::before{content:"";position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.16) 2.6px,transparent 3px);background-size:34px 34px;pointer-events:none}
.chama-bg{position:absolute;opacity:.08;pointer-events:none}
.brilho{position:absolute;border-radius:50%;filter:blur(90px);pointer-events:none}
.marca{position:absolute;display:flex;align-items:center;gap:16px;font-weight:900;font-size:44px;letter-spacing:-.5px}
.marca img{width:64px;height:64px}
.marca b{font-weight:900}.marca i{font-style:normal;font-weight:700;color:#FF47A3;letter-spacing:2px}
.rosa .marca i{color:#171276}
.rodape{position:absolute;left:0;right:0;display:flex;justify-content:space-between;align-items:center;padding:0 70px;font-weight:800;font-size:30px;opacity:.95}
.pill{display:inline-flex;align-items:center;gap:12px;border-radius:999px;padding:14px 30px;font-weight:900;font-size:32px}
.pill.rosa{background:#FF47A3;color:#fff}.pill.marinho{background:#171276;color:#fff}.pill.branco{background:#fff;color:#171276}
h1{font-weight:900;letter-spacing:-1.5px;line-height:1.02}
h1 em{font-style:normal;color:#FF47A3}
.rosa h1 em{color:#171276}
.palco{position:absolute;border-radius:50%;background:radial-gradient(circle at 50% 40%,#2a23a6 0%,#171276 70%);box-shadow:0 0 0 18px rgba(255,71,163,.9),0 0 0 36px rgba(255,255,255,.08)}
.palco.rosa-p{background:radial-gradient(circle at 50% 40%,#ff6fb8 0%,#FF47A3 70%);box-shadow:0 0 0 18px #171276,0 0 0 36px rgba(23,18,118,.12)}
.mascote{position:absolute;filter:drop-shadow(0 30px 40px rgba(0,0,0,.35))}
.num{display:flex;align-items:center;justify-content:center;width:96px;height:96px;border-radius:28px;background:#FF47A3;color:#fff;font-weight:900;font-size:56px;flex:none;box-shadow:0 10px 0 #C2186B}
.card{background:#fff;border-radius:44px;box-shadow:0 18px 50px rgba(23,18,118,.14);padding:44px 48px}
.celular{position:absolute;border-radius:70px;background:#0D0A4A;padding:18px;box-shadow:0 40px 80px rgba(0,0,0,.35)}
.celular img{display:block;width:100%;border-radius:54px}
.setas{position:absolute;font-weight:900;font-size:30px;opacity:.85}
"""


def chama_bg(x, y, size, rot=-12):
    return f'<img class="chama-bg" src="{LOGO}" style="left:{x}px;top:{y}px;width:{size}px;transform:rotate({rot}deg)">'


def marca(x, y, cor_texto="#fff", marinho=False):
    return f'<div class="marca" style="left:{x}px;top:{y}px;color:{cor_texto}"><img src="{LOGO_M if marinho else LOGO}"><span><b>Dona</b><i>GÁS</i></span></div>'


def doc(w, h, body, cls=""):
    css = BASE_CSS.replace("__W__", f"{w}px").replace("__H__", f"{h}px")
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body><div class="c {cls}">{body}</div></body></html>'


def esc(t):
    return html.escape(t).replace("\n", "<br>").replace("[", "<em>").replace("]", "</em>")


# ---------------------------------------------------------------------------
# Feed 1080x1350
# ---------------------------------------------------------------------------
def capa(titulo, sub, mascote, selo="", pagina="1/4"):
    m = b64(A / mascote)
    body = f"""
    <div class="brilho" style="width:700px;height:700px;background:#FF47A3;opacity:.35;right:-200px;bottom:-120px"></div>
    {chama_bg(-120, 820, 520, -18)}{chama_bg(760, -80, 360, 14)}
    {marca(70, 64)}
    <div class="setas" style="right:70px;top:78px;color:#FFB3D9">{pagina} ➜</div>
    {f'<div class="pill rosa" style="position:absolute;left:70px;top:190px;font-size:30px">{esc(selo)}</div>' if selo else ''}
    <h1 style="position:absolute;left:70px;top:{280 if selo else 210}px;width:500px;font-size:{84 if len(titulo) < 26 else 72}px;line-height:1.05">{esc(titulo)}</h1>
    <p style="position:absolute;left:70px;top:{760 if selo else 700}px;width:450px;font-size:38px;font-weight:700;line-height:1.25;color:#E9E6FF">{esc(sub)}</p>
    <div class="palco" style="width:600px;height:600px;right:-70px;bottom:120px"></div>
    <img class="mascote" src="{m}" style="height:900px;right:-30px;bottom:110px">
    <div class="rodape" style="bottom:46px;color:#fff"><span>📲 App grátis · iPhone e Android</span><span>app.donagas.com.br</span></div>
    """
    return doc(1080, 1350, body, "marinho tx-listras")


def passo(numero, titulo, texto, extra_html="", pagina="2/4", chips=()):
    body = f"""
    {chama_bg(760, 980, 420, 12)}
    {marca(70, 64, "#171276")}
    <div class="setas" style="right:70px;top:78px;color:#C2186B">{pagina} ➜</div>
    <div style="position:absolute;left:70px;top:200px;display:flex;gap:34px;align-items:center">
      <div class="num">{numero}</div>
      <h1 style="font-size:72px;width:780px;color:#171276">{esc(titulo)}</h1>
    </div>
    <p style="position:absolute;left:70px;top:{430 if len(titulo) > 22 else 360}px;width:{520 if extra_html else 900}px;font-size:40px;font-weight:700;line-height:1.3;color:#3a3580">{esc(texto)}</p>
    {extra_html or f'<img class="mascote" src="{b64(A / "mascote-celular.png")}" style="height:700px;right:-30px;bottom:100px">'}
    {''.join(f'<div class="pill marinho" style="position:absolute;left:70px;bottom:{170 + i*96}px;font-size:30px">✓ {esc(c)}</div>' for i, c in enumerate(reversed(chips)))}
    <div class="rodape" style="bottom:46px;color:#171276"><span>Dona Gás · gás de cozinha na sua porta</span><span>app.donagas.com.br</span></div>
    """
    return doc(1080, 1350, body, "claro tx-pontos")


def lista(titulo, itens, pagina="2/4", mascote=None):
    li = "".join(
        f'<div class="card" style="display:flex;gap:28px;align-items:center;padding:30px 36px;margin-bottom:24px"><div class="num" style="width:76px;height:76px;font-size:42px;border-radius:22px">{i+1}</div><div style="font-size:36px;font-weight:800;line-height:1.2;color:#171276">{esc(t)}</div></div>'
        for i, t in enumerate(itens)
    )
    if not mascote and len(itens) <= 3:
        mascote = "mascote-celular.png"
    m = f'<img class="mascote" src="{b64(A / mascote)}" style="height:520px;right:-40px;bottom:90px">' if mascote else ""
    width = 700 if mascote else 940
    body = f"""
    {chama_bg(-120, 980, 420, -12)}
    {marca(70, 64, "#171276")}
    <div class="setas" style="right:70px;top:78px;color:#C2186B">{pagina} ➜</div>
    <h1 style="position:absolute;left:70px;top:190px;width:940px;font-size:76px;color:#171276">{esc(titulo)}</h1>
    <div style="position:absolute;left:70px;top:{440 if len(titulo) > 24 else 360}px;width:{width}px">{li}</div>
    {m}
    <div class="rodape" style="bottom:46px;color:#171276"><span>Dona Gás · gás de cozinha na sua porta</span><span>app.donagas.com.br</span></div>
    """
    return doc(1080, 1350, body, "claro tx-pontos")


def tela_app(titulo, texto, tela="tela-inicio.png", pagina="3/4"):
    t = b64(A / tela)
    body = f"""
    <div class="brilho" style="width:600px;height:600px;background:#fff;opacity:.35;left:-160px;bottom:-100px"></div>
    {chama_bg(-140, 760, 520, -16)}
    {marca(70, 64, marinho=True)}
    <div class="setas" style="right:70px;top:78px;color:#171276">{pagina} ➜</div>
    <h1 style="position:absolute;left:70px;top:190px;width:520px;font-size:74px">{esc(titulo)}</h1>
    <p style="position:absolute;left:70px;top:520px;width:470px;font-size:38px;font-weight:800;line-height:1.28;color:#fff">{esc(texto)}</p>
    <div class="celular" style="width:470px;right:60px;top:170px;transform:rotate(4deg)"><img src="{t}"></div>
    <div class="rodape" style="bottom:46px;color:#fff"><span>Tela real do App Dona Gás</span><span>app.donagas.com.br</span></div>
    """
    return doc(1080, 1350, body, "rosa tx-pontos-b")


def cta(mascote="mascote-celular.png", palavra="APP", pagina="4/4"):
    m = b64(A / mascote)
    body = f"""
    <div class="brilho" style="width:700px;height:700px;background:#fff;opacity:.3;left:-200px;top:-200px"></div>
    {chama_bg(700, 860, 520, 16)}
    {marca(70, 64, marinho=True)}
    <div class="setas" style="right:70px;top:78px;color:#171276">{pagina}</div>
    <h1 style="position:absolute;left:70px;top:190px;width:470px;font-size:80px;line-height:1.1">Comente <span style="background:#171276;color:#fff;border-radius:24px;padding:0 22px">{palavra}</span><br>e receba o link no direct</h1>
    <p style="position:absolute;left:70px;top:700px;width:420px;font-size:34px;font-weight:800;line-height:1.28">Baixe grátis, informe o CEP e pague só na entrega: Pix, cartão ou dinheiro.</p>
    <div class="palco" style="width:560px;height:560px;right:-60px;bottom:130px"></div>
    <img class="mascote" src="{m}" style="height:860px;right:-10px;bottom:110px">
    <div class="rodape" style="bottom:46px;color:#fff"><span>📲 App Store e Google Play</span><span>app.donagas.com.br</span></div>
    """
    return doc(1080, 1350, body, "rosa tx-listras")


# ---------------------------------------------------------------------------
# Story 1080x1920 (área segura: topo 250, base 340)
# ---------------------------------------------------------------------------
def story(titulo, texto, mascote, fundo="marinho", palavra="APP"):
    from PIL import Image
    if mascote == "mascote-senhora.png":      # cena recortada: não serve para story
        mascote = "mascote-joia.png"
    im = Image.open(A / mascote)
    alt = 700
    larg = int(alt * im.width / im.height)
    m = b64(A / mascote)
    cls = "marinho tx-listras" if fundo == "marinho" else "rosa tx-listras"
    palco = "palco" if fundo == "marinho" else "palco rosa-p"
    em_cor = "#FF47A3" if fundo == "marinho" else "#171276"
    esq = 1080 - 60 - larg                      # borda esquerda do mascote
    pw = max(380, min(500, esq - 80 - 30))      # texto nunca encosta no mascote
    body = f"""
    <div class="brilho" style="width:800px;height:800px;background:{'#FF47A3' if fundo=='marinho' else '#fff'};opacity:.3;right:-250px;top:700px"></div>
    {chama_bg(-160, 1240, 560, -16)}{chama_bg(780, 220, 360, 12)}
    {marca(80, 270, marinho=(fundo != 'marinho'))}
    <h1 style="position:absolute;left:80px;top:390px;width:920px;font-size:{104 if len(titulo) < 40 else 90}px;line-height:1.02">{esc(titulo).replace('<em>', f'<em style="color:{em_cor}">')}</h1>
    <p style="position:absolute;left:80px;top:{760 if len(titulo) < 40 else 800}px;width:{pw}px;font-size:46px;font-weight:800;line-height:1.28">{esc(texto)}</p>
    <div class="{palco}" style="width:620px;height:620px;right:-70px;bottom:520px"></div>
    <img class="mascote" src="{m}" style="height:{alt}px;right:60px;bottom:500px">
    <div style="position:absolute;left:80px;right:80px;bottom:340px;background:#fff;color:#171276;border-radius:40px;padding:30px 40px;font-weight:900;font-size:44px;text-align:center;box-shadow:0 20px 40px rgba(0,0,0,.25)">
      Responda <span style="background:#FF47A3;color:#fff;border-radius:18px;padding:0 16px">{palavra}</span> a este story 💬<br><span style="font-size:32px;font-weight:800;color:#3a3580">e receba o link do app no direct</span>
    </div>
    """
    return doc(1080, 1920, body, cls)


# ---------------------------------------------------------------------------
async def render_all(jobs):
    """jobs: lista de (html, caminho_saida, largura, altura)."""
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page()
        for h, out, w, hh in jobs:
            await pg.set_viewport_size({"width": w, "height": hh})
            await pg.set_content(h)
            await pg.wait_for_timeout(250)
            os.makedirs(os.path.dirname(out), exist_ok=True)
            await pg.screenshot(path=out, type="jpeg", quality=90)
        await b.close()


def render(jobs):
    asyncio.run(render_all(jobs))
