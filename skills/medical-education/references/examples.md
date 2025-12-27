# Medical Education Examples

This document provides complete code templates for common medical education content types.

## Interactive Presentation Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Medical Presentation</title>
    <link href="https://fonts.googleapis.com/css2?family=Crimson+Pro:wght@600;700&family=IBM+Plex+Sans:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #c73e1d;
            --secondary: #2c5f7a;
            --accent: #f4a261;
        }
        
        body {
            font-family: 'IBM Plex Sans', sans-serif;
            margin: 0;
            padding: 0;
        }
        
        .slide-container {
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 3rem;
        }
        
        .slide {
            max-width: 1200px;
            opacity: 0;
            animation: fadeInUp 0.8s ease forwards;
        }
        
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        h1 {
            font-family: 'Crimson Pro', serif;
            font-size: 3.5rem;
            color: var(--primary);
        }
        
        .quiz {
            background: white;
            border: 2px solid #e0e0e0;
            border-radius: 12px;
            padding: 2rem;
            margin: 2rem 0;
        }
        
        .quiz-option {
            padding: 1rem;
            margin: 0.5rem 0;
            background: #f8f8f8;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            cursor: pointer;
        }
        
        .quiz-option:hover {
            border-color: var(--accent);
        }
        
        .quiz-option.correct {
            background: #d4edda;
            border-color: #28a745;
        }
        
        .nav-btn {
            padding: 1rem 2rem;
            background: var(--primary);
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1rem;
        }
    </style>
</head>
<body>
    <div class="slide-container" id="slide1">
        <div class="slide">
            <h1>Your Title Here</h1>
            <!-- Content -->
        </div>
    </div>
    
    <div class="navigation">
        <button class="nav-btn" onclick="previousSlide()">← Previous</button>
        <button class="nav-btn" onclick="nextSlide()">Next →</button>
    </div>
    
    <script>
        let currentSlide = 1;
        const totalSlides = 5;
        
        function updateDisplay() {
            for (let i = 1; i <= totalSlides; i++) {
                document.getElementById(`slide${i}`).style.display = 'none';
            }
            document.getElementById(`slide${currentSlide}`).style.display = 'flex';
        }
        
        function nextSlide() {
            if (currentSlide < totalSlides) {
                currentSlide++;
                updateDisplay();
            }
        }
        
        function previousSlide() {
            if (currentSlide > 1) {
                currentSlide--;
                updateDisplay();
            }
        }
        
        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowRight') nextSlide();
            if (e.key === 'ArrowLeft') previousSlide();
        });
        
        updateDisplay();
    </script>
</body>
</html>
```

## Disease Animation Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Disease Process Animation</title>
    <style>
        .canvas {
            position: relative;
            width: 800px;
            height: 600px;
            background: #fafafa;
            border-radius: 12px;
        }
        
        /* Particle animation */
        .particle {
            position: absolute;
            width: 10px;
            height: 10px;
            background: #64b5f6;
            border-radius: 50%;
            animation: flow 3s ease-in-out infinite;
        }
        
        @keyframes flow {
            0% { left: 0%; opacity: 0; }
            10% { opacity: 0.8; }
            90% { opacity: 0.8; }
            100% { left: 100%; opacity: 0; }
        }
        
        /* Growth animation */
        .stone {
            position: absolute;
            background: #795548;
            border-radius: 50%;
            animation: stoneGrow 4s ease-out forwards;
        }
        
        @keyframes stoneGrow {
            0% { width: 20px; height: 20px; }
            100% { width: 60px; height: 60px; }
        }
        
        .stage-btn {
            padding: 1rem;
            margin: 0.5rem;
            background: white;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            cursor: pointer;
        }
        
        .stage-btn.active {
            background: #2c5f7a;
            color: white;
        }
    </style>
</head>
<body>
    <div class="controls">
        <button class="stage-btn active" onclick="showStage(1)">Stage 1</button>
        <button class="stage-btn" onclick="showStage(2)">Stage 2</button>
        <button class="stage-btn" onclick="showStage(3)">Stage 3</button>
    </div>
    
    <div class="canvas" id="canvas">
        <!-- Animated elements added by JavaScript -->
    </div>
    
    <script>
        function showStage(stage) {
            clearCanvas();
            animateStage(stage);
        }
        
        function clearCanvas() {
            const canvas = document.getElementById('canvas');
            canvas.innerHTML = '';
        }
        
        function animateStage(stage) {
            const canvas = document.getElementById('canvas');
            
            if (stage === 1) {
                // Add particles
                for (let i = 0; i < 10; i++) {
                    const particle = document.createElement('div');
                    particle.className = 'particle';
                    particle.style.top = `${200 + Math.random() * 100}px`;
                    particle.style.animationDelay = `${i * 0.3}s`;
                    canvas.appendChild(particle);
                }
            }
            
            if (stage === 2) {
                // Add growing stone
                const stone = document.createElement('div');
                stone.className = 'stone';
                stone.style.top = '50%';
                stone.style.left = '50%';
                stone.style.transform = 'translate(-50%, -50%)';
                canvas.appendChild(stone);
            }
        }
        
        showStage(1);
    </script>
</body>
</html>
```

## Anatomy Viewer Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Anatomy Viewer</title>
    <style>
        .main-grid {
            display: grid;
            grid-template-columns: 280px 1fr 400px;
            height: 100vh;
        }
        
        .view-selector {
            background: #f5f5f5;
            padding: 2rem;
        }
        
        .view-btn {
            width: 100%;
            padding: 1rem;
            margin: 0.5rem 0;
            background: white;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            cursor: pointer;
        }
        
        .view-btn.active {
            background: #1565c0;
            color: white;
        }
        
        .anatomy-viewer {
            background: #fafafa;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .anatomy-view {
            display: none;
        }
        
        .anatomy-view.active {
            display: block;
        }
        
        .landmark {
            position: absolute;
            cursor: pointer;
        }
        
        .landmark-point {
            width: 14px;
            height: 14px;
            background: #d32f2f;
            border: 3px solid white;
            border-radius: 50%;
        }
        
        .landmark:hover .landmark-point {
            transform: scale(1.4);
        }
        
        .info-panel {
            background: #fafafa;
            padding: 2rem;
            overflow-y: auto;
        }
        
        .info-card {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            display: none;
        }
        
        .info-card.active {
            display: block;
        }
    </style>
</head>
<body>
    <div class="main-grid">
        <div class="view-selector">
            <h2>Views</h2>
            <button class="view-btn active" onclick="changeView('anterior')">Anterior</button>
            <button class="view-btn" onclick="changeView('posterior')">Posterior</button>
            <button class="view-btn" onclick="changeView('lateral')">Lateral</button>
        </div>
        
        <div class="anatomy-viewer">
            <div id="view-anterior" class="anatomy-view active">
                <svg width="400" height="600" viewBox="0 0 400 600">
                    <!-- SVG bone/structure drawing -->
                </svg>
                <div class="landmark" style="top: 100px; left: 200px;" onclick="selectLandmark('head')">
                    <div class="landmark-point"></div>
                </div>
            </div>
            
            <div id="view-posterior" class="anatomy-view">
                <svg width="400" height="600" viewBox="0 0 400 600">
                    <!-- Different view -->
                </svg>
            </div>
        </div>
        
        <div class="info-panel">
            <div class="info-card active" id="info-head">
                <h3>Anatomical Structure Name</h3>
                <p><strong>Location:</strong> Description here</p>
                <p><strong>Function:</strong> Description here</p>
                <p><strong>Clinical Significance:</strong> Description here</p>
            </div>
        </div>
    </div>
    
    <script>
        function changeView(view) {
            document.querySelectorAll('.anatomy-view').forEach(v => v.classList.remove('active'));
            document.getElementById(`view-${view}`).classList.add('active');
            
            document.querySelectorAll('.view-btn').forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
        }
        
        function selectLandmark(landmarkId) {
            document.querySelectorAll('.info-card').forEach(card => card.classList.remove('active'));
            document.getElementById(`info-${landmarkId}`).classList.add('active');
        }
    </script>
</body>
</html>
```

## Animation Patterns Reference

### Flow Animation
```css
@keyframes flow {
    0% { left: 0%; opacity: 0; transform: translateY(0); }
    10% { opacity: 0.8; }
    90% { opacity: 0.8; }
    100% { left: 100%; opacity: 0; transform: translateY(0); }
}
```

### Growth Animation
```css
@keyframes grow {
    0% { transform: scale(0); opacity: 0; }
    100% { transform: scale(1); opacity: 1; }
}
```

### Layer Reveal
```css
@keyframes layerAppear {
    0% { opacity: 0; transform: scale(0.8); }
    50% { opacity: 1; }
    100% { opacity: 0.6; transform: scale(1); }
}
```

### Pulse (for highlighting)
```css
@keyframes pulse {
    0%, 100% { box-shadow: 0 0 20px rgba(245, 124, 0, 0.8); }
    50% { box-shadow: 0 0 30px rgba(245, 124, 0, 1); }
}
```

### Inflammation Effect
```css
@keyframes inflame {
    0%, 100% { opacity: 0; transform: scale(0.5); }
    50% { opacity: 0.6; transform: scale(1.2); }
}
```

## SVG Anatomy Drawing Tips

**Bone Structure:**
```html
<defs>
    <linearGradient id="boneGradient">
        <stop offset="0%" style="stop-color:#f5e6d3" />
        <stop offset="50%" style="stop-color:#e8dcc4" />
        <stop offset="100%" style="stop-color:#d4c4aa" />
    </linearGradient>
</defs>
<path d="M x y ..." fill="url(#boneGradient)" stroke="#b8a88a" stroke-width="2"/>
```

**Muscle Overlay:**
```html
<path d="M x y ..." fill="#e57373" opacity="0.6" stroke="#c62828" stroke-width="2"/>
```

**Ligament:**
```html
<rect x="x" y="y" width="w" height="h" fill="#fff9c4" opacity="0.7" stroke="#f9a825"/>
```

## JavaScript Patterns

**Stage Management:**
```javascript
let currentStage = 1;

function showStage(stage) {
    currentStage = stage;
    clearCanvas();
    animateStage(stage);
    updateControls();
}

function clearCanvas() {
    document.querySelectorAll('.animated-element').forEach(el => el.remove());
}

function updateControls() {
    document.querySelectorAll('.stage-btn').forEach((btn, i) => {
        btn.classList.toggle('active', i + 1 === currentStage);
    });
}
```

**Quiz Interaction:**
```javascript
function checkAnswer(element, isCorrect) {
    element.classList.add(isCorrect ? 'correct' : 'incorrect');
    showFeedback(isCorrect);
}

function showFeedback(isCorrect) {
    const feedback = document.getElementById('feedback');
    feedback.textContent = isCorrect ? 'Correct!' : 'Try again';
    feedback.classList.add('show');
}
```

**Progressive Reveal:**
```javascript
function revealSequence(elements, delay = 800) {
    elements.forEach((element, index) => {
        setTimeout(() => {
            element.classList.add('revealed');
        }, index * delay);
    });
}
```
