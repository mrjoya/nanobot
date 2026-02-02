"""
Afghan Cover Art Generator

Core generation logic for creating Afghan music cover art
using reference images and style presets.

Optimized for cultural authenticity and high-quality results
for the Afghan music industry.
"""

import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.api import edit_image, download_image, prepare_image_urls, estimate_cost
from shared.cost_control import safe_api_call, track_cost, cost_confirmation
from afcover.styles import (
    build_style_prompt, 
    STYLES, 
    REGIONAL_STYLES,
    OCCASIONS,
    TYPOGRAPHY_GUIDE,
    INSTRUMENTS,
    get_style_names,
    get_regional_names,
    get_occasion_names,
)


# Prompt engineering templates for better results
PROMPT_TEMPLATES = {
    "album_cover": (
        "Professional music album cover art. "
        "Square format, suitable for streaming platforms (Spotify, Apple Music). "
        "High resolution, print-ready quality. "
    ),
    
    "single_cover": (
        "Professional single release cover art. "
        "Eye-catching design for digital streaming. "
        "Bold and memorable visual impact. "
    ),
    
    "ep_cover": (
        "Extended play (EP) album cover art. "
        "Cohesive design suitable for multi-track release. "
        "Professional quality for streaming and download platforms. "
    ),
}

# Cultural authenticity guidelines embedded in prompts
CULTURAL_GUIDELINES = (
    "Culturally authentic Afghan aesthetic. "
    "Respectful representation of Afghan heritage and traditions. "
    "Appropriate for Afghan music industry standards. "
    "No stereotypical or orientalist imagery. "
)

# Typography placement hints for Dari/Pashto
TYPOGRAPHY_HINTS = {
    "title_prominent": (
        "Leave clear space for large title text placement. "
        "Upper third suitable for Dari/Pashto title in Nastaliq or modern Persian typography. "
    ),
    "title_bottom": (
        "Title area at bottom third of composition. "
        "Clean space for right-to-left Dari/Pashto text. "
    ),
    "minimal_text": (
        "Design accommodates minimal text overlay. "
        "Artist name and title can be added post-production. "
    ),
    "integrated_calligraphy": (
        "Integrate calligraphic elements into the design. "
        "Nastaliq or artistic Dari text as design element. "
    ),
}


class AfghanCoverGenerator:
    """
    Generator for Afghan music cover art.
    
    Uses reference images and style presets to create
    professional album covers for Afghan music.
    
    Features:
    - Culturally authentic Afghan styles
    - Regional variations (Kabuli, Herati, Kandahari, etc.)
    - Occasion-specific themes (Nowruz, Eid, Wedding)
    - Dari/Pashto typography considerations
    - Professional quality for streaming platforms
    """
    
    def __init__(self, output_dir="."):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate(
        self,
        reference_images,
        title=None,
        artist=None,
        style="traditional",
        regional=None,
        occasion=None,
        release_type="album",
        text_placement="title_prominent",
        custom_prompt=None,
        negative_prompt=None,
        resolution="1K",
        num_variations=1,
        output_format="png",
        seed=None,
        limit_generations=True,
        dry_run=False,
    ):
        """
        Generate Afghan music cover art.
        
        Args:
            reference_images: List of reference image paths/URLs
            title: Album/single title (optional, for prompt context)
            artist: Artist name (optional, for prompt context)
            style: Style preset (traditional, modern, fusion, romantic, folk, 
                   ghazal, sufi, wedding, patriotic, hiphop, acoustic)
            regional: Regional modifier (kabuli, herati, kandahari, mazari, 
                      panjshiri, badakhshi, hazaragi, nuristani)
            occasion: Occasion theme (nowruz, eid, independence, winter)
            release_type: Type of release (album, single, ep) - affects prompt
            text_placement: Typography placement hint (title_prominent, title_bottom,
                           minimal_text, integrated_calligraphy)
            custom_prompt: Additional custom prompt instructions
            negative_prompt: What to avoid (added to style's avoid list)
            resolution: Output resolution (1K, 2K, 4K) - 4K costs 2x!
            num_variations: Number of variations to generate (1-4)
            output_format: "png" (default), "jpeg" (smaller), "webp"
            seed: Random seed for reproducibility (optional)
            limit_generations: Prevent prompt injection (default True, RECOMMENDED)
            dry_run: If True, only return cost estimate without generating
        
        Returns:
            dict with generated image paths and metadata
        
        Cost:
            - 1K/2K: $0.15 per image
            - 4K: $0.30 per image
            - Total = cost_per_image × num_variations
        """
        
        # Validate inputs
        if not reference_images:
            raise ValueError("At least one reference image is required")
        
        if style not in STYLES:
            available = get_style_names()
            raise ValueError(f"Unknown style: {style}. Available: {available}")
        
        if regional and regional not in REGIONAL_STYLES:
            available = get_regional_names()
            raise ValueError(f"Unknown regional style: {regional}. Available: {available}")
        
        if occasion and occasion not in OCCASIONS:
            available = get_occasion_names()
            raise ValueError(f"Unknown occasion: {occasion}. Available: {available}")
        
        if num_variations < 1 or num_variations > 4:
            raise ValueError("num_variations must be between 1 and 4")
        
        if text_placement not in TYPOGRAPHY_HINTS:
            raise ValueError(f"Unknown text_placement: {text_placement}. "
                           f"Available: {list(TYPOGRAPHY_HINTS.keys())}")
        
        # Calculate estimated cost
        estimated_cost = estimate_cost(num_variations, resolution)
        
        # If dry_run, just return cost estimate
        if dry_run:
            prompt_preview = self._build_prompt(
                style=style,
                regional=regional,
                occasion=occasion,
                release_type=release_type,
                text_placement=text_placement,
                title=title,
                artist=artist,
                custom_prompt=custom_prompt,
                negative_prompt=negative_prompt,
            )
            return {
                "dry_run": True,
                "estimated_cost": f"${estimated_cost:.2f}",
                "num_images": num_variations,
                "resolution": resolution,
                "style": style,
                "regional": regional,
                "occasion": occasion,
                "prompt_preview": prompt_preview[:500] + "..." if len(prompt_preview) > 500 else prompt_preview,
                "message": f"Would generate {num_variations} image(s) at {resolution} for ${estimated_cost:.2f}"
            }
        
        # Build the prompt
        prompt = self._build_prompt(
            style=style,
            regional=regional,
            occasion=occasion,
            release_type=release_type,
            text_placement=text_placement,
            title=title,
            artist=artist,
            custom_prompt=custom_prompt,
            negative_prompt=negative_prompt,
        )
        
        # Call the API with all cost-control parameters
        # Make sure reference_images are properly processed
        prepared_references = []
        for ref in reference_images:
            if isinstance(ref, str):
                prepared_references.append(ref)
            else:
                # Handle other types if needed
                prepared_references.append(str(ref))
                
        result = edit_image(
            prompt=prompt,
            image_urls=prepared_references,
            resolution=resolution,
            aspect_ratio="1:1",  # Album covers are square
            num_images=num_variations,
            output_format=output_format,
            seed=seed,
            limit_generations=limit_generations,
            enable_web_search=False,
        )
        
        # Download and save images
        downloaded = []
        
        # Handle both direct and queued response formats
        if "images" in result:
            images = result.get("images", [])
        else:
            # Log the unexpected response format
            print(f"Unexpected response format: {result}")
            # Try to handle queued responses
            if "status" in result and result["status"] == "IN_QUEUE":
                print("Request is queued. This should have been handled by the API layer.")
            images = []
        
        for i, img in enumerate(images):
            url = img.get("url")
            if url:
                # Generate descriptive filename
                safe_title = self._safe_filename(title or "cover")
                safe_artist = self._safe_filename(artist or "artist")
                timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
                suffix = f"-{i+1}" if len(images) > 1 else ""
                
                filename = f"afcover-{safe_artist}-{safe_title}-{style}-{timestamp}{suffix}.png"
                output_path = self.output_dir / filename
                
                try:
                    downloaded_path = download_image(url, output_path)
                    downloaded.append(str(output_path.absolute()))
                    print(f"Downloaded image to: {downloaded_path}")
                except Exception as e:
                    print(f"Error downloading image from {url}: {e}")
                    # Continue with other images if any
        
        # Calculate actual cost
        cost = 0.15 * len(downloaded)
        if resolution == "4K":
            cost *= 2
        
        return {
            "success": True,
            "title": title,
            "artist": artist,
            "style": style,
            "regional": regional,
            "occasion": occasion,
            "prompt": prompt,
            "resolution": resolution,
            "images": downloaded,
            "count": len(downloaded),
            "cost": f"${cost:.2f}",
        }
    
    def _build_prompt(
        self, 
        style, 
        regional, 
        occasion,
        release_type,
        text_placement,
        title, 
        artist, 
        custom_prompt,
        negative_prompt,
    ):
        """
        Build the complete prompt for generation.
        
        Prompt structure (optimized order for best results):
        1. Release type and format
        2. Style elements and mood
        3. Cultural authenticity guidelines
        4. Reference image instructions
        5. Title/artist context
        6. Typography and text placement
        7. Quality requirements
        8. Negative prompts (what to avoid)
        """
        
        parts = []
        
        # 1. Release type template
        release_template = PROMPT_TEMPLATES.get(
            f"{release_type}_cover", 
            PROMPT_TEMPLATES["album_cover"]
        )
        parts.append(release_template)
        
        # 2. Style prompt (includes elements, colors, mood, typography, regional, occasion)
        style_prompt = build_style_prompt(
            style, 
            regional=regional, 
            occasion=occasion,
            include_typography=True,
        )
        parts.append(style_prompt)
        
        # 3. Cultural authenticity
        parts.append(CULTURAL_GUIDELINES)
        
        # 4. Reference image instructions
        parts.append(
            "Use the provided reference images as visual style guide. "
            "Maintain consistency with the reference artwork aesthetic. "
            "Create a unique cover inspired by but not copying the references. "
        )
        
        # 5. Title/artist context (helps with mood and theme)
        if title:
            # Transliterate common Dari words for the AI to understand mood
            title_context = self._extract_title_mood(title)
            parts.append(f'Album title: "{title}". {title_context}')
        if artist:
            parts.append(f'For artist: {artist}.')
        
        # 6. Typography and text placement hints
        parts.append(TYPOGRAPHY_HINTS.get(text_placement, TYPOGRAPHY_HINTS["title_prominent"]))
        parts.append(
            "Design should accommodate right-to-left Dari/Pashto text. "
            "Consider Nastaliq calligraphy style for traditional genres, "
            "modern Persian typography for contemporary styles. "
        )
        
        # 7. Custom prompt additions
        if custom_prompt:
            parts.append(custom_prompt)
        
        # 8. Quality finisher
        parts.append(
            "Exceptional quality, professional result. "
            "Suitable for Spotify, Apple Music, YouTube Music. "
            "Clean, polished, industry-standard album artwork. "
            "No watermarks, no text unless specifically requested. "
        )
        
        # 9. Negative prompt / what to avoid
        avoid_parts = []
        if negative_prompt:
            avoid_parts.append(negative_prompt)
        # Add style-specific avoids
        style_avoid = STYLES.get(style, {}).get("avoid")
        if style_avoid:
            avoid_parts.append(style_avoid)
        # Add general avoids
        avoid_parts.append(
            "blurry, low quality, amateur, watermarks, text errors, "
            "culturally inappropriate, stereotypical orientalist imagery"
        )
        
        parts.append(f"Avoid: {', '.join(avoid_parts)}")
        
        return " ".join(parts)
    
    def _extract_title_mood(self, title):
        """
        Extract mood hints from title for better generation.
        Common Dari/Pashto words that indicate mood.
        """
        title_lower = title.lower()
        
        mood_keywords = {
            # Romantic/Love
            "عشق": "romantic love theme",
            "دل": "heart, emotional theme",
            "ishq": "romantic love theme",
            "mohabbat": "love theme",
            "dil": "heart, emotional theme",
            "yar": "beloved, romantic theme",
            "جانان": "beloved, romantic theme",
            
            # Sadness/Longing
            "غم": "melancholic, sad theme",
            "gham": "sadness, melancholy",
            "تنها": "loneliness theme",
            "دوری": "separation, longing theme",
            "اشک": "tears, emotional theme",
            
            # Homeland/Patriotic
            "وطن": "homeland, patriotic theme",
            "watan": "homeland theme",
            "افغان": "Afghan pride theme",
            "کابل": "Kabul, hometown theme",
            "kabul": "Kabul city theme",
            
            # Celebration
            "عروسی": "wedding celebration theme",
            "شادی": "joy, celebration theme",
            "مبارک": "blessing, celebration",
            "عید": "Eid celebration theme",
            
            # Nature
            "بهار": "spring theme",
            "bahar": "spring theme",
            "گل": "flower theme",
            "کوه": "mountain theme",
            
            # Spiritual
            "خدا": "spiritual, devotional theme",
            "عشق الهی": "divine love, Sufi theme",
        }
        
        for keyword, mood in mood_keywords.items():
            if keyword in title_lower:
                return f"({mood})"
        
        return ""
    
    def _safe_filename(self, text):
        """Convert text to a safe filename component."""
        if not text:
            return "untitled"
        # Keep ASCII alphanumeric and basic punctuation
        safe = "".join(c if c.isalnum() or c in "- " else "" for c in text)
        return safe.replace(" ", "-").lower()[:30] or "untitled"


def generate_cover(
    reference_images,
    title=None,
    artist=None,
    style="traditional",
    regional=None,
    occasion=None,
    release_type="album",
    text_placement="title_prominent",
    custom_prompt=None,
    negative_prompt=None,
    resolution="1K",
    num_variations=1,
    output_format="png",
    seed=None,
    limit_generations=True,
    dry_run=False,
    output_dir=".",
):
    """
    Convenience function for generating Afghan music cover art.
    
    This is the main entry point for cover generation.
    
    Args:
        reference_images: List of reference image paths/URLs (required)
        title: Album/single title (helps with mood, optional)
        artist: Artist name (optional)
        style: Style preset - one of:
            - traditional: Classic Afghan, ornate, Nastaliq calligraphy
            - modern: Contemporary pop, clean, bold
            - fusion: East-West blend, bilingual, sophisticated
            - romantic: Soft, emotional, ballads
            - folk: Rustic, earthy, homeland nostalgia
            - ghazal: Poetic, literary, classical
            - sufi: Spiritual, mystical, devotional
            - wedding: Festive, celebratory, Attan
            - patriotic: National pride, Afghan colors
            - hiphop: Urban, street, bold typography
            - acoustic: Intimate, warm, unplugged
        regional: Regional modifier - one of:
            - kabuli: Urban, cosmopolitan
            - herati: Artistic, Persian influence
            - kandahari: Bold, Pashtun aesthetic
            - mazari: Colorful, Turkic influence
            - panjshiri: Mountain majesty
            - badakhshi: High mountain, gem colors
            - hazaragi: Bamiyan heritage
            - nuristani: Forest mountain aesthetic
        occasion: Occasion theme (nowruz, eid, independence, winter)
        release_type: album, single, or ep
        text_placement: Where to leave space for text
            - title_prominent: Upper third clear
            - title_bottom: Bottom third clear
            - minimal_text: Minimal overlay space
            - integrated_calligraphy: Calligraphy as design element
        custom_prompt: Additional instructions
        negative_prompt: What to avoid
        resolution: 1K (default), 2K, or 4K (costs 2x)
        num_variations: 1-4 (each costs $0.15 or $0.30 for 4K)
        output_format: png (default), jpeg, webp
        seed: Random seed for reproducibility
        limit_generations: Prevent prompt injection (default True)
        dry_run: Only return cost estimate
        output_dir: Where to save outputs
    
    Returns:
        dict with results including:
        - success: bool
        - images: list of file paths
        - count: number of images
        - cost: dollar cost
        - prompt: the full prompt used
    
    Example:
        result = generate_cover(
            reference_images=["artist_photo.jpg", "style_reference.png"],
            title="دل تنها",
            artist="احمد ظاهر",
            style="romantic",
            regional="kabuli",
            num_variations=2,
        )
        print(result["images"])
    
    Cost: $0.15/image (1K/2K), $0.30/image (4K)
    """
    generator = AfghanCoverGenerator(output_dir=output_dir)
    return generator.generate(
        reference_images=reference_images,
        title=title,
        artist=artist,
        style=style,
        regional=regional,
        occasion=occasion,
        release_type=release_type,
        text_placement=text_placement,
        custom_prompt=custom_prompt,
        negative_prompt=negative_prompt,
        resolution=resolution,
        num_variations=num_variations,
        output_format=output_format,
        seed=seed,
        limit_generations=limit_generations,
        dry_run=dry_run,
    )


def list_styles():
    """Print all available styles with descriptions."""
    print("\n🎵 Afghan Cover Art Styles\n")
    print("=" * 50)
    for name, style in STYLES.items():
        print(f"\n{name}: {style['name']}")
        print(f"  {style['description']}")
        print(f"  Mood: {style['mood']}")
        print(f"  Colors: {style['colors'][:50]}...")
    print("\n")


def list_regional():
    """Print all available regional styles."""
    print("\n🏔️ Regional Style Modifiers\n")
    print("=" * 50)
    for name, style in REGIONAL_STYLES.items():
        print(f"\n{name}: {style['name']}")
        print(f"  {style['modifier']}")
    print("\n")
