Operation ID Assigner
=====================

Convert Chinese surgical operation combinations into standardized, comma-separated
ID signatures used by procedure templates. **This skill is for personal use.**

What this does
--------------
- Map each operation name to its numeric ID from the reference data
- Expand alternatives separated by `/`
- Apply multi-ID rules for special operations
- Generate all valid signature combinations

When to use
-----------
Use this skill when you need to:
- Normalize mixed surgical operation names into IDs
- Produce canonical signatures for billing or template systems
- Generate all combinations for alternative procedures

Inputs
------
- A single operation combination string
- Operations are separated by `+`
- Alternatives are separated by `/` (e.g., `A/B/C` means three options)

Reference data
--------------
- `reference/operation-ids.csv` (columns: `id`, `name_zh`)
- `reference/Supplement-information.md` (special multi-ID rules)

Matching rules
--------------
- Prefer exact matches against the reference list
- Use fuzzy matching only when exact match fails
- Flag any uncertain match for confirmation
- Apply context-specific rules (see supplement)

Output
------
Default output is a list of signatures:
```
33,14,9
33,14,132
```

CSV output (optional for database import):
```csv
id,disease_id,operation_signature,canonical_name_zh,canonical_name_en,notes
,,"33,14,9",canonical_name_here,,
```

Example
-------
Input:
```
Maxilla resection + neck dissection (A/B/C/D) + free flap repair
```

Output (example signatures):
```
33,14,9
33,14,132
33,15,9
33,15,132
```

Notes
-----
- The reference data is the source of truth for IDs.
- Some operations expand to multiple IDs; follow the supplement rules.
