#!/usr/bin/env python3
"""
Afghan Cover Art Bot Interface for OpenClaw

This module provides the OpenClaw integration layer for generating Afghan music cover art.
It handles natural language requests, file uploads, and conversation flows.

⚠️  COST CONTROL: All commands default to --dry-run mode.
    Use --confirm to actually generate (costs $0.15-$0.30 per image).

OpenClaw Integration:
    The agent uses this module via command-line or Python imports to:
    1. Parse user requests for cover art
    2. Accept reference images uploaded by users
    3. Generate culturally authentic Afghan music covers
    4. Return formatted results for messaging

Example Usage via CLI:
    # Parse a request (FREE - no API call)
    python -m afcover.bot parse "Make a traditional cover for 'Laili Laili' by Ahmad Zahir"
    
    # Estimate cost (DEFAULT - dry run, no API call)
    python -m afcover.bot generate \
        --prompt "Traditional cover for 'Watan' by Ahmad Zahir" \
        --images ref1.jpg ref2.jpg
    
    # Actually generate (COSTS MONEY - requires --confirm)
    python -m afcover.bot generate \
        --prompt "Traditional cover for 'Watan' by Ahmad Zahir" \
        --images ref1.jpg ref2.jpg \
        --confirm

Example Usage in OpenClaw:
    # Agent reads this skill, then executes:
    # Step 1: ALWAYS estimate cost first
    python -m afcover.bot generate --prompt "..." --images img.jpg
    
    # Step 2: Only after user confirms, add --confirm
    python -m afcover.bot generate --prompt "..." --images img.jpg --confirm
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime, date

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# =============================================================================
# Cost Control & Usage Tracking
# =============================================================================

# Daily spending limit in USD
DAILY_LIMIT_USD = 5.00

# Cost per image
COST_1K_2K = 0.15
COST_4K = 0.30

USAGE_FILE = Path(__file__).parent / ".usage_tracking.json"


def get_usage_today() -> Dict[str, Any]:
    """Get today's usage statistics."""
    today = date.today().isoformat()
    
    if USAGE_FILE.exists():
        try:
            with open(USAGE_FILE) as f:
                data = json.load(f)
                if data.get("date") == today:
                    return data
        except (json.JSONDecodeError, KeyError):
            pass
    
    # Return fresh tracking for today
    return {
        "date": today,
        "generations": 0,
        "images_generated": 0,
        "total_cost": 0.0,
    }


def record_usage(num_images: int, cost: float) -> Dict[str, Any]:
    """Record a generation to usage tracking."""
    usage = get_usage_today()
    usage["generations"] += 1
    usage["images_generated"] += num_images
    usage["total_cost"] += cost
    
    with open(USAGE_FILE, "w") as f:
        json.dump(usage, f, indent=2)
    
    return usage


def check_daily_limit(estimated_cost: float) -> Dict[str, Any]:
    """Check if generation would exceed daily limit."""
    usage = get_usage_today()
    remaining = DAILY_LIMIT_USD - usage["total_cost"]
    
    return {
        "allowed": estimated_cost <= remaining,
        "estimated_cost": estimated_cost,
        "spent_today": usage["total_cost"],
        "remaining": remaining,
        "limit": DAILY_LIMIT_USD,
        "generations_today": usage["generations"],
    }


def estimate_cost(num_images: int, resolution: str) -> float:
    """Calculate estimated cost for generation."""
    base_cost = COST_4K if resolution == "4K" else COST_1K_2K
    return base_cost * num_images

from afcover.generator import generate_cover, list_styles, list_regional
from afcover.styles import (
    get_style_names, 
    get_regional_names, 
    get_occasion_names,
    STYLES, 
    REGIONAL_STYLES,
    OCCASIONS,
)
from afcover.library import (
    ReferenceLibrary,
    get_artist_references,
    get_style_references,
    add_artist_reference,
    add_style_reference,
)


# =============================================================================
# Request Parsing
# =============================================================================

def parse_request(text: str) -> Dict[str, Any]:
    """
    Parse a natural language request for Afghan cover art generation.
    
    Extracts parameters like title, artist, style, regional modifiers,
    and custom instructions from a text request.
    
    Args:
        text: Natural language request string
        
    Returns:
        dict with extracted parameters:
        - title: Album/song title
        - artist: Artist name
        - style: Style preset (traditional, modern, fusion, etc.)
        - regional: Regional modifier (kabuli, herati, kandahari, etc.)
        - occasion: Occasion theme (nowruz, eid, etc.)
        - custom: Additional custom instructions
        - resolution: Output resolution (1K, 2K, 4K)
        - num_variations: Number of variations to generate
        
    Examples:
        >>> parse_request("Make a cover for 'Laili Laili' by Ahmad Zahir")
        {'title': 'Laili Laili', 'artist': 'Ahmad Zahir', 'style': 'traditional'}
        
        >>> parse_request("Create a modern Kabuli style cover for my song 'Watan'")
        {'title': 'Watan', 'style': 'modern', 'regional': 'kabuli'}
    """
    # Initialize with defaults
    params = {
        'title': None,
        'artist': None,
        'style': 'traditional',  # Default for Afghan music
        'regional': None,
        'occasion': None,
        'custom': None,
        'resolution': '1K',
        'num_variations': 1,
        'release_type': 'album',
        'text_placement': 'title_prominent',
    }
    
    # ---------- Extract title ----------
    title_patterns = [
        r"(?:for|titled|named|called)\s+['\"]([^'\"]+)['\"]",  # for "Title"
        r"['\"]([^'\"]+)['\"]",  # "Title" anywhere
        r"(?:for|titled|named|called)\s+([^\s,]+(?:\s+[^\s,]+)?)",  # for Title (2 words max)
    ]
    
    for pattern in title_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            params['title'] = match.group(1).strip()
            break
    
    # ---------- Extract artist ----------
    artist_patterns = [
        r"by\s+([A-Za-z\s]+?)(?:\s+in|\s+with|\s+style|,|\.|$)",
        r"(?:artist|singer|musician)\s+([A-Za-z\s]+?)(?:\s+in|\s+with|,|\.|$)",
    ]
    
    for pattern in artist_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            params['artist'] = match.group(1).strip()
            break
    
    # ---------- Determine style ----------
    style_names = get_style_names()
    text_lower = text.lower()
    
    # Check for explicit style mentions
    for style in style_names:
        if re.search(r'\b' + re.escape(style) + r'\b', text_lower):
            params['style'] = style
            break
    
    # ---------- Determine regional modifier ----------
    regional_names = get_regional_names()
    for regional in regional_names:
        if re.search(r'\b' + re.escape(regional) + r'\b', text_lower):
            params['regional'] = regional
            break
    
    # ---------- Determine occasion ----------
    occasion_names = get_occasion_names()
    for occasion in occasion_names:
        if re.search(r'\b' + re.escape(occasion) + r'\b', text_lower):
            params['occasion'] = occasion
            break
    
    # ---------- Extract resolution ----------
    if re.search(r'\b4K\b', text, re.IGNORECASE):
        params['resolution'] = '4K'
    elif re.search(r'\b2K\b', text, re.IGNORECASE):
        params['resolution'] = '2K'
    
    # ---------- Extract variation count ----------
    variations_match = re.search(r'(\d+)\s+(?:variations|versions|options)', text, re.IGNORECASE)
    if variations_match:
        num = int(variations_match.group(1))
        params['num_variations'] = min(max(num, 1), 4)
    
    # ---------- Determine release type ----------
    if re.search(r'\bsingle\b', text_lower):
        params['release_type'] = 'single'
    elif re.search(r'\b(?:ep|extended\s+play)\b', text_lower):
        params['release_type'] = 'ep'
    
    # ---------- Extract custom instructions ----------
    # Look for specific descriptive phrases
    custom_patterns = [
        r'with\s+([^\.]+(?:and|,)[^\.]+)',  # with X and Y / with X, Y
        r'featuring\s+([^\.]+)',
        r'include\s+([^\.]+)',
        r'showing\s+([^\.]+)',
        r'depicting\s+([^\.]+)',
    ]
    
    for pattern in custom_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            params['custom'] = match.group(1).strip()
            break
    
    return params


def extract_mood_hints(text: str) -> List[str]:
    """
    Extract mood and thematic hints from text.
    Useful for enhancing generation prompts.
    """
    hints = []
    text_lower = text.lower()
    
    mood_keywords = {
        # Romantic
        'romantic': 'romantic love theme',
        'love': 'romantic theme',
        'عشق': 'romantic love (ishq)',
        'دل': 'emotional heart theme',
        
        # Sad/Nostalgic
        'sad': 'melancholic sad theme',
        'nostalgic': 'nostalgic longing',
        'غم': 'melancholy (gham)',
        
        # Celebratory
        'happy': 'joyful celebratory',
        'celebration': 'festive celebration',
        'wedding': 'wedding celebration',
        
        # Patriotic
        'homeland': 'patriotic homeland',
        'وطن': 'homeland (watan)',
        'افغان': 'Afghan pride',
        
        # Spiritual
        'spiritual': 'spiritual devotional',
        'sufi': 'mystical Sufi',
    }
    
    for keyword, hint in mood_keywords.items():
        if keyword in text_lower:
            hints.append(hint)
    
    return hints


# =============================================================================
# Generation Functions
# =============================================================================

def generate_from_request(
    text: str,
    image_paths: List[str],
    output_dir: str = ".",
    confirm: bool = False,
) -> Dict[str, Any]:
    """
    Generate Afghan cover art from a natural language request.
    
    ⚠️  COST CONTROL: Defaults to dry-run mode (cost estimate only).
        Set confirm=True to actually generate (costs money).
    
    This is the main entry point for OpenClaw integration.
    
    Args:
        text: Natural language request describing desired cover art
        image_paths: List of reference image paths (required)
        output_dir: Directory to save generated images
        confirm: If True, actually generate (COSTS MONEY). 
                 If False (default), only return cost estimate.
        
    Returns:
        Generation result dict with:
        - success: bool
        - images: list of generated file paths (only if confirm=True)
        - cost: estimated/actual cost
        - title, artist, style: extracted parameters
        - prompt: the full prompt used
        - requires_confirmation: True if this is a dry-run
        
    Example:
        # Step 1: Get cost estimate (default, free)
        >>> result = generate_from_request(
        ...     "Make a traditional cover for 'Laili' by Ahmad Zahir",
        ...     image_paths=["ref1.jpg", "ref2.jpg"],
        ... )
        >>> print(result['estimated_cost'])  # "$0.15"
        >>> print(result['requires_confirmation'])  # True
        
        # Step 2: After user confirms, actually generate
        >>> result = generate_from_request(
        ...     "Make a traditional cover for 'Laili' by Ahmad Zahir",
        ...     image_paths=["ref1.jpg", "ref2.jpg"],
        ...     confirm=True  # User confirmed, now generate
        ... )
    """
    # Parse the request
    params = parse_request(text)
    
    # Validate we have reference images
    if not image_paths:
        return {
            'success': False,
            'error': 'At least one reference image is required for Afghan cover art generation.',
            'hint': 'Please upload reference images (artist photos, style examples, etc.)',
        }
    
    # Validate image paths exist
    missing = [p for p in image_paths if not Path(p).exists() and not p.startswith(('http://', 'https://'))]
    if missing:
        return {
            'success': False,
            'error': f'Image files not found: {missing}',
        }
    
    # Calculate estimated cost
    est_cost = estimate_cost(params['num_variations'], params['resolution'])
    
    # Check daily limit before proceeding
    limit_check = check_daily_limit(est_cost)
    
    # If not confirmed, return cost estimate (DRY RUN - DEFAULT BEHAVIOR)
    if not confirm:
        return {
            'success': True,
            'dry_run': True,
            'requires_confirmation': True,
            'title': params['title'],
            'artist': params['artist'],
            'style': params['style'],
            'regional': params['regional'],
            'resolution': params['resolution'],
            'num_images': params['num_variations'],
            'estimated_cost': f"${est_cost:.2f}",
            'daily_usage': {
                'spent_today': f"${limit_check['spent_today']:.2f}",
                'remaining': f"${limit_check['remaining']:.2f}",
                'limit': f"${limit_check['limit']:.2f}",
            },
            'message': f"Would generate {params['num_variations']} image(s) at {params['resolution']} for ${est_cost:.2f}",
            'next_step': "Add --confirm to actually generate (costs money)",
        }
    
    # ===== CONFIRMED GENERATION (COSTS MONEY) =====
    
    # Check daily limit
    if not limit_check['allowed']:
        return {
            'success': False,
            'error': 'Daily spending limit reached',
            'spent_today': f"${limit_check['spent_today']:.2f}",
            'limit': f"${limit_check['limit']:.2f}",
            'hint': f"You've spent ${limit_check['spent_today']:.2f} today. Limit is ${DAILY_LIMIT_USD:.2f}.",
        }
    
    # Generate the cover
    try:
        result = generate_cover(
            reference_images=image_paths,
            title=params['title'],
            artist=params['artist'],
            style=params['style'],
            regional=params['regional'],
            occasion=params['occasion'],
            release_type=params['release_type'],
            text_placement=params['text_placement'],
            custom_prompt=params['custom'],
            resolution=params['resolution'],
            num_variations=params['num_variations'],
            dry_run=False,  # Actually generate
            output_dir=output_dir,
        )
        
        # Record usage on success
        if result.get('success'):
            num_generated = len(result.get('images', []))
            actual_cost = estimate_cost(num_generated, params['resolution'])
            usage = record_usage(num_generated, actual_cost)
            result['daily_usage'] = {
                'spent_today': f"${usage['total_cost']:.2f}",
                'remaining': f"${DAILY_LIMIT_USD - usage['total_cost']:.2f}",
                'generations_today': usage['generations'],
            }
        
        return result
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
        }


def generate_with_library_references(
    text: str,
    artist_name: Optional[str] = None,
    style_name: Optional[str] = None,
    additional_images: Optional[List[str]] = None,
    output_dir: str = ".",
    dry_run: bool = False,
) -> Dict[str, Any]:
    """
    Generate cover art using references from the built-in library.
    
    Allows generation using stored reference collections.
    
    Args:
        text: Natural language request
        artist_name: Use references from this artist's collection
        style_name: Use references from this style collection
        additional_images: Extra reference images to include
        output_dir: Output directory
        dry_run: Only estimate cost
        
    Returns:
        Generation result dict
    """
    image_paths = []
    
    # Get artist references
    if artist_name:
        artist_refs = get_artist_references(artist_name)
        image_paths.extend(artist_refs)
    
    # Get style references
    if style_name:
        style_refs = get_style_references(style_name)
        image_paths.extend(style_refs)
    
    # Add any additional images
    if additional_images:
        image_paths.extend(additional_images)
    
    if not image_paths:
        return {
            'success': False,
            'error': f'No reference images found for artist "{artist_name}" or style "{style_name}"',
            'hint': 'Add references to the library first, or provide image paths directly.',
        }
    
    return generate_from_request(text, image_paths, output_dir, dry_run)


# =============================================================================
# Response Formatting
# =============================================================================

def format_response(result: Dict[str, Any]) -> str:
    """
    Format generation result for messaging (Telegram, Discord, etc.).
    
    Creates a user-friendly message from generation results.
    
    Args:
        result: Result dict from generate_from_request
        
    Returns:
        Formatted message string with emojis
    """
    lines = []
    
    # Handle errors
    if not result.get('success', True):
        lines.append(f"❌ {result.get('error', 'Generation failed')}")
        if result.get('hint'):
            lines.append(f"💡 {result['hint']}")
        if result.get('spent_today'):
            lines.append(f"📊 Spent today: {result['spent_today']} / {result.get('limit', '$5.00')}")
        return "\n".join(lines)
    
    # Handle dry run / confirmation required (DEFAULT BEHAVIOR)
    if result.get('dry_run') or result.get('requires_confirmation'):
        lines.append("📊 **Cost Estimate** (no charge yet)")
        lines.append("")
        if result.get('title'):
            lines.append(f"🎵 Title: \"{result['title']}\"")
        if result.get('artist'):
            lines.append(f"👤 Artist: {result['artist']}")
        lines.append(f"🎨 Style: {result.get('style', 'traditional')}")
        if result.get('regional'):
            lines.append(f"📍 Regional: {result['regional']}")
        lines.append(f"📐 Resolution: {result.get('resolution', '1K')}")
        lines.append(f"🖼️ Images: {result.get('num_images', 1)}")
        lines.append("")
        lines.append(f"💰 **Estimated cost: {result.get('estimated_cost', '$0.15')}**")
        lines.append("")
        
        # Show daily usage
        if result.get('daily_usage'):
            usage = result['daily_usage']
            lines.append(f"📈 Today: {usage.get('spent_today', '$0.00')} spent, {usage.get('remaining', '$5.00')} remaining")
        
        lines.append("")
        lines.append("⚠️ To generate, user must confirm.")
        lines.append("Then run with --confirm flag.")
        return "\n".join(lines)
    
    # Success header
    title = result.get('title')
    artist = result.get('artist')
    
    if title and artist:
        lines.append(f"✅ **Generated Afghan Cover Art**")
        lines.append(f"🎵 \"{title}\" by {artist}")
    elif title:
        lines.append(f"✅ **Generated Afghan Cover Art**")
        lines.append(f"🎵 \"{title}\"")
    else:
        lines.append(f"✅ **Generated Afghan Cover Art**")
    
    # Style info
    style_name = result.get('style', 'traditional')
    if style_name in STYLES:
        style_info = STYLES[style_name]
        lines.append(f"🎨 Style: {style_info['name']}")
    
    # Regional modifier
    if result.get('regional'):
        regional = result['regional']
        if regional in REGIONAL_STYLES:
            lines.append(f"📍 Regional: {REGIONAL_STYLES[regional]['name']}")
    
    # Occasion
    if result.get('occasion'):
        occasion = result['occasion']
        if occasion in OCCASIONS:
            lines.append(f"🎉 Theme: {OCCASIONS[occasion]['name']}")
    
    # Generated images
    images = result.get('images', [])
    if len(images) == 1:
        lines.append(f"📀 {images[0]}")
    elif len(images) > 1:
        lines.append(f"📀 Generated {len(images)} variations:")
        for i, img in enumerate(images, 1):
            lines.append(f"   {i}. {img}")
    
    # Cost
    if result.get('cost'):
        lines.append(f"💰 Cost: {result['cost']}")
    
    return "\n".join(lines)


def format_response_json(result: Dict[str, Any]) -> str:
    """Format result as JSON for programmatic use."""
    return json.dumps(result, indent=2, ensure_ascii=False)


# =============================================================================
# Library Management
# =============================================================================

def list_library() -> Dict[str, Any]:
    """List all reference collections in the library."""
    library = ReferenceLibrary()
    return library.list_collections()


def add_to_library(
    image_path: str,
    collection_type: str,  # 'artist' or 'style'
    collection_name: str,
    metadata: Optional[Dict] = None,
) -> Dict[str, Any]:
    """
    Add a reference image to the library.
    
    Args:
        image_path: Path to the image file
        collection_type: 'artist' or 'style'
        collection_name: Name of the collection
        metadata: Optional metadata dict
        
    Returns:
        Result dict with success status and saved path
    """
    try:
        if collection_type == 'artist':
            saved_path = add_artist_reference(collection_name, image_path, metadata)
        elif collection_type == 'style':
            saved_path = add_style_reference(collection_name, image_path, metadata)
        else:
            return {'success': False, 'error': f'Unknown collection type: {collection_type}'}
        
        return {
            'success': True,
            'message': f'Added to {collection_type} collection "{collection_name}"',
            'path': saved_path,
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}


# =============================================================================
# Style Information
# =============================================================================

def get_styles_info() -> str:
    """Get formatted information about available styles."""
    lines = ["🎨 **Available Afghan Music Cover Styles**\n"]
    
    for name, style in STYLES.items():
        lines.append(f"**{name}** - {style['name']}")
        lines.append(f"  {style['description']}")
        lines.append(f"  Mood: {style['mood']}")
        lines.append("")
    
    return "\n".join(lines)


def get_regional_info() -> str:
    """Get formatted information about regional modifiers."""
    lines = ["📍 **Regional Style Modifiers**\n"]
    
    for name, style in REGIONAL_STYLES.items():
        lines.append(f"**{name}** - {style['name']}")
        lines.append(f"  {style['modifier']}")
        lines.append("")
    
    return "\n".join(lines)


def get_occasions_info() -> str:
    """Get formatted information about occasion themes."""
    lines = ["🎉 **Occasion Themes**\n"]
    
    for name, occasion in OCCASIONS.items():
        lines.append(f"**{name}** - {occasion['name']}")
        lines.append(f"  Elements: {occasion['elements']}")
        lines.append("")
    
    return "\n".join(lines)


# =============================================================================
# CLI Interface for OpenClaw
# =============================================================================

def main():
    """Command-line interface for OpenClaw integration."""
    parser = argparse.ArgumentParser(
        description="Afghan Cover Art Generator - OpenClaw Integration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Parse a request (FREE)
  python3 -m afcover.bot parse "Make a traditional cover for 'Laili' by Ahmad Zahir"
  
  # Get cost estimate (DEFAULT - FREE, no API call)
  python3 -m afcover.bot generate \\
      --prompt "Traditional cover for 'Watan' by Ahmad Zahir" \\
      --images ref1.jpg ref2.jpg
  
  # Actually generate (COSTS MONEY - requires --confirm)
  python3 -m afcover.bot generate \\
      --prompt "Traditional cover for 'Watan' by Ahmad Zahir" \\
      --images ref1.jpg ref2.jpg \\
      --output ./output \\
      --confirm
  
  # Check daily spending
  python3 -m afcover.bot usage
  
  # List available styles
  python3 -m afcover.bot styles
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # ---------- Parse command ----------
    parse_parser = subparsers.add_parser('parse', help='Parse a natural language request')
    parse_parser.add_argument('text', help='Request text to parse')
    parse_parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    # ---------- Generate command ----------
    gen_parser = subparsers.add_parser('generate', help='Generate cover art (defaults to cost estimate)')
    gen_parser.add_argument('--prompt', '-p', required=True, help='Natural language prompt')
    gen_parser.add_argument('--images', '-i', nargs='+', required=True, help='Reference image paths')
    gen_parser.add_argument('--output', '-o', default='.', help='Output directory')
    gen_parser.add_argument('--confirm', action='store_true', 
                           help='⚠️ Actually generate (COSTS MONEY). Without this, only shows cost estimate.')
    gen_parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    # ---------- Usage command ----------
    usage_parser = subparsers.add_parser('usage', help='Show daily usage and spending')
    usage_parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    # ---------- Styles command ----------
    styles_parser = subparsers.add_parser('styles', help='List available styles')
    styles_parser.add_argument('--type', choices=['all', 'styles', 'regional', 'occasions'], 
                               default='all', help='Type of styles to list')
    
    # ---------- Library command ----------
    lib_parser = subparsers.add_parser('library', help='Manage reference library')
    lib_subparsers = lib_parser.add_subparsers(dest='lib_command')
    
    # Library list
    lib_list = lib_subparsers.add_parser('list', help='List library collections')
    lib_list.add_argument('--type', choices=['all', 'artists', 'styles'], default='all')
    
    # Library add
    lib_add = lib_subparsers.add_parser('add', help='Add reference to library')
    lib_add.add_argument('--type', required=True, choices=['artist', 'style'], help='Collection type')
    lib_add.add_argument('--name', required=True, help='Collection name')
    lib_add.add_argument('--image', required=True, help='Image path to add')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # ---------- Execute commands ----------
    
    if args.command == 'parse':
        params = parse_request(args.text)
        if args.json:
            print(json.dumps(params, indent=2, ensure_ascii=False))
        else:
            print("Parsed Parameters:")
            for k, v in params.items():
                if v is not None:
                    print(f"  {k}: {v}")
    
    elif args.command == 'generate':
        # Show warning if --confirm is used
        if args.confirm:
            print("⚠️  GENERATING (this will cost money)...", file=sys.stderr)
        
        result = generate_from_request(
            text=args.prompt,
            image_paths=args.images,
            output_dir=args.output,
            confirm=args.confirm,  # Default False = dry run
        )
        
        if args.json:
            print(format_response_json(result))
        else:
            print(format_response(result))
    
    elif args.command == 'usage':
        usage = get_usage_today()
        limit_info = check_daily_limit(0)
        
        if args.json:
            print(json.dumps({
                "date": usage["date"],
                "generations": usage["generations"],
                "images_generated": usage["images_generated"],
                "spent_today": f"${usage['total_cost']:.2f}",
                "remaining": f"${limit_info['remaining']:.2f}",
                "daily_limit": f"${DAILY_LIMIT_USD:.2f}",
            }, indent=2))
        else:
            print("📊 **Daily Usage**")
            print(f"Date: {usage['date']}")
            print(f"Generations: {usage['generations']}")
            print(f"Images created: {usage['images_generated']}")
            print(f"Spent today: ${usage['total_cost']:.2f}")
            print(f"Remaining: ${limit_info['remaining']:.2f}")
            print(f"Daily limit: ${DAILY_LIMIT_USD:.2f}")
    
    elif args.command == 'styles':
        if args.type in ['all', 'styles']:
            print(get_styles_info())
        if args.type in ['all', 'regional']:
            print(get_regional_info())
        if args.type in ['all', 'occasions']:
            print(get_occasions_info())
    
    elif args.command == 'library':
        if args.lib_command == 'list':
            collections = list_library()
            print(json.dumps(collections, indent=2))
        elif args.lib_command == 'add':
            result = add_to_library(
                image_path=args.image,
                collection_type=args.type,
                collection_name=args.name,
            )
            print(json.dumps(result, indent=2))
        else:
            lib_parser.print_help()


if __name__ == "__main__":
    main()
