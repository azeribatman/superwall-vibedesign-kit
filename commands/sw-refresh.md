---
description: Refresh the local Superwall grammar/fragments by pulling latest templates and re-mining
argument-hint: (none)
allowed-tools: [Bash]
---

# /sw-refresh — Refresh local grammar from Superwall

Run after Superwall releases new templates so the grammar reflects them.

```bash
python3 scripts/pull_templates.py        # pulls new template ids only
python3 scripts/mine_full_grammar.py     # rewrites data/grammar/*.json + docs/REFERENCE.md
python3 scripts/mine_fragments.py        # rewrites data/fragments/
```

Then tell the user how many new templates and any new fonts/icons/click
actions appeared.
