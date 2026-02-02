# NanoBot Usage Guide

This guide provides detailed instructions and examples for using the NanoBot tools, with a primary focus on the `afcover` Afghan music cover art generator.

## Table of Contents
- [Installation](#installation)
- [Environment Setup](#environment-setup)
- [Basic Usage](#basic-usage)
- [Command Line Interface](#command-line-interface)
- [Python API](#python-api)
- [Natural Language Interface](#natural-language-interface)
- [Style Guide](#style-guide)
- [Regional Modifiers](#regional-modifiers)
- [Reference Library](#reference-library)
- [Advanced Options](#advanced-options)
- [Cost Management](#cost-management)
- [Troubleshooting](#troubleshooting)
- [Generic Tools](#generic-tools)

## Installation

### Prerequisites
- Python 3.6+
- pip package manager
- Internet connection for API calls

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/nanobot.git
   cd nanobot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Verify installation:
   ```bash
   python -m afcover.cli --list-styles
   ```
   This should display a list of available Afghan music cover art styles.

## Environment Setup

The application requires a fal.ai API key to function:

1. Sign up for fal.ai at https://fal.ai
2. Navigate to https://fal.ai/dashboard/keys to get your API key
3. Create a `.env` file from the template:
   ```bash
   cp .env.example .env
   ```
4. Edit the `.env` file and add your API key:
   ```
   FAL_KEY=your_actual_api_key
   ```

**Note**: The `.env` file is included in `.gitignore` to prevent accidental exposure of your API key.

## Basic Usage

### Generate Your First Cover

```bash
# Using CLI with a reference image
python -m afcover.cli \
  --ref path/to/reference.jpg \
  --title "My Album" \
  --artist "Artist Name" \
  --style traditional
```

This will create a traditional Afghan style album cover based on your reference image, with spaces for the specified title and artist.

## Command Line Interface

The `afcover.cli` module provides a command-line interface for the generator:

```bash
python -m afcover.cli [options]
```

### Essential Options

- `--ref, --reference`: Path to reference image(s) (can use multiple times)
- `--title`: Album/single title
- `--artist`: Artist name
- `--style`: Style preset (default: traditional)
- `--regional`: Regional style modifier
- `--custom`: Additional custom prompt instructions
- `--resolution`: Output resolution (1K, 2K, or 4K)
- `--num, -n`: Number of variations to generate (1-4)
- `--output-dir, -o`: Output directory
- `--dry-run`: Show cost estimate without generating
- `--json`: Output results as JSON

### Example Commands

```bash
# Basic generation with traditional style
python -m afcover.cli --ref reference.jpg --title "Album Title" --artist "Artist"

# Modern style with Kabul regional influence
python -m afcover.cli --ref ref.jpg --style modern --regional kabuli --title "City Lights"

# Multiple variations with custom prompt
python -m afcover.cli --ref ref.jpg --style folk --num 3 --custom "Include mountain landscape"

# High-resolution output with specific output directory
python -m afcover.cli --ref ref.jpg --resolution 4K --output-dir ./covers

# Preview cost without generating
python -m afcover.cli --ref ref.jpg --title "Test" --dry-run
```

### List Available Options

```bash
# List available styles
python -m afcover.cli --list-styles

# List reference library contents
python -m afcover.cli --list-references
```

## Python API

For programmatic use, import and use the generator directly:

```python
from afcover.generator import generate_cover

# Basic generation
result = generate_cover(
    reference_images=["path/to/reference.jpg"],
    title="Album Title",
    artist="Artist Name",
    style="traditional",
)

# Print paths to generated images
for image_path in result["images"]:
    print(f"Generated: {image_path}")

# Access additional metadata
print(f"Style: {result['style']}")
print(f"Cost: {result['cost']}")
```

### Key Parameters

```python
generate_cover(
    reference_images,              # List of paths to reference images [REQUIRED]
    title=None,                    # Album/single title
    artist=None,                   # Artist name
    style="traditional",           # Style preset
    regional=None,                 # Regional modifier
    occasion=None,                 # Occasion theme (nowruz, eid, etc.)
    release_type="album",          # Type of release (album, single, ep)
    text_placement="title_prominent", # Typography placement hint
    custom_prompt=None,            # Additional instructions
    negative_prompt=None,          # What to avoid
    resolution="1K",               # Output resolution (1K, 2K, 4K)
    num_variations=1,              # Number of variations (1-4)
    output_format="png",           # Output format (png, jpeg, webp)
    seed=None,                     # Random seed for reproducibility
    limit_generations=True,        # Prevent prompt injection
    dry_run=False,                 # Only return cost estimate
    output_dir=".",                # Output directory
)
```

### Advanced API Examples

```python
# Generate multiple variations with specific seed for reproducibility
result = generate_cover(
    reference_images=["ref1.jpg", "ref2.jpg"],
    title="Kabul Nights",
    artist="Aryana Sayeed",
    style="modern",
    regional="kabuli",
    num_variations=3,
    seed=12345,
)

# Special occasion-themed cover
result = generate_cover(
    reference_images=["artist.jpg"],
    title="Spring Celebration",
    artist="Various Artists",
    style="traditional",
    occasion="nowruz",  # Nowruz (Persian New Year) theme
    resolution="2K",
)

# Custom text placement and negative prompts
result = generate_cover(
    reference_images=["ref.jpg"],
    title="Poetry Collection",
    style="ghazal",
    text_placement="integrated_calligraphy",
    custom_prompt="Elegant Nastaliq calligraphy as design element",
    negative_prompt="modern elements, bright colors, Western typography",
)
```

## Natural Language Interface

The `afcover.bot` module provides a natural language interface:

```python
from afcover.bot import generate_from_request, format_response

# Generate from natural language request
result = generate_from_request(
    "Create a traditional Afghan cover with gold details for 'Laili Laili' by Ahmad Zahir",
    image_paths=["reference1.jpg", "reference2.jpg"],
)

# Format response for user display
response = format_response(result)
print(response)
```

### Understanding Language Patterns

The natural language parser understands various patterns:

```python
# Title and artist extraction
"Make a cover for 'Song Title' by Artist Name"

# Style specification
"Generate a modern cover with urban aesthetic"
"Create a traditional style album cover"

# Regional specification
"Design a Herati-style cover with Persian influences"
"Generate a cover with Kandahari aesthetic"

# Combined requests
"Create a modern Kabuli style cover for 'City Lights' by New Artist"
"Make a romantic cover for 'Dil' with soft lighting and rose elements"
```

## Style Guide

The `afcover` generator supports various Afghan music styles, each with unique visual characteristics:

### Traditional (کلاسیک افغانی)
- Classic Afghan aesthetic with ornate details
- Rich gold, burgundy red, emerald green, lapis blue
- Elegant Nastaliq calligraphy spaces
- Ornate borders inspired by carpet patterns
- Best for: Classical music, folk songs, heritage albums

### Modern (پاپ مدرن)
- Contemporary pop music style 
- Clean, minimal design with bold typography
- Vibrant contemporary colors: electric blue, purple, orange
- Urban polished aesthetic reflecting modern Kabul
- Best for: Contemporary pop releases, youth artists

### Fusion (آمیزش شرق و غرب)
- East-West blend for diaspora audiences
- Traditional Afghan motifs with modern design
- Bilingual typography spaces (Dari/Pashto + English)
- Sophisticated international appeal
- Best for: Diaspora releases, international collaborations

### Romantic (عاشقانه)
- Soft, emotional style for love songs
- Soft pink, blush, gold palette
- Dreamy atmosphere with gentle lighting
- Rose motifs and delicate elements
- Best for: Love songs, romantic ballads

### Folk (محلی)
- Rustic, earthy style celebrating regional traditions
- Earth tones: brown, terracotta, wheat gold
- Afghan mountain and village landscape imagery
- Handcrafted authentic feel
- Best for: Regional folk music, village heritage albums

### Ghazal (غزل)
- Poetic, literary style for classical vocals
- Deep blues, blacks, gold leaf
- Ink wash and calligraphy influences
- Sophisticated minimal design
- Best for: Classical ghazal, poetry recitations

### Sufi (صوفیانه)
- Mystical and spiritual aesthetic
- Sacred geometry, soft light rays
- Shrine and mosque architectural elements
- Muted ethereal palette with gold accents
- Best for: Devotional music, spiritual albums

### Wedding (عروسی)
- Festive celebratory style
- Bright red, gold, hot pink, emerald green
- Attan dance silhouettes, festive instruments
- Henna patterns and bridal elements
- Best for: Wedding songs, party compilations

### Patriotic (ملی)
- National pride aesthetic
- Afghan flag colors: black, red, green
- National symbols tastefully integrated
- Dignified, proud presentation
- Best for: Patriotic songs, independence themes

### Hip-Hop (هیپ هاپ)
- Urban street style for Afghan rap
- Bold graffiti-inspired typography
- Gritty textures, street art backgrounds
- Modern Kabul or diaspora city imagery
- Best for: Afghan rap, urban music

### Acoustic (آکوستیک)
- Intimate aesthetic for unplugged recordings
- Warm wood tones, soft lighting
- Close-up instrument details
- Cozy, personal atmosphere
- Best for: Acoustic performances, intimate recordings

## Regional Modifiers

Regional modifiers add specific cultural aesthetics to any base style:

### Kabuli (کابلی)
- Urban cosmopolitan polished aesthetic
- Modern Kabul sophistication
- Blend of traditional and modern elements

### Herati (هراتی)
- Artistic, poetic, classical Persian influences
- Timurid heritage references
- Friday Mosque tile patterns

### Kandahari (کندهاری)
- Bold, strong traditional Pashtun aesthetic
- Pomegranate motifs
- Desert landscape elements

### Mazari (مزاری)
- Colorful, festive Turkic/Uzbek influences
- Blue Mosque (Rawza) imagery
- Nowruz celebration elements

### Panjshiri (پنجشیری)
- Mountain majesty, natural beauty
- Emerald river and green valleys
- Tajik heritage elements

### Badakhshi (بدخشی)
- High mountain Pamiri aesthetic
- Lapis lazuli blue, ruby red (Badakhshan gems)
- Remote pristine landscapes

### Hazaragi (هزاره‌گی)
- Hazara cultural aesthetic
- Bamiyan valley, Band-e-Amir lakes
- Distinctive textile patterns

### Nuristani (نورستانی)
- Mountainous forest aesthetic
- Carved wooden architectural elements
- Isolated mountain culture imagery

## Reference Library

The `afcover` tool includes a reference library for consistent styles:

### Using the Library

```bash
# List available references
python -m afcover.cli --list-references

# Use artist references
python -m afcover.cli --artist-ref "Ahmad Zahir" --title "New Cover" --style traditional

# Use style references
python -m afcover.cli --style-ref "modern" --title "Pop Hit" --artist "New Artist"
```

### Adding to the Library

You can add your own reference images to the library using the Python API:

```python
from afcover.library import add_artist_reference, add_style_reference

# Add artist reference
add_artist_reference(
    artist_name="Ahmad Zahir",
    image_path="path/to/ahmadzahir_photo.jpg",
    metadata={"year": "1977", "album": "Ghazal", "notes": "Classic pose"},
)

# Add style reference
add_style_reference(
    style_name="traditional",
    image_path="path/to/traditional_cover.jpg",
    metadata={"notes": "Good example of ornate borders"},
)
```

## Advanced Options

### Text Placement Options

Control where typography should be placed:

```python
generate_cover(
    # ... other parameters ...
    text_placement="title_prominent",  # Upper third clear for title
    # Other options: "title_bottom", "minimal_text", "integrated_calligraphy"
)
```

### Occasion Themes

Apply seasonal or cultural occasion themes:

```python
generate_cover(
    # ... other parameters ...
    occasion="nowruz",  # Persian New Year theme
    # Other options: "eid", "independence", "winter"
)
```

### Negative Prompts

Specify elements to avoid in the generation:

```python
generate_cover(
    # ... other parameters ...
    negative_prompt="faces, text, watermarks, Western symbols",
)
```

### Output Formats

Control the output file format:

```python
generate_cover(
    # ... other parameters ...
    output_format="jpeg",  # Smaller file size than PNG
    # Other options: "png" (default), "webp"
)
```

### Reproducibility

Use a seed for reproducible results:

```python
generate_cover(
    # ... other parameters ...
    seed=12345,  # Will produce consistent results with same parameters
)
```

## Cost Management

### Pricing

- **1K/2K resolution**: $0.15 per image
- **4K resolution**: $0.30 per image (2x cost)
- Each variation counts as a separate image

### Cost-Efficient Workflow

```python
# 1. Dry run to check prompt and cost
result = generate_cover(
    reference_images=["ref.jpg"],
    title="Album",
    style="traditional",
    dry_run=True,
)
print(f"Estimated cost: {result['estimated_cost']}")
print(result["prompt_preview"])

# 2. Generate low-res variations to explore styles
result = generate_cover(
    reference_images=["ref.jpg"],
    title="Album",
    style="traditional",
    resolution="1K",
    num_variations=3,  # $0.45 total
)

# 3. Pick the best and generate a final high-res version
best_seed = 12345  # If you noted the seed from a variation you liked
result = generate_cover(
    reference_images=["ref.jpg"],
    title="Album",
    style="traditional", 
    resolution="2K",
    num_variations=1,  # $0.15
    seed=best_seed,
)
```

### Safety Features

- `limit_generations=True` (default): Prevents prompt injection techniques that could generate more images than requested
- `dry_run=True`: Preview cost without charging
- Resolution control: Use 1K for drafts, 2K for finals, 4K only when needed for print

## Troubleshooting

### Common Issues and Solutions

#### Issue: API Key Not Found
```
ValueError: FAL_KEY not found. Please create a .env file with your API key.
```
**Solution**: Make sure you've created a `.env` file with your API key:
```
FAL_KEY=your_api_key_here
```

#### Issue: Reference Images Not Found
```
Error: Reference file not found: path/to/image.jpg
```
**Solution**: Check the file path and make sure the image exists.

#### Issue: Results Look Generic or Western
**Solution**: Add more specific Afghan cultural elements to your custom prompt:
```
--custom "authentic Afghan carpet patterns, Nastaliq calligraphy, lapis lazuli color"
```

#### Issue: Typography Area Not Clear
**Solution**: Explicitly specify text placement and add to custom prompt:
```
--text-placement title_prominent
--custom "Leave upper 30% clear for Dari title text"
```

#### Issue: Unwanted Elements in Images
**Solution**: Use negative prompts to avoid specific elements:
```
--negative-prompt "faces, text, watermarks, blurry, low quality"
```

#### Issue: High Costs
**Solution**: Use dry runs, lower resolution, and fewer variations:
```
--dry-run         # Preview cost
--resolution 1K   # Use 1K for drafts
--num 1           # Generate only one variation
```

### Improving Results

1. **Quality References**: Use high-resolution, well-lit reference images
2. **Multiple References**: 2-3 images give better style consistency
3. **Be Specific**: Detailed custom prompts get better results
4. **Cultural Terms**: Use Dari/Pashto terms for authenticity
5. **Start Low-Res**: Test concepts at 1K before finalizing at 2K/4K

## Generic Tools

Besides `afcover`, NanoBot includes generic image generation tools:

### Text-to-Image (generate.py)

```bash
python scripts/generate.py \
  --prompt "Description of the desired image" \
  --resolution 1K \
  --num 1 \
  --output output.png
```

### Image-to-Image Editing (edit.py)

```bash
python scripts/edit.py \
  --input input.jpg \
  --prompt "Instructions for editing the image" \
  --resolution 1K \
  --num 1 \
  --output edited.png
```

These tools use the same underlying API but without the Afghan music-specific style guides and optimizations.

---

## Additional Resources

- [docs/TESTING.md](docs/TESTING.md) - Comprehensive testing guide with examples
- [ROADMAP.md](ROADMAP.md) - Future development plans
- [SPEC.md](SPEC.md) - Technical specification