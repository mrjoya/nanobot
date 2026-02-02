#!/usr/bin/env python3
"""
Afghan Cover Art Bot Interface

This module provides a natural language interface for generating Afghan music cover art.
It parses user requests, extracts parameters, and manages the generation process.

Example usage:
    from afcover.bot import parse_request, generate_from_request, format_response
    
    # Parse a natural language request
    params = parse_request("Make a cover for 'Laili Laili' by Ahmad Zahir in traditional style")
    
    # Generate cover art with reference images
    result = generate_from_request(
        "Create a traditional Afghan cover with gold details", 
        image_paths=["ref1.jpg", "ref2.jpg"]
    )
    
    # Format the response for messaging
    message = format_response(result)
"""

import re
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from afcover.generator import generate_cover
from afcover.styles import get_style_names, get_regional_names, STYLES, REGIONAL_STYLES


def parse_request(text):
    """
    Parse a natural language request for cover art generation.
    
    Extracts parameters like title, artist, style, and regional modifiers
    from a text request. Handles common request patterns.
    
    Args:
        text: Natural language request string
        
    Returns:
        dict with extracted parameters
        
    Examples:
        >>> parse_request("Make a cover for 'Song Title' by Artist")
        {'title': 'Song Title', 'artist': 'Artist'}
        
        >>> parse_request("Create a traditional Afghan cover with gold details")
        {'style': 'traditional', 'custom': 'with gold details'}
        
        >>> parse_request("Generate modern Kabuli style cover for my new song 'Watan'")
        {'style': 'modern', 'regional': 'kabuli', 'title': 'Watan'}
    """
    # Initialize parameters with defaults
    params = {
        'title': None,
        'artist': None,
        'style': 'traditional',  # Default style
        'regional': None,
        'custom': None,
        'resolution': '1K',
        'num_variations': 1,
    }
    
    # Extract title - look for text in quotes or after "for" and before "by"
    title_patterns = [
        r"(?:for|titled|named|called)\s+['\"]([^'\"]+)['\"]",  # for "Title"
        r"['\"]([^'\"]+)['\"]",  # "Title" anywhere in text
    ]
    
    for pattern in title_patterns:
        title_match = re.search(pattern, text, re.IGNORECASE)
        if title_match:
            params['title'] = title_match.group(1).strip()
            break
    
    # Extract artist - usually comes after "by" or before "song/album/music"
    artist_patterns = [
        r"by\s+([A-Za-z\s]+?)(?:\s+in|\s+with|\s+style|\s*$)",  # by Artist in/with/style
        r"by\s+([A-Za-z\s]+)",  # by Artist
    ]
    
    for pattern in artist_patterns:
        artist_match = re.search(pattern, text, re.IGNORECASE)
        if artist_match:
            params['artist'] = artist_match.group(1).strip()
            break
    
    # Determine style - check for exact style names from our presets
    style_names = get_style_names()
    for style in style_names:
        if re.search(r'\b' + re.escape(style) + r'\b', text.lower()):
            params['style'] = style
            break
    
    # Determine regional style
    regional_names = get_regional_names()
    for regional in regional_names:
        if re.search(r'\b' + re.escape(regional) + r'\b', text.lower()):
            params['regional'] = regional
            break
    
    # Look for resolution requests
    if re.search(r'\b4K\b', text, re.IGNORECASE):
        params['resolution'] = '4K'
    elif re.search(r'\b2K\b', text, re.IGNORECASE):
        params['resolution'] = '2K'
    
    # Look for variation count requests
    variations_match = re.search(r'(\d+)\s+(?:variations|versions)', text, re.IGNORECASE)
    if variations_match:
        try:
            num = int(variations_match.group(1))
            params['num_variations'] = min(max(num, 1), 4)  # Limit between 1-4
        except ValueError:
            pass
    
    # Extract custom prompt instructions - anything that's not covered by other parameters
    # This is more complex and would benefit from a better NLP approach, but this is a simple start
    if params['style'] in text.lower():
        style_pattern = r'\b' + re.escape(params['style']) + r'\b\s+([^\.]+)'
        custom_match = re.search(style_pattern, text.lower())
        if custom_match:
            params['custom'] = custom_match.group(1).strip()
    
    # If no custom prompt was found but there's a request for specific elements
    if not params['custom'] and 'with' in text.lower():
        custom_match = re.search(r'with\s+([^\.]+)', text.lower())
        if custom_match:
            params['custom'] = custom_match.group(1).strip()
    
    return params


def generate_from_request(text, image_paths, output_dir="."):
    """
    Generate cover art based on natural language request and reference images.
    
    High-level function that combines parsing and generation.
    
    Args:
        text: Natural language request text
        image_paths: List of reference image paths
        output_dir: Directory to save generated images
        
    Returns:
        Generation result dict
        
    Example:
        >>> result = generate_from_request(
        ...     "Make a traditional cover for 'Laili' by Ahmad Zahir", 
        ...     image_paths=["ref1.jpg", "ref2.jpg"]
        ... )
    """
    # Parse the request
    params = parse_request(text)
    
    # Log what we understood from the request
    print(f"Generating cover with parameters:")
    for key, value in params.items():
        if value is not None:
            print(f"  {key}: {value}")
    
    # Ensure we have reference images
    if not image_paths:
        raise ValueError("At least one reference image is required")
    
    # Generate the cover
    result = generate_cover(
        reference_images=image_paths,
        title=params['title'],
        artist=params['artist'],
        style=params['style'],
        regional=params['regional'],
        custom_prompt=params['custom'],
        resolution=params['resolution'],
        num_variations=params['num_variations'],
        output_dir=output_dir
    )
    
    return result


def format_response(result):
    """
    Format a generation result for messaging.
    
    Creates a user-friendly message from generation results.
    
    Args:
        result: Result dict from generate_cover or generate_from_request
        
    Returns:
        Formatted message string
        
    Example:
        >>> result = generate_from_request("Make a cover for 'Watan'", ["ref.jpg"])
        >>> print(format_response(result))
        ✅ Generated Afghan cover art for "Watan"!
        Style: traditional
        📀 /path/to/generated/image.png
        💰 Cost: $0.15
    """
    lines = []
    
    # Success header with title if available
    if result.get('title'):
        lines.append(f"✅ Generated Afghan cover art for \"{result['title']}\"!")
    else:
        lines.append(f"✅ Generated Afghan cover art!")
    
    # Add artist if available
    if result.get('artist'):
        lines.append(f"Artist: {result['artist']}")
    
    # Add style info with friendly description
    style_name = result.get('style', 'traditional')
    if style_name in STYLES:
        style_desc = STYLES[style_name]['description']
        lines.append(f"Style: {style_name} ({style_desc})")
    else:
        lines.append(f"Style: {style_name}")
    
    # Add regional style if used
    if result.get('regional') and result['regional'] in REGIONAL_STYLES:
        regional = result['regional']
        regional_desc = REGIONAL_STYLES[regional]['name']
        lines.append(f"Regional: {regional_desc}")
    
    # List generated images
    images = result.get('images', [])
    if len(images) == 1:
        lines.append(f"📀 {images[0]}")
    else:
        lines.append(f"Generated {len(images)} variations:")
        for img in images:
            lines.append(f"📀 {img}")
    
    # Add cost
    if result.get('cost'):
        lines.append(f"💰 Cost: {result['cost']}")
    
    return "\n".join(lines)


def extract_relevant_phrases(text):
    """
    Extract phrases relevant to Afghan music cover art from free text.
    
    Utility function to help identify important elements in a request.
    
    Args:
        text: Free text input
        
    Returns:
        dict with categorized phrases
    
    Example:
        >>> extract_relevant_phrases("I want a cover with mountains and traditional patterns in bright colors")
        {
            'elements': ['mountains', 'traditional patterns'],
            'colors': ['bright colors'],
            'style_hints': ['traditional']
        }
    """
    result = {
        'elements': [],
        'colors': [],
        'style_hints': []
    }
    
    # Style keywords
    style_words = ['traditional', 'modern', 'fusion', 'romantic', 'folk', 'ghazal', 
                  'classic', 'contemporary', 'pop', 'elegant', 'rustic']
    
    # Element keywords
    element_words = ['mountains', 'landscape', 'calligraphy', 'patterns', 'ornate',
                    'minimal', 'urban', 'rural', 'instruments', 'borders', 'frame']
    
    # Color keywords
    color_words = ['gold', 'red', 'blue', 'green', 'vibrant', 'bright', 'dark',
                  'warm', 'cool', 'earthy', 'jewel tones', 'pastel']
    
    # Simple word matching - a more sophisticated NLP approach would be better
    words = text.lower().split()
    
    for word in style_words:
        if word in text.lower():
            result['style_hints'].append(word)
    
    for word in element_words:
        if word in text.lower():
            result['elements'].append(word)
    
    for word in color_words:
        if word in text.lower():
            result['colors'].append(word)
    
    return result


# Main function for testing
if __name__ == "__main__":
    # Simple test cases
    test_requests = [
        "Make a cover for 'Laili Laili' by Ahmad Zahir",
        "Create a traditional Afghan cover with gold details",
        "Generate modern Kabuli style cover for 'Watan'",
        "I need 3 variations of a romantic cover for 'Dilbar' by Aryana Sayeed",
        "Make a folk style album cover with mountains and traditional instruments"
    ]
    
    print("Testing parse_request function:\n")
    
    for req in test_requests:
        print(f"Request: {req}")
        params = parse_request(req)
        print("Parsed parameters:")
        for k, v in params.items():
            if v is not None:
                print(f"  {k}: {v}")
        print()