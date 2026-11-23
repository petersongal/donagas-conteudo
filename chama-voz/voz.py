"""Locução da campanha Chama da Sorte (FamaGás) — voz da "senhora" por IA (fal.ai).
Lê chama-voz/pedidos/*.json
  {"motor": "minimax" | "kokoro" | "eleven", "voz": "...", "speed": 1.0, "trechos": ["texto 1", ...]}
e grava chama-voz/saida/<pedido>/NN.mp3 (um arquivo por trecho = uma cena do vídeo).
Trechos já gerados são pulados. Português do Brasil: prefira "minimax" (language_boost Portuguese)
ou "kokoro" (modelo próprio de pt-BR). Não ponha "FamaGás" no texto falado (pronúncia ruim).
"""
import json, os, pathlib, time, requests
ROOT = pathlib.Path(__file__).parent
KEY = os.environ["FAL_KEY"]
H = {"Authorization": f"Key {KEY}", "Content-Type": "application/json"}


def fal(modelo, payload, timeout=300):
    q = requests.post(f"https://queue.fal.run/{modelo}", headers=H, json=payload, timeout=60)
    q.raise_for_status(); q = q.json(); t0 = time.time()
    while time.time() - t0 < timeout:
        s = requests.get(q["status_url"], headers=H, timeout=30).json()
        if s.get("status") == "COMPLETED":
            r = requests.get(q["response_url"], headers=H, timeout=60); r.raise_for_status(); return r.json()
        if s.get("status") in ("FAILED", "ERROR"): raise RuntimeError(s)
        time.sleep(4)
    raise TimeoutError(modelo)


def gerar(cfg, txt, dest):
    motor = cfg.get("motor", "eleven")
    if motor == "minimax":
        res = fal(cfg.get("modelo", "fal-ai/minimax/speech-02-hd"), {
            "text": txt, "language_boost": "Portuguese", "output_format": "url",
            "voice_setting": {k: v for k, v in {"voice_id": cfg.get("voz", "Wise_Woman"), "speed": cfg.get("speed", 1.0), "vol": 1,
                              "pitch": cfg.get("pitch", 0), "emotion": cfg.get("emocao")}.items() if v is not None}})
    elif motor == "kokoro":
        res = fal("fal-ai/kokoro/brazilian-portuguese", {"prompt": txt, "voice": cfg.get("voz", "pf_dora"), "speed": cfg.get("speed", 1.0)})
    else:
        res = fal(cfg.get("modelo", "fal-ai/elevenlabs/tts/eleven-v3"), {
            "text": txt, "voice": cfg.get("voz", "Matilda"), "language_code": "pt",
            "stability": cfg.get("stability", 0.5), "similarity_boost": 0.8, "style": cfg.get("style", 0.35)})
    a = res["audio"]; url = a["url"] if isinstance(a, dict) else a
    dest.write_bytes(requests.get(url, timeout=120).content)
    print("ok", dest, dest.stat().st_size, flush=True)


for ped in sorted((ROOT / "pedidos").glob("*.json")):
    cfg = json.loads(ped.read_text(encoding="utf-8"))
    out = ROOT / "saida" / ped.stem; out.mkdir(parents=True, exist_ok=True)
    for i, txt in enumerate(cfg["trechos"], 1):
        dest = out / f"{i:02d}.mp3"
        if dest.exists(): continue
        try:
            gerar(cfg, txt, dest)
        except Exception as e:
            print("ERRO", ped.stem, i, e, flush=True)
