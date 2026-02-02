---
name: cover-art
description: Generate and edit professional music album/single cover art using AI (Nano Banana Pro via fal.ai). Invoke when user requests album artwork, cover art editing, single covers, EP artwork, playlist covers, or music-related visual assets. Supports text-to-image generation with genre presets, image-to-image editing, custom text placement, artist imagery, and logo integration. Cost: $0.15/image.
---

# Cover Art Generator & Editor

Generate and edit album covers via fal.ai's Nano Banana Pro (Gemini 3 Pro Image).

## Quick Start

```bash
python scripts/generate.py \
  --title "Album Title" \
  --artist "Artist Name" \
  --genre synthwave
```

## Parameters

| Param | Required | Description |
|-------|----------|-------------|
| `--title` | Yes | Album/single title (rendered on cover) |
| `--artist` | Yes | Artist name |
| `--genre` | No | Style preset: synthwave, hip-hop, metal, jazz, electronic, indie, pop, classical, r&b, rock, lo-fi, ambient |
| `--style` | No | Custom style override (e.g., "cyberpunk cityscape, rain") |
| `--colors` | No | Color palette (e.g., "purple, cyan, magenta") |
| `--logo` | No | Logo description to include |
| `--subject` | No | Main visual subject/imagery |
| `--resolution` | No | 1K (default), 2K, or 4K ($0.30) |
| `--num` | No | Number of variations (default: 1) |
| `--output` | No | Output file path |

## Workflow

1. Parse user request for title, artist, genre, style cues
2. Run `scripts/generate.py` with extracted parameters
3. Script composes prompt, calls fal.ai, downloads image
4. Return image path to user

## Genre Presets

See `references/genres.md` for full visual breakdown. Quick reference:

- **synthwave**: Neon, retro-futuristic, purple/cyan
- **hip-hop**: Urban, bold typography, gold accents
- **metal**: Dark, gothic, distressed type
- **jazz**: Sophisticated, warm tones, elegant
- **lo-fi**: Anime aesthetic, cozy, warm pastels
- **electronic**: Abstract geometry, vibrant
- **indie**: Minimalist, muted, artistic

## Environment

Requires `FAL_KEY` environment variable with fal.ai API key.

## Example Invocations

**Simple:**
```bash
python scripts/generate.py --title "Neon Dreams" --artist "Synthwave Kid" --genre synthwave
```

**Custom style:**
```bash
python scripts/generate.py \
  --title "Lost in Tokyo" \
  --artist "Lofi Beats" \
  --genre lo-fi \
  --style "anime girl studying at desk, rainy window, warm lamp light" \
  --colors "soft pink, warm orange, cream"
```

**Multiple variations:**
```bash
python scripts/generate.py --title "Velocity" --artist "Speed Demon" --genre electronic --num 4
```

## Image Editing

Edit existing album covers or images with powerful AI:

```bash
python scripts/edit.py \
  --prompt "Make it more vibrant and add neon accents" \
  --image album.jpg
```

### Edit Parameters

| Param | Required | Description |
|-------|----------|-------------|
| `--prompt` | Yes | Editing instructions |
| `--image` | Yes | Input image to edit (can use multiple times) |
| `--aspect-ratio` | No | Output aspect ratio (default: auto) |
| `--resolution` | No | 1K (default), 2K, or 4K ($0.30) |
| `--output` | No | Output file path |
| `--num` | No | Number of variations (default: 1) |

### Edit Examples

**Simple edit:**
```bash
python scripts/edit.py --prompt "Add a vintage filter and grain" --image cover.jpg
```

**Specific modifications:**
```bash
python scripts/edit.py \
  --prompt "Replace background with cosmic space scene, keep artist and text intact" \
  --image cover.jpg \
  --resolution 2K
```

**Edit multiple images:**
```bash
python scripts/edit.py \
  --prompt "Apply consistent dark moody aesthetic to all covers" \
  --image cover1.jpg \
  --image cover2.jpg \
  --image cover3.jpg
```

## Cost

- 1K/2K: $0.15/image
- 4K: $0.30/image
