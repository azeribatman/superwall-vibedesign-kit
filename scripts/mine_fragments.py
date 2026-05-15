#!/usr/bin/env python3
"""Extract reusable subtrees ("fragments") from all templates, grouped by their
designer-assigned name (Hero, Purchase Button, Continue, Footer, FAQ, etc.).

Output: data/fragments/<slug>/<template_id>.json
        data/fragments/INDEX.json   — slug -> [{template_id, root_id, depth, n_nodes, name}, ...]
"""
import json, re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[1]
TPL_DIR = ROOT / "data" / "templates"
OUT_DIR = ROOT / "data" / "fragments"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def slug(s):
    s = (s or "").lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "unnamed"


def load_store(path):
    d = json.loads(path.read_text())
    snap = d["snapshot"]
    inner = snap.get("snapshot", snap)
    return inner.get("store", {}), d.get("meta", {})


def collect_subtree(store, root_node_id, nodes_by_id):
    """Return all node ids in the subtree rooted at root_node_id."""
    out = [root_node_id]
    stack = [root_node_id]
    children_of = defaultdict(list)
    for nid, n in nodes_by_id.items():
        pid = n.get("parentId")
        if pid:
            children_of[pid].append(nid)
    while stack:
        cur = stack.pop()
        for c in children_of.get(cur, []):
            out.append(c)
            stack.append(c)
    return out


# names worth extracting — these recur across templates
NAME_WHITELIST_PATTERNS = [
    "hero", "header", "navbar", "navigation",
    "purchase", "continue", "cta", "buy", "subscribe", "start",
    "restore", "terms", "privacy", "links", "footer",
    "feature", "benefit", "checklist", "list",
    "product", "plan", "tier", "card", "price",
    "trial", "timeline", "intro",
    "faq", "question",
    "testimonial", "review", "rating",
    "drawer", "sheet", "modal",
    "image", "carousel", "gallery",
    "title", "subtitle", "description",
    "close", "dismiss", "x",
    "tab", "page",
]


def matches_whitelist(name):
    if not name: return None
    n = name.lower()
    for pat in NAME_WHITELIST_PATTERNS:
        if pat in n:
            return pat
    return None


def main():
    files = sorted(TPL_DIR.glob("*.json"))
    print(f"mining fragments from {len(files)} templates...")

    index = defaultdict(list)
    total_fragments = 0

    for f in files:
        try:
            store, meta = load_store(f)
        except Exception:
            continue
        tid = meta.get("id") or f.stem
        nodes_by_id = {r.get("id", rid): r for rid, r in store.items()
                       if r.get("typeName") == "node"}

        for nid, n in nodes_by_id.items():
            name = n.get("name", "")
            cat = matches_whitelist(name)
            if not cat:
                continue
            # only meaningful subtrees: at least 2 nodes, at most 50
            sub = collect_subtree(store, nid, nodes_by_id)
            if len(sub) < 2 or len(sub) > 50:
                continue
            sl = slug(cat)
            # write subtree records (just the nodes, not states/products — references resolved later)
            records = {rid: store[rid] for rid in sub if rid in store}
            # also try by id-keyed records
            for nid2 in sub:
                if nid2 in store:
                    records[nid2] = store[nid2]
                else:
                    # store may key by record id rather than node id; find it
                    for rid, rec in store.items():
                        if rec.get("id") == nid2 and rec.get("typeName") == "node":
                            records[rid] = rec
                            break

            slug_dir = OUT_DIR / sl
            slug_dir.mkdir(parents=True, exist_ok=True)
            out = {
                "fragment_name": cat,
                "designer_name": name,
                "template_id": tid,
                "root_node_id": nid,
                "n_nodes": len(sub),
                "records": records,
            }
            out_path = slug_dir / f"{tid}_{nid.replace(':','_')[:40]}.json"
            out_path.write_text(json.dumps(out))
            index[sl].append({
                "template_id": tid,
                "designer_name": name,
                "root_node_id": nid,
                "n_nodes": len(sub),
                "path": str(out_path.relative_to(ROOT)),
            })
            total_fragments += 1

    # Sort each slug by n_nodes ascending (smaller = more reusable)
    for sl in index:
        index[sl].sort(key=lambda e: e["n_nodes"])

    (OUT_DIR / "INDEX.json").write_text(json.dumps(dict(index), indent=2))
    print(f"\nextracted {total_fragments} fragments into {len(index)} categories")
    for sl, entries in sorted(index.items(), key=lambda kv: -len(kv[1]))[:15]:
        print(f"  {sl}: {len(entries)}")


if __name__ == "__main__":
    main()
