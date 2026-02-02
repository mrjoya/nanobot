# NanoBot Development Roadmap

## Project Overview

**NanoBot** is a collection of AI-powered visual tools using Google's Nano Banana Pro via fal.ai.

### Primary Tool: afcover
Afghan music cover art generator — an image-to-image tool designed specifically for the Afghan music industry.

### Future Tools (Planned)
- General cover art generator
- Promotional material creator
- Social media asset generator

---

## afcover — Afghan Music Cover Art

### Core Concept

Transform reference artwork and artist photos into professional Afghan music cover art while maintaining cultural aesthetics and industry standards.

### Key Features

1. **Reference-Based Generation**
   - Accept multiple reference images (previous covers, style guides)
   - Extract and apply consistent visual styles
   - Maintain artist/label branding across releases

2. **Afghan Music Aesthetics**
   - Traditional patterns and motifs
   - Dari/Pashto typography support
   - Cultural color palettes
   - Regional style variations (Kabul, Herat, etc.)

3. **Artist Photo Integration**
   - Clean background replacement
   - Consistent lighting and color grading
   - Professional composition

4. **Text Overlay System**
   - Album/single title placement
   - Artist name in Latin + Dari/Pashto
   - Label branding

---

## Development Phases

### Phase 1: Foundation ✅
- [x] Basic image-to-image editing (edit.py)
- [x] API key management
- [x] Repository structure

### Phase 2: afcover Core (Current)
- [ ] Create afcover tool structure
- [ ] Reference image handling system
- [ ] Afghan style presets
- [ ] Multi-image input workflow
- [ ] Output format optimization

### Phase 3: Style Library
- [ ] Build reference artwork database structure
- [ ] Create style extraction system
- [ ] Implement style mixing
- [ ] Artist/label profiles

### Phase 4: Production Features
- [ ] Batch processing for album sets
- [ ] Consistent series generation
- [ ] Template system
- [ ] Export presets (Spotify, YouTube, Instagram)

### Phase 5: Integration
- [ ] OpenClaw bot commands
- [ ] Telegram inline interface
- [ ] Web interface (optional)

---

## afcover Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                        INPUT                                     │
├─────────────────────────────────────────────────────────────────┤
│  • Reference covers (1-5 previous works for style)              │
│  • Artist photo (optional)                                       │
│  • Title text (Dari/Pashto + Latin)                             │
│  • Artist name                                                   │
│  • Style direction (traditional, modern, fusion)                │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      PROCESSING                                  │
├─────────────────────────────────────────────────────────────────┤
│  1. Analyze reference images for style elements                 │
│  2. Build composite prompt with Afghan aesthetics               │
│  3. Generate via Nano Banana Pro (image-to-image)              │
│  4. Apply text overlays if needed                               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        OUTPUT                                    │
├─────────────────────────────────────────────────────────────────┤
│  • Multiple variations (1-4)                                    │
│  • Multiple formats (square, story, banner)                     │
│  • Print-ready and web-optimized versions                       │
└─────────────────────────────────────────────────────────────────┘
```

---

## Afghan Music Style Presets

### Traditional
- Ornate borders and frames
- Gold and deep jewel tones
- Calligraphic Dari/Pashto text
- Traditional instrument imagery

### Modern Pop
- Clean, minimal design
- Bold typography
- Vibrant colors
- Contemporary composition

### Fusion
- Blend of traditional and modern
- Cultural motifs with modern treatment
- Bilingual typography
- East-meets-West aesthetics

### Regional Variations
- **Kabuli**: Urban, polished, cosmopolitan
- **Herati**: Artistic, poetic, classical influences
- **Kandahari**: Bold, strong, traditional
- **Mazari**: Colorful, festive, Turkic influences

---

## Technical Architecture

```
nanobot/
├── README.md
├── ROADMAP.md
├── requirements.txt
├── .env.example
├── .env (local only)
│
├── afcover/                    # Main tool
│   ├── __init__.py
│   ├── cli.py                  # Command-line interface
│   ├── generator.py            # Core generation logic
│   ├── styles.py               # Style definitions
│   ├── presets/                # Afghan music presets
│   │   ├── traditional.json
│   │   ├── modern.json
│   │   └── fusion.json
│   └── references/             # Reference artwork storage
│       └── .gitkeep
│
├── scripts/                    # Standalone utilities
│   ├── generate.py             # Generic text-to-image
│   └── edit.py                 # Generic image-to-image
│
└── shared/                     # Shared utilities
    ├── api.py                  # fal.ai API wrapper
    └── utils.py                # Common utilities
```

---

## Agent Tasks

### Agent 1: afcover Core
Build the main afcover tool structure:
- Create afcover/ directory structure
- Implement generator.py with reference handling
- Build CLI interface
- Create initial style presets

### Agent 2: Style System
Develop the Afghan music style library:
- Define style parameters
- Create preset files
- Build style extraction from references
- Implement style mixing logic

### Agent 3: Integration
Connect afcover to OpenClaw:
- Create skill definition
- Build conversation flow
- Implement image handling
- Design output presentation

### Agent 4: Testing & Refinement
Quality assurance and optimization:
- Test with real Afghan music covers
- Refine prompts for cultural accuracy
- Optimize for consistent results
- Document best practices

---

## Immediate Next Steps

1. **Create afcover directory structure**
2. **Build core generator with reference image support**
3. **Define Afghan music style presets**
4. **Create CLI for testing**
5. **Integrate with OpenClaw as skill**

---

## Success Metrics

- Consistent style matching from references
- Accurate cultural representation
- Professional typography handling
- Fast generation times
- High user satisfaction from Afghan music artists/labels
