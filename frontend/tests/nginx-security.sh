#!/usr/bin/env bash
# Tests de non-regression HTTP du frontend (a lancer contre un conteneur de test, jamais la prod).
# Usage: BASE_URL=http://localhost:8080 ./tests/nginx-security.sh
BASE_URL="${BASE_URL:-http://localhost:8080}"
pass=0; fail=0
TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT

# req <path> -> remplit CODE, CTYPE, et $TMP/body
req() {
  CODE=$(curl -s --path-as-is -o "$TMP/body" -D "$TMP/hdr" -w '%{http_code}' "$BASE_URL$1")
  CTYPE=$(grep -i '^content-type:' "$TMP/hdr" | tr -d '\r' | cut -d' ' -f2- | cut -d';' -f1)
}
ok()  { pass=$((pass+1)); echo "PASS  $1"; }
bad() { fail=$((fail+1)); echo "FAIL  $1 -> $2"; }

# deny <path> <code> : code attendu, et corps = ni SPA ni contenu sensible
deny() {
  req "$1"
  if [ "$CODE" != "$2" ]; then bad "$1" "HTTP $CODE (attendu $2)"; return; fi
  if grep -q 'id="app"' "$TMP/body"; then bad "$1" "servi par le fallback SPA"; return; fi
  if grep -qE 'SECRET|PASSWORD|DATABASE_URL|\[core\]|FROM node|"dependencies"' "$TMP/body"; then bad "$1" "contenu sensible"; return; fi
  ok "$1 -> $CODE"
}
# spa <path> : 200, text/html, index.html
spa() {
  req "$1"
  if [ "$CODE" = 200 ] && [ "$CTYPE" = text/html ] && grep -q 'id="app"' "$TMP/body"; then ok "SPA $1"; else bad "SPA $1" "HTTP $CODE $CTYPE"; fi
}

for p in /.env /.env.example /.env.production /.git/config /.git/HEAD /.htaccess /.DS_Store /%2eenv //.env /assets/../.env \
         /Dockerfile /docker-compose.yml /docker-compose.prod.yml /package.json /package-lock.json /vite.config.js \
         /config.php /wp-config.php /backup.zip /dump.sql /app.bak /nginx.conf /src/main.js.map; do
  deny "$p" 404
done
deny /.well-known/inexistant 404
deny /assets/inexistant.js 404
deny /assets/inexistant.css 404
deny /image-inexistante.png 404

# Fichiers publics legitimes
spa /index.html
req /favicon.ico; [ "$CODE" = 200 ] && ok "/favicon.ico" || bad "/favicon.ico" "HTTP $CODE"

# Routes SPA, avec et sans slash final
for r in / /menus /menu/1 /contact /login /register /mot-de-passe-oublie /reinitialiser-mdp /commande \
         /mon-compte /mes-commandes /avis /admin /admin/menus /employe /mentions-legales /cgv /route-inconnue \
         /menus/ /login/ /mon-compte/ /mes-commandes/ /avis/; do
  spa "$r"
done

# Assets generes par le build, references par index.html
req /; assets=$(grep -oE '/assets/[^"]+\.(js|css)' "$TMP/body")
[ -n "$assets" ] || bad "assets" "aucun asset reference dans index.html"
for a in $assets; do
  req "$a"
  case "$a" in *.js) want=javascript;; *.css) want=text/css;; esac
  if [ "$CODE" = 200 ] && echo "$CTYPE" | grep -q "$want"; then ok "asset $a"; else bad "asset $a" "HTTP $CODE $CTYPE"; fi
done

# En-tetes de securite
req /; for h in x-content-type-options referrer-policy x-frame-options permissions-policy content-security-policy; do
  grep -qi "^$h:" "$TMP/hdr" && ok "header $h" || bad "header $h" "absent"
done
grep -qi '^server: nginx/' "$TMP/hdr" && bad "server_tokens" "version exposee" || ok "server_tokens off"
# les en-tetes doivent aussi etre presents sur un 404
req /.env; grep -qi '^x-content-type-options:' "$TMP/hdr" && ok "header sur 404" || bad "header sur 404" "absent"

echo; echo "Resultat: $pass reussis, $fail echoues"
[ "$fail" -eq 0 ]
