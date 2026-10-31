#!/usr/bin/env python3
"""Télécharge les polices Google Fonts (sous-ensemble latin, format woff2)
pour l'auto-hébergement RGPD. À lancer depuis la racine du site :
    python download-fonts.py
"""
import os
import re
import sys
import urllib.request

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

CSS_URL = (
    "https://fonts.googleapis.com/css2"
    "?family=Unbounded:wght@500;600;700;800"
    "&family=Space+Grotesk:wght@400;500;600;700"
    "&family=Space+Mono:wght@400;700"
    "&display=swap"
)

# nom de famille (slug google) -> préfixe de fichier local
FAMILY_SLUG = {
    "unbounded": "unbounded",
    "space grotesk": "space-grotesk",
    "space mono": "space-mono",
}


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8")


def main():
    os.makedirs("fonts", exist_ok=True)

    css = fetch(CSS_URL)

    # Chaque @font-face du sous-ensemble latin (une famille + une graisse).
    latin_faces = re.findall(
        r"/\* latin \*/\s*@font-face\s*{(.*?)}",
        css,
        flags=re.DOTALL,
    )
    if not latin_faces:
        print("ERREUR : aucun bloc « latin » trouvé dans le CSS récupéré.")
        return

    downloaded = 0
    for face in latin_faces:
        family = re.search(r"font-family:\s*'([^']+)'", face)
        weight = re.search(r"font-weight:\s*(\d+)", face)
        url = re.search(r"url\((https://[^)]+\.woff2)\)", face)
        if not (family and weight and url):
            print("  -> bloc ignoré (champ manquant)")
            continue
        slug = FAMILY_SLUG.get(family.group(1).lower())
        if not slug:
            print(f"  -> famille ignorée : {family.group(1)}")
            continue
        filename = f"fonts/{slug}-{weight.group(1)}.woff2"
        print(f"Téléchargement : {filename}")
        req = urllib.request.Request(url.group(1), headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=60) as r:
            data = r.read()
        with open(filename, "wb") as f:
            f.write(data)
        downloaded += 1

    print(f"\nTerminé : {downloaded} fichiers woff2 dans fonts/.")


if __name__ == "__main__":
    main()
