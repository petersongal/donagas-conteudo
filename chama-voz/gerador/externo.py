"""Vídeo EXTERNO (clientes: Reels do @famagas_ e status) da campanha Chama da Sorte. Derivado de interno.py.
Cenas: gancho → prêmios (medalhões) → como participar (3 passos) → selo + regras curtas → chamada (0800 + link).
Campos do dia.json: data, slug, pose_a, pose_e, hook, arg{topo,ouro,linhas}, passos[3], fecho, voz[5].

Base: Vídeo INTERNO diário da campanha Chama da Sorte para o grupo "Equipe Fama gás".
1080x1920, 22 s, 30 fps, com trilha sintetizada.
Uso: python3 interno.py dia.json previa 1,5,10,15,20   -> previa/*.jpg
     python3 interno.py dia.json render                -> saida/interno-AAAA-MM-DD.mp4
Pasta: assets/ (chama-*.webp do site, public/chama/) e fonts/ (@fontsource barlow-condensed e nunito).
dia.json: {data, pose_a, pose_e, hook:[[texto,estilo]...], arg:{topo, ouro, linhas[]},
           ranking:[{cidade,n}...] (já ordenado), total, meta, acao:[3 textos], fecho:[[texto,estilo]...]}
estilos: w branco, y amarelo, chip tarja amarela, chipr tarja vermelha.
"""
import asyncio, json, sys, subprocess, os, wave, pathlib
import numpy as np
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).parent
FPS, DUR = 30, 22.0
T = [0, 3.6, 8.0, 13.0, 18.0, 22.0]
BASE = [3.4, 4.2, 4.6, 4.6, 5.0]   # duração mínima de cada cena (s)

def dur_audio(f):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)], capture_output=True, text=True).stdout
    return float(out.strip())

def tempos(cfg):
    """Com locução (cfg["voz"] = 5 arquivos, um por cena), cada cena dura o necessário para a fala caber."""
    global T, DUR
    if cfg.get("voz"):
        d = [max(BASE[k], 0.35 + dur_audio(ROOT / f) + 0.45) for k, f in enumerate(cfg["voz"])]
        T = [0.0]
        for x in d: T.append(round(T[-1] + x, 2))
        DUR = T[-1]


FONTS = """
@font-face{font-family:"BC";src:url("fonts/barlow-condensed-latin-900-italic.woff2");font-weight:900;font-style:italic}
@font-face{font-family:"BC";src:url("fonts/barlow-condensed-latin-800-italic.woff2");font-weight:800;font-style:italic}
@font-face{font-family:"BC";src:url("fonts/barlow-condensed-latin-900-normal.woff2");font-weight:900}
@font-face{font-family:"Nu";src:url("fonts/nunito-latin-700-normal.woff2");font-weight:700}
@font-face{font-family:"Nu";src:url("fonts/nunito-latin-800-normal.woff2");font-weight:800}
@font-face{font-family:"Nu";src:url("fonts/nunito-latin-900-normal.woff2");font-weight:900}
:root{--az:#185ea7;--noite:#0b2e57;--am:#f8d527;--cr:#fff9e3;--vm:#e4352b}
*{box-sizing:border-box}html,body{margin:0;background:#000}
"""
CSS = FONTS + """
#st{position:relative;width:1080px;height:1920px;overflow:hidden;font-family:Nu,sans-serif;color:#fff}
.sc{position:absolute;inset:0;overflow:hidden;background:radial-gradient(80% 50% at 50% 38%,#3f9cf0 0%,#1f6fc4 32%,#134f93 60%,#0a2c55 100%)}
.sc.r{background:radial-gradient(80% 50% at 50% 38%,#f4574b 0%,#d9302a 40%,#9e1a14 100%)}
.pat{position:absolute;inset:0;opacity:.07;background-image:radial-gradient(#fff 2.2px,transparent 2.6px);background-size:44px 44px}
.rays{position:absolute;left:50%;top:44%;width:2600px;height:2600px;margin:-1300px;border-radius:50%;background:repeating-conic-gradient(rgba(255,255,255,.085) 0 9deg,transparent 9deg 18deg)}
.col{z-index:3;position:absolute;left:60px;right:60px;display:flex;flex-direction:column;align-items:center;text-align:center}
.t{font-weight:900;text-transform:uppercase;line-height:.98;white-space:nowrap;letter-spacing:-.02em}
.w{color:#fff;-webkit-text-stroke:.11em #0b2e57;paint-order:stroke fill;text-shadow:0 .07em 0 #061a33}
.y{color:var(--am);-webkit-text-stroke:.11em #0b2e57;paint-order:stroke fill;text-shadow:0 .07em 0 #061a33}
.chip{background:var(--am);color:var(--noite);border:.07em solid #0b2e57;border-radius:.32em;padding:.04em .3em .1em;box-shadow:0 .1em 0 #061a33}
.chipr{background:var(--vm);color:#fff;border:.07em solid #0b2e57;border-radius:.32em;padding:.04em .3em .1em;box-shadow:0 .1em 0 #061a33}
.gold{position:relative;display:inline-block;font-weight:900;line-height:.9;letter-spacing:-.03em;white-space:nowrap}
.gold .s{color:#8a5a00;text-shadow:0 .012em 0 #a36c00,0 .03em 0 #8f5c00,0 .06em 0 #7a4d00,0 .1em .06em rgba(0,0,0,.45);-webkit-text-stroke:.035em #7a4d00}
.gold .f{position:absolute;left:0;top:0;background:linear-gradient(180deg,#fffbe0 0%,#ffe873 22%,#f8d527 46%,#e2a40c 60%,#ffe77a 78%,#fff6c4 100%);-webkit-background-clip:text;background-clip:text;color:transparent}
.pes{position:absolute;filter:drop-shadow(0 20px 30px rgba(0,0,0,.45))}
.coin{position:absolute;left:0;top:0;filter:drop-shadow(0 12px 12px rgba(0,0,0,.4))}
#aviso{z-index:50;position:absolute;left:0;right:0;top:0;height:112px;background:var(--am);border-bottom:8px solid #0b2e57;display:flex;flex-direction:column;align-items:center;justify-content:center;color:#0b2e57;font-weight:900;text-align:center;box-shadow:0 8px 20px rgba(0,0,0,.35)}
#aviso b{font-size:40px;letter-spacing:.02em;line-height:1}#aviso span{font-size:25px;letter-spacing:.06em;margin-top:6px}
.pod{position:absolute;bottom:0;border-radius:26px 26px 0 0;border:7px solid #0b2e57;border-bottom:0;display:flex;flex-direction:column;align-items:center;justify-content:flex-start;padding-top:22px;box-shadow:inset 0 -40px 60px rgba(0,0,0,.18)}
.pod .pos{font-family:BC;font-weight:900;font-style:italic;font-size:150px;line-height:.85;color:#0b2e57}
.pod .num{font-weight:900;font-size:44px;color:#0b2e57;margin-top:10px}
.cid{position:absolute;width:330px;text-align:center;font-weight:900;font-size:52px;line-height:1.02;text-transform:uppercase;color:#fff;-webkit-text-stroke:.1em #0b2e57;paint-order:stroke fill}
.crown{position:absolute;font-size:90px}
.step{display:flex;align-items:center;gap:30px;background:var(--cr);color:var(--noite);border:7px solid #0b2e57;border-radius:34px;padding:26px 34px;width:940px;text-align:left;box-shadow:0 14px 0 #061a33;margin-top:44px}
.step b{flex:none;width:110px;height:110px;border-radius:50%;background:var(--vm);color:#fff;font-family:BC;font-style:italic;font-weight:900;font-size:86px;display:flex;align-items:center;justify-content:center;border:6px solid #0b2e57}
.step span{font-weight:900;font-size:56px;line-height:1.1}
.bar{width:900px;height:74px;border-radius:40px;background:#061a33;border:6px solid #0b2e57;overflow:hidden;position:relative;box-shadow:0 10px 0 #061a33}
.bar i{position:absolute;left:0;top:0;bottom:0;background:linear-gradient(90deg,#f8d527,#ffe873);border-radius:40px}
.cf{position:absolute;border-radius:5px}
.step.s4{padding:20px 30px;margin-top:30px}.step.s4 span{font-size:48px}.step.s4 b{width:96px;height:96px;font-size:74px}
"""

JS = r"""
const $=s=>document.querySelector(s), clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x)), cub=p=>1-Math.pow(1-p,3),
 expo=p=>p>=1?1:1-Math.pow(2,-10*p), back=p=>{const c=1.9;return 1+(c+1)*Math.pow(p-1,3)+c*Math.pow(p-1,2)};
const T=TT;
function rnd(i){const x=Math.sin(i*127.1+311.7)*43758.5453;return x-Math.floor(x)}
function gold(t,sz){return `<span class="gold" style="font-size:${sz}px"><span class="s">${t}</span><span class="f">${t}</span></span>`}
function coins(n,cls){let h='';for(let i=0;i<n;i++)h+=`<img class="coin ${cls}" data-i="${i}" src="assets/chama-moeda1.webp" style="width:${90+rnd(i+40)*70}px">`;return h}
function lines(arr,t0,step,max){return arr.map((l,i)=>`<div class="t ${l[1]} fit" data-in="${(t0+i*step).toFixed(2)}" data-fx="slam" data-max="${max}" style="margin-top:${i?26:0}px">${l[0]}</div>`).join('')}
function build(){
 const A=`<div class="sc" id="A"><div class="pat"></div><div class="rays"></div>
  <img class="pes" data-in="0" data-fx="up" src="assets/chama-senhora-${C.pose_a}.webp" style="left:50%;margin-left:-410px;bottom:-60px;height:1250px">
  <div style="position:absolute;left:0;right:0;bottom:0;height:520px;background:linear-gradient(0deg,rgba(6,24,48,.92),transparent)"></div>
  <div class="col" style="top:120px">${lines(C.hook,0.1,0.42,138)}</div></div>`;
 const B=`<div class="sc" id="B"><div class="pat"></div>${coins(9,'cb')}
  <div class="col" style="top:250px"><div class="t w fit" data-max="96" data-in="0.2" data-fx="up">${C.arg.topo}</div>
   <div data-in="0.55" data-fx="pop" style="margin-top:50px">${gold(C.arg.ouro,C.arg.ouro.length>6?260:360)}</div>
   ${C.arg.linhas.map((l,i)=>`<div class="t ${i==C.arg.linhas.length-1?'chip':'y'} fit" data-max="96" data-in="${(1.1+i*0.35).toFixed(2)}" data-fx="up" style="margin-top:${i?26:60}px">${l}</div>`).join('')}
  </div><img data-in="1.9" data-fx="up" src="assets/chama-hero.webp" style="position:absolute;left:50%;margin-left:-470px;bottom:-40px;width:940px;z-index:2"></div>`;
 const PR=[['4x','Air Fryer','airfryer'],['5x','Liquidificador','liquidificador'],['5x','Sanduicheira','sanduicheira'],['4x','Mixer','mixer'],['2x','Jogo de panelas','panelas']];
 const pos=[[90,520],[570,520],[90,960],[570,960],[330,1400]];
 const Cc=`<div class="sc" id="C"><div class="pat"></div><div class="rays"></div>
  <div class="col" style="top:150px"><div class="t chip" data-in="0.1" data-fx="slam" style="font-size:96px">20 prêmios</div>
   <div class="t w fit" data-max="76" data-in="0.4" data-fx="up" style="margin-top:36px">pra sua cozinha!</div></div>
  ${PR.map((p,k)=>`<div data-in="${(0.7+k*0.25).toFixed(2)}" data-fx="pop" style="position:absolute;left:${pos[k][0]}px;top:${pos[k][1]}px;width:420px;text-align:center">
   <div style="position:relative;width:330px;height:330px;margin:0 auto;border-radius:50%;background:radial-gradient(circle at 35% 28%,#fff,#fff9e3 55%,#f1e6bd);box-shadow:0 0 0 12px #f8d527,0 0 0 18px #b47c05,0 22px 30px rgba(0,0,0,.4);display:flex;align-items:center;justify-content:center">
   <img src="assets/chama-premio-${p[2]}.webp" style="max-width:72%;max-height:72%;object-fit:contain">
   <span style="position:absolute;right:-6px;top:-12px;width:110px;height:110px;border-radius:50%;background:var(--vm);color:#fff;font-weight:900;font-size:50px;display:flex;align-items:center;justify-content:center;border:7px solid #fff">${p[0]}</span></div>
   <div class="t w" style="font-size:46px;margin-top:26px">${p[1]}</div></div>`).join('')}
  <div class="col" style="top:1830px"><div style="font-weight:800;font-size:26px;opacity:.9">Imagens meramente ilustrativas.</div></div></div>`;
 const D=`<div class="sc" id="D"><div class="pat"></div>
  <div class="col" style="top:150px"><div class="t chipr" data-in="0.1" data-fx="slam" style="font-size:96px">${C.passos_titulo||'Como participar'}</div>
   ${C.passos.map((a,i)=>`<div class="step${C.passos.length>3?' s4':''}" data-in="${(0.6+i*0.55).toFixed(2)}" data-fx="pop"><b>${i+1}</b><span>${a}</span></div>`).join('')}
  </div>
  <img class="pes" data-in="1.4" data-fx="up" src="assets/chama-senhora-apontando-flip.webp" style="left:-40px;bottom:-60px;height:960px"></div>`;
 const E=`<div class="sc" id="E"><div class="pat"></div><div class="rays"></div><div id="conf"></div>${coins(8,'ce')}
  <img data-in="0.1" data-fx="pop" src="assets/chama-selo.webp" style="position:absolute;left:50%;margin-left:-300px;top:60px;width:600px">
  <div class="col" style="top:760px">${lines(C.fecho,0.5,0.35,92)}
   <div id="fone" data-in="1.2" data-fx="pop" style="margin-top:36px;background:var(--am);color:var(--noite);border-radius:40px;padding:16px 40px 22px;border:8px solid #0b2e57;box-shadow:0 16px 0 #061a33"><div style="font-weight:900;font-size:32px;letter-spacing:.03em">LIGUE GRÁTIS E PEÇA SEU GÁS</div><div style="font-family:BC;font-style:italic;font-weight:900;font-size:118px;line-height:.95">0800 010 9669</div></div>
   <div data-in="1.6" data-fx="up" style="margin-top:34px;font-weight:900;font-size:42px;line-height:1.2;text-shadow:0 4px 0 #061a33">Já comprou? Pegue seus 100 números:<br><span style="color:var(--am);background:#061a33;padding:8px 18px;border-radius:14px;display:inline-block;margin-top:12px;font-size:40px">famagas.com.br/chama-da-sorte</span></div>
   <div data-in="1.9" data-fx="up" style="margin-top:30px"><div class="t chipr" style="font-size:58px">Sorteio 05/01/2027</div></div></div>
  <div style="z-index:9;position:absolute;left:0;right:0;bottom:0;padding:14px 50px 20px;background:rgba(6,24,48,.88);color:#dbe6f4;font-weight:700;font-size:22px;line-height:1.3;text-align:center">Participação até 31/12/2026 com compra de gás na FamaGás. 100 números por CPF a cada mês com compra. Imagens ilustrativas. Regulamento em famagas.com.br/chama-da-sorte/regulamento</div></div>`;
 $('#st').innerHTML=A+B+Cc+D+E;
 let cf='';for(let i=0;i<60;i++){const s=14+rnd(i)*22;cf+=`<i class="cf" data-i="${i}" style="width:${s}px;height:${s*(rnd(i+9)>.5?1:.45)}px;background:${['#f8d527','#fff','#e4352b','#7fb6ee'][i%4]}"></i>`}
 $('#conf').innerHTML=cf;
 document.querySelectorAll('.fit').forEach(e=>{let f=+e.dataset.max;e.style.fontSize=f+'px';while(e.getBoundingClientRect().width>930&&f>36){f-=2;e.style.fontSize=f+'px'}});
 document.querySelectorAll('.fit2').forEach(e=>{let f=52;e.style.fontSize=f+'px';while(e.scrollWidth>330&&f>22){f-=2;e.style.fontSize=f+'px'}});
}
function fx(e,p,k){
 if(k==='pop'){const s=p<=0?0:0.3+0.7*back(clamp(p));e.style.transform=`scale(${s})`;e.style.opacity=clamp(p*4)}
 else if(k==='up'){e.style.transform=(e.dataset.base||'')+` translateY(${(1-cub(clamp(p)))*90}px)`;e.style.opacity=clamp(p*2.5)}
 else if(k==='slam'){const q=expo(clamp(p));e.style.transform=`scale(${2.6-1.6*q}) rotate(${(1-q)*-6}deg)`;e.style.opacity=clamp(p*5)}
 else if(k==='rise'){e.style.transform=`translateY(${(1-back(clamp(p)))*1100}px)`;e.style.opacity=p>0?1:0}
}
window.render=function(t){
 ['A','B','C','D','E'].forEach((id,k)=>{const sc=$('#'+id),t0=T[k],t1=T[k+1],on=t>=t0&&t<t1+0.0001||(k<4&&t>=t1&&t<t1+0.4);
  sc.style.display=on?'block':'none';if(!on)return;sc.style.zIndex=k;
  let tr='';if(k>0){const p=cub(clamp((t-t0)/0.38));tr=k%2?`translateX(${(1-p)*1080}px)`:`translateY(${(1-p)*1920}px)`}
  if(k===0){let sh=0;C.hook.forEach((l,i)=>{const d=t-(0.1+i*0.42)-0.12;if(d>0&&d<0.16)sh=(1-d/0.16)*10});tr+=` translate(${Math.sin(t*90)*sh}px,${Math.cos(t*70)*sh}px)`}
  sc.style.transform=tr;
  sc.querySelectorAll('[data-in]').forEach(e=>fx(e,(t-t0-(+e.dataset.in))/0.42,e.dataset.fx));
  const r=sc.querySelector('.rays');if(r)r.style.transform=`rotate(${t*14}deg)`;});
 const fall=(cls,t0)=>document.querySelectorAll('.'+cls).forEach(e=>{const i=+e.dataset.i,d=t-t0-0.3-rnd(i+13)*1.4;if(d<0){e.style.opacity=0;return}
  const x=40+rnd(i+21)*900+Math.sin(d*2+i)*30,y=-200+d*(430+rnd(i+22)*380);e.style.opacity=y>1750?0:1;e.style.transform=`translate(${x}px,${y}px) rotate(${d*140*(rnd(i+25)-.5)}deg)`});
 fall('cb',T[1]);fall('ce',T[4]);
 if(t>T[4]+1.8)$('#fone').style.transform=`scale(${1+0.035*Math.sin((t-T[4])*7)})`;
 const td=t-T[4];document.querySelectorAll('.cf').forEach(e=>{const i=+e.dataset.i,d=td-0.25-rnd(i+3)*0.9;if(d<0){e.style.opacity=0;return}
  const x=rnd(i+1)*1080+Math.sin(d*3+i)*40,y=-60+d*(520+rnd(i+2)*520);e.style.opacity=y>1700?0:.9;e.style.transform=`translate(${x}px,${y}px) rotate(${d*300*(rnd(i+5)-.5)}deg)`});
};
document.fonts.ready.then(()=>{build();window.render(0);window.READY=true});
"""

def html(cfg):
    s = (f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div id="st"></div><script>'
         f'const C={json.dumps(cfg, ensure_ascii=False)},TT={json.dumps(T)};{JS}</script></body></html>')
    (ROOT / "render-externo.html").write_text(s, encoding="utf-8")

# ---------- áudio ----------
SR = 44100
def env(n, a=0.002, d=0.05):
    t = np.arange(n) / SR; return np.minimum(1, t / a) * np.exp(-t / d)
def pluck(f, dur=0.5, g=0.3):
    n = int(dur * SR); t = np.arange(n) / SR
    return sum(np.sin(2 * np.pi * f * k * t) / k ** 1.6 for k in range(1, 6)) * env(n, 0.002, dur / 3.2) * g
def bass(f, dur=0.45):
    n = int(dur * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t)) * env(n, 0.004, dur / 2.2) * 0.42
def kick():
    n = int(0.22 * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * (48 * t + 60 * (1 - np.exp(-t * 28)) / 28)) * env(n, 0.001, 0.07) * 0.75
def noise(r, d, dec, g): n = int(d * SR); return r.uniform(-1, 1, n) * env(n, 0.001, dec) * g
def whoosh(r):
    n = int(0.42 * SR); t = np.arange(n) / SR; x = r.uniform(-1, 1, n); out = np.zeros(n); y = 0.0
    for i in range(n):
        a = 0.02 + 0.5 * (i / n) ** 1.5; y += a * (x[i] - y); out[i] = y
    return out * np.sin(np.pi * t / t[-1]) ** 2 * 0.8
def hit(r):
    n = int(0.3 * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * 85 * t * np.exp(-t * 5)) * 0.9 + r.uniform(-1, 1, n) * 0.25) * env(n, 0.001, 0.07) * 0.8
def pop():
    n = int(0.11 * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * (520 + 900 * t / t[-1]) * t) * env(n, 0.001, 0.03) * 0.45
def chime():
    n = int(1.5 * SR); t = np.arange(n) / SR; s = np.zeros(n)
    for k, f in enumerate([1046.5, 1318.5, 1568.0, 2093.0]):
        st = int(k * 0.07 * SR); tt = t[: n - st]; s[st:] += np.sin(2 * np.pi * f * tt) * np.exp(-tt / 0.45) * 0.22
    return s

def audio(cfg, path, seed):
    r = np.random.default_rng(seed); mix = np.zeros(int(DUR * SR) + 1)
    def add(t, s, g=1.0):
        i = int(t * SR)
        if 0 <= i < len(mix): j = min(len(mix), i + len(s)); mix[i:j] += s[: j - i] * g
    beat = 60 / 124; k = 2 ** ([0, 2, -2, 3, -3][seed % 5] / 12)
    ch = [[261.6, 329.6, 392.0], [196.0, 246.9, 293.7], [220.0, 261.6, 329.6], [174.6, 220.0, 261.6]]
    for b in range(int(DUR / beat) + 1):
        t = b * beat; c = ch[(b // 4) % 4]; cheio = t >= T[1] - 0.01
        add(t, kick(), 1.0 if cheio else 0.8)
        if b % 2 == 1: add(t, noise(r, 0.14, 0.035, 0.3))
        for s in range(4): add(t + s * beat / 4, noise(r, 0.05, 0.014, 0.08), 1.0 if cheio else 0.5)
        if cheio:
            add(t, bass(c[0] * k / 2)); add(t + beat / 2, bass(c[0] * k / 2), 0.8)
            for s, ni in enumerate([0, 1, 2, 1]): add(t + s * beat / 4, pluck(c[ni] * k * 2, 0.4), 0.9)
            if b % 4 == 0:
                for f in c: add(t, pluck(f * k, 0.9, 0.22))
    for i in range(len(cfg["hook"])): add(0.1 + i * 0.42 + 0.1, hit(r), 0.9)
    for t0 in T[1:5]: add(t0 - 0.05, whoosh(r), 0.8)
    add(T[1] + 0.6, hit(r), 0.7); add(T[1] + 0.8, chime(), 0.8)
    add(T[2] + 0.2, hit(r), 0.8)
    for i in range(3): add(T[2] + 1.0 + i * 0.3, pop())
    add(T[2] + 2.0, chime(), 0.8)
    add(T[3] + 0.2, hit(r), 0.8)
    for i in range(3): add(T[3] + 0.7 + i * 0.55, pop())
    add(T[4] + 0.4, hit(r), 0.7); add(T[4] + 2.3, chime(), 1.0)
    mix *= 0.8
    if cfg.get("voz"):
        voz = np.zeros_like(mix)
        for k, f in enumerate(cfg["voz"]):
            raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(ROOT / f), "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"], capture_output=True).stdout
            v = np.frombuffer(raw, dtype=np.int16).astype(np.float64) / 32767
            v = v / (np.abs(v).max() + 1e-9) * 0.95
            i = int((T[k] + 0.35) * SR); j = min(len(voz), i + len(v)); voz[i:j] += v[: j - i]
        # música abaixa (ducking) enquanto a voz fala
        envv = np.convolve(np.abs(voz), np.ones(int(0.15 * SR)) / int(0.15 * SR), mode="same")
        duck = 1 - 0.72 * np.clip(envv * 8, 0, 1)
        mix = mix * duck + voz * 1.0
    fo = int(1.2 * SR); mix[-fo:] *= np.linspace(1, 0, fo) ** 1.5
    mix = np.tanh(mix * 1.1) * 0.92
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())

async def abrir(p):
    b = await p.chromium.launch(args=["--allow-file-access-from-files"])
    pg = await b.new_page(viewport={"width": 1080, "height": 1920})
    await pg.goto(f"file://{ROOT}/render-externo.html")
    await pg.wait_for_function("window.READY===true"); await pg.wait_for_timeout(500)
    return b, pg

async def previa(ts):
    (ROOT / "previa").mkdir(exist_ok=True)
    async with async_playwright() as p:
        b, pg = await abrir(p)
        for t in ts:
            await pg.evaluate(f"window.render({t})")
            await pg.screenshot(path=str(ROOT / "previa" / f"i-{t:05.2f}.jpg"), type="jpeg", quality=70)
        await b.close()

async def render(cfg):
    out = ROOT / "saida"; out.mkdir(exist_ok=True)
    mudo = ROOT / "_mudo.mp4"; wav = ROOT / "_audio.wav"; final = out / f"externo-{cfg['data']}-{cfg.get('slug','x')}.mp4"
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "mjpeg", "-i", "-",
                           "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-pix_fmt", "yuv420p", str(mudo)], stdin=subprocess.PIPE)
    async with async_playwright() as p:
        b, pg = await abrir(p)
        for i in range(int(DUR * FPS)):
            await pg.evaluate(f"window.render({i / FPS})")
            ff.stdin.write(await pg.screenshot(type="jpeg", quality=88))
        await b.close()
    ff.stdin.close()
    if ff.wait() != 0: raise SystemExit("ffmpeg falhou")
    audio(cfg, wav, int(cfg["data"].replace("-", "")) % 97)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mudo), "-i", str(wav), "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", str(final)], check=True)
    mudo.unlink(); wav.unlink()
    print("ok", final, round(final.stat().st_size / 1e6, 1), "MB")

if __name__ == "__main__":
    cfg = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
    tempos(cfg); html(cfg)
    if sys.argv[2] == "previa": asyncio.run(previa([float(x) for x in sys.argv[3].split(",")]))
    else: asyncio.run(render(cfg))
