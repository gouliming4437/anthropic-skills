# Special ID Mapping Rules

## 1. 游离皮瓣修复术 (Free Flap Repair)

**Always maps to 3 IDs**: 1, 3, 4

Generate 3 separate signature variants for each occurrence.

## 2. 游离肌骨皮瓣修复术 (Free Osteocutaneous Flap)

**Context-dependent mapping** - scan the entire operation combination for keywords:

| Context Keyword | IDs | Billing Meaning |
|-----------------|-----|-----------------|
| `上颌` (maxilla) | 9, 132 | Upper jaw reconstruction |
| `下颌` (mandible) | 8, 131 | Lower jaw reconstruction |

Generate 2 separate signature variants based on detected context.

**Note**: If neither keyword is found, flag for manual review.