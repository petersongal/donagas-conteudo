"""Fábrica de Reels do @famagas_ (mesma fábrica do @appdonagas, com a marca FamaGás)

Roda no GitHub Actions (ver .github/workflows/reels.yml). Cenas: "ia" (mascote recortado no palco da marca),
"foto" (cena completa do mascote com câmera viva) e "texto" (cartão). (roda no GitHub Actions; ver .github/workflows/reels.yml).

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
from arte import A, b64, doc, esc, marca  # noqa: E402

FAL_KEY = os.environ.get("FAL_KEY", "").strip()
_CFG_P = Path(__file__).resolve().parent / "config.json"
CFG = json.loads(_CFG_P.read_text()) if _CFG_P.exists() else {}
MODELO_VIDEO = os.environ.get("MODELO_VIDEO") or CFG.get("modelo_video", "fal-ai/kling-video/v2.6/pro/image-to-video")
MODELO_VOZ = os.environ.get("MODELO_VOZ") or CFG.get("modelo_voz", "elevenlabs/tts/eleven-v4-turbo")
VOZ = os.environ.get("VOZ") or CFG.get("voz", "Brian")
SIMILARIDADE_MINIMA = float(CFG.get("similaridade_minima", 0.85))
ANIMACAO = CFG.get("animacao_mascote", "poses")   # "poses" (sem IA, boca parada) ou "ia" (Kling)
MAX_POR_EXECUCAO = int(os.environ.get("MAX_REELS", "3"))
W, H = 1080, 1920
TMP = RAIZ / ".reels-tmp"

ESTILO = ("3D animated cartoon mascot: a silver cooking-gas cylinder character with big blue eyes, red superhero cape and "
          "blue shorts, exactly as in the image, same design, Pixar-like quality, smooth natural motion, stable camera, "
          "vertical 9:16, no text, no captions, no extra characters. "
          "IMPORTANT: the character does NOT talk or speak. He only reacts with expressive faces and gestures "
          "(raised eyebrows, wide eyes, big smile, laughing, surprised face, nod, head tilt, thumbs up). "
          "The mouth may open for an expression and then hold it, but never moves as if saying words")
NEGATIVO = ("talking, speaking, saying words, lip sync, repeated mouth movements, mouth flapping, singing, chewing, "
            "text, letters, watermark, deformed hands, extra fingers, extra limbs, blurry face, flicker, distorted logo")


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
CLS = {"azul": "azul tx-faixas", "noite": "noite tx-faixas", "amarelo": "amarelo tx-pontos", "creme": "creme tx-pontos"}
ALT_POSE = 1120   # altura do mascote no palco (px)
TOPO_POSE = 560   # abaixo do gancho; pés perto de 1680 (acima da área das legendas do Instagram)


def _palco(fundo):
    return f"""
    <div class="brilho" style="width:900px;height:900px;background:{'#f8d527' if fundo in ('azul', 'noite') else '#fff'};opacity:.28;left:90px;top:520px"></div>
    <div class="palco" style="width:840px;height:840px;left:120px;top:700px"></div>
    """


def quadro_cena(mascote, fundo="azul"):
    """Mascote grande no palco da marca, sem nenhum texto (serve de capa e de quadro para a IA)."""
    m = b64(A / mascote)
    body = _palco(fundo) + f'<img class="mascote" src="{m}" style="height:{ALT_POSE}px;left:50%;transform:translateX(-50%);top:{TOPO_POSE}px">'
    return doc(W, H, body, CLS.get(fundo, CLS["azul"]))


def quadro_fundo(fundo="azul"):
    """Cenário da marca SEM o mascote (o mascote entra por cima, animado pelo ffmpeg)."""
    return doc(W, H, _palco(fundo), CLS.get(fundo, CLS["azul"]))


def quadro_real(imagem):
    """Foto real (banco gratuito, revisada) em tela cheia, com véu azul-noite em cima e embaixo para o texto ler bem."""
    body = f"""
    <img src="{b64(A / 'fotos' / imagem)}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover">
    <div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(11,46,87,.85) 0px,rgba(11,46,87,.25) 520px,rgba(11,46,87,0) 800px,rgba(11,46,87,0) 1200px,rgba(11,46,87,.7) 1920px)"></div>
    """
    return doc(W, H, body, "noite")


def quadro_foto(imagem):
    """Cena completa do mascote (cozinha, panela de pressão...). A imagem desce 300 px para o rosto
    ficar abaixo do gancho; o topo vira uma faixa azul-noite que se desfaz na foto."""
    body = f"""
    <img src="{b64(A / imagem)}" style="position:absolute;left:0;top:300px;width:1080px;height:1920px;object-fit:cover">
    <div style="position:absolute;inset:0;background:linear-gradient(180deg,#0b2e57 0px,#0b2e57 300px,rgba(11,46,87,0) 620px,rgba(11,46,87,0) 1250px,rgba(11,46,87,.55) 1920px)"></div>
    """
    return doc(W, H, body, "noite")


# O mascote NÃO fala (a boca não sincroniza com a voz). Ele é animado sem IA: entra pulando, balança,
# "respira", vira de lado e troca de pose. Para cada pose, a que entra em seguida:
POSE_SEGUINTE = {}


def _poses_disponiveis():
    return sorted(p.name for p in A.glob("mascote-*.png"))


def cena_pose(fundo_png, poses, dur, dest):
    """Cada pose ocupa uma fatia do tempo: entra de baixo com um pulo, balança de leve e respira.
    Fatias ímpares entram espelhadas e um pouco maiores (o mascote "vira" e chega mais perto)."""
    partes = []
    fatia = dur / len(poses)
    for i, pose in enumerate(poses):
        out = str(dest).replace(".mp4", f"-p{i}.mp4")
        alt = ALT_POSE if i % 2 == 0 else int(ALT_POSE * 1.06)
        topo = TOPO_POSE if i % 2 == 0 else TOPO_POSE - 30
        vira = ""   # nunca espelhar: o mascote tem o logo escrito (caneca, peito)
        filtro = (
            f"[1:v]{vira}scale=-1:{alt},format=rgba,"
            f"rotate='0.035*sin(2*PI*t*0.8)':c=none:ow=rotw(0.07):oh=roth(0.07)[m];"
            f"[0:v][m]overlay=x='(W-w)/2+10*sin(2*PI*t*0.45)':"
            f"y='{topo}+16*sin(2*PI*t*1.1)+if(lt(t,0.32),(0.32-t)*(0.32-t)*5200,0)':shortest=1,"
            f"fps=30,format=yuv420p"
        )
        sh(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-i", str(fundo_png), "-loop", "1", "-i", str(A / pose),
            "-filter_complex", filtro, "-t", f"{fatia:.2f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", out])
        partes.append(out)
    lista = str(dest).replace(".mp4", "-lista.txt")
    Path(lista).write_text("".join(f"file '{p}'\n" for p in partes))
    sh(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lista, "-c", "copy", str(dest)])
    return dest


def cena_foto(png, dur, dest, sentido=1):
    """Cena completa com câmera viva: aproxima devagar e desliza de lado (parece filmado)."""
    frames = int(dur * 30)
    vf = (f"scale={W*2}:{H*2},zoompan=z='1.0+0.08*on/{frames}':"
          f"x='iw/2-(iw/zoom/2)+{sentido}*40*sin(2*PI*on/{frames}/2)':y='ih/2-(ih/zoom/2)':"
          f"d={frames}:s={W}x{H}:fps=30,format=yuv420p")
    sh(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-i", str(png), "-t", str(dur), "-vf", vf,
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", str(dest)])
    return dest


def cartao_texto(titulo, sub="", fundo="creme", emoji=""):
    cls = CLS.get(fundo, CLS["creme"])
    n = len(re.sub(r"[\[\]]", "", titulo))
    fs = 190 if n <= 16 else 160 if n <= 26 else 132 if n <= 44 else 110
    body = f"""
    {marca(80, 270)}
    <div style="position:absolute;left:80px;top:{440 if emoji else 520}px;width:920px;display:flex;flex-direction:column;gap:44px">
      {f'<div style="font-size:180px;line-height:1">{emoji}</div>' if emoji else ''}
      <h1 style="font-size:{fs}px">{esc(titulo)}</h1>
      {f'<p style="font-size:58px;font-weight:800;line-height:1.2;opacity:.95">{esc(sub)}</p>' if sub else ''}
    </div>
    """
    return doc(W, H, body, cls)


def cartao_final(titulo, sub, mascote="mascote-cafe.png"):
    m = b64(A / mascote)
    n = len(re.sub(r"[\[\]]", "", titulo))
    body = f"""
    <div class="brilho" style="width:800px;height:800px;background:#fff;opacity:.35;left:-200px;top:-100px"></div>
    {marca(80, 270)}
    <div style="position:absolute;left:80px;top:420px;width:920px;display:flex;flex-direction:column;gap:30px">
      <h1 style="font-size:{170 if n <= 20 else 140 if n <= 32 else 116}px">{esc(titulo)}</h1>
      <p style="font-size:52px;font-weight:800;line-height:1.2;width:420px">{esc(sub)}</p>
    </div>
    <div class="palco" style="width:640px;height:640px;right:-50px;bottom:270px"></div>
    <img class="mascote" src="{m}" style="height:800px;right:20px;bottom:270px">
    <div style="position:absolute;left:80px;bottom:240px;font-weight:900;font-size:46px">@famagas_</div>
    """
    return doc(W, H, body, "amarelo tx-pontos")


def legenda_png(texto, posicao="baixo", destaque=False):
    """Uma frase curta da legenda, em caixa, para sobrepor ao vídeo."""
    top = 1400 if posicao == "baixo" else 300
    cor_bg = "#f8d527" if destaque else "#fff"
    body = f"""
    <div style="position:absolute;left:70px;right:70px;top:{top}px;display:flex;justify-content:center">
      <div style="background:{cor_bg};color:#0b2e57;border-radius:34px;padding:22px 36px;font-weight:900;font-size:66px;line-height:1.12;text-align:center;box-shadow:0 14px 40px rgba(0,0,0,.4);max-width:940px">{esc(texto).replace('<em>', '').replace('</em>', '')}</div>
    </div>"""
    return doc(W, H, body, "").replace("<body>", '<body style="background:transparent">')


def gancho_png(texto):
    n = len(re.sub(r"[\[\]]", "", texto))
    fs = 150 if n <= 22 else 128 if n <= 34 else 108
    body = f"""
    <div style="position:absolute;left:56px;right:56px;top:250px;background:rgba(11,46,87,.92);border:8px solid #f8d527;border-radius:44px;padding:34px 44px 40px;box-shadow:0 20px 50px rgba(0,0,0,.4)">
      <h1 style="font-size:{fs}px;color:#fff">{esc(texto)}</h1>
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
    # Conferência independente: outra IA (Whisper) ouve a voz e transcreve com tempo por palavra.
    conf = conferir_audio(res["audio"]["url"], texto)
    globals()["_ULTIMA_CONFERENCIA"] = conf
    if conf.get("palavras"):
        return dest, conf["palavras"]          # legendas sincronizadas com o que foi realmente falado
    return dest, palavras_dos_tempos(res.get("timestamps"), texto, duracao(dest))


def _norm(t):
    t = unicodedata.normalize("NFKD", t.lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    return re.findall(r"[a-z0-9]+", t)


def alinhar(rot, falas):
    """Legenda SEMPRE com o texto do roteiro; os tempos vêm do Whisper, casando palavra por palavra.
    Palavras do roteiro sem par (ex.: Whisper ouviu "a app" no lugar de "APP") recebem tempo interpolado."""
    import difflib
    if not falas:
        return []
    a = [(_norm(w) or [""])[0] for w in rot]
    b = [(_norm(f["w"]) or [""])[0] for f in falas]
    tempos = [None] * len(rot)
    for blk in difflib.SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks():
        for k in range(blk.size):
            f = falas[blk.b + k]
            tempos[blk.a + k] = (f["s"], f["e"])
    # interpola os buracos entre vizinhos conhecidos
    ini, fim = falas[0]["s"], falas[-1]["e"]
    i = 0
    while i < len(rot):
        if tempos[i] is None:
            j = i
            while j < len(rot) and tempos[j] is None:
                j += 1
            t0 = tempos[i - 1][1] if i > 0 else ini
            t1 = tempos[j][0] if j < len(rot) else fim
            passo = max(0.05, (t1 - t0) / (j - i))
            for k in range(i, j):
                tempos[k] = (t0 + (k - i) * passo, t0 + (k - i + 1) * passo)
            i = j
        else:
            i += 1
    return [{"w": w, "s": t[0], "e": t[1]} for w, t in zip(rot, tempos)]


def conferir_audio(audio_url, texto_roteiro):
    """Transcreve a narração com Whisper e compara com o texto do roteiro (0 a 1)."""
    import difflib
    try:
        r = fal("fal-ai/whisper", {"audio_url": audio_url, "task": "transcribe", "language": "pt", "chunk_level": "word"}, timeout=300)
    except Exception as e:
        log("conferência de áudio falhou:", e)
        return {"erro": str(e)}
    transc = r.get("text", "")
    sim = difflib.SequenceMatcher(None, _norm(texto_roteiro), _norm(transc)).ratio()
    palavras = []
    for c in r.get("chunks") or []:
        ts = c.get("timestamp") or [c.get("start"), c.get("end")]
        w = str(c.get("text", "")).strip()
        if w and ts and ts[0] is not None:
            palavras.append({"w": w, "s": float(ts[0]), "e": float(ts[1] if ts[1] is not None else ts[0] + 0.3)})
    # As legendas mostram o texto do ROTEIRO (ortografia certa) nos tempos do Whisper, quando a contagem bate.
    palavras = alinhar(texto_roteiro.split(), palavras)
    langs = r.get("inferred_languages") or []
    return {"transcricao": transc, "similaridade": round(sim, 3), "idiomas": langs, "palavras": palavras}


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
        if c["tipo"] == "real" and not (A / "fotos" / c["imagem"]).exists():
            log(rid, "foto real ausente:", c["imagem"], "→ uso a cena do mascote")
            c["tipo"], c["imagem"] = "foto", c.get("reserva", "cena-panela.jpg")
        if c["tipo"] == "real":
            jobs.append((quadro_real(c["imagem"]), str(pasta / f"q{i}.png")))
        elif c["tipo"] == "foto":
            jobs.append((quadro_foto(c["imagem"]), str(pasta / f"q{i}.png")))
        elif c["tipo"] == "ia" and ANIMACAO == "poses":
            jobs.append((quadro_fundo(c.get("fundo", "azul")), str(pasta / f"fundo{i}.png")))
            jobs.append((quadro_cena(c["mascote"], c.get("fundo", "azul")), str(pasta / f"q{i}.png")))  # capa
        elif c["tipo"] == "ia":
            jobs.append((quadro_cena(c["mascote"], c.get("fundo", "azul")), str(pasta / f"q{i}.png")))
        else:
            jobs.append((cartao_texto(c["titulo"], c.get("sub", ""), c.get("fundo", "creme"), c.get("emoji", "")), str(pasta / f"q{i}.png")))
    fim = rot.get("final", {})
    jobs.append((cartao_final(fim.get("titulo", "Siga [@famagas_]"), fim.get("sub", ""), fim.get("mascote", "mascote-cafe.png")), str(pasta / "final.png")))
    render_png(jobs)

    alvo = dur_voz + 0.3
    soma = sum(c.get("dur", 5) for c in cenas)
    if soma < alvo:  # estica a última cena para cobrir a voz
        cenas[-1]["dur"] = cenas[-1].get("dur", 5) + (alvo - soma)
    clipes = []
    for i, c in enumerate(cenas):
        dest = pasta / f"c{i}.mp4"
        if c["tipo"] in ("foto", "real"):
            cena_foto(pasta / f"q{i}.png", c.get("dur", 5), dest, sentido=1 if i % 2 == 0 else -1)
        elif c["tipo"] == "ia" and ANIMACAO == "poses":
            outras = [p for p in _poses_disponiveis() if p != c["mascote"]]
            seguinte = POSE_SEGUINTE.get(c["mascote"]) or (outras[i % len(outras)] if outras else c["mascote"])
            poses = c.get("poses") or [c["mascote"], seguinte]
            cena_pose(pasta / f"fundo{i}.png", poses, c.get("dur", 5), dest)
        elif c["tipo"] == "ia":
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
    musica = CFG.get("musica")
    musica_p = RAIZ / musica if musica else None
    if musica_p and musica_p.exists():
        # Trilha padrão: em loop, baixinha, com fade, e abaixa sozinha enquanto a voz fala (ducking).
        n = len(ins) // 2
        ins_m = ins + ["-stream_loop", "-1", "-i", str(musica_p)]
        vol = 10 ** (float(CFG.get("volume_musica_db", -16)) / 20)
        fa = (f"[1:a]apad=pad_dur={max(0.1, total - dur_voz):.2f},asplit=2[voz][sc];"
              f"[{n}:a]volume={vol:.3f},afade=t=in:d=0.4,afade=t=out:st={max(0, total - 1.2):.2f}:d=1.2[mus];"
              f"[mus][sc]sidechaincompress=threshold=0.02:ratio=6:attack=15:release=350[musd];"
              f"[voz][musd]amix=inputs=2:duration=first:normalize=0[aout]")
        sh(["ffmpeg", "-y", "-v", "error", *ins_m, "-filter_complex", ";".join(filtros) + ";" + fa,
            "-map", ult, "-map", "[aout]",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-pix_fmt", "yuv420p", "-r", "30",
            "-c:a", "aac", "-b:a", "160k", "-t", f"{total:.2f}", "-movflags", "+faststart", str(final)])
    else:
        sh(["ffmpeg", "-y", "-v", "error", *ins, "-filter_complex", ";".join(filtros), "-map", ult, "-map", "1:a",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-pix_fmt", "yuv420p", "-r", "30",
            "-c:a", "aac", "-b:a", "160k", "-af", f"apad=pad_dur={max(0.1, total - dur_voz):.2f}", "-t", f"{total:.2f}",
            "-movflags", "+faststart", str(final)])

    # 4) capa (quadro da 1ª cena + gancho)
    capa_png = pasta / "capa.png"
    sh(["ffmpeg", "-y", "-v", "error", "-i", str(pasta / "q0.png"), "-i", str(pasta / "gancho.png"), "-filter_complex", "overlay=0:0", str(capa_png)])
    sh(["ffmpeg", "-y", "-v", "error", "-i", str(capa_png), "-q:v", "3", str(saida / "capa.jpg")])
    conf = globals().get("_ULTIMA_CONFERENCIA") or {}
    (saida / "verificacao.json").write_text(json.dumps({
        "roteiro": rot["voz"], "transcricao": conf.get("transcricao"), "similaridade": conf.get("similaridade"),
        "idiomas_detectados": conf.get("idiomas"), "voz": VOZ, "modelo_voz": MODELO_VOZ, "modelo_video": MODELO_VIDEO,
        "legendas": [b["t"] for b in blocos], "duracao_s": round(duracao(final), 1),
    }, ensure_ascii=False, indent=1))
    log(rid, f"pronto: {final.relative_to(RAIZ)} ({duracao(final):.1f}s, {final.stat().st_size/1e6:.1f} MB), similaridade da voz {conf.get('similaridade')}")
    return final


def amostras():
    """Gera amostras de voz (reels/amostras/pedido.json) para o Peterson escolher de ouvido."""
    pasta = RAIZ / "reels" / "amostras"
    ped = json.loads((pasta / "pedido.json").read_text())
    for c in ped["candidatas"]:
        nome = re.sub(r"[^a-z0-9]+", "-", f"{c['modelo'].split('/')[-1]}-{c['voz']}".lower())
        mp3 = pasta / f"{nome}.mp3"
        if mp3.exists():
            continue
        res = fal(c["modelo"], {"text": ped["texto"], "voice": c["voz"], "language_code": "pt", "stability": 0.45, "similarity_boost": 0.8}, timeout=300)
        baixar(res["audio"]["url"], mp3)
        conf = conferir_audio(res["audio"]["url"], ped["texto"])
        conf.pop("palavras", None)
        (pasta / f"{nome}.json").write_text(json.dumps({"modelo": c["modelo"], "voz": c["voz"], **conf}, ensure_ascii=False, indent=1))
        log("amostra", nome, conf.get("similaridade"))


def musicas():
    """Gera as opções de trilha (reels/musica/pedido.json) para o Peterson escolher."""
    pasta = RAIZ / "reels" / "musica"
    ped = json.loads((pasta / "pedido.json").read_text())
    for o in ped["opcoes"]:
        mp3 = pasta / f"opcao-{o['nome']}.mp3"
        if mp3.exists():
            continue
        res = fal("fal-ai/elevenlabs/music", {"prompt": o["prompt"], "music_length_ms": ped.get("duracao_ms", 30000),
                                             "force_instrumental": True}, timeout=600)
        url = (res.get("audio") or res.get("audio_file") or {}).get("url") or res.get("url")
        baixar(url, mp3)
        log("trilha", mp3.name)


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
        conf = globals().get("_ULTIMA_CONFERENCIA") or {}
        voz_ok = (conf.get("similaridade") or 0) >= SIMILARIDADE_MINIMA
        if FAL_KEY and not voz_ok:
            log(rid, "VOZ REPROVADA na conferência (similaridade", conf.get("similaridade"), ") — não vai para a agenda")
        if FAL_KEY and voz_ok and rid not in ids:  # só agenda vídeo de verdade e com a voz conferida
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
                "palavra": rot.get("palavra"), "gancho": rot.get("gancho"), "formato": rot.get("formato"),
            })
            ids.add(rid)
    agenda.sort(key=lambda a: a["agendado_para"])
    agenda_p.write_text(json.dumps(agenda, ensure_ascii=False, indent=1))
    log(f"{feitos} reels produzidos")


if __name__ == "__main__":
    if FAL_KEY and (RAIZ / "reels" / "musica" / "pedido.json").exists():
        try:
            musicas()
        except Exception as e:
            log("trilhas falharam:", e)
    if FAL_KEY and (RAIZ / "reels" / "amostras" / "pedido.json").exists():
        try:
            amostras()
        except Exception as e:
            log("amostras de voz falharam:", e)
    main()
