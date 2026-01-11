---
name: operation-id-assigner
description: Convert surgical operation combinations (Chinese names) into standardized comma-separated ID signatures for procedure templates.
---

# Operation ID Assigner

Convert surgical operation combinations into ID-based signatures.

## Task

Given operation combinations (Chinese surgical procedure names), convert each operation to its numeric ID from reference data, producing comma-separated signatures.

## Reference Data

1. **Load `reference/operation-ids.csv`** - Use `id` and `name_zh` columns for mapping
2. **Check `reference/Supplement-information.md`** - Special rules for multi-ID operations

## Instructions

1. Parse the input operation combination (separated by `+`)
2. Handle `/` as alternatives (e.g., `A/B/C术` means three operations: `A术`, `B术`, `C术`)
3. Match each operation name to reference data
4. Apply multi-ID rules from supplement when applicable
5. Generate all signature combinations

## Matching Rules

- **Exact match first** - Look for exact name in reference
- **Fuzzy match** - If no exact match, find the closest match using your understanding (typos, missing characters, synonyms)
- **Flag uncertain matches** - Report to user for confirmation if unsure
- **Context matters** - For `游离肌骨皮瓣修复术`, check if combination contains `上颌` or `下颌` to select correct IDs

## Multi-ID Operations

From `reference/Supplement-information.md`:

| Operation | IDs | Condition |
|-----------|-----|-----------|
| 游离皮瓣修复术 | 1, 3, 4 | Always 3 variants |
| 游离肌骨皮瓣修复术 | 9, 132 | When `上颌` in combination |
| 游离肌骨皮瓣修复术 | 8, 131 | When `下颌` in combination |

Generate all combinations (Cartesian product) when multiple IDs apply.

## Output

**Simple list** (default):
```
33,14,9
33,14,132
33,15,9
...
```

**CSV format** (when requested for database import):
```csv
id,disease_id,operation_signature,canonical_name_zh,canonical_name_en,notes
,,"33,14,9",canonical_name_here,,
```

## Example

**Input**:
```
上颌骨全切术+肩胛舌骨上/改良根治性/根治性/扩大根治性颈淋巴清扫术+游离肌骨皮瓣修复术
```

**Output** (8 signatures):
```
33,14,9
33,14,132
33,15,9
33,15,132
33,16,9
33,16,132
33,17,9
33,17,132
```
