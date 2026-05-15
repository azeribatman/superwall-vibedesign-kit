"""Grammar loader. Reads data/grammar/*.json into a single object the
validator and builder can query.

Usage:
    from superwall_kit.grammar import Grammar
    g = Grammar.load()
    g.allowed_children("stack")            # set[str]
    g.required_props("text")               # set[str] (props present in >=95% of instances)
    g.is_known_action("purchase")          # bool
    g.is_known_operator("=")               # bool
    g.known_states()                       # set[str]  (state ids seen across templates)
    g.known_interface_tokens()             # set[str]
    g.click_action_kinds()                 # set[str]
"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]
GRAMMAR_DIR = ROOT / "data" / "grammar"


class Grammar:
    def __init__(self, *, composition, properties, states, theme_tokens,
                 click_behaviors, conditional_operators, node_index, fonts, icons):
        self._composition = composition
        self._properties = properties
        self._states = states
        self._theme_tokens = theme_tokens
        self._click_behaviors = click_behaviors
        self._conditional_operators = conditional_operators
        self._node_index = node_index
        self._fonts = fonts
        self._icons = icons

    @classmethod
    def load(cls, grammar_dir=GRAMMAR_DIR):
        def J(name):
            p = Path(grammar_dir) / name
            return json.loads(p.read_text()) if p.exists() else {}
        # composition.json may not exist if only mine_full_grammar ran
        comp = J("composition.json")
        if not comp:
            # derive minimal composition from property_catalog presence
            comp = {}
        return cls(
            composition=comp,
            properties=J("property_catalog.json") or J("properties.json"),
            states=J("states.json"),
            theme_tokens=J("theme_tokens.json") or J("interface_tokens.json"),
            click_behaviors=J("click_behaviors.json"),
            conditional_operators=J("conditional_operators.json"),
            node_index=J("node_index.json"),
            fonts=J("fonts.json"),
            icons=J("icons.json"),
        )

    # ---- Queries ----
    def known_node_types(self):
        return set(self._node_index.keys()) | set(self._properties.keys())

    def allowed_children(self, parent_type):
        return set((self._composition.get(parent_type) or {}).keys())

    def required_props(self, node_type, threshold_pct=95.0):
        info = self._properties.get(node_type) or {}
        props = info.get("properties") or info  # support both new + old shapes
        out = set()
        node_total = info.get("node_count") or info.get("total_nodes") or 1
        for prop, slot in props.items():
            if not isinstance(slot, dict): continue
            count = slot.get("count") or slot.get("present_count") or 0
            pct = (100.0 * count / node_total) if node_total else 0
            # accept either pre-computed pct or computed
            pct = slot.get("present_pct", pct)
            if pct >= threshold_pct:
                out.add(prop)
        return out

    def all_props(self, node_type):
        info = self._properties.get(node_type) or {}
        props = info.get("properties") or info
        return set(props.keys())

    def click_action_kinds(self):
        return set((self._click_behaviors.get("kinds") or {}).keys())

    def known_operators(self):
        return set(self._conditional_operators.keys())

    def known_interface_tokens(self):
        return set(self._theme_tokens.keys() if isinstance(self._theme_tokens, dict) else [])

    def known_states(self):
        return set(self._states.keys())

    def known_icons(self):
        return set(self._icons.keys())

    def known_fonts(self):
        return set(self._fonts.keys())

    # ---- Convenience checks ----
    def is_known_action(self, kind):
        return kind in self.click_action_kinds()

    def is_known_operator(self, op):
        return op in self.known_operators()

    def is_known_node_type(self, t):
        return t in self.known_node_types()


__all__ = ["Grammar"]
