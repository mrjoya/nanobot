# NanoBot

AI-powered visual tools using Google's Nano Banana Pro via fal.ai.

## Main Tool: afcover

**afcover** is an Afghan music cover art generator designed specifically for the Afghan music industry. It uses reference images and cultural style presets to create professional album covers.

### Features

- **Reference-Based Generation**: Use previous covers as style guides
- **Afghan Music Styles**: Traditional, modern, fusion, romantic, folk, ghazal, etc.
- **Regional Variations**: Kabuli, Herati, Kandahari, Mazari, Panjshiri aesthetics
- **Cultural Authenticity**: Designed for Afghan music industry standards
- **Dari/Pashto Support**: Typography optimized for Afghan scripts

## Quick Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/nanobot.git
   cd nanobot
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **API Key Setup**:
   - Get a fal.ai API key at https://fal.ai/dashboard/keys
   - Copy the example environment file:
     ```bash
     cp .env.example .env
     ```
   - Edit the `.env` file and add your API key:
     ```
     FAL_KEY=your_actual_api_key
     ```

4. **Verify installation**:
   ```bash
   python -m afcover.cli --list-styles
   ```

## Basic Usage

### Generate Cover Art (CLI)

```bash
# Generate with reference images
python -m afcover.cli \
  --ref previous_cover.jpg \
  --title "Dilbar" \
  --artist "Ahmad Zahir" \
  --style traditional

# Modern style with Kabul aesthetic
python -m afcover.cli \
  --ref ref1.jpg --ref ref2.jpg \
  --title "Kabul Nights" \
  --artist "Aryana Sayeed" \
  --style modern \
  --regional kabuli

# Generate multiple variations
python -m afcover.cli \
  --ref reference.jpg \
  --title "Watan" \
  --style folk \
  --num 4
```

### Generate Cover Art (Python API)

```python
from afcover.generator import generate_cover

# Basic generation
result = generate_cover(
    reference_images=["artist_photo.jpg", "style_reference.jpg"],
    title="دل تنها",
    artist="احمد ظاهر",
    style="romantic",
    regional="kabuli",
    num_variations=2,
)

# Print paths to generated images
print(result["images"])

# Cost estimate only (no generation)
result = generate_cover(
    reference_images=["reference.jpg"],
    title="Test Album",
    style="traditional",
    dry_run=True,
)
print(f"Estimated cost: {result['estimated_cost']}")
```

### Natural Language Interface

```python
from afcover.bot import generate_from_request

# Generate from natural language request
result = generate_from_request(
    "Make a traditional cover for 'Laili Laili' by Ahmad Zahir with gold details",
    image_paths=["reference1.jpg", "reference2.jpg"],
)

# Format response
from afcover.bot import format_response
print(format_response(result))
```

## Available Styles

| Style | Description |
|-------|-------------|
| `traditional` | Classic Afghan with ornate details and gold accents |
| `modern` | Contemporary pop style, clean and polished |
| `fusion` | East-West blend, bilingual appeal |
| `romantic` | Soft, emotional for love songs |
| `folk` | Rustic, earthy, homeland imagery |
| `ghazal` | Poetic, calligraphic, literary |
| `sufi` | Mystical and spiritual aesthetic |
| `wedding` | Festive, celebratory aesthetic |
| `patriotic` | National pride and symbolism |
| `hiphop` | Urban Afghan street style |
| `acoustic` | Intimate, unplugged aesthetic |

## Regional Modifiers

| Region | Aesthetic |
|--------|-----------|
| `kabuli` | Urban, cosmopolitan Kabul |
| `herati` | Artistic, Persian classical |
| `kandahari` | Bold, traditional Pashtun |
| `mazari` | Colorful, festive Turkic |
| `panjshiri` | Mountain imagery, natural beauty |
| `badakhshi` | High mountains, gem colors |
| `hazaragi` | Bamiyan heritage, resilient |
| `nuristani` | Forest mountains, wooden |

## Reference Library

The generator includes a reference library for consistent styles:

```bash
# List available references
python -m afcover.cli --list-references

# Use artist references from library
python -m afcover.cli --artist-ref "Ahmad Zahir" --title "New Cover" --style traditional

# Use style references from library
python -m afcover.cli --style-ref "modern" --title "Pop Hit" --artist "New Artist"
```

## OpenClaw Integration

The `afcover` tool is designed to work seamlessly with OpenClaw. See [SKILL.md](SKILL.md) for the full skill definition.

### Bot Interface for OpenClaw

```bash
# Parse a natural language request
python3 -m afcover.bot parse "Make a traditional cover for 'Laili' by Ahmad Zahir"

# Generate with reference images (main entry point for OpenClaw)
python3 -m afcover.bot generate \
    --prompt "Traditional cover for 'Watan' by Ahmad Zahir" \
    --images reference1.jpg reference2.jpg \
    --output ./output

# Cost estimate only
python3 -m afcover.bot generate \
    --prompt "Modern Kabuli cover" \
    --images ref.jpg \
    --dry-run

# List available styles
python3 -m afcover.bot styles

# Manage reference library
python3 -m afcover.bot library list
python3 -m afcover.bot library add --type artist --name "Ahmad Zahir" --image photo.jpg
```

### OpenClaw Conversation Flow

1. User uploads reference images (artist photos, style examples)
2. User describes desired cover in natural language
3. OpenClaw parses the request via `afcover.bot parse`
4. OpenClaw generates the cover via `afcover.bot generate`
5. OpenClaw returns the generated image to the user

## Other Tools

- `scripts/generate.py` - Generic text-to-image generation
- `scripts/edit.py` - Generic image-to-image editing

## Project Structure

```
nanobot/
├── afcover/              # Afghan music cover art tool
│   ├── cli.py            # Command-line interface
│   ├── bot.py            # Natural language interface
│   ├── generator.py      # Core generation logic
│   ├── styles.py         # Style definitions
│   ├── library.py        # Reference image management
│   └── references/       # Store reference artwork
│       ├── artists/      # Artist-specific references
│       └── styles/       # Style-specific references
├── scripts/              # Generic utilities
│   ├── generate.py       # Text-to-image
│   └── edit.py           # Image-to-image
├── shared/               # Shared modules
│   └── api.py            # fal.ai API wrapper
├── tests/                # Test cases
│   └── test_styles.py    # Style validation tests
├── docs/                 # Documentation
│   └── TESTING.md        # Comprehensive testing guide
├── USAGE.md              # Detailed usage guide
├── ROADMAP.md            # Development roadmap
└── README.md             # This file
```

## Cost

- Standard (1K/2K): $0.15/image
- High-res (4K): $0.30/image

## Troubleshooting

See the [USAGE.md](USAGE.md) file for detailed troubleshooting tips and the [docs/TESTING.md](docs/TESTING.md) for comprehensive testing guidelines.

## License

MIT