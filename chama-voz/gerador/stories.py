"""Stories (1080x1920 JPG) da campanha Chama da Sorte para o @famagas_.
Uso: python3 stories.py stories.json saida_dir
stories.json: [{"id": "...", "modelo": "pessoa|premios|contagem|numeros", "l1": "...", "l2": "...", "l3": "...", "pose": "rosto|comemorando|apontando-flip", "dias": N}]
Assets em assets/ (chama-*.webp do site) e fontes em fonts/ (mesmas do interno.py).
Área segura: conteúdo entre y=230 e y=1640 (topo e rodapé do Instagram cobrem o resto).
"""
import asyncio, json, sys, pathlib
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).parent
sys.path.insert(0, str(ROOT))
from interno import FONTS

CSS = FONTS + """
body{width:1080px;height:1920px;overflow:hidden;font-family:Nu,sans-serif;color:#fff;
 background:radial-gradient(80% 50% at 50% 38%,#3f9cf0 0%,#1f6fc4 32%,#134f93 60%,#0a2c55 100%);position:relative}
.pat{position:absolute;inset:0;opacity:.07;background-image:radial-gradient(#fff 2.2px,transparent 2.6px);background-size:44px 44px}
.rays{position:absolute;left:50%;top:44%;width:2600px;height:2600px;margin:-1300px;border-radius:50%;background:repeating-conic-gradient(rgba(255,255,255,.085) 0 9deg,transparent 9deg 18deg);transform:rotate(7deg)}
.col{position:absolute;left:60px;right:60px;display:flex;flex-direction:column;align-items:center;text-align:center;z-index:3}
.t{font-weight:900;text-transform:uppercase;line-height:.98;letter-spacing:-.02em}
.w{color:#fff;-webkit-text-stroke:.11em #0b2e57;paint-order:stroke fill;text-shadow:0 .07em 0 #061a33}
.y{color:var(--am);-webkit-text-stroke:.11em #0b2e57;paint-order:stroke fill;text-shadow:0 .07em 0 #061a33}
.chip{background:var(--am);color:var(--noite);border:.07em solid #0b2e57;border-radius:.32em;padding:.04em .3em .1em;box-shadow:0 .1em 0 #061a33}
.chipr{background:var(--vm);color:#fff;border:.07em solid #0b2e57;border-radius:.32em;padding:.04em .3em .1em;box-shadow:0 .1em 0 #061a33}
.gold{position:relative;display:inline-block;font-weight:900;line-height:.9;letter-spacing:-.03em;white-space:nowrap}
.gold .s{color:#8a5a00;text-shadow:0 .03em 0 #8f5c00,0 .06em 0 #7a4d00,0 .1em .06em rgba(0,0,0,.45);-webkit-text-stroke:.035em #7a4d00}
.gold .f{position:absolute;left:0;top:0;background:linear-gradient(180deg,#fffbe0 0%,#ffe873 22%,#f8d527 46%,#e2a40c 60%,#ffe77a 78%,#fff6c4 100%);-webkit-background-clip:text;background-clip:text;color:transparent}
.pes{position:absolute;filter:drop-shadow(0 20px 30px rgba(0,0,0,.45))}
.fone{background:var(--am);color:var(--noite);border-radius:36px;padding:14px 36px 18px;border:8px solid #0b2e57;box-shadow:0 14px 0 #061a33;text-align:center}
.fone small{display:block;font-weight:900;font-size:28px;letter-spacing:.03em}.fone b{font-family:BC;font-style:italic;font-weight:900;font-size:100px;line-height:.95}
.link{color:var(--am);background:#061a33;padding:10px 20px;border-radius:16px;font-weight:900;font-size:40px}
.med{position:relative;width:220px;height:220px;border-radius:50%;background:radial-gradient(circle at 35% 28%,#fff,#fff9e3 55%,#f1e6bd);box-shadow:0 0 0 10px #f8d527,0 0 0 16px #b47c05,0 18px 26px rgba(0,0,0,.4);display:flex;align-items:center;justify-content:center}
.med img{max-width:72%;max-height:72%;object-fit:contain}
.coin{position:absolute;filter:drop-shadow(0 12px 12px rgba(0,0,0,.4))}
.legal{position:absolute;left:0;right:0;bottom:225px;text-align:center;font-weight:700;font-size:22px;opacity:.85;padding:0 70px}
"""

def gold(t, sz): return f'<span class="gold" style="font-size:{sz}px"><span class="s">{t}</span><span class="f">{t}</span></span>'
def fit(cls, txt, mx): return f'<div class="t {cls} fit" data-max="{mx}" style="margin-top:22px">{txt}</div>'
COINS = ''.join(f'<img class="coin" src="assets/chama-moeda1.webp" style="left:{x}px;top:{y}px;width:{w}px;transform:rotate({r}deg)">'
                for x, y, w, r in [(60, 330, 110, -15), (900, 420, 90, 20), (120, 900, 70, 10), (930, 980, 120, -25)])
LEGAL = '<div class="legal">Sorteio 05/01/2027 · participação até 31/12/2026 · regulamento em famagas.com.br/chama-da-sorte · imagens ilustrativas</div>'
FONE = '<div class="fone"><small>LIGUE GRÁTIS E PEÇA SEU GÁS</small><b>0800 010 9669</b></div>'

def html(s):
    m = s["modelo"]
    if m == "pessoa":
        body = f'''<div class="rays"></div>{COINS}
<div class="col" style="top:240px">{fit('w', s['l1'], 120)}{fit('y', s['l2'], 120)}{fit('chip', s['l3'], 110)}</div>
<img class="pes" src="assets/chama-senhora-{s.get('pose','comemorando')}.webp" style="left:50%;margin-left:-330px;top:820px;height:1100px">
<img src="assets/chama-selo.webp" style="position:absolute;right:30px;top:1180px;width:360px;z-index:4;filter:drop-shadow(0 14px 20px rgba(0,0,0,.4))">
<div class="col" style="top:1500px;z-index:5"><span class="link">famagas.com.br/chama-da-sorte</span></div>'''
    elif m == "premios":
        pr = [("4x", "Air Fryer", "airfryer"), ("5x", "Liquidificador", "liquidificador"), ("5x", "Sanduicheira", "sanduicheira"), ("4x", "Mixer", "mixer")]
        meds = ''.join(f'<div style="display:flex;flex-direction:column;align-items:center;width:440px;margin-top:34px"><div class="med"><img src="assets/chama-premio-{p[2]}.webp"><span style="position:absolute;right:-6px;top:-10px;width:96px;height:96px;border-radius:50%;background:var(--vm);color:#fff;font-weight:900;font-size:44px;display:flex;align-items:center;justify-content:center;border:6px solid #fff">{p[0]}</span></div><div class="t w" style="font-size:44px;margin-top:18px">{p[1]}</div></div>' for p in pr)
        body = f'''<div class="rays"></div>
<div class="col" style="top:240px">{fit('w', s['l1'], 96)}<div style="margin-top:10px">{gold('R$ 3 MIL', 230)}</div>{fit('y', s['l2'], 80)}</div>
<div style="position:absolute;left:100px;right:100px;top:640px;display:flex;flex-wrap:wrap;justify-content:space-between">{meds}</div>
<div class="col" style="top:1440px">{FONE}</div>{LEGAL}'''
    elif m == "contagem":
        body = f'''<div class="rays"></div>{COINS}
<div class="col" style="top:250px">{fit('w', s['l1'], 100)}<div style="margin-top:14px">{gold(str(s['dias']), 520)}</div>
{fit('y', 'dias', 130)}{fit('chip', s['l2'], 84)}<div style="margin-top:60px">{FONE}</div>
<div style="margin-top:36px"><span class="link">famagas.com.br/chama-da-sorte</span></div></div>{LEGAL}'''
    else:  # numeros
        body = f'''<div class="rays"></div>{COINS}
<div class="col" style="top:250px">{fit('w', s['l1'], 110)}{fit('y', s['l2'], 110)}<div style="margin-top:20px">{gold('100', 400)}</div>
{fit('chip', 'números da sorte', 96)}</div>
<img class="pes" src="assets/chama-senhora-{s.get('pose','apontando-flip')}.webp" style="left:-60px;top:1060px;height:860px">
<div style="position:absolute;right:40px;top:1240px;width:600px;z-index:5;text-align:center;font-weight:900;font-size:46px;line-height:1.15;text-shadow:0 4px 0 #061a33">{s['l3']}<br><span class="link" style="display:inline-block;margin-top:18px;font-size:30px;white-space:nowrap">famagas.com.br/chama-da-sorte</span></div>'''
    return f'''<html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="pat"></div>{body}
<script>document.fonts.ready.then(()=>{{document.querySelectorAll('.fit').forEach(e=>{{let f=+e.dataset.max;e.style.fontSize=f+'px';while(e.getBoundingClientRect().width>950&&f>36){{f-=2;e.style.fontSize=f+'px'}}}});window.READY=true}})</script></body></html>'''

async def main(spec, out):
    out.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--allow-file-access-from-files"])
        pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        for s in spec:
            f = ROOT / "_story.html"; f.write_text(html(s), encoding="utf-8")
            await pg.goto(f"file://{f}"); await pg.wait_for_function("window.READY===true"); await pg.wait_for_timeout(300)
            await pg.screenshot(path=str(out / f"{s['id']}.jpg"), type="jpeg", quality=90)
            print("ok", s["id"])
        await b.close()

if __name__ == "__main__":
    asyncio.run(main(json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")), pathlib.Path(sys.argv[2])))
