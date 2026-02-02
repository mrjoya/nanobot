# Cover Art Generator — Technical Specification

## Overview

A skill for OpenClaw that enables Octo to generate professional music cover art on demand using fal.ai's Nano Banana Pro API.

**User Experience:**
```
User: "Generate album cover for 'Midnight Drive' by The Neon Collective, 
       synthwave vibe, purple and cyan palette"

Octo: [invokes skill] → generates image → returns result
      "Here's your cover art for 'Midnight Drive'..."
      [IMAGE]
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         OpenClaw                                 │
│  ┌─────────────┐    ┌──────────────────────────────────────┐   │
│  │    Octo     │───▶│         cover-art skill              │   │
│  │  (Agent)    │    │  ┌────────────────────────────────┐  │   │
│  └─────────────┘    │  │  scripts/generate.py           │  │   │
│                     │  │  - Prompt composition          │  │   │
│                     │  │  - fal.ai API call             │  │   │
│                     │  │  - Image download & return     │  │   │
│                     │  └────────────────────────────────┘  │   │
│                     │  ┌────────────────────────────────┐  │   │
│                     │  │  references/                   │  │   │
│                     │  │  - genres.md (style presets)   │  │   │
│                     │  │  - prompts.md (templates)      │  │   │
│                     │  └────────────────────────────────┘  │   │
│                     └──────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │      fal.ai API       │
                    │  (Nano Banana Pro)    │
                    │  $0.15/image          │
                    └───────────────────────┘
```

---

## Skill Structure

```
skills/cover-art/
├── SKILL.md                    # Main skill file (triggers + instructions)
├── scripts/
│   └── generate.py             # Core generation script
├── references/
│   ├── genres.md               # Genre-specific style presets
│   └── prompts.md              # Prompt templates & examples
└── assets/
    └── (empty - generated images go to workspace)
```

---

## SKILL.md Content

```yaml
---
name: cover-art
description: Generate professional music album/single cover art using AI. 
  Invoke when user requests album artwork, cover art, single covers, 
  EP artwork, or music-related visual assets. Supports genre-specific 
  styles (synthwave, hip-hop, metal, jazz, etc.), custom text placement, 
  artist imagery, and logo integration.
---
```

### Body Outline:
1. Quick Start (example command)
2. Parameters (title, artist, genre, style, colors, logo description)
3. Generation workflow (compose prompt → call script → return image)
4. Reference to genres.md for style presets
5. Reference to prompts.md for advanced templating

---

## Core Script: `scripts/generate.py`

```python
#!/usr/bin/env python3
"""
Cover Art Generator - Nano Banana Pro via fal.ai
Usage: python generate.py --title "Album Name" --artist "Artist" --genre "synthwave" [options]
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

FAL_API_URL = "https://queue.fal.run/fal-ai/nano-banana-pro"

def build_prompt(args):
    """Compose the generation prompt from parameters."""
    
    # Base template
    prompt_parts = [
        "Professional album cover art, square format, print-ready quality.",
    ]
    
    # Genre styling
    genre_styles = {
        "synthwave": "synthwave aesthetic, neon lights, retro-futuristic, purple and cyan color palette, 80s vibes, chrome text",
        "hip-hop": "urban aesthetic, bold typography, street art influence, high contrast, gold accents",
        "metal": "dark and intense, gothic elements, sharp edges, dramatic lighting, bold distressed typography",
        "jazz": "sophisticated and smooth, warm tones, vintage feel, elegant typography, artistic brushstrokes",
        "electronic": "abstract geometric patterns, vibrant colors, digital aesthetic, clean modern typography",
        "indie": "minimalist design, muted colors, artistic photography style, handwritten or serif typography",
        "pop": "bright and colorful, playful elements, glossy finish, bold sans-serif typography",
        "classical": "elegant and refined, orchestral imagery, gold and deep colors, ornate serif typography",
        "r&b": "smooth and sultry, warm lighting, intimate mood, stylish modern typography",
        "rock": "edgy and raw, gritty textures, bold imagery, strong typography",
        "lo-fi": "nostalgic, warm analog aesthetic, soft colors, Japanese influence, cozy vibes",
        "ambient": "ethereal, dreamy landscapes, soft gradients, minimal text, atmospheric",
    }
    
    style = genre_styles.get(args.genre.lower(), args.genre) if args.genre else ""
    if style:
        prompt_parts.append(f"Style: {style}.")
    
    # Custom style override
    if args.style:
        prompt_parts.append(f"Visual direction: {args.style}.")
    
    # Title
    if args.title:
        prompt_parts.append(f'Album title "{args.title}" prominently displayed, legible typography.')
    
    # Artist
    if args.artist:
        prompt_parts.append(f'Artist name "{args.artist}" included in design.')
    
    # Colors
    if args.colors:
        prompt_parts.append(f"Color palette: {args.colors}.")
    
    # Logo
    if args.logo:
        prompt_parts.append(f"Include logo element: {args.logo}.")
    
    # Subject/imagery
    if args.subject:
        prompt_parts.append(f"Main visual subject: {args.subject}.")
    
    # Quality markers
    prompt_parts.append("High resolution, no watermarks, album cover composition.")
    
    return " ".join(prompt_parts)


def generate_cover(prompt, api_key, resolution="1K", num_images=1):
    """Call fal.ai Nano Banana Pro API."""
    
    payload = {
        "prompt": prompt,
        "aspect_ratio": "1:1",  # Album covers are square
        "resolution": resolution,
        "num_images": num_images,
        "output_format": "png"
    }
    
    headers = {
        "Authorization": f"Key {api_key}",
        "Content-Type": "application/json"
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(FAL_API_URL, data=data, headers=headers, method='POST')
    
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8') if e.fp else str(e)
        print(f"API Error {e.code}: {error_body}", file=sys.stderr)
        sys.exit(1)


def download_image(url, output_path):
    """Download generated image to local path."""
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=60) as response:
        with open(output_path, 'wb') as f:
            f.write(response.read())
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Generate album cover art")
    parser.add_argument("--title", required=True, help="Album/single title")
    parser.add_argument("--artist", required=True, help="Artist name")
    parser.add_argument("--genre", help="Music genre (synthwave, hip-hop, metal, jazz, etc.)")
    parser.add_argument("--style", help="Custom style description")
    parser.add_argument("--colors", help="Color palette description")
    parser.add_argument("--logo", help="Logo description to include")
    parser.add_argument("--subject", help="Main visual subject/imagery")
    parser.add_argument("--resolution", default="1K", choices=["1K", "2K", "4K"])
    parser.add_argument("--output", help="Output file path")
    parser.add_argument("--num", type=int, default=1, help="Number of variations")
    parser.add_argument("--prompt-only", action="store_true", help="Only output the prompt")
    
    args = parser.parse_args()
    
    # Build prompt
    prompt = build_prompt(args)
    
    if args.prompt_only:
        print(prompt)
        return
    
    # Get API key
    api_key = os.environ.get("FAL_KEY")
    if not api_key:
        print("Error: FAL_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)
    
    print(f"Generating cover art for '{args.title}' by {args.artist}...", file=sys.stderr)
    print(f"Prompt: {prompt}", file=sys.stderr)
    
    # Generate
    result = generate_cover(prompt, api_key, args.resolution, args.num)
    
    # Handle output
    images = result.get("images", [])
    if not images:
        print("Error: No images returned", file=sys.stderr)
        sys.exit(1)
    
    output_dir = Path(args.output).parent if args.output else Path(".")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    downloaded = []
    for i, img in enumerate(images):
        url = img.get("url")
        if url:
            # Generate filename
            safe_title = "".join(c if c.isalnum() or c in "- " else "" for c in args.title)
            safe_title = safe_title.replace(" ", "-").lower()[:30]
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            
            if args.output and len(images) == 1:
                out_path = args.output
            else:
                out_path = output_dir / f"cover-{safe_title}-{timestamp}-{i+1}.png"
            
            download_image(url, out_path)
            downloaded.append(str(out_path))
            print(f"Saved: {out_path}")
    
    # Output JSON summary
    output = {
        "title": args.title,
        "artist": args.artist,
        "genre": args.genre,
        "prompt": prompt,
        "images": downloaded,
        "cost_estimate": f"${0.15 * len(downloaded):.2f}"
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
```

---

## Reference Files

### `references/genres.md`

| Genre | Visual Elements | Typography | Colors |
|-------|----------------|------------|--------|
| Synthwave | Neon grids, sunset, chrome, retro cars | Chrome/neon outlined | Purple, cyan, magenta, orange |
| Hip-Hop | Urban landscapes, gold chains, graffiti | Bold sans-serif, 3D | Gold, black, red |
| Metal | Skulls, flames, gothic architecture | Distressed, blackletter | Black, red, silver |
| Jazz | Instruments, smoke, nightclub scenes | Elegant serif, script | Warm browns, gold, cream |
| Electronic | Abstract geometry, waveforms, circuits | Clean modern sans | Vibrant neons, gradients |
| Indie | Polaroid aesthetics, nature, minimalism | Handwritten, vintage serif | Muted, desaturated |
| Lo-Fi | Anime aesthetics, cozy rooms, rain | Japanese, soft sans | Warm pastels, soft pink/blue |

### `references/prompts.md`

Advanced prompt patterns, composition guidelines, and example outputs for reference during generation.

---

## Configuration

### Environment Variable
```bash
export FAL_KEY="your-fal-ai-api-key"
```

### OpenClaw Integration
The skill will be installed in the workspace skills directory and automatically available to Octo.

---

## Usage Examples

**Basic:**
```bash
python generate.py --title "Midnight Drive" --artist "The Neon Collective" --genre synthwave
```

**Full options:**
```bash
python generate.py \
  --title "City Lights" \
  --artist "DJ Shadow" \
  --genre electronic \
  --style "cyberpunk cityscape at night, rain reflections" \
  --colors "blue, purple, white neon" \
  --logo "small record label logo in corner" \
  --resolution 2K \
  --num 3
```

**From Octo (natural language):**
```
"Make me an album cover for 'Lost in Tokyo' by Lofi Beats,
 lo-fi aesthetic, anime girl studying, rainy window, warm lighting"
```

---

## Cost Analysis

| Resolution | Cost/Image | Use Case |
|------------|-----------|----------|
| 1K | $0.15 | Drafts, social media |
| 2K | $0.15 | Standard release |
| 4K | $0.30 | Print, high-res |

**Batch pricing:** 10 variations = $1.50

---

## Next Steps

1. [ ] Get fal.ai API key
2. [ ] Create skill directory structure
3. [ ] Implement generate.py script
4. [ ] Create genre presets
5. [ ] Test with sample generations
6. [ ] Install skill to OpenClaw

---

## Future Enhancements

- **Image-to-image mode**: Use reference images for style transfer
- **Logo upload**: Accept actual logo files for compositing
- **Batch mode**: Generate full album artwork sets
- **Style memory**: Save and reuse custom styles
- **Flux LoRA training**: Train custom style models for consistent branding
