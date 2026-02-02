"""
Afghan Music Cover Art Styles

Defines visual styles specific to Afghan music industry aesthetics.
Culturally authentic style definitions for professional album cover generation.
"""

# Base style elements common to all Afghan music covers
BASE_STYLE = {
    "quality": "professional album cover art, high resolution, print-ready, 300 DPI quality",
    "composition": "centered composition, balanced layout, clear visual hierarchy",
    "format": "square format 1:1 aspect ratio, suitable for Spotify, Apple Music, YouTube Music",
    "cultural": "Afghan cultural authenticity, respectful representation",
}

# Typography guidance for Dari/Pashto text
TYPOGRAPHY_GUIDE = {
    "nastaliq": {
        "name": "Nastaliq Script",
        "description": "Traditional Persian/Dari calligraphy, flowing right-to-left",
        "use_for": ["ghazal", "traditional", "classical", "poetic content"],
        "characteristics": "elegant curves, diagonal baseline, ornate flourishes",
    },
    "naskh": {
        "name": "Naskh Script",
        "description": "Clear, readable Arabic-style script",
        "use_for": ["modern", "fusion", "pop", "readable text"],
        "characteristics": "horizontal baseline, clear letterforms, modern feel",
    },
    "dari_modern": {
        "name": "Modern Dari",
        "description": "Contemporary Dari typography for pop music",
        "use_for": ["pop", "hip-hop", "electronic"],
        "characteristics": "bold, geometric, clean sans-serif Persian",
    },
    "bilingual": {
        "name": "Bilingual Layout",
        "description": "Dari/Pashto + English combination",
        "use_for": ["diaspora audience", "international releases"],
        "characteristics": "balanced hierarchy, Dari prominent, English secondary",
    },
}

# Traditional Afghan instruments for visual reference
INSTRUMENTS = {
    "rubab": "Afghan rubab (national instrument), wooden lute with sympathetic strings",
    "tabla": "tabla drums, pair of hand drums",
    "harmonium": "pump harmonium, keyboard instrument common in Afghan music",
    "tanbur": "long-necked lute, fretted string instrument",
    "dhol": "double-headed drum, used in folk and Attan",
    "surnai": "double-reed wind instrument, festive sound",
    "chang": "Afghan jaw harp",
    "ghichak": "bowed string instrument, spiked fiddle",
    "dutar": "two-stringed long-necked lute",
    "zerbaghali": "goblet drum, ceramic or wooden",
}

# Afghan decorative motifs and patterns
MOTIFS = {
    "gul": "traditional flower motifs from Afghan carpets (Turkmen, Baluch)",
    "boteh": "paisley-like motif, teardrop shape with curved top",
    "geometric": "interlocking geometric patterns, eight-pointed stars, hexagons",
    "islimi": "arabesque scrolling vine patterns",
    "medallion": "central medallion design from carpet traditions",
    "border_patterns": "repeated border motifs, running dog, reciprocal patterns",
    "tile_work": "geometric tile patterns inspired by Herat and Mazar shrines",
    "minaret": "architectural elements, minarets, domes, arches",
}

# Main style presets - enhanced with cultural specificity
STYLES = {
    "traditional": {
        "name": "Traditional Afghan (کلاسیک افغانی)",
        "description": "Classic Afghan music aesthetic with ornate details, suitable for classical and folk releases",
        "elements": [
            "ornate decorative borders inspired by Afghan carpet patterns (gul motifs)",
            "traditional Afghan geometric patterns and arabesque (islimi) designs",
            "rich gold leaf accents and deep jewel tones (ruby red, emerald green, lapis lazuli blue)",
            "elegant Nastaliq calligraphy for Dari/Pashto text",
            "classical instrument imagery: rubab, harmonium, tabla in artistic arrangement",
            "rich textures reminiscent of Turkmen and Baluch carpet weaving",
            "subtle background texture of Afghan silk or velvet fabric",
            "architectural elements: pointed arches, geometric tile patterns",
        ],
        "colors": "gold, burgundy red (#8B0000), emerald green (#046307), lapis lazuli blue (#26619C), ivory cream",
        "typography": "Nastaliq calligraphy for titles, clear Naskh for secondary text, gold or cream text colors",
        "mood": "dignified, timeless, culturally rich, respectful of heritage",
        "avoid": "neon colors, overly modern effects, culturally inappropriate imagery",
    },
    
    "modern": {
        "name": "Modern Afghan Pop (پاپ مدرن)",
        "description": "Contemporary Afghan pop music style for mainstream releases",
        "elements": [
            "clean minimal design with strategic negative space",
            "bold modern Persian/Dari typography (geometric sans-serif style)",
            "vibrant contemporary color gradients",
            "professional studio photography aesthetic, dramatic lighting",
            "sleek gradients and cinematic lighting effects",
            "urban polished aesthetic reflecting modern Kabul",
            "subtle Afghan pattern accents in modern treatment",
            "clean geometric shapes and lines",
        ],
        "colors": "electric blue (#0066FF), vibrant purple (#8B5CF6), sunset orange (#F97316), clean white, charcoal black",
        "typography": "bold modern Persian sans-serif, clean geometric Dari fonts, strong contrast",
        "mood": "confident, fresh, contemporary, professional",
        "avoid": "overly traditional elements, busy patterns, dated effects",
    },
    
    "fusion": {
        "name": "East-West Fusion (آمیزش شرق و غرب)",
        "description": "Blend of traditional Afghan and modern Western aesthetics for diaspora and international audiences",
        "elements": [
            "traditional Afghan motifs reimagined with modern graphic design",
            "gul and geometric patterns in contemporary color treatments",
            "bilingual typography hierarchy: Dari/Pashto prominent, English secondary",
            "blend of warm traditional gold with modern teal and coral",
            "cultural patterns integrated into minimal modern layouts",
            "sophisticated international appeal while honoring roots",
            "abstract interpretations of Afghan landscapes and architecture",
            "modern lighting with traditional subject matter",
        ],
        "colors": "warm gold (#D4AF37), modern teal (#14B8A6), coral (#F43F5E), cream, deep charcoal",
        "typography": "mixed Nastaliq headers with modern Naskh body, English in complementary sans-serif",
        "mood": "sophisticated, bridge between cultures, accessible yet authentic",
        "avoid": "stereotypical fusion clichés, disrespectful cultural mixing",
    },
    
    "romantic": {
        "name": "Romantic Ballad (عاشقانه)",
        "description": "Soft, emotional style for love songs and romantic ballads",
        "elements": [
            "soft dreamy atmosphere with gentle bokeh lighting",
            "warm romantic golden-hour lighting",
            "roses (گل سرخ) and traditional Afghan floral elements",
            "gentle pink and gold gradients",
            "intimate and emotional mood, subtle visual poetry",
            "elegant refined composition with soft focus elements",
            "delicate Nastaliq calligraphy with flourishes",
            "silk and velvet texture overlays",
        ],
        "colors": "soft rose pink (#FDA4AF), blush (#FFF1F2), warm gold (#F59E0B), cream, soft burgundy",
        "typography": "elegant Nastaliq script with romantic flourishes, delicate and flowing",
        "mood": "tender, emotional, intimate, poetic",
        "avoid": "harsh colors, aggressive typography, cold tones",
    },
    
    "folk": {
        "name": "Afghan Folk (محلی)",
        "description": "Rustic folk music aesthetic celebrating regional traditions",
        "elements": [
            "natural earthy textures: clay, wood grain, handwoven fabric",
            "Afghan mountain and valley landscape imagery (Hindu Kush, Pamir)",
            "traditional village life elements: chai, bread ovens, courtyards",
            "handcrafted authentic feel, artisanal quality",
            "warm nostalgic golden-hour atmosphere",
            "connection to Afghan homeland, ancestral villages",
            "folk instruments prominently featured: dhol, surnai, dutar",
            "natural materials and textures as backgrounds",
        ],
        "colors": "earth brown (#92400E), terracotta (#C2410C), wheat gold (#EAB308), sky blue (#38BDF8), sage green (#84CC16)",
        "typography": "handwritten feel, warm and authentic, slightly imperfect humanist touch",
        "mood": "nostalgic, grounded, authentic, connected to land and heritage",
        "avoid": "overly polished effects, urban aesthetics, synthetic textures",
    },
    
    "ghazal": {
        "name": "Ghazal Poetry (غزل)",
        "description": "Poetic and literary style for ghazal and classical vocal performances",
        "elements": [
            "poetic literary aesthetic inspired by Persian poetry traditions",
            "ink wash and calligraphy influences, brush stroke textures",
            "subtle sophisticated minimal design",
            "classical Persian/Dari poetry visual elements",
            "refined artistic sensibility, museum-quality presentation",
            "deep cultural and spiritual depth",
            "parchment and aged paper textures",
            "single rose or nightingale (بلبل) motif traditional to ghazal",
        ],
        "colors": "midnight blue (#1E3A5F), lampblack, gold leaf (#FFD700), aged cream (#F5F5DC), deep wine (#722F37)",
        "typography": "exquisite Nastaliq calligraphy, poetry-worthy letterforms, traditional proportions",
        "mood": "contemplative, poetic, spiritually deep, intellectually refined",
        "avoid": "loud colors, modern pop aesthetics, casual typography",
    },
    
    "sufi": {
        "name": "Sufi/Spiritual (صوفیانه)",
        "description": "Mystical and spiritual aesthetic for Sufi music and devotional songs",
        "elements": [
            "spiritual and mystical atmosphere, ethereal lighting",
            "whirling dervish silhouettes, sacred geometry",
            "geometric patterns representing divine order (eight-pointed stars)",
            "soft light rays and divine illumination effects",
            "shrine and mosque architectural elements (Mazar-i-Sharif Blue Mosque)",
            "muted ethereal color palette with gold accents",
            "calligraphic Allah, bismillah, or poetry elements",
            "incense smoke and candlelight atmosphere",
        ],
        "colors": "spiritual green (#065F46), deep blue (#1E40AF), gold (#D4AF37), soft white, muted purple (#6B21A8)",
        "typography": "flowing Nastaliq, Thuluth-style sacred calligraphy, respectful and devotional",
        "mood": "transcendent, peaceful, spiritually elevating, contemplative",
        "avoid": "flashy effects, inappropriate religious imagery, disrespectful treatment",
    },
    
    "wedding": {
        "name": "Wedding/Celebration (عروسی)",
        "description": "Festive celebratory style for wedding songs (Attan) and party music",
        "elements": [
            "joyful celebratory atmosphere, festive energy",
            "traditional Afghan wedding colors and decorations",
            "Attan dance silhouettes, circular dance formations",
            "festive instruments: dhol, surnai, zerbaghali",
            "henna patterns (مهندی) and bridal decorative elements",
            "sparkle and shimmer effects, celebratory lighting",
            "traditional embroidery and mirror-work patterns",
            "confetti and festive atmosphere",
        ],
        "colors": "bright red (#DC2626), gold (#EAB308), hot pink (#EC4899), emerald green (#10B981), royal purple (#7C3AED)",
        "typography": "festive, bold, celebratory Dari typography, joyful energy",
        "mood": "joyous, energetic, celebratory, festive",
        "avoid": "somber colors, minimalist aesthetics, sad imagery",
    },
    
    "patriotic": {
        "name": "Patriotic/Milli (ملی)",
        "description": "National pride aesthetic for patriotic and homeland songs",
        "elements": [
            "Afghan flag colors (black, red, green) tastefully integrated",
            "national symbols: wheat sheaves, mosque, rising sun",
            "Afghan landscape pride: Hindu Kush mountains, valleys",
            "historical architectural elements: Minaret of Jam, Bamiyan",
            "unity and strength visual metaphors",
            "dignified proud presentation",
            "map of Afghanistan as subtle background element",
            "national heroes and historical pride references",
        ],
        "colors": "Afghan flag black (#000000), red (#BE0000), green (#007A36), gold accent (#FFD700)",
        "typography": "strong, dignified Dari typography, powerful but respectful",
        "mood": "proud, dignified, unified, hopeful",
        "avoid": "political divisiveness, inappropriate nationalism, dated propaganda style",
    },
    
    "hiphop": {
        "name": "Afghan Hip-Hop (هیپ هاپ)",
        "description": "Urban street style for Afghan rap and hip-hop artists",
        "elements": [
            "urban street aesthetic with Afghan cultural elements",
            "bold graffiti-inspired typography mixing Dari and English",
            "gritty textures, concrete and street art backgrounds",
            "modern Kabul or diaspora city imagery",
            "bold contrast and dramatic lighting",
            "youth culture energy, rebellious but respectful",
            "chain and streetwear elements with cultural twist",
            "spray paint and stencil effects",
        ],
        "colors": "black, bright yellow (#FBBF24), neon green (#22C55E), white, accent red",
        "typography": "bold graffiti-style, mixed Dari/English, street art influence",
        "mood": "bold, youthful, urban, authentic street culture",
        "avoid": "inappropriate cultural disrespect, gang imagery, offensive content",
    },
    
    "acoustic": {
        "name": "Acoustic/Unplugged (آکوستیک)",
        "description": "Intimate acoustic performance aesthetic for unplugged recordings",
        "elements": [
            "warm intimate setting, studio or living room feel",
            "natural wood textures, acoustic instruments prominent",
            "soft warm lighting, candle or lamp-light atmosphere",
            "minimal and focused composition",
            "authentic and raw emotional quality",
            "close-up instrument details: rubab strings, guitar frets",
            "cozy atmosphere, personal and intimate",
            "analog and handmade aesthetic",
        ],
        "colors": "warm wood brown (#A16207), cream (#FFFBEB), soft amber (#F59E0B), charcoal (#374151), soft white",
        "typography": "understated, warm serif or humanist sans, intimate and personal",
        "mood": "intimate, authentic, warm, personal",
        "avoid": "flashy effects, large scale imagery, stadium aesthetics",
    },
}

# Regional style variations - enhanced with specific visual elements
REGIONAL_STYLES = {
    "kabuli": {
        "name": "Kabul Style (کابلی)",
        "modifier": "urban cosmopolitan polished aesthetic, modern Kabul sophistication",
        "visual_elements": [
            "Kabul cityscape elements, Bala Hissar fort",
            "urban Afghan sophistication, educated cosmopolitan",
            "blend of traditional and modern architecture",
            "contemporary urban fashion mixed with traditional",
        ],
        "colors": "sophisticated greys, modern blues, urban palette",
    },
    "herati": {
        "name": "Herat Style (هراتی)", 
        "modifier": "artistic poetic classical Persian influences, refined Timurid heritage",
        "visual_elements": [
            "Herat Friday Mosque minarets and tile work",
            "miniature painting influences, Persian artistic tradition",
            "poetry and literature references, Jami and Rumi",
            "exquisite tile patterns, turquoise and cobalt blue",
        ],
        "colors": "turquoise blue, cobalt, gold, refined Persian palette",
    },
    "kandahari": {
        "name": "Kandahar Style (کندهاری)",
        "modifier": "bold strong traditional Pashtun aesthetic, powerful and proud",
        "visual_elements": [
            "Pashtun cultural pride, tribal patterns",
            "bold strong typography, masculine energy",
            "pomegranate (انار) - Kandahar is famous for them",
            "desert landscape, southern Afghan aesthetics",
        ],
        "colors": "bold red, black, gold, earth tones, strong contrast",
    },
    "mazari": {
        "name": "Mazar-i-Sharif Style (مزاری)",
        "modifier": "colorful festive Turkic Uzbek influences, vibrant Nowruz celebration",
        "visual_elements": [
            "Blue Mosque (Rawza) shrine imagery",
            "Nowruz celebration, Mela-e-Gul-e-Surkh (red tulip festival)",
            "buzkashi horse game imagery",
            "Uzbek and Turkmen textile patterns, vibrant colors",
        ],
        "colors": "shrine blue, bright festive colors, Turkic vibrancy",
    },
    "panjshiri": {
        "name": "Panjshir Style (پنجشیری)",
        "modifier": "mountain majesty natural beauty, proud Panjshir Valley heritage",
        "visual_elements": [
            "dramatic mountain landscapes, Panjshir Valley",
            "emerald river and green valleys",
            "proud Tajik heritage, resistance legacy",
            "natural unspoiled beauty, precious gems (emeralds)",
        ],
        "colors": "emerald green, mountain grey, river blue, natural palette",
    },
    "badakhshi": {
        "name": "Badakhshan Style (بدخشی)",
        "modifier": "high mountain Pamiri aesthetic, precious gems and remote beauty",
        "visual_elements": [
            "Pamir mountains, high altitude landscapes",
            "lapis lazuli blue, ruby red (Badakhshan gems)",
            "Pamiri and Ismaili cultural elements",
            "river valleys, remote pristine nature",
        ],
        "colors": "lapis lazuli blue, ruby red, snow white, mountain palette",
    },
    "hazaragi": {
        "name": "Hazara Style (هزاره‌گی)",
        "modifier": "Hazara cultural aesthetic, Bamiyan heritage, resilient beauty",
        "visual_elements": [
            "Bamiyan valley landscapes, Buddha niche silhouettes",
            "Band-e-Amir lakes, turquoise waters",
            "Hazara textile patterns, distinctive embroidery",
            "dambura instrument, Hazara folk traditions",
        ],
        "colors": "turquoise, mountain earth tones, distinctive red accents",
    },
    "nuristani": {
        "name": "Nuristan Style (نورستانی)",
        "modifier": "mountainous forest aesthetic, unique Nuristani heritage",
        "visual_elements": [
            "forested mountain valleys, unique alpine setting",
            "carved wooden architecture, traditional Nuristani buildings",
            "distinctive Nuristani textile and carving patterns",
            "isolated pristine mountain culture",
        ],
        "colors": "forest green, wood brown, mountain blue",
    },
}

# Seasonal and occasion modifiers
OCCASIONS = {
    "nowruz": {
        "name": "Nowruz (نوروز)",
        "elements": "Haft Mewa, spring flowers, red tulips, renewal symbolism, Samanak",
        "colors": "spring green, yellow, pink cherry blossoms, fresh vibrant",
    },
    "eid": {
        "name": "Eid (عید)",
        "elements": "crescent moon, festive decorations, family celebration, sweets",
        "colors": "gold, green, festive whites, elegant celebration",
    },
    "independence": {
        "name": "Independence Day (استقلال)",
        "elements": "Afghan flag, national pride, historical celebration",
        "colors": "black, red, green (Afghan flag colors)",
    },
    "winter": {
        "name": "Winter/Zemestaani (زمستانی)",
        "elements": "snow-capped Hindu Kush, warm indoor scenes, bokhari stove",
        "colors": "cool blues, warm interior gold, snow white",
    },
}


def build_style_prompt(style_name, regional=None, occasion=None, custom_elements=None, include_typography=True):
    """
    Build a comprehensive style prompt string from style definitions.
    
    Args:
        style_name: One of the STYLES keys (traditional, modern, fusion, etc.)
        regional: Optional regional modifier (kabuli, herati, etc.)
        occasion: Optional occasion modifier (nowruz, eid, etc.)
        custom_elements: Optional list of additional style elements
        include_typography: Whether to include typography guidance (default True)
    
    Returns:
        A formatted style prompt string optimized for image generation
    """
    if style_name not in STYLES:
        raise ValueError(f"Unknown style: {style_name}. Available: {list(STYLES.keys())}")
    
    style = STYLES[style_name]
    
    # Start with base quality
    parts = [BASE_STYLE["quality"], BASE_STYLE["composition"]]
    
    # Add style name for context
    parts.append(f"Style: {style['name']}")
    
    # Add style elements (limit to most important for prompt efficiency)
    parts.extend(style["elements"][:6])  # Top 6 elements
    
    # Add color palette
    parts.append(f"Color palette: {style['colors']}")
    
    # Add mood
    parts.append(f"Mood: {style['mood']}")
    
    # Add typography guidance if requested
    if include_typography:
        parts.append(f"Typography: {style['typography']}")
    
    # Add regional modifier if specified
    if regional and regional in REGIONAL_STYLES:
        reg = REGIONAL_STYLES[regional]
        parts.append(reg["modifier"])
        # Add one key visual element
        if reg.get("visual_elements"):
            parts.append(reg["visual_elements"][0])
    
    # Add occasion modifier if specified
    if occasion and occasion in OCCASIONS:
        occ = OCCASIONS[occasion]
        parts.append(f"{occ['name']} theme: {occ['elements']}")
    
    # Add custom elements
    if custom_elements:
        parts.extend(custom_elements)
    
    # Add what to avoid
    if style.get("avoid"):
        parts.append(f"Avoid: {style['avoid']}")
    
    # Add format and cultural authenticity
    parts.append(BASE_STYLE["format"])
    parts.append(BASE_STYLE["cultural"])
    
    return ". ".join(parts) + "."


def get_style_names():
    """Return list of available style names."""
    return list(STYLES.keys())


def get_regional_names():
    """Return list of available regional style names."""
    return list(REGIONAL_STYLES.keys())


def get_occasion_names():
    """Return list of available occasion names."""
    return list(OCCASIONS.keys())


def describe_style(style_name):
    """Return a detailed description of a style."""
    if style_name in STYLES:
        s = STYLES[style_name]
        return f"{s['name']}: {s['description']}\nMood: {s['mood']}\nColors: {s['colors']}"
    return None


def get_instruments():
    """Return dictionary of Afghan instruments with descriptions."""
    return INSTRUMENTS


def get_motifs():
    """Return dictionary of Afghan decorative motifs."""
    return MOTIFS


def get_typography_guide():
    """Return typography guidance for Dari/Pashto text."""
    return TYPOGRAPHY_GUIDE
