"""Fábrica de Reels do @appdonagas (roda no GitHub Actions; ver .github/workflows/reels.yml).

Para cada reels/roteiros/<id>.json que ainda não tem posts/<id>/reel.mp4:
  1) desenha os quadros 9:16 das cenas (mascote oficial no cenário da marca, SEM texto);
  2) cenas "ia": a fal.ai (Kling 2.6 Pro, imagem → vídeo, sem áudio) anima o mascote;
     cenas "texto": cartão da marca com zoom suave (custo zero);
  3) narração em português (ElevenLabs v4 Turbo na fal.ai) com tempos por palavra;
  4) monta o vídeo 1080x1920 com ffmpeg: cenas + gancho na tela + legendas animadas
     + cartão final de CTA; gera a capa;
  5) acrescenta o item tipo "reels" ao agenda.json (o publicador posta sozinho).

Sem a chave FAL_KEY (segredo do repositório) roda em MODO TESTE: anima o quadro com
zoom e usa silêncio no lugar da voz — serve para conferir o visual sem gastar nada.

Custo de referência (fal.ai, nov/2026): Kling 2.6 Pro US$ 0,07/s sem áudio; voz
US$ 0,04 por 1.000 caracteres. Um Reels com 2 cenas de IA de 5 s ≈ US$ 0,72.
"""
import base64, json, math, os, re, subprocess, sys, time, unicodedata
from pathlib import Path

import requests

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "gerador"))
from arte import A, b64, doc, esc, chama_bg, marca, render  # noqa: E402

FAL_KEY = os.environ.get("FAL_KEY", "").strip()
MODELO_VIDEO = os.environ.get("MODELO_VIDEO", "fal-ai/kling-video/v2.6/pro/image-to-video")
MODELO_VOZ = os.environ.get("MODELO_VOZ", "elevenlabs/tts/eleven-v4-turbo")
VOZ = os.environ.get("VOZ", "Brian")
MAX_POR_EXECUCAO = int(os.environ.get("MAX_REELS", "3"))
W, H = 1080, 1920
TMP = RAIZ / ".reels-tmp"

ESTILO = ("3D animated cartoon mascot, same character design, same face, beard, pink cap and pink uniform "
          "with the logo exactly as in the image, Pixar-like quality, smooth natural motion, stable camera, "
          "vertical 9:16, no text, no captions, no extra characters")
NEGATIVO = "text, letters, watermark, deformed hands, extra fingers, extra limbs, blurry face, flicker, distorted logo"


def log(*a):
    print("[reels]", *a, flush=True)


def sh(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"comando falhou: {' '.join(map(str, cmd[:6]))}...\n{r.stderr[-1500:]}")
    return r.stdout


def duracao(path) -> float:
    return float(sh(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(path)]).strip())


# ---------------------------------------------------------------- quadros (Playwright)
def quadro_cena(mascote, fundo="marinho"):
    """Mascote grande no palco da marca, sem nenhum texto (a IA anima isto)."""
    m = b64(A / mascote)
    cls = "marinho tx-listras" if fundo == "marinho" else "rosa tx-listras"
    palco = "palco" if fundo == "marinho" else "palco rosa-p"
    body = f"""
    <div class="brilho" style="width:900px;height:900px;background:{'#FF47A3' if fundo=='marinho' else '#fff'};opacity:.35;left:90px;top:520px"></div>
    {chama_bg(-160, 1300, 560, -16)}{chama_bg(760, 160, 380, 12)}
    <div class="{palco}" style="width:820px;height:820px;left:130px;top:620px"></div>
    <img class="mascote" src="{m}" style="height:1180px;left:50%;transform:translateX(-50%);top:430px">
    """
    return doc(W, H, body, cls)


def cartao_texto(titulo, sub="", fundo="claro", emoji=""):
    escuro = fundo == "marinho"
    cls = "marinho tx-listras" if escuro else ("rosa tx-listras" if fundo == "rosa" else "claro tx-pontos")
    cor = "#fff" if fundo in ("marinho", "rosa") else "#171276"
    n = len(re.sub(r"[\[\]]", "", titulo))
    fs = 130 if n <= 22 else 110 if n <= 40 else 92
    body = f"""
    {chama_bg(640, 1280, 560, 14)}
    {f'<div style="position:absolute;left:90px;top:430px;font-size:190px">{emoji}</div>' if emoji else ''}
    <h1 style="position:absolute;left:90px;top:{700 if emoji else 560}px;width:900px;font-size:{fs}px;color:{cor};line-height:1.0">{esc(titulo)}</h1>
    {f'<p style="position:absolute;left:90px;top:1060px;width:860px;font-size:58px;font-weight:800;line-height:1.22;color:{cor};opacity:.92">{esc(sub)}</p>' if sub else ''}
    """
    return doc(W, H, body, cls)


def cartao_final(titulo, sub, mascote="mascote-celular.png"):
    m = b64(A / mascote)
    body = f"""
    <div class="brilho" style="width:800px;height:800px;background:#fff;opacity:.3;left:-200px;top:-100px"></div>
    {chama_bg(700, 1300, 500, 16)}
    {marca(90, 300, marinho=True)}
    <h1 style="position:absolute;left:90px;top:440px;width:900px;font-size:104px;line-height:1.04">{esc(titulo).replace('<em>', '<em style="font-style:normal;white-space:nowrap;color:#fff;background:#171276;border-radius:22px;padding:0 18px">')}</h1>
    <p style="position:absolute;left:90px;top:{760 if len(titulo) < 30 else 860}px;width:500px;font-size:54px;font-weight:800;line-height:1.24">{esc(sub)}</p>
    <div class="palco" style="width:640px;height:640px;right:-60px;bottom:330px"></div>
    <img class="mascote" src="{m}" style="height:900px;right:20px;bottom:330px">
    <div style="position:absolute;left:90px;bottom:220px;font-weight:900;font-size:44px">@appdonagas</div>
    """
    return doc(W, H, body, "rosa tx-listras")


def legenda_png(texto, posicao="baixo", destaque=False):
    """Uma frase curta da legenda, em caixa branca, para sobrepor ao vídeo."""
    top = 1400 if posicao == "baixo" else 300
    cor_bg = "#FF47A3" if destaque else "#fff"
    cor = "#fff" if destaque else "#171276"
    body = f"""
    <div style="position:absolute;left:70px;right:70px;top:{top}px;display:flex;justify-content:center">
      <div style="background:{cor_bg};color:{cor};border-radius:34px;padding:22px 36px;font-weight:900;font-size:66px;line-height:1.12;text-align:center;box-shadow:0 14px 40px rgba(0,0,0,.35);max-width:940px">{esc(texto)}</div>
    </div>"""
    return doc(W, H, body, "").replace("<body>", '<body style="background:transparent">')


def gancho_png(texto):
    n = len(re.sub(r"[\[\]]", "", texto))
    fs = 104 if n <= 26 else 88
    body = f"""
    <div style="position:absolute;left:60px;right:60px;top:250px;background:rgba(13,10,74,.88);border-radius:44px;padding:40px 46px;box-shadow:0 20px 50px rgba(0,0,0,.35)">
      <h1 style="font-size:{fs}px;color:#fff;line-height:1.02">{esc(texto)}</h1>
    </div>"""
    return doc(W, H, body, "").replace("<body>", '<body style="background:transparent">')


async def _render_png(jobs):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page()
        for html, out in jobs:
            await pg.set_viewport_size({"width": W, "height": H})
            await pg.set_content(html)
            await pg.wait_for_timeout(200)
            os.makedirs(os.path.dirname(out), exist_ok=True)
            await pg.screenshot(path=out, type="png", omit_background=True)
        await b.close()


def render_png(jobs):
    import asyncio
    asyncio.run(_render_png(jobs))


# ---------------------------------------------------------------- fal.ai
def fal(modelo, payload, timeout=900):
    h = {"Authorization": f"Key {FAL_KEY}", "Content-Type": "application/json"}
    r = requests.post(f"https://queue.fal.run/{modelo}", headers=h, json=payload, timeout=60)
    r.raise_for_status()
    q = r.json()
    status_url, resp_url = q["status_url"], q["response_url"]
    t0 = time.time()
    while time.time() - t0 < timeout:
        s = requests.get(status_url, headers=h, timeout=30).json()
        if s.get("status") == "COMPLETED":
            out = requests.get(resp_url, headers=h, timeout=60)
            out.raise_for_status()
            return out.json()
        if s.get("status") in ("FAILED", "ERROR"):
            raise RuntimeError(f"fal {modelo}: {s}")
        time.sleep(6)
    raise TimeoutError(f"fal {modelo}: demorou mais de {timeout}s")


def baixar(url, dest):
    r = requests.get(url, timeout=180)
    r.raise_for_status()
    Path(dest).write_bytes(r.content)
    return dest


def data_uri(path):
    return "data:image/jpeg;base64," + base64.b64encode(Path(path).read_bytes()).decode()


def cena_ia(quadro_png, movimento, dur, dest):
    jpg = str(quadro_png).replace(".png", ".jpg")
    sh(["ffmpeg", "-y", "-v", "error", "-i", str(quadro_png), "-q:v", "3", jpg])
    if not FAL_KEY:
        return cena_estatica(quadro_png, dur, dest, zoom=True)
    res = fal(MODELO_VIDEO, {
        "prompt": f"{movimento}. {ESTILO}",
        "start_image_url": data_uri(jpg),
        "duration": "10" if dur > 5 else "5",
        "negative_prompt": NEGATIVO,
        "generate_audio": False,
    })
    bruto = str(dest).replace(".mp4", "-bruto.mp4")
    baixar(res["video"]["url"], bruto)
    sh(["ffmpeg", "-y", "-v", "error", "-i", bruto, "-an", "-vf",
        f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps=30,format=yuv420p",
        "-t", str(dur), "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", str(dest)])
    return dest


def cena_estatica(png, dur, dest, zoom=True):
    frames = int(dur * 30)
    vf = (f"scale={W*2}:{H*2},zoompan=z='min(1+0.0009*on,1.12)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s={W}x{H}:fps=30,format=yuv420p"
          if zoom else f"scale={W}:{H},fps=30,format=yuv420p")
    sh(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-i", str(png), "-t", str(dur), "-vf", vf,
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", str(dest)])
    return dest


def narracao(texto, dest):
    """Retorna (arquivo de áudio, lista de palavras com início/fim em segundos)."""
    if not FAL_KEY:
        palavras = texto.split()
        dur = max(6.0, len(palavras) * 0.38)
        sh(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono", "-t", str(dur), "-c:a", "aac", str(dest)])
        passo = dur / max(1, len(palavras))
        return dest, [{"w": p, "s": i * passo, "e": (i + 1) * passo} for i, p in enumerate(palavras)]
    res = fal(MODELO_VOZ, {"text": texto, "voice": VOZ, "language_code": "pt", "timestamps": True,
                           "stability": 0.45, "similarity_boost": 0.8}, timeout=300)
    mp3 = str(dest).replace(".m4a", ".mp3")
    baixar(res["audio"]["url"], mp3)
    sh(["ffmpeg", "-y", "-v", "error", "-i", mp3, "-c:a", "aac", "-b:a", "160k", str(dest)])
    return dest, palavras_dos_tempos(res.get("timestamps"), texto, duracao(dest))


def palavras_dos_tempos(ts, texto, dur_total):
    """Aceita tempos por palavra ou por caractere; se não vier nada, distribui pelo tempo total."""
    out = []
    try:
        itens = ts if isinstance(ts, list) else (ts or {}).get("words") or []
        if itens and isinstance(itens[0], dict):
            k_txt = next(k for k in ("text", "word", "character", "char") if k in itens[0])
            k_s = next(k for k in ("start", "start_time", "start_seconds") if k in itens[0])
            k_e = next(k for k in ("end", "end_time", "end_seconds") if k in itens[0])
            atual = None
            for it in itens:
                t = str(it[k_txt])
                if t.strip() == "":
                    if atual:
                        out.append(atual); atual = None
                    continue
                if len(t) > 1 or atual is None:
                    if atual and len(t) > 1:
                        out.append(atual); atual = None
                    if atual is None:
                        atual = {"w": t, "s": float(it[k_s]), "e": float(it[k_e])}
                    else:
                        atual["w"] += t; atual["e"] = float(it[k_e])
                else:
                    atual["w"] += t; atual["e"] = float(it[k_e])
            if atual:
                out.append(atual)
    except Exception as e:  # formato inesperado: cai no plano B
        log("tempos da voz em formato inesperado:", e)
        out = []
    if len(out) < max(3, len(texto.split()) // 2):
        palavras = texto.split()
        passo = dur_total / max(1, len(palavras))
        out = [{"w": p, "s": i * passo, "e": (i + 1) * passo} for i, p in enumerate(palavras)]
    return out


def blocos_de_legenda(palavras, max_pal=3, max_chars=18):
    blocos, atual = [], []
    for p in palavras:
        atual.append(p)
        txt = " ".join(x["w"] for x in atual)
        if len(atual) >= max_pal or len(txt) >= max_chars or re.search(r"[.!?,:]$", p["w"]):
            blocos.append({"t": txt, "s": atual[0]["s"], "e": atual[-1]["e"]})
            atual = []
    if atual:
        blocos.append({"t": " ".join(x["w"] for x in atual), "s": atual[0]["s"], "e": atual[-1]["e"]})
    for i in range(len(blocos) - 1):  # sem buraco entre blocos
        blocos[i]["e"] = blocos[i + 1]["s"]
    return blocos


# ---------------------------------------------------------------- montagem
def produzir(rot):
    rid = rot["id"]
    pasta = TMP / rid
    pasta.mkdir(parents=True, exist_ok=True)
    saida = RAIZ / "posts" / rid
    saida.mkdir(parents=True, exist_ok=True)

    # 1) narração
    audio, palavras = narracao(rot["voz"], pasta / "voz.m4a")
    dur_voz = duracao(audio)
    log(rid, f"voz {dur_voz:.1f}s, {len(palavras)} palavras")

    # 2) cenas
    jobs, cenas = [], rot["cenas"]
    for i, c in enumerate(cenas):
        if c["tipo"] == "ia":
            jobs.append((quadro_cena(c["mascote"], c.get("fundo", "marinho")), str(pasta / f"q{i}.png")))
        else:
            jobs.append((cartao_texto(c["titulo"], c.get("sub", ""), c.get("fundo", "claro"), c.get("emoji", "")), str(pasta / f"q{i}.png")))
    fim = rot.get("final", {})
    jobs.append((cartao_final(fim.get("titulo", "Siga [@appdonagas]"), fim.get("sub", ""), fim.get("mascote", "mascote-celular.png")), str(pasta / "final.png")))
    render_png(jobs)

    alvo = dur_voz + 0.3
    soma = sum(c.get("dur", 5) for c in cenas)
    if soma < alvo:  # estica a última cena para cobrir a voz
        cenas[-1]["dur"] = cenas[-1].get("dur", 5) + (alvo - soma)
    clipes = []
    for i, c in enumerate(cenas):
        dest = pasta / f"c{i}.mp4"
        if c["tipo"] == "ia":
            ia_dur = min(10, c.get("dur", 5))
            cena_ia(pasta / f"q{i}.png", c.get("movimento", "the character smiles and waves"), ia_dur, dest)
            if c.get("dur", 5) > ia_dur + 0.05:  # completa com o último quadro parado
                ext = pasta / f"c{i}x.mp4"
                sh(["ffmpeg", "-y", "-v", "error", "-i", str(dest), "-vf", f"tpad=stop_mode=clone:stop_duration={c['dur']-ia_dur:.2f}",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", str(ext)])
                dest = ext
        else:
            cena_estatica(pasta / f"q{i}.png", c.get("dur", 4), dest)
        clipes.append(dest)
    clipes.append(cena_estatica(pasta / "final.png", 2.8, pasta / "cfim.mp4"))

    lista = pasta / "lista.txt"
    lista.write_text("".join(f"file '{p}'\n" for p in clipes))
    base = pasta / "base.mp4"
    sh(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lista), "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", str(base)])
    total = duracao(base)

    # 3) sobreposições: gancho (0–2,6 s) + legendas da voz
    blocos = blocos_de_legenda(palavras)
    over = [(gancho_png(rot["gancho"]), str(pasta / "gancho.png"))]
    for j, b in enumerate(blocos):
        over.append((legenda_png(b["t"], destaque=(j % 4 == 3)), str(pasta / f"l{j}.png")))
    render_png(over)

    ins = ["-i", str(base), "-i", str(audio), "-i", str(pasta / "gancho.png")]
    filtros, ult = [], "[0:v]"
    filtros.append(f"{ult}[2:v]overlay=0:0:enable='between(t,0,2.6)'[v0]")
    ult = "[v0]"
    fim_voz = dur_voz
    for j, b in enumerate(blocos):
        ins += ["-i", str(pasta / f"l{j}.png")]
        s, e = max(0, b["s"]), min(b["e"], fim_voz + 0.2)
        filtros.append(f"{ult}[{3+j}:v]overlay=0:0:enable='between(t,{s:.2f},{e:.2f})'[v{j+1}]")
        ult = f"[v{j+1}]"
    final = saida / "reel.mp4"
    sh(["ffmpeg", "-y", "-v", "error", *ins, "-filter_complex", ";".join(filtros), "-map", ult, "-map", "1:a",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-pix_fmt", "yuv420p", "-r", "30",
        "-c:a", "aac", "-b:a", "160k", "-af", f"apad=pad_dur={max(0.1, total - dur_voz):.2f}", "-t", f"{total:.2f}",
        "-movflags", "+faststart", str(final)])

    # 4) capa (quadro da 1ª cena + gancho)
    capa_png = pasta / "capa.png"
    sh(["ffmpeg", "-y", "-v", "error", "-i", str(pasta / "q0.png"), "-i", str(pasta / "gancho.png"), "-filter_complex", "overlay=0:0", str(capa_png)])
    sh(["ffmpeg", "-y", "-v", "error", "-i", str(capa_png), "-q:v", "3", str(saida / "capa.jpg")])
    log(rid, f"pronto: {final.relative_to(RAIZ)} ({duracao(final):.1f}s, {final.stat().st_size/1e6:.1f} MB)")
    return final


def main():
    roteiros = sorted((RAIZ / "reels" / "roteiros").glob("*.json"))
    agenda_p = RAIZ / "agenda.json"
    agenda = json.loads(agenda_p.read_text())
    ids = {a["id"] for a in agenda}
    feitos = 0
    for rp in roteiros:
        rot = json.loads(rp.read_text())
        rid = rot["id"]
        if (RAIZ / "posts" / rid / "reel.mp4").exists() and rid in ids:
            continue
        if feitos >= MAX_POR_EXECUCAO:
            log("limite desta execução atingido; o resto fica para a próxima")
            break
        log("produzindo", rid, "(MODO TESTE, sem IA)" if not FAL_KEY else "")
        produzir(rot)
        feitos += 1
        if FAL_KEY and rid not in ids:  # só agenda vídeo de verdade
            from datetime import datetime, timedelta, timezone
            quando = datetime.fromisoformat(rot["quando"])
            agora = datetime.now(timezone.utc)
            while quando < agora + timedelta(minutes=30):  # roteiro atrasado: vai para o próximo dia, mesmo horário
                quando += timedelta(days=1)
            rot["quando"] = quando.isoformat()
            agenda.append({
                "id": rid, "tipo": "reels", "abordagem": rot.get("abordagem", "")[:80], "legenda": rot["legenda"],
                "imagens": [f"posts/{rid}/reel.mp4", f"posts/{rid}/capa.jpg"],
                "video": f"posts/{rid}/reel.mp4", "capa": f"posts/{rid}/capa.jpg",
                "agendado_para": rot["quando"], "aprovado": rot.get("aprovado", True),
                "pilar": rot.get("pilar"), "layout": "reels", "objetivo": rot.get("objetivo"), "cta": rot.get("cta"), "lote": rot.get("lote", "reels"),
            })
            ids.add(rid)
    agenda.sort(key=lambda a: a["agendado_para"])
    agenda_p.write_text(json.dumps(agenda, ensure_ascii=False, indent=1))
    log(f"{feitos} reels produzidos")


if __name__ == "__main__":
    main()
