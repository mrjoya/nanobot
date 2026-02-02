# NanoBot

NanoBot is an AI-powered music cover art generator and editor using Google's Nano Banana Pro (Gemini 3 Pro Image) API via fal.ai.

## Features

- **Text-to-Image Cover Generation**: Create album covers from natural language descriptions
- **Image-to-Image Editing**: Modify existing covers with AI
- **Genre-Specific Presets**: 16 built-in music genre visual styles
- **High-Quality Typography**: Excellent text rendering for album titles and artist names
- **Multiple Variations**: Generate alternatives for selection

## Components

- `scripts/generate.py` - Text-to-image generator for creating new covers
- `scripts/edit.py` - Image-to-image editor for modifying existing images
- `references/genres.md` - Visual style references for music genres

## Requirements

- Python 3.6+
- fal.ai API key
- Python dependencies:
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
3. Edit the `.env` file and replace `your_api_key_here` with your actual API key
   ```
   FAL_KEY=your_actual_api_key_from_fal.ai
   ```

Note: `.env` is in the `.gitignore` file, so your API key won't be committed to the repository.

## Usage

### Generate a Cover

```bash
python scripts/generate.py \
  --title "Neon Dreams" \
  --artist "Synthwave Kid" \
  --genre synthwave
```

### Edit a Cover

```bash
python scripts/edit.py \
  --prompt "Make it more vibrant with neon accents" \
  --image cover.jpg
```

## Cost

- Standard images (1K/2K): $0.15/image
- High-resolution (4K): $0.30/image

## License

MIT