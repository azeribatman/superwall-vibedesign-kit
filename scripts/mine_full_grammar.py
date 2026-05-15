#!/usr/bin/env python3
"""Deep grammar miner. Extracts everything needed to author paywalls fluently:
inner type tags, sample values, units, enums, click behaviors, fonts, icons,
colors, layout recipes, conditional patterns.

Outputs to data/grammar/ + auto-generates docs/REFERENCE.md.
"""
import json, re
from pathlib import Path
from collections import defaultdict, Counter

ROOT = Path(__file__).resolve().parents[1]
TPL_DIR = ROOT / "data" / "templates"
OUT_DIR = ROOT / "data" / "grammar"
DOC_DIR = ROOT / "docs"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def load_store(path):
    d = json.loads(path.read_text())
    snap = d["snapshot"]
    inner = snap.get("snapshot", snap)
    return inner.get("store", {}), d.get("meta", {})


def stable_sample(samples, v, cap=5):
    s = json.dumps(v, sort_keys=True)
    if len(samples) < cap and s not in {json.dumps(x, sort_keys=True) for x in samples}:
        samples.append(v)


def inner_type(val):
    """Return the inner ``type`` tag of a literal value, or a synthetic tag."""
    if not isinstance(val, dict):
        return f"raw:{type(val).__name__}"
    t = val.get("type")
    if t == "literal":
        v = val.get("value")
        if isinstance(v, dict):
            return v.get("type", "literal:dict")
        return f"literal:{type(v).__name__}"
    if t == "conditional":
        return "conditional"
    if t == "referential":
        return "referential"
    if t == "tombstone":
        return "tombstone"
    return t or "unknown"


def main():
    # --- Per (node_type, property) catalog -----------------------------------
    prop_catalog = defaultdict(lambda: defaultdict(lambda: {
        "count": 0,
        "inner_types": Counter(),
        "samples": [],          # list of sample raw values
        "units": Counter(),     # for css-length etc
        "enum_values": Counter(),
        "references_states": Counter(),
        "in_conditional": 0,
    }))
    node_count = Counter()

    # --- Independent catalogs ------------------------------------------------
    fonts = defaultdict(lambda: {"weights": Counter(), "kinds": Counter(), "count": 0, "url_sample": None})
    icons = Counter()
    images_count = 0
    image_hosts = Counter()
    colors = Counter()         # hex/rgba literals
    color_tokens = Counter()   # state:style.interface.* refs
    click_behaviors = []       # list of shapes
    click_behavior_kinds = Counter()
    units_global = Counter()
    interface_tokens = Counter()
    state_value_kinds = defaultdict(Counter)
    state_operators = defaultdict(Counter)
    conditional_operators = Counter()
    layout_recipes = Counter() # frozenset of (prop, summarized-value) for stacks

    files = sorted(TPL_DIR.glob("*.json"))
    print(f"deep-mining {len(files)} templates...")

    def record_value(ntype, prop, val, conditional_path=False):
        slot = prop_catalog[ntype][prop]
        slot["count"] += 1
        kind = inner_type(val)
        slot["inner_types"][kind] += 1
        if conditional_path:
            slot["in_conditional"] += 1

        if isinstance(val, dict):
            t = val.get("type")
            if t == "literal":
                v = val.get("value")
                stable_sample(slot["samples"], v)
                if isinstance(v, dict):
                    inner = v.get("type")
                    # css-length / css-percentage / css-number — units
                    if "unit" in v:
                        slot["units"][v.get("unit")] += 1
                        units_global[v.get("unit")] += 1
                    # enum-ish small string fields
                    for ek in ("alignment", "alignItems", "justifyContent", "flexDirection",
                               "fit", "objectFit", "wrap", "kind", "style", "variant",
                               "weight", "decoration", "transform", "borderStyle"):
                        if ek in v and isinstance(v[ek], (str, int)):
                            slot["enum_values"][f"{ek}={v[ek]}"] += 1
                    # css-font
                    if inner == "css-font":
                        name = v.get("value")
                        if name:
                            f = fonts[name]
                            f["count"] += 1
                            if v.get("variant"): f["weights"][str(v["variant"])] += 1
                            if v.get("kind"): f["kinds"][v["kind"]] += 1
                            if not f["url_sample"] and v.get("url"):
                                f["url_sample"] = v["url"]
                    # property-icon
                    if inner == "property-icon" and v.get("name"):
                        icons[v["name"]] += 1
                    # property-image
                    if inner == "property-image" and v.get("src"):
                        nonlocal_image_count.append(1)
                        try:
                            host = re.match(r"https?://([^/]+)/", v["src"])
                            if host:
                                image_hosts[host.group(1)] += 1
                        except Exception:
                            pass
                    # css-color
                    if inner == "css-color":
                        cv = v.get("value")
                        if isinstance(cv, str):
                            colors[cv[:32]] += 1
                else:
                    # primitive literal
                    if isinstance(v, str) and len(v) < 40:
                        slot["enum_values"][f"value={v}"] += 1
            elif t == "conditional":
                for opt in val.get("options", []):
                    # Real shape: opt = {query: {combinator, rules: [{field, operator, value, ...}]}, value: ...}
                    query = opt.get("query") or {}
                    for rule in query.get("rules", []) or []:
                        op = rule.get("operator")
                        field = rule.get("field")
                        if op:
                            conditional_operators[op] += 1
                            if field:
                                state_operators[field][op] += 1
                    inner_v = opt.get("value")
                    if inner_v is not None:
                        record_value(ntype, prop, inner_v, conditional_path=True)
            elif t == "referential":
                sid = val.get("stateId")
                if sid:
                    slot["references_states"][sid] += 1
                    if sid.startswith("state:style.interface."):
                        color_tokens[sid] += 1

    nonlocal_image_count = []  # poor-man's nonlocal counter

    for f in files:
        try:
            store, meta = load_store(f)
        except Exception as e:
            print(f"skip {f.name}: {e}")
            continue

        for rid, rec in store.items():
            tn = rec.get("typeName")
            if tn == "node":
                ntype = rec.get("type", "?")
                node_count[ntype] += 1

                for prop, val in (rec.get("properties") or {}).items():
                    record_value(ntype, prop, val)
                # Real click actions live in prop:click-behavior -> clickActions
                def harvest_click(v):
                    if not isinstance(v, dict): return
                    if v.get("type") == "literal":
                        inner = v.get("value")
                        if isinstance(inner, dict) and inner.get("type") == "property-click-behavior":
                            for ca in inner.get("clickActions", []) or []:
                                act = (ca or {}).get("action") or {}
                                kind = act.get("type", "?")
                                click_behavior_kinds[kind] += 1
                                if len(click_behaviors) < 80:
                                    click_behaviors.append({"node_type": ntype, "action": act, "wrapper": ca.get("type")})
                    elif v.get("type") == "conditional":
                        for opt in v.get("options", []):
                            harvest_click(opt.get("value"))
                cbprop = (rec.get("properties") or {}).get("prop:click-behavior")
                if cbprop:
                    harvest_click(cbprop)

                # layout recipes: only summarize stacks
                if ntype == "stack":
                    recipe = []
                    for prop in ("css:flexDirection", "css:alignItems", "css:justifyContent",
                                 "css:gap", "css:padding", "css:width", "css:height"):
                        v = (rec.get("properties") or {}).get(prop)
                        if isinstance(v, dict) and v.get("type") == "literal":
                            inner = v.get("value")
                            if isinstance(inner, dict):
                                if "value" in inner and "unit" in inner:
                                    summary = f"{inner['value']}{inner['unit']}"
                                elif "value" in inner:
                                    summary = str(inner["value"])
                                else:
                                    summary = inner.get("type", "?")
                                recipe.append((prop, summary))
                    if recipe:
                        layout_recipes[tuple(sorted(recipe))] += 1

            elif tn == "state":
                sid = rec.get("id", rid)
                if isinstance(sid, str):
                    if sid.startswith("state:style.interface."):
                        interface_tokens[sid] += 1
                    default = rec.get("default") or rec.get("value")
                    if default is not None:
                        state_value_kinds[sid][inner_type(default if isinstance(default, dict) else {"type":"literal","value":default})] += 1

    # --- Serialize -----------------------------------------------------------
    def slot_out(slot):
        return {
            "count": slot["count"],
            "in_conditional": slot["in_conditional"],
            "inner_types": dict(slot["inner_types"].most_common()),
            "units": dict(slot["units"].most_common()),
            "enum_values": dict(slot["enum_values"].most_common(20)),
            "references_states": dict(slot["references_states"].most_common(20)),
            "samples": slot["samples"],
        }

    catalog_out = {}
    for ntype, props in prop_catalog.items():
        catalog_out[ntype] = {
            "node_count": node_count[ntype],
            "properties": {p: slot_out(s) for p, s in sorted(props.items(), key=lambda kv: -kv[1]["count"])},
        }
    (OUT_DIR / "property_catalog.json").write_text(json.dumps(catalog_out, indent=2, sort_keys=True))

    (OUT_DIR / "fonts.json").write_text(json.dumps({
        name: {"count": f["count"], "weights": dict(f["weights"]), "kinds": dict(f["kinds"]),
               "url_sample": f["url_sample"]}
        for name, f in sorted(fonts.items(), key=lambda kv: -kv[1]["count"])
    }, indent=2))

    (OUT_DIR / "icons.json").write_text(json.dumps(dict(icons.most_common()), indent=2))
    (OUT_DIR / "colors.json").write_text(json.dumps({
        "literal_hex_or_rgba": dict(colors.most_common(200)),
        "token_references": dict(color_tokens.most_common()),
    }, indent=2))
    (OUT_DIR / "click_behaviors.json").write_text(json.dumps({
        "kinds": dict(click_behavior_kinds.most_common()),
        "examples": click_behaviors[:30],
    }, indent=2))
    (OUT_DIR / "units.json").write_text(json.dumps(dict(units_global.most_common()), indent=2))
    (OUT_DIR / "interface_tokens.json").write_text(json.dumps(dict(interface_tokens.most_common()), indent=2))
    (OUT_DIR / "conditional_operators.json").write_text(json.dumps(dict(conditional_operators.most_common()), indent=2))
    (OUT_DIR / "image_hosts.json").write_text(json.dumps(dict(image_hosts.most_common()), indent=2))

    layout_recipes_out = []
    for recipe, n in layout_recipes.most_common(40):
        layout_recipes_out.append({"count": n, "props": dict(recipe)})
    (OUT_DIR / "layout_recipes.json").write_text(json.dumps(layout_recipes_out, indent=2))

    # --- Generate docs/REFERENCE.md -----------------------------------------
    md = []
    md.append("# Superwall Paywall Reference (auto-generated)\n")
    md.append(f"Mined from {len(files)} templates. Source: `data/grammar/*.json`.\n")
    md.append("This is the complete grammar of what's authorable. If a property, value, "
              "icon, font, click behavior, or state is not listed here, it has not been "
              "seen in any real Superwall template — assume it is invalid until verified.\n")

    # Node types
    md.append("\n## Node types\n")
    md.append("| type | instances | templates |\n|---|---|---|")
    for nt, n in node_count.most_common():
        # count templates from catalog (approx via catalog presence); easier: re-scan node_count not enough
        md.append(f"| `{nt}` | {n} | — |")

    # Composition cheat sheet
    md.append("\n## Layout system\n")
    md.append("Everything visual is a `stack` (a flexbox container) or sits inside one. "
              "`stack` composes via:\n")
    md.append("- `css:flexDirection` — column/row")
    md.append("- `css:alignItems`, `css:justifyContent` — cross/main axis alignment")
    md.append("- `css:gap` — child spacing (css-length)")
    md.append("- `css:padding` — inner padding (css-length, often per-side via object)")
    md.append("- `css:width`, `css:height` — sizing (css-length, css-percentage, or `auto`)")
    md.append("\nAll lengths use the `css-length` value type — see the **Value types** section.\n")

    # Layout recipes — most common stack configs
    md.append("\n### Common stack recipes (top patterns)\n")
    for r in layout_recipes_out[:15]:
        md.append(f"- ×{r['count']} — " + ", ".join(f"`{k}={v}`" for k, v in r["props"].items()))

    # Per-node property reference
    md.append("\n## Properties by node type\n")
    for ntype in sorted(catalog_out, key=lambda k: -catalog_out[k]["node_count"]):
        info = catalog_out[ntype]
        md.append(f"\n### `{ntype}` ({info['node_count']} instances)\n")
        md.append("| property | %set | inner types | enums | example |\n|---|---|---|---|---|")
        for prop, s in info["properties"].items():
            pct = round(100 * s["count"] / info["node_count"], 1) if info["node_count"] else 0
            inner = ", ".join(f"`{k}`" for k in list(s["inner_types"])[:3])
            enums = ", ".join(f"`{k}`" for k in list(s["enum_values"])[:3]) or "—"
            ex = ""
            if s["samples"]:
                raw = json.dumps(s["samples"][0])
                ex = "`" + (raw[:60] + ("…" if len(raw) > 60 else "")) + "`"
            md.append(f"| `{prop}` | {pct}% | {inner} | {enums} | {ex} |")

    # Click behaviors
    md.append("\n## Click behaviors\n")
    md.append("All values seen on `clickBehavior` (top-level node field, not under `properties`):\n")
    md.append("| kind | count |\n|---|---|")
    for k, n in click_behavior_kinds.most_common():
        md.append(f"| `{k}` | {n} |")
    md.append("\nExamples:\n")
    for ex in click_behaviors[:8]:
        md.append(f"- on `{ex['node_type']}`: `{json.dumps(ex.get('action', ex))[:160]}`")

    # Fonts
    md.append("\n## Fonts\n")
    md.append("| family | count | weights | kind |\n|---|---|---|---|")
    for name, f in sorted(fonts.items(), key=lambda kv: -kv[1]["count"])[:25]:
        ws = ",".join(sorted(f["weights"]))
        ks = ",".join(f["kinds"])
        md.append(f"| {name} | {f['count']} | {ws} | {ks} |")

    # Icons (top 60)
    md.append("\n## Icons (top 60)\n")
    md.append("Icon names usable in `prop:icon` / `name`:\n")
    md.append(", ".join(f"`{n}`" for n, _ in icons.most_common(60)))

    # Theme tokens
    md.append("\n## Interface tokens (theme)\n")
    md.append("Reference these via `{type: referential, stateId: <token>}` in any color/style prop:\n")
    md.append("| token | templates_using |\n|---|---|")
    for t, n in interface_tokens.most_common():
        md.append(f"| `{t}` | {n} |")

    # Conditionals
    md.append("\n## Conditional operators seen\n")
    md.append("Conditional values use `{type: conditional, options: [{condition: {stateId, operator, value}, value: ...}, ...]}`.\n")
    md.append("Operators in use:\n")
    for op, n in conditional_operators.most_common():
        md.append(f"- `{op}` ({n}×)")

    # Units
    md.append("\n## Units\n")
    for u, n in units_global.most_common():
        md.append(f"- `{u}` ({n}×)")

    # Image hosts
    md.append("\n## Image hosts seen\n")
    for h, n in image_hosts.most_common(10):
        md.append(f"- `{h}` ({n}×)")

    md.append("\n---\nRegenerate with `python3 scripts/mine_full_grammar.py`.\n")
    (DOC_DIR / "REFERENCE.md").write_text("\n".join(md))

    print(f"\nwrote {len(list(OUT_DIR.glob('*.json')))} grammar files")
    print(f"wrote docs/REFERENCE.md ({len(''.join(md))//1024} KB)")
    print(f"  node types: {len(node_count)}")
    print(f"  unique properties: {sum(len(c['properties']) for c in catalog_out.values())}")
    print(f"  fonts: {len(fonts)}, icons: {len(icons)}, click behaviors: {len(click_behavior_kinds)}")
    print(f"  conditional ops: {len(conditional_operators)}, interface tokens: {len(interface_tokens)}")


if __name__ == "__main__":
    main()
