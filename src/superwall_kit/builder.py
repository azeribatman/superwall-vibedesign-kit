"""High-level snapshot builder. Designed so the agent (or the user) can write
SwiftUI-style code that emits a valid Superwall snapshot.

Two starting strategies:
  1. PaywallBuilder.from_template(path)   — clone a known-good template, mutate.
  2. PaywallBuilder.from_donor(template_id) — load from data/templates/<id>.json.

After construction, common mutations:
  .set_name(str)
  .set_text(needle, replacement)        — bulk replace text across the snapshot
  .set_theme(token, hex_or_dict)        — override an interface token
  .set_product(slot, identifier)        — replace a paywall_product identifier
  .set_image(node_name_or_id, url)      — replace a property-image src
  .remove_node(name_or_id)              — drop a node (and its subtree)
  .snapshot()                           — return the (mutated) inner snapshot dict
  .validate()                           — return issues list

The builder *never* invents records from thin air. Composition is always
template-derived. This sidesteps the "from-scratch 400" problem.
"""
import copy, json
from pathlib import Path
from .grammar import Grammar
from .validate import validate_snapshot

ROOT = Path(__file__).resolve().parents[2]
TPL_DIR = ROOT / "data" / "templates"


class PaywallBuilder:
    def __init__(self, snapshot):
        self._snapshot = snapshot
        self._grammar = Grammar.load()

    # ----- Construction ----------------------------------------------------
    @classmethod
    def from_template(cls, path):
        d = json.loads(Path(path).read_text())
        snap = d.get("snapshot", d)
        # `data/templates/*.json` wraps as {meta, snapshot: {snapshot: {...}, version, ...}}
        # the actual mutable snapshot is the inner one
        return cls(copy.deepcopy(snap))

    @classmethod
    def from_donor(cls, template_id):
        return cls.from_template(TPL_DIR / f"{template_id}.json")

    # ----- Internals -------------------------------------------------------
    def _store(self):
        inner = self._snapshot.get("snapshot", self._snapshot)
        return inner.setdefault("store", {})

    def _records(self, type_name):
        return [r for r in self._store().values() if r.get("typeName") == type_name]

    def _node_by(self, name_or_id):
        for r in self._store().values():
            if r.get("typeName") != "node": continue
            if r.get("id") == name_or_id or r.get("name") == name_or_id:
                return r
        return None

    # ----- Mutations -------------------------------------------------------
    def set_name(self, name):
        for p in self._records("paywall"):
            p["name"] = name
        return self

    def set_identifier(self, ident):
        for p in self._records("paywall"):
            p["identifier"] = ident
        return self

    def set_text(self, needle, replacement):
        """Replace literal text across all `prop:text` (and any 'value' string) recursively."""
        def walk(o):
            if isinstance(o, dict):
                for k, v in list(o.items()):
                    if isinstance(v, str) and needle in v:
                        o[k] = v.replace(needle, replacement)
                    else:
                        walk(v)
            elif isinstance(o, list):
                for v in o:
                    walk(v)
        walk(self._store())
        return self

    def set_theme(self, token, value, mode="light"):
        """Override an interface token's default color. `value` is a hex string or css-color dict.
        `token` may be the bare token (e.g. 'state:style.interface.primary') or include the
        '.light'/'.dark' suffix; bare tokens get the `mode` suffix appended.
        """
        if isinstance(value, str):
            value = {"type": "css-color", "value": value}
        target = token if token.endswith((".light", ".dark")) else f"{token}.{mode}"
        store = self._store()
        for rid, rec in store.items():
            sid = rec.get("id", rid)
            if rec.get("typeName") == "state" and sid == target:
                rec["defaultValue"] = value
                # legacy field name
                if "default" in rec:
                    rec["default"] = value
                return self
        raise KeyError(f"interface token '{target}' not present in this snapshot")

    def set_product(self, slot_key, identifier):
        """Set a paywall_product identifier by slot key (e.g. 'annual')."""
        target = f"paywall_product:{slot_key}"
        for rid, rec in self._store().items():
            if rec.get("typeName") == "paywall_product" and (rec.get("id") == target or rid == target or rec.get("key") == slot_key):
                rec["identifier"] = identifier
                return self
        raise KeyError(f"paywall_product '{slot_key}' not found")

    def set_image(self, name_or_id, url):
        """Replace src of any property-image inside the named node's properties."""
        node = self._node_by(name_or_id)
        if not node:
            raise KeyError(f"node '{name_or_id}' not found")
        def walk(o):
            if isinstance(o, dict):
                if o.get("type") == "property-image":
                    o["src"] = url
                for v in o.values():
                    walk(v)
            elif isinstance(o, list):
                for v in o:
                    walk(v)
        walk(node.get("properties") or {})
        return self

    def remove_node(self, name_or_id):
        node = self._node_by(name_or_id)
        if not node:
            return self
        target_id = node.get("id")
        # collect subtree
        store = self._store()
        nodes_by_id = {r.get("id", rid): (rid, r) for rid, r in store.items() if r.get("typeName") == "node"}
        children_of = {}
        for nid, (rid, n) in nodes_by_id.items():
            children_of.setdefault(n.get("parentId"), []).append(nid)
        to_remove = [target_id]
        stack = [target_id]
        while stack:
            cur = stack.pop()
            for c in children_of.get(cur, []):
                to_remove.append(c)
                stack.append(c)
        for nid in to_remove:
            rid, _ = nodes_by_id.get(nid, (None, None))
            if rid and rid in store:
                del store[rid]
        return self

    # ----- Output ----------------------------------------------------------
    def snapshot(self):
        # superwall_kit.client.push_snapshot expects the full envelope (with version, store, schema)
        return self._snapshot.get("snapshot", self._snapshot)

    def envelope(self):
        return self._snapshot

    def validate(self):
        return validate_snapshot(self._snapshot, grammar=self._grammar)


__all__ = ["PaywallBuilder"]
