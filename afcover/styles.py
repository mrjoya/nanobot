"""
Afghan Music Cover Art Styles

Defines visual styles specific to Afghan music industry aesthetics.
"""

# Base style elements common to all Afghan music covers
BASE_STYLE = {
    "quality": "professional album cover art, high resolution, print-ready",
    "composition": "centered composition, balanced layout",
    "format": "square format suitable for music streaming platforms",
}

# Main style presets
STYLES = {
    "traditional": {
        "name": "Traditional Afghan",
        "description": "Classic Afghan music aesthetic with ornate details",
        "elements": [
            "ornate decorative borders and frames",
            "traditional Afghan patterns and motifs",
            "gold accents and deep jewel tones (ruby red, emerald green, sapphire blue)",
            "elegant Dari/Pashto calligraphy style",
            "classical instrument imagery (rubab, tabla, harmonium)",
            "rich textures reminiscent of Afghan carpets and textiles",
        ],
        "colors": "gold, deep red, emerald green, royal blue, burgundy",
        "typography": "ornate, calligraphic, traditional",
    },
    
    "modern": {
        "name": "Modern Afghan Pop",
        "description": "Contemporary Afghan pop music style",
        "elements": [
            "clean minimal design",
            "bold modern typography",
            "vibrant contemporary colors",
            "professional studio photography style",
            "sleek gradients and lighting effects",
            "urban and polished aesthetic",
        ],
        "colors": "vibrant blues, purples, oranges, clean whites",
        "typography": "bold sans-serif, clean, modern",
    },
    
    "fusion": {
        "name": "East-West Fusion",
        "description": "Blend of traditional Afghan and modern Western aesthetics",
        "elements": [
            "traditional motifs with modern treatment",
            "cultural patterns in contemporary layouts",
            "bilingual typography (Dari/Pashto + English)",
            "blend of classic and modern color palettes",
            "respectful fusion of East and West design",
            "sophisticated and international appeal",
        ],
        "colors": "warm golds, modern teals, balanced earth tones",
        "typography": "mixed traditional and modern fonts",
    },
    
    "romantic": {
        "name": "Romantic Ballad",
        "description": "Soft, emotional style for love songs and ballads",
        "elements": [
            "soft dreamy atmosphere",
            "warm romantic lighting",
            "roses and floral elements",
            "gentle gradients and bokeh effects",
            "intimate and emotional mood",
            "elegant and refined composition",
        ],
        "colors": "soft pinks, warm reds, cream, gold highlights",
        "typography": "elegant script, romantic serif",
    },
    
    "folk": {
        "name": "Afghan Folk",
        "description": "Rustic folk music aesthetic",
        "elements": [
            "natural earthy textures",
            "mountain and landscape imagery",
            "traditional village life elements",
            "handcrafted authentic feel",
            "warm nostalgic atmosphere",
            "connection to Afghan heritage and homeland",
        ],
        "colors": "earth tones, warm browns, sunset oranges, sky blues",
        "typography": "handwritten feel, authentic, grounded",
    },
    
    "ghazal": {
        "name": "Ghazal Poetry",
        "description": "Poetic and artistic style for ghazal performances",
        "elements": [
            "poetic and literary aesthetic",
            "ink and calligraphy influences",
            "subtle and sophisticated design",
            "classical Persian/Dari poetry elements",
            "refined artistic sensibility",
            "cultural depth and meaning",
        ],
        "colors": "deep blues, blacks, gold accents, cream",
        "typography": "beautiful Nastaliq calligraphy, poetic",
    },
}

# Regional style variations
REGIONAL_STYLES = {
    "kabuli": {
        "name": "Kabul Style",
        "modifier": "urban, cosmopolitan, polished, modern Kabul aesthetic",
    },
    "herati": {
        "name": "Herat Style", 
        "modifier": "artistic, poetic, classical Persian influences, refined",
    },
    "kandahari": {
        "name": "Kandahar Style",
        "modifier": "bold, strong, traditional Pashtun aesthetic, powerful",
    },
    "mazari": {
        "name": "Mazar-i-Sharif Style",
        "modifier": "colorful, festive, Turkic influences, vibrant celebration",
    },
    "panjshiri": {
        "name": "Panjshir Style",
        "modifier": "mountain imagery, natural beauty, proud heritage",
    },
}


def build_style_prompt(style_name, regional=None, custom_elements=None):
    """
    Build a style prompt string from style definitions.
    
    Args:
        style_name: One of the STYLES keys (traditional, modern, fusion, etc.)
        regional: Optional regional modifier (kabuli, herati, etc.)
        custom_elements: Optional list of additional style elements
    
    Returns:
        A formatted style prompt string
    """
    if style_name not in STYLES:
        raise ValueError(f"Unknown style: {style_name}. Available: {list(STYLES.keys())}")
    
    style = STYLES[style_name]
    
    # Start with base quality
    parts = [BASE_STYLE["quality"], BASE_STYLE["composition"]]
    
    # Add style elements
    parts.extend(style["elements"])
    
    # Add color palette
    parts.append(f"Color palette: {style['colors']}")
    
    # Add typography style
    parts.append(f"Typography: {style['typography']}")
    
    # Add regional modifier if specified
    if regional and regional in REGIONAL_STYLES:
        parts.append(REGIONAL_STYLES[regional]["modifier"])
    
    # Add custom elements
    if custom_elements:
        parts.extend(custom_elements)
    
    # Add format
    parts.append(BASE_STYLE["format"])
    
    return ". ".join(parts) + "."


def get_style_names():
    """Return list of available style names."""
    return list(STYLES.keys())


def get_regional_names():
    """Return list of available regional style names."""
    return list(REGIONAL_STYLES.keys())


def describe_style(style_name):
    """Return a description of a style."""
    if style_name in STYLES:
        s = STYLES[style_name]
        return f"{s['name']}: {s['description']}"
    return None
