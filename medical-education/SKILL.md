---
name: medical-education
description: Create interactive medical education materials including presentations, animations, anatomy viewers, and molecular visualizations. Use when the user asks to create medical/anatomy lectures, disease process animations, interactive anatomy viewers for bones/organs/systems, pathophysiology explanations, drug mechanism visualizations, 3D molecular structure viewers, or any educational content for medical/healthcare teaching.
---

# Medical Education Content Creator

This skill provides guidance for creating high-quality, interactive medical education materials using web technologies (HTML/CSS/JavaScript). All outputs are self-contained HTML files.

## Core Principles

**Always read relevant skills first:**
- Read `/mnt/skills/public/frontend-design/SKILL.md` for aesthetic guidance
- For presentations, also read `/mnt/skills/public/pptx/SKILL.md`

**Web-based vs PowerPoint:**
- Default to HTML for interactive content, animations, anatomy viewers
- Use PowerPoint only when user explicitly requests it or must fit existing workflows

## Content Types

### 1. Interactive Medical Presentations

**When to use:** User requests lectures about diseases, medications, or medical concepts.

**Key Features:**
- Progressive disclosure (reveal step-by-step)
- Embedded quizzes with immediate feedback
- Interactive diagrams (clickable, hoverable)
- Smooth animations between slides
- Navigation controls + keyboard shortcuts

**Best Practices:**
- Distinctive typography (NOT Inter, Roboto, Arial)
- Medically appropriate colors
- Clinical pearls and "why this matters" context
- See `references/examples.md` for template

### 2. Disease Process Animations

**When to use:** User wants to show disease development or pathophysiology.

**Key Features:**
- Step-by-step animated progression
- Clickable stages with explanations
- "Play All" button for auto-progression
- Visual indicators (colors, arrows, labels)

**Examples:** Stone formation, atherosclerosis, infection progression, drug mechanisms

### 3. Anatomy Viewers

**When to use:** User requests interactive exploration of anatomical structures.

**Structure (3 columns):**
- View Selector: Anterior/Posterior/Lateral/Medial buttons + layer toggles
- Anatomy Canvas: SVG drawings, clickable landmarks (red dots), zoom controls
- Info Panel: Legend, structure details, clinical significance

**For each landmark include:**
- Location, Features, Function, Relationships
- Clinical Significance (injuries, surgical notes, palpation)
- Measurements when relevant

**Toggle Layers:** Muscles (red), Ligaments (yellow), Nerves (purple), Vessels (red/blue)

### 4. Molecular Structure Viewers

**When to use:** User wants to visualize drug molecules, proteins, enzymes.

**Implementation:**
```html
<script src="https://3Dmol.csb.pitt.edu/build/3Dmol-min.js"></script>
<script>
    let viewer = $3Dmol.createViewer(element, {backgroundColor: 'white'});
    $3Dmol.download('pdb:4INS', viewer, {}, function() {
        viewer.setStyle({}, {stick: {colorscheme: 'default'}});
        viewer.zoomTo();
        viewer.render();
    });
</script>
```

## Design Guidelines

**Typography:**
- Headlines: Playfair Display, Merriweather, Cormorant Garamond, Crimson Pro
- Body: Source Sans Pro, Work Sans, IBM Plex Sans

**Color Palettes:**
```css
--bone: #e8dcc4; --cartilage: #b8d4e8; --muscle: #e57373;
--ligament: #fff9c4; --nerve: #ce93d8; --artery: #ef5350; --vein: #5c6bc0;
```

**Animations:**
- CSS animations primarily (more performant)
- 0.3-0.8s for UI transitions, 2-4s for educational animations
- Use `animation-fill-mode: forwards` to maintain end state

## Workflow

1. **Clarify:** What structure/concept? Audience level? Format preference?
2. **Read Skills:** Always read `/mnt/skills/public/frontend-design/SKILL.md` first
3. **Plan:** Outline sections, identify interactive elements, determine views
4. **Create:** HTML skeleton → static structure → interactivity → animations
5. **Deliver:** Save to `/mnt/user-data/outputs/[name].html`, use `present_files`

## Common Pitfalls

**Don't:**
- Use generic AI aesthetics (purple gradients, Inter font)
- Create separate CSS/JS files (must be single HTML)
- Skip clinical relevance

**Do:**
- Make visually distinctive and professional
- Include comprehensive clinical correlations
- Provide multiple interaction methods (click, hover, keyboard)
- Use meaningful colors and clear labels

## Quality Checklist

- ✓ All interactions work
- ✓ Animations smooth
- ✓ Clinical info accurate
- ✓ Typography distinctive
- ✓ Navigation intuitive
- ✓ Includes clinical pearls
