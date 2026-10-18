#!/bin/bash
# Install onepack on this Mac: clone to ~/.onepack, link the CLI, register the
# marketplace in Claude Code with auto-update on. Safe to re-run.
set -euo pipefail

DIR="${ONEPACK_HOME:-$HOME/.onepack}"
BIN="$HOME/.local/bin"

if [ -d "$DIR/.git" ]; then
  git -C "$DIR" pull -q --ff-only
else
  gh repo clone SoyDonOnega/onepack "$DIR" -- -q
fi
mkdir -p "$BIN"
ln -sfn "$DIR/bin/onepack" "$BIN/onepack"
chmod +x "$DIR/bin/onepack"
# The /onepack skill (skills/onepack) is installed by OneStack with the other skills.
# Drop the link older versions of this script created.
[ -L "$HOME/.claude/skills/onepack" ] && rm "$HOME/.claude/skills/onepack"

claude plugin marketplace list 2>/dev/null | grep -q "❯ onepack\b" || claude plugin marketplace add SoyDonOnega/onepack

# Auto-update: Claude Code refreshes the marketplace after each session starts.
python3 - <<'EOF'
import json, os
p = os.path.expanduser("~/.claude/settings.json")
s = json.load(open(p)) if os.path.exists(p) else {}
m = s.setdefault("extraKnownMarketplaces", {}).setdefault("onepack", {})
m.setdefault("source", {"source": "github", "repo": "SoyDonOnega/onepack"})
m["autoUpdate"] = True
json.dump(s, open(p, "w"), indent=2)
open(p, "a").write("\n")
print("onepack: auto-update on in ~/.claude/settings.json")
EOF

echo "onepack: installed ($("$BIN/onepack" help >/dev/null && echo ok)). Try: onepack list"
