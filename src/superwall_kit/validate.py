"""Pre-push structural validator. Run on a snapshot before pushing to catch
problems Superwall would reject (or silently render broken).

    from superwall_kit.validate import validate_snapshot
    issues = validate_snapshot(snapshot)
    for level, code, msg in issues:
        print(level, code, msg)
"""
from .grammar import Grammar


def _walk_values(obj, on_value):
    """Visit every wrapped value (dict with 'type' literal/conditional/referential)."""
    if isinstance(obj, dict):
        if obj.get("type") in ("literal", "conditional", "referential", "tombstone"):
            on_value(obj)
        for v in obj.values():
            _walk_values(v, on_value)
    elif isinstance(obj, list):
        for v in obj:
            _walk_values(v, on_value)


def validate_snapshot(snapshot, grammar=None):
    """Return a list of (level, code, message) tuples. Empty list = clean."""
    if grammar is None:
        grammar = Grammar.load()

    issues = []
    # Snapshot may be the outer envelope or just the inner store-bearing object
    inner = snapshot.get("snapshot", snapshot)
    store = inner.get("store") or {}

    # Index nodes
    nodes_by_id = {}
    for rid, rec in store.items():
        if rec.get("typeName") == "node":
            nodes_by_id[rec.get("id", rid)] = rec

    known_actions = grammar.click_action_kinds()
    known_ops = grammar.known_operators()
    known_states = grammar.known_states()
    known_tokens = grammar.known_interface_tokens()
    known_node_types = grammar.known_node_types()

    # Collect all state ids defined in this snapshot
    local_states = set()
    valid_parents = set(nodes_by_id.keys())  # nodes can be parents
    for rid, rec in store.items():
        tn = rec.get("typeName")
        if tn == "state":
            sid = rec.get("id", rid)
            if isinstance(sid, str):
                local_states.add(sid)
        elif tn in ("page", "navigation"):
            # pages and navigation containers are valid parentIds for top-level nodes
            valid_parents.add(rec.get("id", rid))
        elif tn == "style_variable_group":
            # theme groups expose interface tokens as states
            for var in (rec.get("variables") or rec.get("states") or []):
                if isinstance(var, dict) and var.get("id"):
                    local_states.add(var["id"])
            for k in (rec.get("interface") or {}):
                local_states.add(f"state:style.interface.{k}")

    # 1. Required top-level records
    has_paywall = any(r.get("typeName") == "paywall" for r in store.values())
    if not has_paywall:
        issues.append(("error", "missing_paywall_record",
                       "snapshot has no paywall record"))
    has_page = any(r.get("typeName") == "page" for r in store.values())
    if not has_page:
        issues.append(("error", "missing_page_record",
                       "snapshot has no page record"))

    # 2. Per-node checks
    for nid, n in nodes_by_id.items():
        ntype = n.get("type")
        if ntype not in known_node_types:
            issues.append(("error", "unknown_node_type",
                           f"node {nid}: unknown type '{ntype}'"))

        # parentId must point to an existing node, page, or navigation record
        pid = n.get("parentId")
        if pid and pid not in valid_parents and pid not in store:
            issues.append(("error", "orphan_parent",
                           f"node {nid}: parentId '{pid}' not in store"))

        # required props
        present = set((n.get("properties") or {}).keys()) | set((n.get("defaultProperties") or {}).keys())
        for req in grammar.required_props(ntype):
            if req not in present:
                issues.append(("warn", "missing_common_prop",
                               f"node {nid} ({ntype}): missing usually-required '{req}'"))

    # 3. Walk all values to validate referential & conditional
    def state_resolves(sid):
        if not isinstance(sid, str): return False
        if sid in local_states or sid in known_states or sid in known_tokens:
            return True
        # interface tokens are referenced without .light/.dark suffix; the actual records have it
        if sid.startswith("state:style.interface."):
            return any((sid + suf) in local_states or (sid + suf) in known_states
                       for suf in (".light", ".dark"))
        return False

    def check_value(v):
        t = v.get("type")
        if t == "referential":
            sid = v.get("stateId")
            if sid and not state_resolves(sid):
                issues.append(("warn", "unknown_state_ref",
                               f"references unknown state '{sid}'"))
        elif t == "conditional":
            for opt in v.get("options", []) or []:
                query = opt.get("query") or {}
                for rule in query.get("rules", []) or []:
                    op = rule.get("operator")
                    if op and op not in known_ops:
                        issues.append(("error", "unknown_operator",
                                       f"conditional uses unknown operator '{op}'"))
                    field = rule.get("field")
                    if field and not state_resolves(field):
                        issues.append(("warn", "conditional_unknown_state",
                                       f"conditional references unknown state '{field}'"))

    _walk_values(store, check_value)

    # 4. Click action kinds
    for nid, n in nodes_by_id.items():
        cb = (n.get("properties") or {}).get("prop:click-behavior")
        if not cb: continue
        def check_actions(v):
            if not isinstance(v, dict): return
            if v.get("type") == "literal":
                inner = v.get("value")
                if isinstance(inner, dict) and inner.get("type") == "property-click-behavior":
                    for ca in inner.get("clickActions", []) or []:
                        a = (ca or {}).get("action") or {}
                        kind = a.get("type")
                        if kind and kind not in known_actions:
                            issues.append(("error", "unknown_click_action",
                                           f"node {nid}: unknown click action '{kind}'"))
            elif v.get("type") == "conditional":
                for opt in v.get("options", []) or []:
                    check_actions(opt.get("value"))
        check_actions(cb)

    return issues


def summarize(issues):
    if not issues:
        return "OK — no structural issues."
    by_level = {"error": [], "warn": []}
    for lvl, code, msg in issues:
        by_level.setdefault(lvl, []).append((code, msg))
    out = []
    for lvl in ("error", "warn"):
        items = by_level.get(lvl, [])
        if not items: continue
        out.append(f"{lvl.upper()}: {len(items)}")
        for code, msg in items[:30]:
            out.append(f"  [{code}] {msg}")
        if len(items) > 30:
            out.append(f"  ... and {len(items)-30} more")
    return "\n".join(out)


__all__ = ["validate_snapshot", "summarize"]
