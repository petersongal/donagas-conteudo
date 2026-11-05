import asyncio, sys
from playwright.async_api import async_playwright
F='/home/claude/dg-arte/node_modules/@fontsource/nunito/files/'
CSS="".join(f"@font-face{{font-family:'Nunito';font-weight:{w};src:url('/__f/nunito-latin-{w}-normal.woff2') format('woff2')}}" for w in (400,600,700,800,900))
async def main(path,out):
  async with async_playwright() as p:
    b=await p.chromium.launch()
    ctx=await b.new_context(viewport={'width':390,'height':844},device_scale_factor=3,is_mobile=True,has_touch=True)
    pg=await ctx.new_page()
    async def fonts(route): await route.fulfill(status=200,content_type='text/css',body=CSS)
    async def ff(route):
      name=route.request.url.split('/__f/')[1]; await route.fulfill(status=200,content_type='font/woff2',body=open(F+name,'rb').read())
    import re; await pg.route(re.compile(r'fonts\.googleapis\.com'),fonts)
    await pg.route('**/__f/**',ff)
    await pg.add_init_script("try{sessionStorage.setItem('donagas_intro_seen','1');localStorage.setItem('donagas_intro_seen','1')}catch(e){}")
    await pg.goto('http://localhost:8765'+path); await pg.add_style_tag(content=CSS+"*{font-family:'Nunito',sans-serif !important}"); await pg.wait_for_timeout(8000)
    await pg.screenshot(path=out)
    await b.close()
asyncio.run(main(sys.argv[1],sys.argv[2]))
