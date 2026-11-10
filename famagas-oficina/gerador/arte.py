"""Base visual das peças do Instagram da FamaGás (@famagas_).

Design system FamaGás: azul #185EA7, amarelo #F8D527, azul-noite #0B2E57, creme #FFF9E3, branco.
Títulos em Barlow Condensed 900 itálico; texto em Nunito. Todo fundo leva textura discreta
(azul/noite: faixas brancas diagonais; amarelo/creme: pontos azul-noite). Logo sempre o arquivo oficial,
nunca digitado. Mascote: o botijão de capa, sempre inteiro (nunca recorte com mão, braço ou pé cortado).
Story/Reels 1080x1920 (área segura: 250 px no topo, 340 px na base).
"""
import base64, html
from pathlib import Path

ROOT = Path(__file__).parent
A = ROOT / "assets"
F = ROOT / "node_modules/@fontsource"


def b64(path: Path) -> str:
    ext = path.suffix.lower().lstrip(".")
    mime = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg", "webp": "image/webp", "woff2": "font/woff2"}[ext]
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()


def _face(fam, arq, peso, estilo="normal"):
    return f"@font-face{{font-family:'{fam}';font-weight:{peso};font-style:{estilo};src:url('{b64(F / arq)}') format('woff2')}}"


FONT_CSS = (
    _face("Barlow Condensed", "barlow-condensed/files/barlow-condensed-latin-900-italic.woff2", 900, "italic")
    + _face("Barlow Condensed", "barlow-condensed/files/barlow-condensed-latin-800-italic.woff2", 800, "italic")
    + _face("Barlow Condensed", "barlow-condensed/files/barlow-condensed-latin-700-normal.woff2", 700)
    + "".join(_face("Nunito", f"nunito/files/nunito-latin-{w}-normal.woff2", w) for w in (700, 800, 900))
)

AZUL, AMARELO, NOITE, CREME = "#185ea7", "#f8d527", "#0b2e57", "#fff9e3"

BASE_CSS = FONT_CSS + """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:100%;height:100%}
body{font-family:'Nunito',sans-serif;-webkit-font-smoothing:antialiased}
.c{position:relative;overflow:hidden;width:__W__;height:__H__}
.azul{background:#185ea7;color:#fff}
.noite{background:#0b2e57;color:#fff}
.amarelo{background:#f8d527;color:#0b2e57}
.creme{background:#fff9e3;color:#0b2e57}
.tx-faixas::before{content:"";position:absolute;inset:-20%;background:repeating-linear-gradient(-35deg,rgba(255,255,255,.07) 0 30px,transparent 30px 84px);pointer-events:none}
.tx-pontos::before{content:"";position:absolute;inset:0;background-image:radial-gradient(rgba(11,46,87,.16) 3px,transparent 3.4px);background-size:36px 36px;pointer-events:none;
  -webkit-mask-image:radial-gradient(circle at 100% 100%,#000 0,transparent 62%);mask-image:radial-gradient(circle at 100% 100%,#000 0,transparent 62%)}
.brilho{position:absolute;border-radius:50%;filter:blur(90px);pointer-events:none}
h1{font-family:'Barlow Condensed','Arial Narrow',sans-serif;font-weight:900;font-style:italic;letter-spacing:-1px;line-height:.95;text-transform:uppercase}
h1 em{font-style:italic;color:#f8d527}
.amarelo h1 em,.creme h1 em{color:#185ea7}
.palco{position:absolute;border-radius:50%;background:radial-gradient(circle at 50% 38%,#2a7fd0 0%,#185ea7 68%);box-shadow:0 0 0 18px #f8d527,0 0 0 40px rgba(255,255,255,.10)}
.amarelo .palco,.creme .palco{box-shadow:0 0 0 18px #0b2e57,0 0 0 40px rgba(11,46,87,.10)}
.mascote{position:absolute;filter:drop-shadow(0 30px 40px rgba(0,0,0,.35))}
.pilula{position:absolute;display:flex;align-items:center;background:#fff;border-radius:999px;padding:16px 34px;box-shadow:0 14px 34px rgba(11,46,87,.28)}
.pilula img{height:56px;width:auto;display:block}
"""

LOGO = b64(A / "logo-famagas.png")


def marca(x, y, altura=56):
    """Logo oficial numa pílula branca (funciona sobre qualquer fundo da marca)."""
    return f'<div class="pilula" style="left:{x}px;top:{y}px"><img src="{LOGO}" alt="FamaGás" style="height:{altura}px"></div>'


def doc(w, h, body, cls=""):
    css = BASE_CSS.replace("__W__", f"{w}px").replace("__H__", f"{h}px")
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body><div class="c {cls}">{body}</div></body></html>'


def esc(t):
    return html.escape(t).replace("\n", "<br>").replace("[", "<em>").replace("]", "</em>")
