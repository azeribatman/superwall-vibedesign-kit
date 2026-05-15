"""From-scratch snapshot generator. Every visual node is generated from
primitives — no design is cloned. Protocol scaffolding (paywall record,
document, page, device states, style_variable_groups) is loaded from a
reference template since those are renderer-protocol, not design.

Usage:
    from superwall_kit.scratch import Scratch, length, color, font, text_value
    s = Scratch(name="Test", identifier="test_paywall")
    s.theme(background="#000000", text="#ffffff", primary="#3b82f6", ctaText="#0b1220",
            ctaBg="#a8c3e6", border="#222222", borderSelected="#3b82f6", cardBg="#0a0a0a")
    s.product("primary", "com.example.weekly")
    s.product("secondary", "com.example.monthly")
    root = s.root_stack(axis="y", crossAxis="center", main="start", padding="24px",
                        gap="20px", bg=ref_token("background"))
    pill = s.pill(parent=root, text="Premium", color=ref_token("primary"),
                  borderColor=ref_token("primary"))
    title = s.text(parent=root, content="Get the full picture with Premium",
                   size=32, weight="700", color=ref_token("text"), align="center")
    ...
    snap = s.build()
"""
import json, secrets, copy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REF_TEMPLATE = ROOT / "data" / "templates" / "25513.json"


# ----- value wrappers --------------------------------------------------------

def lit(value):
    return {"type": "literal", "value": value}

def length(v, unit="px"):
    return lit({"type": "css-length", "value": str(v), "unit": unit})

def color(hex_str):
    return lit({"type": "css-color", "value": hex_str})

def text_value(s):
    return lit({"type": "property-text", "value": s, "rendering": {"type": "literal"}})


def text_liquid(s, required_state_ids=None):
    """A text value rendered through Liquid templating, e.g. '{{ products.primary.price }}/yr'."""
    return lit({
        "type": "property-text", "value": s,
        "rendering": {"type": "liquid", "requiredStateIds": required_state_ids or []},
    })

def font(family="Inter", weight="400"):
    weight_to_url = {
        "400": "https://fonts.gstatic.com/s/inter/v13/UcCO3FwrK3iLTeHuS_fvQtMwCp50KnMa1ZL7.woff2",
        "500": "https://fonts.gstatic.com/s/inter/v13/UcCO3FwrK3iLTeHuS_fvQtMwCp50KnMa1pL7.woff2",
        "600": "https://fonts.gstatic.com/s/inter/v13/UcCO3FwrK3iLTeHuS_fvQtMwCp50KnMa05L7.woff2",
        "700": "https://fonts.gstatic.com/s/inter/v13/UcCO3FwrK3iLTeHuS_fvQtMwCp50KnMa0ZL7.woff2",
    }
    return lit({
        "type": "css-font", "value": family, "style": "normal",
        "variant": str(weight), "weight": str(weight), "kind": "google",
        "url": weight_to_url.get(str(weight), weight_to_url["400"]),
    })

def ref_token(token_name):
    """Reference a theme token like 'primary', 'text', 'background'."""
    return {"type": "referential", "stateId": f"state:style.interface.{token_name}"}

def icon_value(name, color_hex="currentColor", size=24):
    return lit({
        "type": "property-icon", "name": name,
        "strokeLinecap": "round", "strokeLinejoin": "round",
        "strokeColor": color_hex, "strokeWidth": 2.5,
        "width": size, "height": size,
    })

def stack_property(*, axis="y", main="start", cross="start", gap="0px",
                   wrap="nowrap", scroll="none", snap="center"):
    return lit({
        "type": "property-stack", "axis": axis, "reverse": False,
        "crossAxisAlignment": cross, "mainAxisDistribution": main,
        "wrap": wrap, "gap": gap, "scroll": scroll, "snapPosition": snap,
    })

def click_behavior(actions):
    """actions is a list of {type: 'purchase'|'restore'|'close'|'open-url'|'set-product-index'|...}."""
    return lit({
        "type": "property-click-behavior",
        "clickActions": [
            {"type": "action-execution", "id": f"action:{secrets.token_hex(3)}", "action": a}
            for a in actions
        ],
        "animation": "none",
    })


# ----- index allocator -------------------------------------------------------

def _idx(i):
    """Generate a fractional-rank index string. Templates use 'a0','a1','a1A',..."""
    base = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if i < len(base):
        return f"a{base[i]}"
    return f"a{base[i // len(base)]}{base[i % len(base)]}"


# ----- main builder ----------------------------------------------------------

class Scratch:
    """Compose a paywall snapshot from primitives.

    Protocol records (device states, style groups) are loaded from a
    reference snapshot. Design records (nodes, theme states, products)
    are generated.
    """

    def __init__(self, *, name="Untitled", identifier="kit_built", reference_path=REF_TEMPLATE):
        # load protocol scaffolding
        ref = json.loads(Path(reference_path).read_text())
        ref_inner = ref["snapshot"]["snapshot"]
        ref_store = ref_inner["store"]

        self.records = {}
        # device states + style_variable_groups + document — copy untouched
        for rid, rec in ref_store.items():
            tn = rec.get("typeName")
            if tn == "state":
                sid = rec.get("id", rid)
                if isinstance(sid, str) and sid.startswith("state:device."):
                    self.records[rid] = copy.deepcopy(rec)
            elif tn == "style_variable_group":
                self.records[rid] = copy.deepcopy(rec)
            elif tn == "document":
                self.records[rid] = copy.deepcopy(rec)

        # paywall + page (regenerated)
        self.records["paywall:paywall"] = {
            "name": name,
            "presentationCondition": "CHECK_USER_SUBSCRIPTION",
            "presentationStyle": "FULLSCREEN",
            "featureGating": "GATED",
            "onDeviceCache": "ENABLED",
            "version": 1,
            "editable": True,
            "identifier": identifier,
            "templateType": "UNLISTED",
            "webCheckoutDestination": "EXTERNAL",
            "id": "paywall:paywall",
            "typeName": "paywall",
            "localizationProvider": {
                "id": "localization_provider:superwall:1:default",
                "projectDisplayName": "Default",
                "internalLocalizationProviderId": 40,
            },
        }
        self.records["page:page"] = {
            "meta": {}, "id": "page:page", "name": "Page 1", "index": "a1",
            "typeName": "page",
        }

        # snapshot envelope — push_snapshot expects this shape (store + schema at top)
        self._envelope = {
            "store": self.records,
            "schema": copy.deepcopy(ref_inner.get("schema", {})),
        }

        self._sibling_idx = {}  # parent_id -> next sibling index counter

    # ----- helpers -----
    def _new_node_id(self):
        return f"node:{secrets.token_urlsafe(16)}"

    def _next_index(self, parent_id):
        i = self._sibling_idx.get(parent_id, 0)
        self._sibling_idx[parent_id] = i + 1
        return _idx(i)

    def _put_node(self, *, parent_id, ntype, name, properties, default_properties=None):
        nid = self._new_node_id()
        # Per-type required `props` scaffolding (server-side schema check)
        props_default = {}
        if ntype == "text":
            props_default = {"text": {"type": "literal", "text": ""}}
        elif ntype == "img":
            props_default = {}
        elif ntype == "icon":
            props_default = {}
        rec = {
            "x": 0, "y": 0, "rotation": 0, "isLocked": False, "opacity": 1,
            "defaultProperties": default_properties or {},
            "properties": properties,
            "meta": {}, "requiredRecordIds": [],
            "clickBehavior": {"type": "do-nothing"},
            "name": name, "type": ntype,
            "index": self._next_index(parent_id),
            "parentId": parent_id, "props": props_default,
            "id": nid, "typeName": "node",
        }
        self.records[nid] = rec
        return nid

    # ----- theme -----
    def theme(self, **tokens):
        """Define interface tokens. Each kwarg is `name=hex_or_dict` (light by default)."""
        for name, val in tokens.items():
            v = val if isinstance(val, dict) else {"type": "css-color", "value": val}
            for mode in ("light", "dark"):
                rid = f"state:style.interface.{name}.{mode}"
                self.records[rid] = {
                    "locked": False, "derivation": None, "id": rid,
                    "defaultValue": v, "typeName": "state",
                }
            # ensure variable group exists for this token
            grp_id = f"style_variable_group:interface.variable.{name}"
            if grp_id not in self.records:
                self.records[grp_id] = {
                    "id": grp_id, "index": _idx(len([k for k in self.records if k.startswith("style_variable_group:interface.variable.")])),
                    "variableType": {"type": "value-type", "value": "css-color"},
                    "typeName": "style_variable_group",
                }
        return self

    # ----- products -----
    def product(self, slot, identifier):
        rid = f"paywall_product:{slot}"
        existing_count = sum(1 for k in self.records if k.startswith("paywall_product:"))
        self.records[rid] = {
            "identifier": identifier, "id": rid, "typeName": "paywall_product",
            "index": _idx(existing_count),
            "productVariables": {"source": "sdk"}, "store": None,
        }
        return self

    # ----- nodes -----
    def root_stack(self, *, axis="y", main="start", cross="start", gap="0px",
                   bg=None, padding=None, name="Main"):
        properties = {
            "prop:stack": stack_property(axis=axis, main=main, cross=cross, gap=gap),
            "css:width": length(100, "vw"),
            "css:height": length(100, "vh"),
        }
        if bg is not None:
            properties["css:backgroundColor"] = bg if isinstance(bg, dict) else color(bg)
        apply_padding(properties, padding)
        return self._put_node(parent_id="page:page", ntype="stack", name=name,
                              properties=properties)

    def stack(self, parent, *, axis="y", main="start", cross="start", gap="0px",
              padding=None, width=None, height=None, bg=None, border_color=None,
              border_width=None, radius=None, name="Stack",
              scroll="none", snap="center", wrap="nowrap"):
        props = {
            "prop:stack": stack_property(axis=axis, main=main, cross=cross, gap=gap,
                                          scroll=scroll, snap=snap, wrap=wrap),
        }
        if width is not None:
            props["css:width"] = _coerce_length(width)
        if height is not None:
            props["css:height"] = _coerce_length(height)
        if bg is not None:
            props["css:backgroundColor"] = bg if isinstance(bg, dict) else color(bg)
        apply_padding(props, padding)
        if border_color is not None:
            props["css:borderColor"] = border_color if (isinstance(border_color, dict) and border_color.get("type") in ("literal","conditional","referential")) else (border_color if isinstance(border_color, dict) else color(border_color))
        if border_width is not None:
            props["css:borderTopWidth;borderRightWidth;borderBottomWidth;borderLeftWidth"] = _coerce_length(border_width)
            # also need style=solid for border to render
            props["css:borderTopStyle;borderRightStyle;borderBottomStyle;borderLeftStyle"] = lit({"type": "css-string", "value": "solid"})
        if radius is not None:
            props["css:borderTopLeftRadius;borderTopRightRadius;borderBottomRightRadius;borderBottomLeftRadius"] = _coerce_length(radius)
        return self._put_node(parent_id=parent, ntype="stack", name=name, properties=props)

    def text_liquid(self, parent, content, required_state_ids=None, **kwargs):
        """Same as .text() but renders Liquid templates like '{{ products.primary.price }}/year'."""
        kwargs["_text_value_override"] = text_liquid(content, required_state_ids)
        return self.text(parent, content, **kwargs)

    def text(self, parent, content, *, size=14, weight="400", color_=None,
             align="start", name=None, line_height=None, _text_value_override=None):
        align_map = {"start": "left", "left": "left", "center": "center", "end": "right", "right": "right"}
        props = {
            "prop:text": _text_value_override or text_value(content),
            "css:font": font("Inter", weight),
            "css:fontSize": length(size),
            "css:textAlign": lit({"type": "css-string", "value": align_map.get(align, align)}),
        }
        if color_ is not None:
            props["css:color"] = color_ if isinstance(color_, dict) else color(color_)
        if line_height is not None:
            if isinstance(line_height, (int, float)):
                props["css:lineHeight"] = length(line_height)
            elif isinstance(line_height, str):
                props["css:lineHeight"] = length(*_split_unit(line_height))
            else:
                props["css:lineHeight"] = line_height
        return self._put_node(parent_id=parent, ntype="text", name=name or content[:20],
                              properties=props)

    def icon(self, parent, name_str, *, color_=None, size=24, node_name=None):
        # Icons render via stroke=currentColor and inherit css:color, so set the token there.
        props = {
            "prop:icon": icon_value(name_str, "currentColor", size),
            "css:width": length(size),
            "css:height": length(size),
        }
        if color_ is not None:
            props["css:color"] = color_ if isinstance(color_, dict) else color(color_)
        return self._put_node(parent_id=parent, ntype="icon", name=node_name or f"icon:{name_str}",
                              properties=props)

    def image_box(self, parent, url, *, width, height, fit="cover",
                  radius=0, h_pos="center", v_pos="center", name="Image"):
        """Create a fixed-size stack and fill it with an image.

        This is the right primitive for "user pasted a screenshot with an image":
        the layout is locked by the box's width+height, and the image just fills
        whatever is set, so source dimensions never warp the surrounding layout.

        fit:    "cover" (aspect fill) or "contain" (aspect fit)
        radius: corner radius in px
        url:    final user-content URL (from c.generate_and_upload_image or pre-uploaded)
        """
        bg_image = lit({
            "type": "css-background-image",
            "functions": [{
                "type": "image", "url": url,
                "size": fit,
                "horizontalPosition": h_pos,
                "verticalPosition": v_pos,
            }],
        })
        props = {
            "prop:stack": stack_property(axis="y", main="center", cross="center"),
            "css:width": _coerce_length(width),
            "css:height": _coerce_length(height),
            "css:backgroundImage": bg_image,
        }
        if radius:
            props["css:borderTopLeftRadius;borderTopRightRadius;borderBottomRightRadius;borderBottomLeftRadius"] = _coerce_length(radius)
        return self._put_node(parent_id=parent, ntype="stack", name=name, properties=props)

    def img(self, parent, src, *, width=None, height=None, name="Image"):
        props = {
            "prop:image": lit({"type": "property-image", "src": src,
                               "rendering": {"type": "literal"}}),
        }
        if width is not None:
            props["css:width"] = length(width) if isinstance(width, (int, float)) else lit(width)
        if height is not None:
            props["css:height"] = length(height) if isinstance(height, (int, float)) else lit(height)
        return self._put_node(parent_id=parent, ntype="img", name=name, properties=props)

    def set_click(self, node_id, actions):
        """Attach click behavior to an existing node."""
        rec = self.records[node_id]
        rec["properties"]["prop:click-behavior"] = click_behavior(actions)
        return self

    # ----- output -----
    def build(self):
        return self._envelope


def apply_padding(props, spec):
    """Mutate props to apply padding from a spec dict.
    spec keys (any combo): all, x, y, top, right, bottom, left.
    """
    if spec is None: return
    if isinstance(spec, (int, float)):
        spec = {"all": spec}
    if not isinstance(spec, dict): return
    if "all" in spec:
        props["css:paddingTop;paddingBottom"] = _coerce_length(spec["all"])
        props["css:paddingLeft;paddingRight"] = _coerce_length(spec["all"])
    if "x" in spec:
        props["css:paddingLeft;paddingRight"] = _coerce_length(spec["x"])
    if "y" in spec:
        props["css:paddingTop;paddingBottom"] = _coerce_length(spec["y"])
    if "top" in spec:
        props["css:paddingTop"] = _coerce_length(spec["top"])
    if "right" in spec:
        props["css:paddingRight"] = _coerce_length(spec["right"])
    if "bottom" in spec:
        props["css:paddingBottom"] = _coerce_length(spec["bottom"])
    if "left" in spec:
        props["css:paddingLeft"] = _coerce_length(spec["left"])


def _coerce_length(v):
    """Accept int/float/str/dict and return a wrapped css-length literal.
    If `v` is already a wrapped value (has top-level 'type' literal/conditional/referential), pass through."""
    if isinstance(v, (int, float)):
        return length(v)
    if isinstance(v, str):
        return length(*_split_unit(v))
    if isinstance(v, dict):
        # already-wrapped value? leave alone
        if v.get("type") in ("literal", "conditional", "referential", "tombstone"):
            return v
        # raw inner value (e.g. {type: css-length, value, unit})
        return lit(v)
    return v


def _split_unit(s):
    s = str(s)
    for u in ("vw", "vh", "px", "rem", "em", "%"):
        if s.endswith(u):
            return s[:-len(u)], u
    return s, "px"


__all__ = [
    "Scratch", "length", "color", "font", "text_value", "icon_value",
    "stack_property", "click_behavior", "ref_token", "lit",
]
