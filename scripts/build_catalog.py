#!/usr/bin/env python3
"""Walk every pulled template and emit a deterministic schema catalog.

Outputs to data/catalog/:
  node_types.json          - all node.type values with counts
  node_names.json          - unique node names (often semantic hints)
  properties.json          - every property key + distinct value type shapes
  state_ids.json           - every state:* identifier referenced + usage sites
  conditional_fields.json  - condition query fields + operators seen
  notifications.json       - paywall_notification types + sample structure
  style_tokens.json        - style_variable_group catalog
  click_behaviors.json     - click behavior types + sample payloads
  products.json            - paywall_product shapes
  templates_index.json     - per-template summary (id, name, node count, unique types)
"""
import json, os, re
from pathlib import Path
from collections import Counter, defaultdict

ROOT = Path(__file__).resolve().parents[1]
TPL_DIR = ROOT / "data" / "templates"
OUT_DIR = ROOT / "data" / "catalog"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def value_shape(v, depth=0):
    """Produce a shape signature for a value."""
    if depth > 6:
        return "<deep>"
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "bool"
    if isinstance(v, (int, float)):
        return "number"
    if isinstance(v, str):
        return "string"
    if isinstance(v, list):
        if not v:
            return "[]"
        return f"[{value_shape(v[0], depth+1)}]"
    if isinstance(v, dict):
        t = v.get("type")
        if t == "literal" and "value" in v:
            inner = v["value"]
            if isinstance(inner, dict) and "type" in inner:
                return f"literal<{inner.get('type')}>"
            return f"literal<{value_shape(inner, depth+1)}>"
        if t == "conditional":
            return "conditional"
        if t == "referential":
            return f"ref<{v.get('stateId','?')}>"
        if t == "tombstone":
            return "tombstone"
        if t is not None:
            return f"<{t}>"
        keys = sorted(v.keys())
        if len(keys) > 6:
            return f"{{{','.join(keys[:6])},...}}"
        return f"{{{','.join(keys)}}}"
    return type(v).__name__


def walk_conditionals(obj, path=""):
    """Yield (field, operator, valueType) for every conditional rule."""
    if isinstance(obj, dict):
        if obj.get("type") == "conditional":
            for opt in obj.get("options", []):
                q = opt.get("query", {})
                for rule in q.get("rules", []):
                    if isinstance(rule, dict):
                        yield (
                            rule.get("field", "?"),
                            rule.get("operator", "?"),
                            (rule.get("value") or {}).get("type", "?"),
                        )
        for k, v in obj.items():
            yield from walk_conditionals(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk_conditionals(v, f"{path}[{i}]")


def walk_state_refs(obj):
    """Yield state:* identifier strings appearing anywhere."""
    if isinstance(obj, dict):
        if obj.get("type") == "referential" and "stateId" in obj:
            yield obj["stateId"]
        for v in obj.values():
            yield from walk_state_refs(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from walk_state_refs(v)


def main():
    templates = sorted(TPL_DIR.glob("*.json"))
    print(f"analyzing {len(templates)} templates")

    node_types = Counter()
    node_names = Counter()
    # prop_key -> { shape_str -> sample_locations[:5] }
    property_shapes = defaultdict(lambda: defaultdict(list))
    state_refs = Counter()
    state_defs = {}  # state_id -> {defaultValue shape, sample}
    condition_fields = Counter()
    condition_operators = Counter()
    condition_pairs = Counter()
    notification_types = set()
    notification_sample = None
    style_groups = {}
    click_behavior_types = Counter()
    click_behavior_sample = {}
    product_shapes = Counter()
    templates_index = []

    for f in templates:
        rec = json.loads(f.read_text())
        meta = rec["meta"]
        snap_wrap = rec["snapshot"]
        snap = snap_wrap.get("snapshot", {})
        store = snap.get("store", {})
        if not store:
            continue

        t_node_types = Counter()
        t_unique_names = set()

        for node_id, node in store.items():
            if not isinstance(node, dict):
                continue
            tn = node.get("typeName")
            nt = node.get("type")
            if nt:
                node_types[nt] += 1
                t_node_types[nt] += 1
            if node.get("name"):
                node_names[node["name"]] += 1
                t_unique_names.add(node["name"])

            # properties + defaultProperties
            for src in ("properties", "defaultProperties"):
                props = node.get(src) or {}
                if not isinstance(props, dict):
                    continue
                for pk, pv in props.items():
                    shape = value_shape(pv)
                    slot = property_shapes[pk][shape]
                    if len(slot) < 3:
                        slot.append(f"{meta['name']}#{node_id[:12]}")

            # click behaviors
            cb = node.get("clickBehavior")
            if isinstance(cb, dict):
                t = cb.get("type", "?")
                click_behavior_types[t] += 1
                if t not in click_behavior_sample and t != "do-nothing":
                    click_behavior_sample[t] = cb

            # products
            if tn == "paywall_product":
                product_shapes[tuple(sorted(node.keys()))] += 1

            # notifications
            if tn == "paywall_notification":
                notification_types.add(node.get("id"))
                if notification_sample is None:
                    notification_sample = node

            # states
            if tn == "state":
                sid = node.get("id")
                if sid and sid not in state_defs:
                    state_defs[sid] = {
                        "defaultValue_shape": value_shape(node.get("defaultValue")),
                        "derivation": node.get("derivation"),
                    }

            # style groups
            if tn == "style_variable_group":
                style_groups[node.get("id")] = {
                    k: v for k, v in node.items() if k not in ("typeName",)
                }

        # state references (per template, dedupe)
        for sid in set(walk_state_refs(store)):
            state_refs[sid] += 1

        # conditionals
        for field, op, vtype in walk_conditionals(store):
            condition_fields[field] += 1
            condition_operators[op] += 1
            condition_pairs[(field, op, vtype)] += 1

        templates_index.append({
            "id": meta["id"],
            "name": meta["name"],
            "nodeCount": len(store),
            "nodeTypes": dict(t_node_types),
            "uniqueNamesCount": len(t_unique_names),
            "previews": meta.get("previews"),
        })

    # --- Write outputs ---
    def dump(name, data):
        (OUT_DIR / name).write_text(json.dumps(data, indent=2, default=str))
        print(f"  {name}: {len(json.dumps(data))//1024}KB")

    dump("node_types.json", dict(node_types.most_common()))
    dump("node_names.json", {
        "total": len(node_names),
        "top": dict(node_names.most_common(200)),
    })
    # properties: convert defaultdict
    prop_out = {}
    for pk, shapes in property_shapes.items():
        prop_out[pk] = {s: exs for s, exs in shapes.items()}
    dump("properties.json", prop_out)
    dump("state_ids.json", {
        "referenced": dict(state_refs.most_common()),
        "definitions": state_defs,
    })
    dump("conditional_fields.json", {
        "fields": dict(condition_fields.most_common()),
        "operators": dict(condition_operators.most_common()),
        "combos": [
            {"field": f, "op": op, "valueType": vt, "count": c}
            for (f, op, vt), c in condition_pairs.most_common(200)
        ],
    })
    dump("notifications.json", {
        "types": sorted(notification_types),
        "sample": notification_sample,
    })
    dump("style_tokens.json", style_groups)
    dump("click_behaviors.json", {
        "types": dict(click_behavior_types.most_common()),
        "samples": click_behavior_sample,
    })
    dump("products.json", {str(k): v for k, v in product_shapes.items()})
    dump("templates_index.json", templates_index)

    # Summary
    print(f"\n=== SUMMARY ===")
    print(f"templates analyzed: {len(templates_index)}")
    print(f"unique node types: {len(node_types)}")
    print(f"unique property keys: {len(property_shapes)}")
    print(f"unique state refs: {len(state_refs)}")
    print(f"unique conditional fields: {len(condition_fields)}")
    print(f"conditional operators: {sorted(condition_operators)}")
    print(f"click behavior types: {sorted(click_behavior_types)}")
    print(f"notification types: {sorted(notification_types)}")


if __name__ == "__main__":
    main()
