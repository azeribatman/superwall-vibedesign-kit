#!/usr/bin/env python3
"""Mine generative grammar from all templates in data/templates/.

Produces data/grammar/*.json:
  composition.json — parent_node_type -> {child_node_type: count}
  properties.json  — node_type -> {prop_name: {count, present_in_pct, value_shapes}}
  states.json      — state_id -> {value_kinds, operators, templates_using}
  theme_tokens.json— interface token -> {templates_with_token, light_default_kinds}
  node_index.json  — node_type -> {count, templates_using}
  skeleton.json    — minimum record set common to all templates
"""
import json
from pathlib import Path
from collections import defaultdict, Counter

ROOT = Path(__file__).resolve().parents[1]
TPL_DIR = ROOT / "data" / "templates"
OUT_DIR = ROOT / "data" / "grammar"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def load_store(path):
    d = json.loads(path.read_text())
    snap = d["snapshot"]
    inner = snap.get("snapshot", snap)
    return inner.get("store", {}), d.get("meta", {})


def value_shape(v):
    """Classify a wrapped value into a shape tag."""
    if not isinstance(v, dict):
        return type(v).__name__
    t = v.get("type")
    if t == "literal":
        val = v.get("value")
        if isinstance(val, dict):
            return f"literal:{','.join(sorted(val.keys()))[:80]}"
        return f"literal:{type(val).__name__}"
    if t == "conditional":
        ops = sorted({o.get("condition", {}).get("operator") for o in v.get("options", []) if o.get("condition")})
        return f"conditional:{','.join(o for o in ops if o)}"
    if t == "referential":
        return f"referential:{v.get('stateId','?')[:40]}"
    if t == "tombstone":
        return "tombstone"
    return f"other:{t}"


def main():
    composition = defaultdict(Counter)        # parent_type -> Counter(child_type)
    properties = defaultdict(lambda: defaultdict(Counter))  # node_type -> prop -> Counter(shape)
    node_count = defaultdict(int)              # node_type -> count
    node_templates = defaultdict(set)          # node_type -> {template_ids}
    type_count_per_template = defaultdict(int) # node_type -> templates_using_count via set above; computed at end
    state_kinds = defaultdict(Counter)         # state_id -> Counter(value_kind)
    state_ops = defaultdict(Counter)           # state_id -> Counter(operator)
    state_templates = defaultdict(set)         # state_id -> templates
    token_present = Counter()                  # interface token -> templates
    token_light_kinds = defaultdict(Counter)   # token -> Counter(value_kind on .light)
    record_types_per_template = defaultdict(set)  # template_id -> {recordId}
    template_ids = []

    files = sorted(TPL_DIR.glob("*.json"))
    print(f"mining {len(files)} templates...")

    for f in files:
        try:
            store, meta = load_store(f)
        except Exception as e:
            print(f"skip {f.name}: {e}")
            continue
        tid = meta.get("id") or f.stem
        template_ids.append(tid)

        # Build id->record and parent map for nodes
        nodes_by_id = {}
        for rid, rec in store.items():
            if rec.get("typeName") == "node":
                nodes_by_id[rec.get("id", rid)] = rec
            record_types_per_template[tid].add(rid)

        # Composition: parent type -> child type
        for nid, nrec in nodes_by_id.items():
            parent_id = nrec.get("parentId")
            parent = nodes_by_id.get(parent_id)
            ptype = parent.get("type") if parent else "_root"
            ctype = nrec.get("type", "?")
            composition[ptype][ctype] += 1

            # Properties per node type
            for prop, val in (nrec.get("properties") or {}).items():
                properties[ctype][prop][value_shape(val)] += 1
            for prop, val in (nrec.get("defaultProperties") or {}).items():
                # mark as default-only with prefix
                properties[ctype][f"(default){prop}"][value_shape(val)] += 1

            node_count[ctype] += 1
            node_templates[ctype].add(tid)

        # States
        for rid, rec in store.items():
            if rec.get("typeName") == "state":
                sid = rec.get("id", rid)
                # strip the unique tail for variable states; keep the "state:" path
                # use full id if it starts with state:
                key = sid if isinstance(sid, str) and sid.startswith("state:") else rid
                # value kind from default
                default = rec.get("default") or rec.get("value") or {}
                kind = value_shape(default if isinstance(default, dict) else {"type":"literal","value":default})
                state_kinds[key][kind] += 1
                state_templates[key].add(tid)

                # interface token tracking
                if isinstance(key, str) and key.startswith("state:style.interface."):
                    token_present[key] += 1
                    light = rec.get("default") if isinstance(rec.get("default"), dict) else None
                    if light:
                        token_light_kinds[key][value_shape(light)] += 1

        # Conditional operators referencing states
        def walk(obj):
            if isinstance(obj, dict):
                if obj.get("type") == "conditional":
                    for opt in obj.get("options", []):
                        cond = opt.get("condition") or {}
                        sref = cond.get("stateId") or cond.get("state")
                        op = cond.get("operator")
                        if sref and op:
                            state_ops[sref][op] += 1
                for v in obj.values():
                    walk(v)
            elif isinstance(obj, list):
                for v in obj:
                    walk(v)
        walk(store)

    # Derive: for each node type, which props are universal vs optional
    properties_summary = {}
    for ntype, props in properties.items():
        total = node_count[ntype]
        ps = {}
        for prop, shapes in props.items():
            present = sum(shapes.values())
            ps[prop] = {
                "present_count": present,
                "present_pct": round(100 * present / total, 1) if total else 0,
                "value_shapes": dict(shapes.most_common(8)),
            }
        properties_summary[ntype] = {
            "total_nodes": total,
            "templates_using": len(node_templates[ntype]),
            "props": dict(sorted(ps.items(), key=lambda kv: -kv[1]["present_count"])),
        }

    composition_summary = {
        p: dict(c.most_common()) for p, c in composition.items()
    }

    states_summary = {}
    for sid, kinds in state_kinds.items():
        states_summary[sid] = {
            "value_kinds": dict(kinds),
            "operators_used": dict(state_ops.get(sid, {})),
            "templates_using": len(state_templates[sid]),
        }

    theme_tokens_summary = {
        tok: {
            "templates_with_token": token_present[tok],
            "value_kinds": dict(token_light_kinds[tok]),
        }
        for tok in sorted(token_present, key=lambda k: -token_present[k])
    }

    node_index_summary = {
        nt: {
            "node_instances": node_count[nt],
            "templates_using": len(node_templates[nt]),
        }
        for nt in sorted(node_count, key=lambda k: -node_count[k])
    }

    # Skeleton: record id prefixes present in every template
    if record_types_per_template:
        # use record id prefixes (before the unique tail) — keep things like paywall:paywall, page:page, state:style.interface.primary
        def normalize(rid):
            if rid.startswith("node:") or rid.startswith("paywall_product:") or rid.startswith("paywall_notification:"):
                return rid.split(":")[0] + ":*"
            return rid
        normalized = {tid: {normalize(r) for r in rs} for tid, rs in record_types_per_template.items()}
        common = set.intersection(*normalized.values()) if normalized else set()
        skeleton = sorted(common)
    else:
        skeleton = []

    (OUT_DIR / "composition.json").write_text(json.dumps(composition_summary, indent=2, sort_keys=True))
    (OUT_DIR / "properties.json").write_text(json.dumps(properties_summary, indent=2, sort_keys=True))
    (OUT_DIR / "states.json").write_text(json.dumps(states_summary, indent=2, sort_keys=True))
    (OUT_DIR / "theme_tokens.json").write_text(json.dumps(theme_tokens_summary, indent=2))
    (OUT_DIR / "node_index.json").write_text(json.dumps(node_index_summary, indent=2))
    (OUT_DIR / "skeleton.json").write_text(json.dumps({"common_records": skeleton, "n_templates": len(template_ids)}, indent=2))

    print(f"\nwrote {len(list(OUT_DIR.glob('*.json')))} grammar files to {OUT_DIR}")
    print(f"  node types: {len(node_index_summary)}")
    print(f"  states tracked: {len(states_summary)}")
    print(f"  interface tokens: {len(theme_tokens_summary)}")
    print(f"  skeleton size: {len(skeleton)} records always present")
    print(f"\ncompositions:")
    for p, kids in sorted(composition_summary.items(), key=lambda kv: -sum(kv[1].values()))[:8]:
        top = ", ".join(f"{k}({v})" for k, v in list(kids.items())[:5])
        print(f"  {p}: {top}")


if __name__ == "__main__":
    main()
