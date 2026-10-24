#!/usr/bin/env python3
"""Analyse CHAQUE couche d'une image exportee par `docker save` (pas seulement le systeme de fichiers final).

Usage : scan-image-layers.py IMAGE.tar [--canary VALEUR ...] [--allow NOM ...]

- Un fichier supprime dans une couche ulterieure reste lisible dans la couche d'origine : on les parcourt toutes.
- Ne affiche jamais le contenu des fichiers ni la valeur des variables : uniquement noms et chemins.
- Code de sortie 1 si une trouvaille de severite HAUTE existe, 0 sinon.
"""
import argparse, io, json, os, re, sys, tarfile

PRIVATE_KEY = re.compile(rb"-----BEGIN (?:[A-Z]+ )?PRIVATE KEY-----")
AWS_KEY = re.compile(rb"AKIA[0-9A-Z]{16}")
ASSIGN = re.compile(rb"(?im)^\s*(?:export\s+)?[A-Z0-9_]*(?:PASSWORD|SECRET|TOKEN|API_KEY)[A-Z0-9_]*\s*[=:]\s*['\"]?[^\s'\"$<{]{4,}")
ENV_NAME = re.compile(r"(PASSWORD|SECRET|TOKEN|API_KEY|PRIVATE)", re.I)
NOISE_DIRS = ("site-packages/", "dist-packages/", "usr/share/", "usr/lib/", "var/lib/dpkg/", "node_modules/", "etc/ssl/", "usr/local/lib/")
MAX_READ = 5 * 1024 * 1024


def sensitive_name(path, allow):
    parts = path.strip("/").split("/")
    base = parts[-1]
    if base in allow:
        return None
    if base == ".env" or (base.startswith(".env.") and base not in (".env.example",)):
        return "fichier .env"
    if ".git" in parts[:-1] or base == ".git":
        return "dossier .git"
    if any(p in ("venv", ".venv") for p in parts[:-1]):
        return "environnement virtuel"
    if base in ("id_rsa", "id_ed25519", ".htpasswd", ".npmrc", ".pgpass", "credentials"):
        return "fichier d'identifiants"
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tar")
    ap.add_argument("--canary", action="append", default=[], help="valeur factice injectee dans le contexte de test")
    ap.add_argument("--allow", action="append", default=[], help="nom de fichier legitime (ex: .env.production)")
    a = ap.parse_args()
    canaries = [c.encode() for c in a.canary]
    high, review = [], []

    with tarfile.open(a.tar) as img:
        manifest = json.load(img.extractfile("manifest.json"))
        for entry in manifest:
            cfg = json.load(img.extractfile(entry["Config"]))
            for e in cfg.get("config", {}).get("Env", []) or []:
                name, _, val = e.partition("=")
                if ENV_NAME.search(name) and val:
                    high.append(f"ENV de l'image : variable {name} non vide")
            for h in cfg.get("history", []) or []:
                cmd = h.get("created_by", "")
                if re.search(r"(ARG|ENV)\s+\w*(PASSWORD|SECRET|TOKEN|API_KEY)\w*=\S+", cmd, re.I):
                    review.append("historique : une instruction ARG/ENV semble definir un secret")
            for i, layer in enumerate(entry["Layers"]):
                raw = img.extractfile(layer).read()
                with tarfile.open(fileobj=io.BytesIO(raw), mode="r:*") as lt:
                    for m in lt:
                        p = m.name.lstrip("./")
                        base = os.path.basename(p)
                        if base.startswith(".wh."):
                            review.append(f"couche {i}: suppression (whiteout) de {p[:-len(base)]}{base[4:]} -> le fichier reste dans une couche anterieure")
                            continue
                        why = sensitive_name(p, a.allow)
                        if why and m.isfile():
                            high.append(f"couche {i}: {why} : /{p}")
                        if not m.isfile() or m.size > MAX_READ:
                            continue
                        data = lt.extractfile(m).read()
                        for c in canaries:
                            if c in data:
                                high.append(f"couche {i}: valeur canari presente dans /{p}")
                        if PRIVATE_KEY.search(data):
                            high.append(f"couche {i}: cle privee dans /{p}")
                        elif AWS_KEY.search(data):
                            high.append(f"couche {i}: motif de cle AWS dans /{p}")
                        elif ASSIGN.search(data) and not any(n in p for n in NOISE_DIRS):
                            review.append(f"couche {i}: affectation de type secret dans /{p} (a examiner)")

    for f in sorted(set(high)):
        print("HAUTE   ", f)
    for f in sorted(set(review)):
        print("A VOIR  ", f)
    print(f"\n{len(set(high))} trouvaille(s) haute(s), {len(set(review))} a examiner")
    sys.exit(1 if high else 0)


if __name__ == "__main__":
    main()
