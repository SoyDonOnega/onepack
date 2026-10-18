#!/usr/bin/env python3
"""Rebuild plugins/<id>/ for every plugin pack: latest upstream + José's overlays.

For each pack with kind "plugin" in packs.json:
  1. Shallow-clone upstream repo@ref and copy `path` (only `include` entries if set)
     into plugins/<id>/.
  2. Rename the plugin to <id> (skills become /<id>:<skill>) and drop its pinned
     version, so Claude Code versions it by commit and picks up every rebuild.
  3. Apply overlays: overlays/<id>/files/** is copied on top (new files);
     overlays/<id>/patches/*.patch is applied in order with `git apply`
     (paths relative to the repo root, e.g. plugins/pocock/skills/...).
  4. Regenerate CATALOG.md (guides/ + the skill index of each built plugin), read by /onepack.
  5. Write plugins/<id>/.onepack.json (upstream sha, patches; no timestamp, so an
     unchanged upstream produces no diff and no new version) and .claude-plugin/marketplace.json.

A patch that no longer applies fails the build (exit 1) and nothing is written:
the last good build stays in git. Standard library only.

Usage: python3 scripts/build.py [pack-id ...]
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def build_pack(pid, spec, work):
    up = spec["upstream"]
    clone = work / pid
    run(["git", "clone", "-q", "--depth", "1", "--branch", up["ref"],
         f"https://github.com/{up['repo']}.git", str(clone)])
    sha = run(["git", "rev-parse", "HEAD"], cwd=clone)
    src = clone / up["path"]

    out = work / "out" / pid
    out.mkdir(parents=True)
    for name in up["include"] or [p.name for p in src.iterdir() if p.name != ".git"]:
        s = src / name
        if s.is_dir():
            shutil.copytree(s, out / name)
        elif s.exists():
            shutil.copy2(s, out / name)
    if not (out / "LICENSE").exists() and (clone / "LICENSE").exists():
        shutil.copy2(clone / "LICENSE", out / "LICENSE")

    manifest = out / ".claude-plugin" / "plugin.json"
    data = json.loads(manifest.read_text())
    data["name"] = pid
    data.pop("version", None)
    manifest.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")

    files = ROOT / "overlays" / pid / "files"
    if files.is_dir():
        shutil.copytree(files, out, dirs_exist_ok=True)
    return out, sha, data


def apply_patches(pid, staged_root):
    """Apply overlays/<pid>/patches/*.patch onto the staged copy (repo-root-relative paths)."""
    patches = sorted((ROOT / "overlays" / pid / "patches").glob("*.patch"))
    for p in patches:
        r = subprocess.run(["git", "apply", "--check", str(p)], cwd=staged_root, capture_output=True, text=True)
        if r.returncode:
            raise RuntimeError(f"overlay {p.relative_to(ROOT)} no longer applies:\n{r.stderr.strip()}")
        run(["git", "apply", str(p)], cwd=staged_root)
    return [p.name for p in patches]


def main(only):
    reg = json.loads((ROOT / "packs.json").read_text())
    plugins = {k: v for k, v in reg["packs"].items() if v["kind"] == "plugin" and (not only or k in only)}
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        staged_root = work / "stage"
        built = {}
        for pid, spec in plugins.items():
            out, sha, data = build_pack(pid, spec, work)
            (staged_root / "plugins").mkdir(parents=True, exist_ok=True)
            shutil.move(str(out), staged_root / "plugins" / pid)
            try:
                applied = apply_patches(pid, staged_root)
            except RuntimeError as e:
                print(f"FAIL {pid}: {e}", file=sys.stderr)
                return 1
            info = {"upstream": spec["upstream"]["repo"], "ref": spec["upstream"]["ref"], "sha": sha,
                    "path": spec["upstream"]["path"], "patches": applied}
            (staged_root / "plugins" / pid / ".onepack.json").write_text(json.dumps(info, indent=2) + "\n")
            built[pid] = (data, info)

        # Only now touch the repo: every pack built and every patch applied.
        for pid in built:
            dest = ROOT / "plugins" / pid
            if dest.exists():
                shutil.rmtree(dest)
            shutil.move(str(staged_root / "plugins" / pid), dest)
            print(f"OK {pid} <- {built[pid][1]['upstream']}@{built[pid][1]['sha'][:7]} patches={built[pid][1]['patches']}")

    write_marketplace(reg)
    write_catalog(reg)
    return 0


def write_marketplace(reg):
    entries = []
    for pid, spec in reg["packs"].items():
        if spec["kind"] != "plugin" or not (ROOT / "plugins" / pid).is_dir():
            continue
        entries.append({"name": pid, "source": f"./plugins/{pid}", "description": spec["description"]})
    market = {"name": "onepack", "owner": {"name": "SoyDonOnega"},
              "description": "José's per-project packs: upstream skills rebuilt daily with his overlays.",
              "plugins": entries}
    (ROOT / ".claude-plugin").mkdir(exist_ok=True)
    (ROOT / ".claude-plugin" / "marketplace.json").write_text(json.dumps(market, indent=2) + "\n")


def skill_index(pid):
    """One line per skill of a built plugin: name and the first sentence of its description."""
    root = ROOT / "plugins" / pid
    declared = json.loads((root / ".claude-plugin" / "plugin.json").read_text()).get("skills")
    files = ([root / d / "SKILL.md" for d in declared] if declared
             else sorted((root / "skills").rglob("SKILL.md")))
    rows = []
    for f in files:
        if not f.exists():
            continue
        text = f.read_text(encoding="utf-8", errors="replace")
        if not text.startswith("---"):
            continue
        front = text.split("---", 2)[1]
        name, desc, in_desc = f.parent.name, "", False
        for line in front.splitlines():
            if line.startswith("name:"):
                name = line.split(":", 1)[1].strip().strip('"')
            elif line.startswith("description:"):
                desc, in_desc = line.split(":", 1)[1].strip().strip(">|-").strip().strip('"'), True
            elif in_desc and line.startswith((" ", "\t")):
                desc += " " + line.strip()
            else:
                in_desc = False
        parts = desc.split(". ")
        first = parts[0] if len(parts[0]) >= 25 or len(parts) == 1 else ". ".join(parts[:2])
        first = first.rstrip(".")
        rows.append(f"- `{name}` — {first}")
    return rows


def write_catalog(reg):
    g = ROOT / "guides"
    out = ["# onepack catalog", "",
           "Generated by scripts/build.py from guides/ and the built plugins. Do not edit by hand.", ""]
    if (g / "_choosing.md").exists():
        out += [(g / "_choosing.md").read_text().strip(), ""]
    out += ["## Packs", ""]
    for pid, spec in reg["packs"].items():
        grp = f"group `{spec['group']}`" if spec.get("group") else "no group (combines with anything)"
        out += [f"### {pid} — {grp}, {spec['kind']}", ""]
        if (g / f"{pid}.md").exists():
            out += [(g / f"{pid}.md").read_text().strip(), ""]
        if spec["kind"] == "plugin" and (ROOT / "plugins" / pid).is_dir():
            rows = skill_index(pid)
            out += [f"**Skills ({len(rows)}, invoke as `/{pid}:<name>`):**", ""] + rows + [""]
    (ROOT / "CATALOG.md").write_text("\n".join(out))


if __name__ == "__main__":
    sys.exit(main(set(sys.argv[1:])))
