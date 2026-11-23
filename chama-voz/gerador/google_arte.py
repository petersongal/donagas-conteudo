import asyncio, pathlib, sys
from playwright.async_api import async_playwright
sys.path.insert(0,'.')
from interno import FONTS
ROOT=pathlib.Path('.').resolve()
pr=[("airfryer","Air Fryer"),("liquidificador","Liquidificador"),("sanduicheira","Sanduicheira"),("mixer","Mixer")]
meds=''.join(f'<div style="display:flex;flex-direction:column;align-items:center;width:180px"><div style="width:160px;height:160px;border-radius:50%;background:radial-gradient(circle at 35% 28%,#fff,#fff9e3 55%,#f1e6bd);box-shadow:0 0 0 8px #f8d527,0 0 0 13px #b47c05,0 14px 20px rgba(0,0,0,.35);display:flex;align-items:center;justify-content:center"><img src="assets/chama-premio-{a}.webp" style="max-width:70%;max-height:70%"></div><div style="font-weight:900;font-size:21px;margin-top:16px;white-space:nowrap;text-transform:uppercase;-webkit-text-stroke:.1em #0b2e57;paint-order:stroke fill">{b}</div></div>' for a,b in pr)
h=f'''<html><head><meta charset="utf-8"><style>{FONTS}
body{{width:1200px;height:900px;overflow:hidden;font-family:Nu;color:#fff;position:relative;background:radial-gradient(80% 70% at 40% 40%,#3f9cf0 0%,#1f6fc4 35%,#134f93 65%,#0a2c55 100%)}}
.pat{{position:absolute;inset:0;opacity:.07;background-image:radial-gradient(#fff 2.2px,transparent 2.6px);background-size:40px 40px}}
.t{{font-weight:900;text-transform:uppercase;line-height:.98;letter-spacing:-.02em;-webkit-text-stroke:.1em #0b2e57;paint-order:stroke fill;text-shadow:0 .07em 0 #061a33}}
</style></head><body><div class="pat"></div>
<img src="assets/chama-senhora-comemorando.webp" style="position:absolute;right:-40px;bottom:-40px;height:860px;filter:drop-shadow(0 20px 30px rgba(0,0,0,.45))">
<div style="position:absolute;left:60px;top:60px;width:760px">
<div class="t" style="font-size:42px;color:#f8d527">Promoção de fim de ano</div>
<div class="t" style="font-size:118px;margin-top:10px">Chama</div><div class="t" style="font-size:118px;color:#f8d527">da Sorte</div>
<div style="display:inline-block;margin-top:24px;background:#f8d527;color:#0b2e57;border:6px solid #0b2e57;border-radius:20px;padding:6px 22px 10px;font-weight:900;font-size:40px;white-space:nowrap;text-transform:uppercase;box-shadow:0 8px 0 #061a33">20 prêmios para a sua cozinha</div>
<div style="display:flex;gap:12px;margin-top:46px">{meds}</div>
<div style="font-weight:700;font-size:20px;margin-top:26px;opacity:.85">Sorteio em 05/01/2027 · imagens ilustrativas · regulamento no site</div></div>
<script>document.fonts.ready.then(()=>window.READY=true)</script></body></html>'''
(ROOT/'_g.html').write_text(h,encoding='utf-8')
async def m():
    async with async_playwright() as p:
        b=await p.chromium.launch(args=["--allow-file-access-from-files"]);pg=await b.new_page(viewport={"width":1200,"height":900})
        await pg.goto(f"file://{ROOT}/_g.html");await pg.wait_for_function("window.READY===true");await pg.wait_for_timeout(300)
        await pg.screenshot(path="saida/google-chama-teste.jpg",type="jpeg",quality=90);await b.close()
asyncio.run(m())
