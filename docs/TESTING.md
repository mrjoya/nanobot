# Afghan Cover Art (afcover) Testing Guide

This document provides testing guidelines, example prompts, and best practices for generating high-quality Afghan music cover art.

## Quick Start Testing

### Prerequisites
- At least one reference image (artist photo or style reference)
- API credentials configured
- Python environment with dependencies

### Basic Test Command
```python
from afcover.generator import generate_cover

# Dry run to see cost estimate and prompt
result = generate_cover(
    reference_images=["artist_photo.jpg"],
    title="Test Album",
    artist="Test Artist",
    style="traditional",
    dry_run=True,
)
print(result["prompt_preview"])
print(result["estimated_cost"])
```

---

## Test Cases by Style

### 1. Traditional Style (کلاسیک افغانی)
**Best for:** Classical music, folk songs, heritage albums

```python
result = generate_cover(
    reference_images=["ahmad_zahir_photo.jpg", "traditional_cover_reference.jpg"],
    title="آهنگ های ماندگار",
    artist="استاد سرآهنگ",
    style="traditional",
    regional="herati",
    text_placement="title_prominent",
    resolution="2K",
    num_variations=2,
)
```

**Expected Result:**
- Ornate borders with gul (carpet) patterns
- Rich jewel tones: ruby red, emerald green, lapis blue
- Nastaliq calligraphy-ready layout
- Classical instruments may be subtly incorporated

**Quality Checklist:**
- [ ] Gold accents present but not overwhelming
- [ ] Cultural patterns look authentic, not generic "oriental"
- [ ] Clear space for Dari/Pashto title
- [ ] Dignified, respectful composition

---

### 2. Modern Pop Style (پاپ مدرن)
**Best for:** Contemporary pop releases, youth artists, diaspora artists

```python
result = generate_cover(
    reference_images=["modern_artist_photo.jpg"],
    title="New Wave",
    artist="آریانا سعید",
    style="modern",
    regional="kabuli",
    release_type="single",
    text_placement="title_bottom",
    resolution="1K",
    num_variations=3,
)
```

**Expected Result:**
- Clean, minimal design
- Bold contemporary colors (electric blue, purple, orange)
- Professional studio aesthetic
- Urban, polished Kabul vibe

**Quality Checklist:**
- [ ] Modern, not dated effects
- [ ] Clean negative space
- [ ] Bold typography areas clear
- [ ] Professional, international appeal

---

### 3. Fusion Style (آمیزش شرق و غرب)
**Best for:** Diaspora releases, international collaborations, bilingual albums

```python
result = generate_cover(
    reference_images=["artist_diaspora.jpg", "fusion_reference.jpg"],
    title="Between Two Worlds",
    artist="Qais Ulfat",
    style="fusion",
    text_placement="integrated_calligraphy",
    custom_prompt="Subtle Afghan motifs in modern geometric arrangement, sophisticated international appeal",
    resolution="2K",
)
```

**Expected Result:**
- Traditional motifs with modern treatment
- Warm gold + modern teal palette
- Space for bilingual text (Dari + English)
- Sophisticated, bridge-culture feel

**Quality Checklist:**
- [ ] Cultural elements respected, not tokenized
- [ ] Works for both Afghan and international audiences
- [ ] Bilingual layout accommodated
- [ ] Neither too traditional nor too Western

---

### 4. Romantic Ballad Style (عاشقانه)
**Best for:** Love songs, romantic albums, emotional ballads

```python
result = generate_cover(
    reference_images=["romantic_artist.jpg"],
    title="دل تنها",
    artist="فرهاد دریا",
    style="romantic",
    custom_prompt="Soft dreamy atmosphere, single rose element, golden-hour lighting",
    resolution="2K",
)
```

**Expected Result:**
- Soft pink, blush, and gold tones
- Dreamy bokeh effects
- Romantic floral elements (roses)
- Elegant, emotional mood

**Quality Checklist:**
- [ ] Soft, not harsh colors
- [ ] Romantic without being cliché
- [ ] Flowing Nastaliq-ready areas
- [ ] Intimate, emotional atmosphere

---

### 5. Folk Style (محلی)
**Best for:** Regional folk music, Attan songs, village heritage

```python
result = generate_cover(
    reference_images=["folk_singer.jpg", "afghan_landscape.jpg"],
    title="صدای دهکده",
    artist="میرویس نجرابی",
    style="folk",
    regional="panjshiri",
    custom_prompt="Mountain valley landscape, warm nostalgic feeling, natural textures",
    resolution="1K",
)
```

**Expected Result:**
- Earth tones: brown, terracotta, wheat gold
- Mountain or valley imagery
- Handcrafted, artisanal feel
- Connection to homeland

**Quality Checklist:**
- [ ] Natural, not synthetic textures
- [ ] Authentic rural Afghan aesthetic
- [ ] Warm, nostalgic atmosphere
- [ ] Folk instruments may be present

---

### 6. Ghazal Poetry Style (غزل)
**Best for:** Classical ghazal, poetry recitations, Sufi-influenced vocals

```python
result = generate_cover(
    reference_images=["classical_singer.jpg"],
    title="دیوان غزل",
    artist="استاد رحیم بخش",
    style="ghazal",
    regional="herati",
    text_placement="integrated_calligraphy",
    custom_prompt="Persian miniature painting influence, parchment texture, ink wash aesthetic",
    resolution="2K",
)
```

**Expected Result:**
- Deep blues, blacks, gold leaf
- Calligraphic, literary aesthetic
- Parchment or aged paper textures
- Single rose or nightingale motif possible

**Quality Checklist:**
- [ ] Poetic, contemplative mood
- [ ] Museum-quality artistic sensibility
- [ ] Beautiful Nastaliq calligraphy area
- [ ] Intellectually refined composition

---

### 7. Sufi/Spiritual Style (صوفیانه)
**Best for:** Devotional music, Sufi qawwali, spiritual albums

```python
result = generate_cover(
    reference_images=["sufi_artist.jpg"],
    title="نور الهی",
    artist="گروه عرفانی",
    style="sufi",
    regional="mazari",
    custom_prompt="Blue Mosque of Mazar-i-Sharif influence, sacred geometry, ethereal light",
    resolution="2K",
)
```

**Expected Result:**
- Spiritual green, deep blue, gold
- Sacred geometry (eight-pointed stars)
- Ethereal, transcendent lighting
- Shrine or mosque architectural elements

**Quality Checklist:**
- [ ] Spiritually respectful, not appropriative
- [ ] Peaceful, contemplative mood
- [ ] Geometric patterns divine/ordered
- [ ] Appropriate religious imagery

---

### 8. Wedding/Celebration Style (عروسی)
**Best for:** Wedding songs, Attan music, party compilations

```python
result = generate_cover(
    reference_images=["attan_photo.jpg"],
    title="شب عروسی",
    artist="Various Artists",
    style="wedding",
    custom_prompt="Festive, joyful energy, Attan dance silhouettes, celebration atmosphere",
    resolution="1K",
    num_variations=2,
)
```

**Expected Result:**
- Bright red, gold, hot pink, emerald
- Festive, energetic composition
- Dance or celebration elements
- Henna patterns possible

**Quality Checklist:**
- [ ] Joyous, celebratory energy
- [ ] Bold, festive colors
- [ ] Not somber or minimal
- [ ] Party-appropriate aesthetic

---

### 9. Patriotic/Milli Style (ملی)
**Best for:** National pride songs, independence themes, homeland songs

```python
result = generate_cover(
    reference_images=["patriotic_reference.jpg"],
    title="وطن",
    artist="ناشناس",
    style="patriotic",
    custom_prompt="Hindu Kush mountains, dignified Afghan pride, national colors subtle",
    resolution="2K",
)
```

**Expected Result:**
- Afghan flag colors (black, red, green) tastefully integrated
- National symbols: mountains, architecture
- Dignified, proud presentation
- Unity themes

**Quality Checklist:**
- [ ] Dignified, not propaganda-style
- [ ] Flag colors present but artistic
- [ ] Proud without being political
- [ ] Unified, hopeful mood

---

### 10. Hip-Hop Style (هیپ هاپ)
**Best for:** Afghan rap, urban music, youth hip-hop

```python
result = generate_cover(
    reference_images=["hiphop_artist.jpg"],
    title="Streets of Kabul",
    artist="Bezhan Zafarmal",
    style="hiphop",
    text_placement="title_prominent",
    custom_prompt="Urban street aesthetic, graffiti influence, bold Dari typography",
    resolution="1K",
)
```

**Expected Result:**
- Black, yellow, neon accents
- Graffiti/street art influence
- Bold, rebellious energy
- Mixed Dari/English typography space

**Quality Checklist:**
- [ ] Urban, authentic street feel
- [ ] Bold, youthful energy
- [ ] Cultural elements respected
- [ ] Not offensive or inappropriate

---

### 11. Acoustic/Unplugged Style (آکوستیک)
**Best for:** Intimate performances, unplugged recordings, acoustic albums

```python
result = generate_cover(
    reference_images=["acoustic_performance.jpg"],
    title="Unplugged Sessions",
    artist="Farhad Darya",
    style="acoustic",
    custom_prompt="Warm intimate setting, acoustic rubab detail, soft lamp lighting",
    resolution="1K",
)
```

**Expected Result:**
- Warm wood browns, cream, amber
- Intimate, cozy atmosphere
- Instrument close-ups possible
- Personal, authentic feel

**Quality Checklist:**
- [ ] Intimate, not grand
- [ ] Warm, not cold tones
- [ ] Authentic acoustic aesthetic
- [ ] Personal, raw emotion

---

## Regional Style Testing

Test regional modifiers with any base style:

```python
# Test all regional styles with traditional base
regions = ["kabuli", "herati", "kandahari", "mazari", "panjshiri", "badakhshi", "hazaragi", "nuristani"]

for region in regions:
    result = generate_cover(
        reference_images=["test_image.jpg"],
        title=f"Regional Test - {region}",
        style="traditional",
        regional=region,
        dry_run=True,
    )
    print(f"\n{region}:")
    print(result["prompt_preview"][:200])
```

### Regional Expectations:

| Region | Key Visual Elements |
|--------|-------------------|
| kabuli | Urban, cosmopolitan, modern Kabul |
| herati | Persian artistic, tile patterns, poetry |
| kandahari | Bold Pashtun, pomegranates, strong |
| mazari | Blue Mosque, Turkic colors, festive |
| panjshiri | Mountain valleys, emerald river, proud |
| badakhshi | High Pamir, lapis blue, ruby red |
| hazaragi | Bamiyan, Band-e-Amir lakes, resilient |
| nuristani | Forest mountains, wood carvings |

---

## Occasion Theme Testing

Test occasion modifiers:

```python
occasions = ["nowruz", "eid", "independence", "winter"]

for occasion in occasions:
    result = generate_cover(
        reference_images=["test_image.jpg"],
        title=f"Occasion Test - {occasion}",
        style="traditional",
        occasion=occasion,
        dry_run=True,
    )
    print(f"\n{occasion}:")
    print(result["prompt_preview"][:200])
```

---

## Tips for Best Results

### Reference Images
1. **Quality matters:** Use high-resolution, well-lit reference images
2. **Multiple references:** 2-3 images give better style consistency
3. **Mix types:** One artist photo + one style reference works well
4. **Avoid:** Blurry, low-quality, heavily filtered images

### Prompt Engineering
1. **Be specific:** "ornate gold Nastaliq" > "fancy text"
2. **Use Dari/Pashto terms:** Adds cultural specificity
3. **Describe mood:** "melancholic longing" > "sad"
4. **Include instruments:** Mention rubab, tabla, etc. if relevant

### Custom Prompts
Good custom prompts:
```python
custom_prompt="Single red rose in foreground, soft bokeh background, golden-hour lighting"
custom_prompt="Hindu Kush mountains at sunset, dramatic sky, natural majesty"
custom_prompt="Intricate Herati tile pattern border, central medallion design"
```

Bad custom prompts:
```python
custom_prompt="make it cool"  # Too vague
custom_prompt="add lots of stuff"  # No direction
custom_prompt="copy this exactly"  # Not creative
```

### Negative Prompts
Use negative prompts to avoid unwanted elements:
```python
negative_prompt="faces, text, watermarks, blurry, low quality"
negative_prompt="neon colors, anime style, cartoon"
negative_prompt="generic stock photo aesthetic"
```

### Resolution Selection
- **1K ($0.15):** Draft iterations, testing styles
- **2K ($0.15):** Good for most releases, streaming-optimized  
- **4K ($0.30):** Print materials, vinyl covers, billboards

### Variation Strategy
1. Generate 2-4 variations at 1K for style exploration
2. Select best concept
3. Regenerate winner at 2K or 4K with refined prompt
4. Use seed for reproducibility if needed

---

## Cost-Efficient Testing Workflow

```python
# Step 1: Dry run to check prompt
result = generate_cover(..., dry_run=True)
print(result["prompt_preview"])
# Review and adjust if needed

# Step 2: Low-res exploration (3 variations = $0.45)
result = generate_cover(
    ...,
    resolution="1K",
    num_variations=3,
)

# Step 3: High-res final (1 image at 2K = $0.15)
result = generate_cover(
    ...,
    resolution="2K",
    num_variations=1,
    seed=12345,  # If you found a good seed
)
```

---

## Troubleshooting

### Issue: Results look generic/Western
**Fix:** Add more specific Afghan cultural elements to custom_prompt
```python
custom_prompt="authentic Afghan carpet gul patterns, Nastaliq calligraphy style, lapis lazuli blue accents"
```

### Issue: Typography area not clear
**Fix:** Use explicit text_placement and add to custom_prompt
```python
text_placement="title_prominent",
custom_prompt="Leave upper 30% clear for Dari title text placement"
```

### Issue: Colors look wrong for style
**Fix:** Override with specific colors in custom_prompt
```python
custom_prompt="Color palette: burgundy red #8B0000, gold #D4AF37, emerald #046307"
```

### Issue: Too busy/cluttered
**Fix:** Add negative prompt and simplify
```python
negative_prompt="cluttered, busy, too many elements",
custom_prompt="minimal composition, focused design, clean layout"
```

---

## Automated Test Suite

For CI/CD, run the validation tests:

```bash
cd nanobot
python -m pytest afcover/tests/ -v
```

Or run manual validation:
```python
from afcover.styles import get_style_names, get_regional_names, build_style_prompt

# Validate all styles produce valid prompts
for style in get_style_names():
    prompt = build_style_prompt(style)
    assert len(prompt) > 100, f"Style {style} prompt too short"
    assert "Afghan" in prompt or "افغان" in prompt, f"Style {style} missing cultural context"
    print(f"✓ {style}: {len(prompt)} chars")

# Validate all regional combinations
for style in get_style_names():
    for regional in get_regional_names():
        prompt = build_style_prompt(style, regional=regional)
        assert len(prompt) > 150, f"{style}+{regional} prompt too short"
        print(f"✓ {style}+{regional}: OK")
```

---

## Sample Gallery Prompts

Use these tested prompts as starting points:

### Classic Ahmad Zahir Style
```python
generate_cover(
    reference_images=["ahmad_zahir.jpg"],
    title="آهنگ جاودان",
    artist="احمد ظاهر",
    style="traditional",
    regional="kabuli",
    custom_prompt="1970s Afghan music golden era aesthetic, warm nostalgic film grain, elegant simplicity",
)
```

### Modern Diaspora Release
```python
generate_cover(
    reference_images=["diaspora_artist.jpg"],
    title="Homeland Dreams",
    artist="Afghan-American Artist",
    style="fusion",
    custom_prompt="Subtle Afghan geometric patterns in modern minimalist design, bilingual ready",
)
```

### Traditional Wedding Compilation
```python
generate_cover(
    reference_images=["attan_dance.jpg", "wedding_decor.jpg"],
    title="مجلس عروسی",
    style="wedding",
    regional="mazari",
    custom_prompt="Festive Turkmen patterns, joyful celebration energy, dhol drum imagery",
)
```

---

*Last updated: 2025*
*For issues or suggestions, contact the nanobot development team.*
