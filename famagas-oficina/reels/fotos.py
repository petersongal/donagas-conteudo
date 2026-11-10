"""Busca fotos reais em bancos gratuitos (domínio público / CC0, uso comercial sem crédito obrigatório).

Roda no GitHub Actions (a sessão do Claude não alcança os bancos de imagem). Para cada tema de
reels/fotos/pedido.json que ainda não tem candidatas, procura no Openverse (licenças cc0 e pdm) e, se vier pouco,
no Wikimedia Commons (só CC0 / domínio público), baixa até N fotos em gerador/assets/fotos/candidatas/<tema>/
e grava creditos.json (fonte, autor, licença, página). Depois uma sessão do Claude OLHA cada candidata (Read),
escolhe e copia a boa para gerador/assets/fotos/<nome>.jpg. Nenhuma foto vai para vídeo sem essa revisão.
"""
import io, json, re, sys, time
from pathlib import Path

import requests
from PIL import Image

RAIZ = Path(__file__).resolve().parent.parent
DEST = RAIZ / "gerador" / "assets" / "fotos" / "candidatas"
UA = {"User-Agent": "famagas-conteudo/1.0 (conteudo do Instagram @famagas_; contato: famagas.com.br)"}
LIVRES = ("cc0", "pdm", "public domain", "cc-zero")


def baixar(url, dest):
    r = requests.get(url, headers=UA, timeout=60)
    r.raise_for_status()
    im = Image.open(io.BytesIO(r.content)).convert("RGB")
    if min(im.size) < 700:
        raise ValueError(f"pequena demais {im.size}")
    im.thumbnail((1800, 1800))
    im.save(dest, quality=88)
    return im.size


def openverse(q, n):
    r = requests.get("https://api.openverse.org/v1/images/", headers=UA, timeout=40,
                     params={"q": q, "license": "cc0,pdm", "page_size": n * 2, "mature": "false"})
    r.raise_for_status()
    return [{"url": x.get("url"), "autor": x.get("creator"), "licenca": x.get("license"), "fonte": x.get("source"),
             "pagina": x.get("foreign_landing_url"), "titulo": x.get("title")} for x in r.json().get("results", [])]


def commons(q, n):
    r = requests.get("https://commons.wikimedia.org/w/api.php", headers=UA, timeout=40, params={
        "action": "query", "format": "json", "generator": "search", "gsrsearch": f"{q} filetype:bitmap", "gsrnamespace": 6,
        "gsrlimit": n * 4, "prop": "imageinfo", "iiprop": "url|extmetadata", "iiurlwidth": 1800})
    r.raise_for_status()
    out = []
    for p in (r.json().get("query", {}).get("pages", {}) or {}).values():
        ii = (p.get("imageinfo") or [{}])[0]
        md = ii.get("extmetadata", {})
        lic = (md.get("LicenseShortName", {}).get("value") or "").lower()
        if not any(k in lic for k in LIVRES):
            continue
        out.append({"url": ii.get("thumburl") or ii.get("url"), "autor": re.sub(r"<[^>]+>", "", md.get("Artist", {}).get("value", ""))[:80],
                    "licenca": lic, "fonte": "wikimedia commons", "pagina": ii.get("descriptionurl"), "titulo": p.get("title")})
    return out


def main():
    ped = json.loads((RAIZ / "reels" / "fotos" / "pedido.json").read_text())
    n = int(ped.get("por_tema", 5))
    for tema, buscas in ped["temas"].items():
        pasta = DEST / tema
        if (pasta / "creditos.json").exists():
            continue
        pasta.mkdir(parents=True, exist_ok=True)
        achadas, vistos = [], set()
        for q in buscas:
            for fonte in (openverse, commons):
                try:
                    cand = fonte(q, n)
                except Exception as e:
                    print(f"[fotos] {tema}: {fonte.__name__} falhou ({e})", flush=True)
                    cand = []
                for c in cand:
                    if len(achadas) >= n or not c.get("url") or c["url"] in vistos:
                        continue
                    vistos.add(c["url"])
                    arq = pasta / f"{len(achadas) + 1}.jpg"
                    try:
                        c["tamanho"] = baixar(c["url"], arq)
                        c["arquivo"] = arq.name
                        c["busca"] = q
                        achadas.append(c)
                    except Exception as e:
                        print(f"[fotos] {tema}: pulou {c['url'][:70]} ({e})", flush=True)
                time.sleep(1.2)
            if len(achadas) >= n:
                break
        (pasta / "creditos.json").write_text(json.dumps(achadas, ensure_ascii=False, indent=1))
        print(f"[fotos] {tema}: {len(achadas)} candidatas", flush=True)


if __name__ == "__main__":
    main()
