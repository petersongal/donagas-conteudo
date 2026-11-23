"""Locução da campanha Chama da Sorte (FamaGás) — voz da "senhora" por IA (ElevenLabs na fal.ai).
Lê chama-voz/pedidos/*.json  {"voz": "Matilda", "trechos": ["texto 1", "texto 2", ...]}
e grava chama-voz/saida/<pedido>/NN.mp3 (um arquivo por trecho = uma cena do vídeo).
Pedidos já atendidos (pasta de saída com todos os trechos) são pulados.
"""
import json, os, pathlib, time, requests
ROOT = pathlib.Path(__file__).parent
KEY = os.environ["FAL_KEY"]
MODELO = "fal-ai/elevenlabs/tts/eleven-v3"
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

for ped in sorted((ROOT / "pedidos").glob("*.json")):
    cfg = json.loads(ped.read_text(encoding="utf-8"))
    out = ROOT / "saida" / ped.stem; out.mkdir(parents=True, exist_ok=True)
    modelo = cfg.get("modelo", MODELO)
    for i, txt in enumerate(cfg["trechos"], 1):
        dest = out / f"{i:02d}.mp3"
        if dest.exists(): continue
        payload = {"text": txt, "voice": cfg.get("voz", "Matilda"), "language_code": "pt",
                   "stability": cfg.get("stability", 0.5), "similarity_boost": 0.8, "style": cfg.get("style", 0.35)}
        try:
            res = fal(modelo, payload)
        except Exception as e:
            print("falhou com", modelo, e, "→ tentando eleven-v4-turbo")
            res = fal("elevenlabs/tts/eleven-v4-turbo", payload)
        dest.write_bytes(requests.get(res["audio"]["url"], timeout=120).content)
        print("ok", dest, dest.stat().st_size)
