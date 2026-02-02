# NanoBot

AI-powered visual tools using Google's Nano Banana Pro via fal.ai.

## Main Tool: afcover

**afcover** is an Afghan music cover art generator designed specifically for the Afghan music industry. It uses reference images and cultural style presets to create professional album covers.

### Features

- **Reference-Based Generation**: Use previous covers as style guides
- **Afghan Music Styles**: Traditional, modern, fusion, romantic, folk, ghazal
- **Regional Variations**: Kabuli, Herati, Kandahari, Mazari, Panjshiri aesthetics
- **Cultural Authenticity**: Designed for Afghan music industry standards
- **Dari/Pashto Support**: Typography optimized for Afghan scripts

### Quick Start

```bash
# Generate with reference images
python3 afcover/cli.py \
  --ref previous_cover.jpg \
  --title "Dilbar" \
  --artist "Ahmad Zahir" \
  --style traditional

# Modern style with Kabul aesthetic
python3 afcover/cli.py \
  --ref ref1.jpg --ref ref2.jpg \
  --title "Kabul Nights" \
  --artist "Aryana Sayeed" \
  --style modern \
  --regional kabuli

# Generate multiple variations
python3 afcover/cli.py \
  --ref reference.jpg \
  --title "Watan" \
  --style folk \
  --num 4
```

### Available Styles

| Style | Description |
|-------|-------------|
| `traditional` | Classic Afghan with ornate details and gold accents |
| `modern` | Contemporary pop style, clean and polished |
| `fusion` | East-West blend, bilingual appeal |
| `romantic` | Soft, emotional for love songs |
| `folk` | Rustic, earthy, homeland imagery |
| `ghazal` | Poetic, calligraphic, literary |

### Regional Modifiers

| Region | Aesthetic |
|--------|-----------|
| `kabuli` | Urban, cosmopolitan Kabul |
| `herati` | Artistic, Persian classical |
| `kandahari` | Bold, traditional Pashtun |
| `mazari` | Colorful, festive Turkic |
| `panjshiri` | Mountain imagery, natural beauty |

## Other Tools

- `scripts/generate.py` - Generic text-to-image generation
- `scripts/edit.py` - Generic image-to-image editing

## Requirements

- Python 3.6+
- fal.ai API key
- Dependencies:
  ```bash
  pip install -r requirements.txt
  ```

## Setup

### API Key Setup

1. Get a fal.ai API key at https://fal.ai/dashboard/keys
2. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
3. Edit the `.env` file and add your API key:
   ```
   FAL_KEY=your_actual_api_key
   ```

Note: `.env` is in `.gitignore` — your API key won't be committed.

## Project Structure

```
nanobot/
├── afcover/              # Afghan music cover art tool
│   ├── cli.py            # Command-line interface
│   ├── generator.py      # Core generation logic
│   ├── styles.py         # Style definitions
│   └── references/       # Store reference artwork
├── scripts/              # Generic utilities
│   ├── generate.py       # Text-to-image
│   └── edit.py           # Image-to-image
├── shared/               # Shared modules
│   └── api.py            # fal.ai API wrapper
├── ROADMAP.md            # Development roadmap
└── README.md
```

## Cost

- Standard (1K/2K): $0.15/image
- High-res (4K): $0.30/image

## License

MIT
