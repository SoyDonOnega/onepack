#!/bin/bash
# onepack cloud setup: run from a Claude Code cloud environment's setup script (as root,
# before Claude starts). Paste this one line into the environment's "Setup script" field:
#
#   curl -fsSL https://raw.githubusercontent.com/SoyDonOnega/onepack/main/cloud/setup.sh | bash
#
# It installs into the VM:
# - the skills listed in cloud/skills.txt and the /onepack skill → ~/.claude/skills/<name>/
# - onepack itself (catalog, registry, CLI) → ~/.onepack, CLI on the PATH
# - the plugin packs (pocock, pstack) as skills-directory plugins, off by default: a repo
#   turns one on with "<pack>@skills-dir": true in its .claude/settings.json (onepack add)
# - the speckit and openspec CLIs
# Needs network access to github.com and package managers. Re-running replaces what it installed.
# ONEPACK_REF picks a branch (default main); ONEPACK_BIN the CLI folder (default /usr/local/bin).
set -uo pipefail

REF="${ONEPACK_REF:-main}"
HOME_DIR="$HOME/.onepack"
SKILLS="$HOME/.claude/skills"
BIN="${ONEPACK_BIN:-/usr/local/bin}"
log() { echo "onepack-cloud: $*"; }

copy() { # $1 src folder, $2 dest (replaced)
  rm -rf "$2"; mkdir -p "$2"
  (cd "$1" && tar --exclude .git --exclude .DS_Store --exclude .gitignore -cf - .) | (cd "$2" && tar -xf -)
}

rm -rf "$HOME_DIR"
git clone -q --depth 1 --branch "$REF" https://github.com/SoyDonOnega/onepack.git "$HOME_DIR" \
  || { log "error: cannot clone SoyDonOnega/onepack@$REF"; exit 1; }
touch "$HOME_DIR/.last-update"
mkdir -p "$SKILLS" "$BIN"

# Own skills: public repos <name>-skill, installed as /<name>.
while read -r repo; do
  case "$repo" in ''|'#'*) continue ;; esac
  name="$(basename "$repo")"; name="${name%-skill}"
  tmp="$(mktemp -d)"
  if git clone -q --depth 1 "https://github.com/$repo.git" "$tmp/s"; then
    copy "$tmp/s" "$SKILLS/$name"; log "skill /$name"
  else
    log "WARN: cannot clone $repo (public?)"
  fi
  rm -rf "$tmp"
done < "$HOME_DIR/cloud/skills.txt"
copy "$HOME_DIR/skills/onepack" "$SKILLS/onepack"; log "skill /onepack"

# Plugin packs: skills-directory plugins, off until a repo enables "<pack>@skills-dir".
for dir in "$HOME_DIR"/plugins/*/; do
  id="$(basename "$dir")"
  copy "$dir" "$SKILLS/$id"
  python3 - "$SKILLS/$id/.claude-plugin/plugin.json" <<'EOF'
import json, sys
p = sys.argv[1]
m = json.load(open(p))
m["defaultEnabled"] = False
json.dump(m, open(p, "w"), indent=2)
EOF
  log "plugin $id (off by default)"
done

ln -sfn "$HOME_DIR/bin/onepack" "$BIN/onepack"; chmod +x "$HOME_DIR/bin/onepack"; log "CLI $BIN/onepack"

command -v specify >/dev/null || uv tool install -q specify-cli --from git+https://github.com/github/spec-kit.git \
  || log "WARN: specify CLI not installed"
command -v openspec >/dev/null || npm install -g --silent @fission-ai/openspec@latest \
  || log "WARN: openspec CLI not installed"
log "done"
