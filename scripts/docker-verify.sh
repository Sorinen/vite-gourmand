#!/usr/bin/env bash
# Verification pre-deploiement, a lancer sur une machine AVEC Docker. Ne deploie rien, ne pousse rien.
#
# Prerequis reseau : le build tire les images de base et les paquets (npm, pip) = acces lecture seule
# aux registres publics. Aucun secret reel n'est lu : le dossier backend/.env reel n'est JAMAIS copie ;
# toutes les valeurs ci-dessous sont factices et generees pour l'occasion.
#
# Usage : ./scripts/docker-verify.sh        (depuis n'importe ou)
# Ressources creees : images vg-test-*:$ID, conteneurs/reseau vg-t-$ID-*, dossier temporaire.
# Aucun volume nomme, aucun `docker system prune`, aucune suppression hors de ces ressources.
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ID="$(date +%s)$$"
WORK="$(mktemp -d)"
NET="vg-t-$ID-net"; PG="vg-t-$ID-pg"; BACK="vg-t-$ID-back"; FRONT="vg-t-$ID-front"
CANARY="CANARY_$(openssl rand -hex 8)"
TESTPW="$(openssl rand -hex 12)"; TESTKEY="$(openssl rand -hex 16)"
pass=0; fail=0
ok()  { pass=$((pass+1)); echo "PASS  $1"; }
bad() { fail=$((fail+1)); echo "FAIL  $1"; }
check() { if eval "$2"; then ok "$1"; else bad "$1"; fi; }

cleanup() {
  docker rm -f "$BACK" "$FRONT" "$PG" >/dev/null 2>&1
  docker network rm "$NET" >/dev/null 2>&1
  rm -rf "$WORK"
}
trap cleanup EXIT

command -v docker >/dev/null || { echo "docker introuvable"; exit 2; }
docker compose version >/dev/null 2>&1 || { echo "docker compose introuvable"; exit 2; }

# wait_for <description> <timeout_s> <commande...> : attend une condition reelle (pas un sleep fixe)
wait_for() {
  local d="$1" t="$2"; shift 2; local i=0
  until "$@" >/dev/null 2>&1; do i=$((i+1)); [ "$i" -ge "$t" ] && { echo "timeout: $d"; return 1; }; sleep 1; done
}

echo "== 1. Contextes de build de test (le .env reel n'est jamais copie)"
mkdir -p "$WORK/backend" "$WORK/frontend"
rsync -a --exclude='.env' --exclude='.env.*' --exclude='venv' --exclude='.git' --exclude='node_modules' --exclude='dist' \
  "$ROOT/backend/" "$WORK/backend/"
rsync -a --exclude='.env' --exclude='.env.*' --exclude='node_modules' --exclude='dist' \
  "$ROOT/frontend/" "$WORK/frontend/"
cp "$ROOT/frontend/.env.production" "$WORK/frontend/.env.production"
# fichiers pieges FACTICES que les .dockerignore doivent empecher d'entrer dans les images
for d in backend frontend; do
  printf 'DECOY=%s\n' "$CANARY" > "$WORK/$d/.env"
  printf 'DECOY=%s\n' "$CANARY" > "$WORK/$d/.env.local"
  printf -- '-----BEGIN PRIVATE KEY-----\n%s\n' "$CANARY" > "$WORK/$d/decoy.key"
  printf '%s\n' "$CANARY" > "$WORK/$d/decoy.log"
  mkdir -p "$WORK/$d/.git"; printf '[core]\n%s\n' "$CANARY" > "$WORK/$d/.git/config"
done
mkdir -p "$WORK/backend/venv"; printf '%s\n' "$CANARY" > "$WORK/backend/venv/pyvenv.cfg"

echo "== 2. Build"
docker build -q -t "vg-test-backend:$ID"  "$WORK/backend"  >/dev/null && ok "build backend"  || bad "build backend"
docker build -q -t "vg-test-frontend:$ID" "$WORK/frontend" >/dev/null && ok "build frontend" || bad "build frontend"
# controle positif : sans .dockerignore, le scanner DOIT detecter les pieges (sinon le scanner est aveugle)
rm -f "$WORK/backend/.dockerignore"
docker build -q -t "vg-test-backend-noignore:$ID" "$WORK/backend" >/dev/null || bad "build controle positif"
cp "$ROOT/backend/.dockerignore" "$WORK/backend/.dockerignore"

echo "== 3. Analyse de TOUTES les couches (docker save + scanner)"
for pair in "backend:" "frontend:--allow .env.production"; do
  n="${pair%%:*}"; extra="${pair#*:}"
  docker save -o "$WORK/$n.tar" "vg-test-$n:$ID"
  # shellcheck disable=SC2086
  python3 "$ROOT/scripts/scan-image-layers.py" "$WORK/$n.tar" --canary "$CANARY" $extra && ok "couches $n sans piege ni secret" || bad "couches $n : voir ci-dessus"
done
docker save -o "$WORK/noignore.tar" "vg-test-backend-noignore:$ID"
python3 "$ROOT/scripts/scan-image-layers.py" "$WORK/noignore.tar" --canary "$CANARY" >/dev/null
[ $? -eq 1 ] && ok "controle positif : le scanner detecte les pieges sans .dockerignore" || bad "controle positif : scanner aveugle"

echo "== 4. Systeme de fichiers FINAL et configuration"
check "backend : pas de .env dans /app" "! docker run --rm --entrypoint sh vg-test-backend:$ID -c 'test -e /app/.env -o -e /app/venv -o -e /app/.git'"
check "backend : app, requirements presents" "docker run --rm --entrypoint sh vg-test-backend:$ID -c 'test -f /app/app/main.py -a -f /app/requirements.txt'"
check "backend : pas de cle privee (contenu) hors certificats systeme" \
  "! docker run --rm --entrypoint sh vg-test-backend:$ID -c 'grep -rIl --exclude-dir=proc --exclude-dir=sys -e \"BEGIN .*PRIVATE KEY\" /app /root /home 2>/dev/null | grep .'"
check "frontend : index.html + assets, pas de .env" \
  "docker run --rm --entrypoint sh vg-test-frontend:$ID -c 'test -f /usr/share/nginx/html/index.html -a -d /usr/share/nginx/html/assets && ! find /usr/share/nginx/html -name \".*\" -not -name . | grep .'"
for n in backend frontend; do
  echo "   Env de vg-test-$n (noms uniquement) :"
  docker image inspect "vg-test-$n:$ID" --format '{{range .Config.Env}}{{println .}}{{end}}' | cut -d= -f1 | sed 's/^/     /'
done
echo "   Utilisateur du backend : $(docker image inspect vg-test-backend:$ID --format '{{.Config.User}}' | sed 's/^$/(vide = root)/')"

echo "== 5. Compose avec variables fictives (sans .env auto-charge)"
cfg() { env -i PATH="$PATH" HOME="$HOME" ${DOCKER_HOST:+DOCKER_HOST="$DOCKER_HOST"} "$@"; }
for f in docker-compose.yml docker-compose.prod.yml; do
  cfg SECRET_KEY="$TESTKEY" POSTGRES_PASSWORD="$TESTPW" MAIL_USERNAME=u@test MAIL_PASSWORD=x MAIL_FROM=f@test \
    docker compose --env-file /dev/null -f "$ROOT/$f" config > "$WORK/cfg.out" 2>&1 \
    && ok "$f : config valide" || bad "$f : config invalide"
  check "$f : mot de passe PG identique dans POSTGRES_PASSWORD et DATABASE_URL" "[ \$(grep -c '$TESTPW' '$WORK/cfg.out') -ge 2 ]"
  check "$f : MAIL_* transmis" "grep -q 'MAIL_USERNAME' '$WORK/cfg.out' && grep -q 'MAIL_PASSWORD' '$WORK/cfg.out'"
  cfg SECRET_KEY="$TESTKEY" docker compose --env-file /dev/null -f "$ROOT/$f" config >/dev/null 2>&1 \
    && bad "$f : doit refuser sans POSTGRES_PASSWORD" || ok "$f : refuse sans POSTGRES_PASSWORD"
  cfg POSTGRES_PASSWORD="$TESTPW" docker compose --env-file /dev/null -f "$ROOT/$f" config >/dev/null 2>&1 \
    && bad "$f : doit refuser sans SECRET_KEY" || ok "$f : refuse sans SECRET_KEY"
done
echo "   Ports publies par docker-compose.prod.yml :"; cfg SECRET_KEY=x POSTGRES_PASSWORD=x docker compose --env-file /dev/null -f "$ROOT/docker-compose.prod.yml" config 2>/dev/null | grep -A3 'ports:' | sed 's/^/     /'

echo "== 6. Frontend : conteneur isole, tests HTTP reels"
docker run -d --name "$FRONT" -p 127.0.0.1::80 "vg-test-frontend:$ID" >/dev/null
FPORT="$(docker port "$FRONT" 80/tcp | head -1 | sed 's/.*://')"
wait_for "frontend" 30 curl -fs "http://127.0.0.1:$FPORT/" && {
  BASE_URL="http://127.0.0.1:$FPORT" "$ROOT/frontend/tests/nginx-security.sh" | tail -3
  BASE_URL="http://127.0.0.1:$FPORT" "$ROOT/frontend/tests/nginx-security.sh" >/dev/null && ok "nginx-security.sh contre le conteneur" || bad "nginx-security.sh contre le conteneur"
  echo "   --- logs nginx (derniers 5)"; docker logs "$FRONT" 2>&1 | tail -5 | sed 's/^/     /'
} || bad "frontend ne demarre pas"

echo "== 7. Backend : base de test isolee, demarrage reel"
docker network create "$NET" >/dev/null
# donnees en tmpfs : aucun volume cree ; tout disparait avec le conteneur
docker run -d --name "$PG" --network "$NET" --tmpfs /var/lib/postgresql/data \
  -e POSTGRES_PASSWORD="$TESTPW" -e POSTGRES_DB=vite_gourmand postgres:16 >/dev/null
# pg_isready en TCP (-h 127.0.0.1) : le serveur temporaire d'initialisation n'ecoute que sur le socket unix,
# donc ceci n'est vrai qu'une fois le VRAI serveur demarre.
wait_for "postgres (TCP)" 90 docker exec "$PG" pg_isready -h 127.0.0.1 -U postgres -d vite_gourmand && ok "postgres de test pret" || bad "postgres de test"
DBURL="postgresql://postgres:$TESTPW@$PG:5432/vite_gourmand"
run_back() { docker run --rm --network "$NET" -e DATABASE_URL="$DBURL" -e MONGO_URL=mongodb://unused:27017 "$@" "vg-test-backend:$ID" python -c "import app.main"; }

# DATABASE_URL est VALIDE ici : l'echec doit venir de SECRET_KEY, pas d'un autre import (sinon faux positif)
out="$(run_back 2>&1)"; rc=$?
{ [ $rc -ne 0 ] && echo "$out" | grep -q 'SECRET_KEY est absente'; } && ok "sans SECRET_KEY : echec explicite" || bad "sans SECRET_KEY : mauvais comportement (rc=$rc)"
out="$(run_back -e SECRET_KEY= 2>&1)"; rc=$?
{ [ $rc -ne 0 ] && echo "$out" | grep -q 'SECRET_KEY est absente'; } && ok "SECRET_KEY vide : echec explicite" || bad "SECRET_KEY vide : mauvais comportement (rc=$rc)"
run_back -e SECRET_KEY="$TESTKEY" >/dev/null 2>&1 && ok "avec cle de test : import et create_all OK" || bad "avec cle de test : echec"

docker run -d --name "$BACK" --network "$NET" -p 127.0.0.1::8000 \
  -e DATABASE_URL="$DBURL" -e MONGO_URL=mongodb://unused:27017 -e SECRET_KEY="$TESTKEY" \
  -e MAIL_USERNAME=u@test -e MAIL_PASSWORD=x -e MAIL_FROM=f@test "vg-test-backend:$ID" >/dev/null
BPORT="$(docker port "$BACK" 8000/tcp | head -1 | sed 's/.*://')"
wait_for "backend" 40 curl -fs "http://127.0.0.1:$BPORT/" \
  && check "GET / renvoie le message attendu" "curl -s http://127.0.0.1:$BPORT/ | grep -q 'API Vite & Gourmand'" \
  || { bad "backend ne demarre pas"; docker logs "$BACK" 2>&1 | tail -15 | sed 's/^/     /'; }
check "route protegee sans jeton : 401" \
  "[ \$(curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:$BPORT/utilisateurs/admin/employes) = 401 ]"
check "route protegee avec jeton forge : 401" \
  "[ \$(curl -s -o /dev/null -w '%{http_code}' -H 'Authorization: Bearer faux.jeton.x' http://127.0.0.1:$BPORT/utilisateurs/admin/employes) = 401 ]"
check "MAIL_* visibles dans le conteneur, sans .env" "docker exec $BACK sh -c 'test -n \"\$MAIL_USERNAME\" && test ! -e /app/.env'"
echo "   Utilisateur effectif du processus backend : uid=$(docker exec "$BACK" id -u)"

echo; echo "Resultat: $pass reussis, $fail echoues"
[ "$fail" -eq 0 ]
