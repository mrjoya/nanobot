"""
Afghan Cover Art Generator

Core generation logic for creating Afghan music cover art
using reference images and style presets.
"""

import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.api import edit_image, download_image, prepare_image_urls, estimate_cost
from afcover.styles import build_style_prompt, STYLES, get_style_names


class AfghanCoverGenerator:
    """
    Generator for Afghan music cover art.
    
    Uses reference images and style presets to create
    professional album covers for Afghan music.
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
        custom_prompt=None,
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
            style: Style preset name (traditional, modern, fusion, etc.)
            regional: Regional style modifier (kabuli, herati, etc.)
            custom_prompt: Additional custom prompt instructions
            resolution: Output resolution (1K, 2K, 4K) - 4K costs 2x!
            num_variations: Number of variations to generate (1-4)
            output_format: "png" (default), "jpeg" (smaller files), "webp"
            seed: Random seed for reproducibility (optional)
            limit_generations: Prevent prompt from requesting more images (default True, RECOMMENDED)
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
            raise ValueError(f"Unknown style: {style}. Available: {get_style_names()}")
        
        if num_variations < 1 or num_variations > 4:
            raise ValueError("num_variations must be between 1 and 4")
        
        # Calculate estimated cost
        estimated_cost = estimate_cost(num_variations, resolution)
        
        # If dry_run, just return cost estimate
        if dry_run:
            return {
                "dry_run": True,
                "estimated_cost": f"${estimated_cost:.2f}",
                "num_images": num_variations,
                "resolution": resolution,
                "message": f"Would generate {num_variations} image(s) at {resolution} for ${estimated_cost:.2f}"
            }
        
        # Build the prompt
        prompt = self._build_prompt(
            style=style,
            regional=regional,
            title=title,
            artist=artist,
            custom_prompt=custom_prompt,
        )
        
        # Call the API with all cost-control parameters
        result = edit_image(
            prompt=prompt,
            image_urls=reference_images,
            resolution=resolution,
            aspect_ratio="1:1",  # Album covers are square
            num_images=num_variations,
            output_format=output_format,
            seed=seed,
            limit_generations=limit_generations,  # Prevent prompt injection
            enable_web_search=False,  # Not needed, saves potential costs
        )
        
        # Download and save images
        downloaded = []
        images = result.get("images", [])
        
        for i, img in enumerate(images):
            url = img.get("url")
            if url:
                # Generate filename
                safe_title = self._safe_filename(title or "cover")
                safe_artist = self._safe_filename(artist or "artist")
                timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
                suffix = f"-{i+1}" if len(images) > 1 else ""
                
                filename = f"afcover-{safe_artist}-{safe_title}-{timestamp}{suffix}.png"
                output_path = self.output_dir / filename
                
                download_image(url, output_path)
                downloaded.append(str(output_path.absolute()))
        
        # Calculate cost
        cost = 0.15 * len(downloaded)
        if resolution == "4K":
            cost *= 2
        
        return {
            "title": title,
            "artist": artist,
            "style": style,
            "regional": regional,
            "prompt": prompt,
            "resolution": resolution,
            "images": downloaded,
            "count": len(downloaded),
            "cost": f"${cost:.2f}",
        }
    
    def _build_prompt(self, style, regional, title, artist, custom_prompt):
        """Build the complete prompt for generation."""
        
        parts = []
        
        # Start with style prompt
        style_prompt = build_style_prompt(style, regional)
        parts.append(style_prompt)
        
        # Add title/artist context if provided
        if title:
            parts.append(f'Create album cover for "{title}"')
        if artist:
            parts.append(f'Artist: {artist}')
        
        # Core instructions for reference-based generation
        parts.append(
            "Use the provided reference images as style guide. "
            "Maintain visual consistency with the reference artwork. "
            "Create a unique cover that matches the style and quality of the references."
        )
        
        # Afghan music specific instructions
        parts.append(
            "This is for Afghan music. "
            "Ensure cultural authenticity and respect for Afghan aesthetics. "
            "Typography should accommodate Dari/Pashto text if needed."
        )
        
        # Add custom prompt if provided
        if custom_prompt:
            parts.append(custom_prompt)
        
        # Quality finisher
        parts.append(
            "High quality, professional result. "
            "Suitable for streaming platforms and print. "
            "No watermarks."
        )
        
        return " ".join(parts)
    
    def _safe_filename(self, text):
        """Convert text to a safe filename component."""
        if not text:
            return "untitled"
        safe = "".join(c if c.isalnum() or c in "- " else "" for c in text)
        return safe.replace(" ", "-").lower()[:30]


def generate_cover(
    reference_images,
    title=None,
    artist=None,
    style="traditional",
    regional=None,
    custom_prompt=None,
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
    
    Args:
        reference_images: List of reference image paths/URLs
        title: Album/single title
        artist: Artist name
        style: Style preset (traditional, modern, fusion, romantic, folk, ghazal)
        regional: Regional modifier (kabuli, herati, kandahari, mazari, panjshiri)
        custom_prompt: Additional instructions
        resolution: 1K (default), 2K, or 4K (costs 2x)
        num_variations: 1-4 (each costs $0.15 or $0.30 for 4K)
        output_format: png (default), jpeg (smaller), webp
        seed: Random seed for reproducibility
        limit_generations: Prevent prompt from requesting extra images (default True)
        dry_run: Only return cost estimate, don't generate
        output_dir: Where to save outputs
    
    Returns:
        dict with results
    
    Cost: $0.15/image (1K/2K), $0.30/image (4K)
    """
    generator = AfghanCoverGenerator(output_dir=output_dir)
    return generator.generate(
        reference_images=reference_images,
        title=title,
        artist=artist,
        style=style,
        regional=regional,
        custom_prompt=custom_prompt,
        resolution=resolution,
        num_variations=num_variations,
        output_format=output_format,
        seed=seed,
        limit_generations=limit_generations,
        dry_run=dry_run,
    )
