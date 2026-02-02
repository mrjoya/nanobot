---
name: afcover
description: |
  Generate professional Afghan music album cover art using AI (Nano Banana Pro via fal.ai).
  Specializes in culturally authentic Afghan aesthetics with 11 style presets and 8 regional variations.
  
  ⚠️ COST CONTROL: All commands default to cost estimate mode.
     User must explicitly confirm before any charges occur.
     Daily limit: $5.00
  
  TRIGGER PHRASES:
  - "Afghan cover art", "Afghan album cover", "Afghan music cover"
  - "cover for [Dari/Pashto song title]"
  - Artist names: Ahmad Zahir, Aryana Sayeed, Farhad Darya, etc.
  - Styles: traditional, ghazal, sufi, folk, modern, fusion, hiphop
  - Regional: Kabuli, Herati, Kandahari, Mazari, Panjshiri
  - Occasions: Nowruz, Eid, wedding
  
  REQUIRES: Reference images (artist photos, style examples)
  COST: $0.15/image (1K/2K), $0.30/image (4K)
---

# Afghan Music Cover Art Generator (afcover)

Generate professional, culturally authentic Afghan music album covers using reference images and AI.

## ⚠️ CRITICAL: Cost Control

**ALL generation commands default to DRY-RUN mode (cost estimate only).**

1. **First call**: Always shows cost estimate, NO CHARGE
2. **User confirms**: Only then add `--confirm` flag
3. **Daily limit**: $5.00/day enforced automatically

```bash
# Step 1: Get cost estimate (DEFAULT - FREE, no API call)
python3 -m afcover.bot generate \
    --prompt "Traditional cover for 'Laili'" \
    --images photo.jpg

# Step 2: ONLY after user confirms, add --confirm (COSTS MONEY)
python3 -m afcover.bot generate \
    --prompt "Traditional cover for 'Laili'" \
    --images photo.jpg \
    --confirm

# Check daily usage
python3 -m afcover.bot usage
```

## Workflow (Two-Step Confirmation)

1. **User uploads reference images** (artist photos, style examples, existing covers)
2. **User describes desired cover** in natural language
3. **STEP 1 - Cost Estimate** (FREE):
   ```bash
   python3 -m afcover.bot generate --prompt "..." --images img.jpg
   ```
   → Returns cost estimate, style preview, daily usage
4. **Show estimate to user and ASK FOR CONFIRMATION**
5. **STEP 2 - Generate** (COSTS MONEY, only after user confirms):
   ```bash
   python3 -m afcover.bot generate --prompt "..." --images img.jpg --confirm
   ```
6. **Return the generated cover(s)** to the user

## Commands

### Parse Request (FREE)
Analyze a natural language request to see extracted parameters:
```bash
python3 -m afcover.bot parse "Make a romantic cover for 'Dilbar' by Aryana Sayeed with mountain backdrop"
```

### Generate Cover (Two-Step)
```bash
# STEP 1: Get cost estimate (DEFAULT - FREE)
python3 -m afcover.bot generate \
    --prompt "PROMPT_TEXT" \
    --images IMAGE1 [IMAGE2 ...]

# STEP 2: Actually generate (COSTS MONEY - requires --confirm)
python3 -m afcover.bot generate \
    --prompt "PROMPT_TEXT" \
    --images IMAGE1 [IMAGE2 ...] \
    --output OUTPUT_DIR \
    --confirm \
    [--json]
```

### Check Usage (FREE)
```bash
python3 -m afcover.bot usage
python3 -m afcover.bot usage --json
```

### List Styles
Show available style presets:
```bash
python -m afcover.bot styles
python -m afcover.bot styles --type regional
python -m afcover.bot styles --type occasions
```

### Manage Library
Work with reference image collections:
```bash
# List collections
python -m afcover.bot library list

# Add reference to artist collection
python -m afcover.bot library add --type artist --name "Ahmad Zahir" --image photo.jpg

# Add reference to style collection
python -m afcover.bot library add --type style --name "traditional" --image example.jpg
```

## Style Presets

| Style | Description | Best For |
|-------|-------------|----------|
| `traditional` | Classic Afghan, ornate borders, gold details, Nastaliq calligraphy | Classical, folk, established artists |
| `modern` | Contemporary pop, clean design, bold typography | Pop releases, mainstream |
| `fusion` | East-West blend, bilingual, sophisticated | Diaspora audience, international |
| `romantic` | Soft, emotional, roses, gold tones | Love songs, ballads |
| `folk` | Rustic, earthy, mountain landscapes | Folk music, regional |
| `ghazal` | Poetic, literary, ink wash aesthetic | Ghazal, classical vocals |
| `sufi` | Mystical, spiritual, sacred geometry | Devotional, spiritual |
| `wedding` | Festive, colorful, Attan dance | Wedding songs, celebrations |
| `patriotic` | Afghan flag colors, national symbols | Homeland songs |
| `hiphop` | Urban, graffiti-inspired, bold | Afghan rap, hip-hop |
| `acoustic` | Warm, intimate, wooden textures | Unplugged, intimate |

## Regional Modifiers

Add regional character to any style:

| Region | Character |
|--------|-----------|
| `kabuli` | Urban, cosmopolitan, modern Kabul |
| `herati` | Artistic, Persian influence, Timurid heritage |
| `kandahari` | Bold Pashtun aesthetic, strong |
| `mazari` | Colorful, Turkic, Nowruz vibes |
| `panjshiri` | Mountain majesty, emerald valleys |
| `badakhshi` | High mountain, lapis lazuli colors |
| `hazaragi` | Bamiyan heritage, turquoise |
| `nuristani` | Forest mountain, carved wood |

## Occasion Themes

| Occasion | Theme |
|----------|-------|
| `nowruz` | Spring renewal, Haft Mewa, tulips |
| `eid` | Festive, crescent moon, celebration |
| `independence` | National pride, Afghan flag |
| `winter` | Snow-capped peaks, warm interiors |

## Example Conversation Flows

### Basic Request (Two-Step Confirmation)
```
User: Make me a cover for "Laili Laili" by Ahmad Zahir
[User uploads: artist_photo.jpg]

Agent: I'll prepare a traditional Afghan cover for "Laili Laili" by Ahmad Zahir.
       Let me get a cost estimate first...

[STEP 1 - Runs without --confirm (FREE):
python3 -m afcover.bot generate \
    --prompt "Traditional Afghan cover for 'Laili Laili' by Ahmad Zahir" \
    --images /path/to/artist_photo.jpg]

Agent: 📊 **Cost Estimate** (no charge yet)
       
       🎵 Title: "Laili Laili"
       👤 Artist: Ahmad Zahir
       🎨 Style: traditional
       📐 Resolution: 1K
       🖼️ Images: 1
       
       💰 **Estimated cost: $0.15**
       
       📈 Today: $0.00 spent, $5.00 remaining
       
       Would you like me to generate this cover?

User: Yes, go ahead!

[STEP 2 - Runs with --confirm (COSTS MONEY):
python3 -m afcover.bot generate \
    --prompt "Traditional Afghan cover for 'Laili Laili' by Ahmad Zahir" \
    --images /path/to/artist_photo.jpg \
    --output /workspace/output \
    --confirm]

Agent: ✅ Generated Afghan Cover Art
       🎵 "Laili Laili" by Ahmad Zahir
       🎨 Style: Traditional Afghan (کلاسیک افغانی)
       📀 /workspace/output/afcover-ahmad-zahir-laili-laili-traditional-20260202-143022.png
       💰 Cost: $0.15

[Returns image to user]
```

### Multiple Variations (Cost-Aware)
```
User: Generate 3 variations of a romantic cover for "Dilbar" by Aryana Sayeed
[User uploads: artist_photo.jpg]

[STEP 1 - Cost estimate:
python3 -m afcover.bot generate \
    --prompt "3 variations romantic cover for 'Dilbar' by Aryana Sayeed" \
    --images artist_photo.jpg]

Agent: 📊 **Cost Estimate** (no charge yet)
       
       🎵 Title: "Dilbar"
       👤 Artist: Aryana Sayeed
       🎨 Style: romantic
       🖼️ Images: 3 variations
       
       💰 **Estimated cost: $0.45** (3 × $0.15)
       
       📈 Today: $0.15 spent, $4.85 remaining
       
       Generate 3 variations for $0.45?

User: That's fine, proceed.

[STEP 2 - With --confirm]
```

### Check Usage/Limits
```
User: How much have I spent today on covers?

[Runs: python3 -m afcover.bot usage]

Agent: 📊 **Daily Usage**
       Date: 2026-02-02
       Generations: 2
       Images created: 4
       Spent today: $0.60
       Remaining: $4.40
       Daily limit: $5.00
```

### Limit Reached
```
User: Make another cover for "Watan"
[User uploads: photo.jpg]

[STEP 1 - Cost estimate]

Agent: 📊 **Cost Estimate**: $0.15
       
       ⚠️ **Warning**: You've spent $4.95 today. 
       This would exceed your daily limit of $5.00.
       
       Please wait until tomorrow or contact support to increase limits.
```

## File Handling

### Accepting User Images
When user uploads images via messaging:
1. Images are saved to a temporary path (e.g., `/tmp/upload_123.jpg`)
2. Pass these paths to the `--images` parameter
3. Generated images go to `--output` directory

### Returning Results
The generated image path is returned in the result. Send this file back to the user via the messaging channel.

## Environment

Requires `FAL_KEY` environment variable with fal.ai API key.
Location: `/home/ec2-user/.openclaw/workspace/nanobot/.env`

## Cost Control (Critical)

⚠️ **NEVER call generate with --confirm without user approval**

| Rule | Implementation |
|------|----------------|
| Default to dry-run | All `generate` commands without `--confirm` are FREE |
| Require confirmation | Only add `--confirm` after user explicitly approves |
| Daily limit | $5.00/day enforced automatically |
| Check usage | Use `python3 -m afcover.bot usage` to see spending |
| Resolution | Default 1K ($0.15), 4K costs 2x ($0.30) |
| Variations | Each variation costs per-image rate |

### Cost Reference
- 1K/2K resolution: **$0.15/image**
- 4K resolution: **$0.30/image**
- Daily limit: **$5.00**

### Workflow Checklist
1. ☐ Run `generate` without `--confirm` → shows estimate
2. ☐ Show estimate to user with cost
3. ☐ Wait for explicit user confirmation
4. ☐ Only then run with `--confirm`
5. ☐ Check `usage` if approaching limit

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Reference images required" | User must upload at least one image |
| "FAL_KEY not found" | Check .env file exists with valid API key |
| "Unknown style" | Use `python -m afcover.bot styles` to see valid options |
| Generation fails | Check API key balance at fal.ai dashboard |

## Technical Details

- **API**: fal.ai Nano Banana Pro (Gemini 3 Pro Image)
- **Output Format**: PNG (default), JPEG, WebP
- **Aspect Ratio**: 1:1 (album cover standard)
- **Max Images**: 4 variations per request
- **Timeout**: 120 seconds per generation

## File Locations

```
nanobot/
├── SKILL.md                    # This file
├── afcover/
│   ├── bot.py                  # OpenClaw interface
│   ├── generator.py            # Core generation logic
│   ├── styles.py               # Style definitions
│   ├── library.py              # Reference image library
│   └── references/             # Stored reference collections
│       ├── artists/            # Artist-specific references
│       └── styles/             # Style example references
└── shared/
    └── api.py                  # fal.ai API utilities
```
