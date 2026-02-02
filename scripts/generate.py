#!/usr/bin/env python3
"""
Cover Art Generator - Nano Banana Pro via fal.ai
Usage: python generate.py --title "Album Name" --artist "Artist" --genre "synthwave" [options]
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

FAL_API_URL = "https://queue.fal.run/fal-ai/nano-banana-pro"

GENRE_STYLES = {
    "synthwave": "synthwave aesthetic, neon lights, retro-futuristic, purple and cyan color palette, 80s vibes, chrome text, sunset gradient background",
    "hip-hop": "urban aesthetic, bold typography, street art influence, high contrast, gold accents, graffiti elements",
    "metal": "dark and intense, gothic elements, sharp edges, dramatic lighting, bold distressed typography, flames or skulls",
    "jazz": "sophisticated and smooth, warm tones, vintage feel, elegant typography, artistic brushstrokes, saxophone or piano imagery",
    "electronic": "abstract geometric patterns, vibrant colors, digital aesthetic, clean modern typography, waveforms, circuit patterns",
    "indie": "minimalist design, muted colors, artistic photography style, handwritten or serif typography, natural elements",
    "pop": "bright and colorful, playful elements, glossy finish, bold sans-serif typography, contemporary feel",
    "classical": "elegant and refined, orchestral imagery, gold and deep colors, ornate serif typography, baroque elements",
    "r&b": "smooth and sultry, warm lighting, intimate mood, stylish modern typography, silk textures",
    "rock": "edgy and raw, gritty textures, bold imagery, strong typography, electric guitar elements",
    "lo-fi": "nostalgic anime aesthetic, warm analog feel, soft colors, Japanese influence, cozy room vibes, rain or city lights",
    "ambient": "ethereal and dreamy, vast landscapes, soft gradients, minimal text, atmospheric clouds or space",
    "trap": "dark luxury aesthetic, dripping effects, neon accents, bold block letters, money or diamond imagery",
    "country": "rustic americana, warm earth tones, western typography, natural landscapes, vintage texture",
    "reggae": "vibrant jamaican colors (green, yellow, red), tropical vibes, rastafarian influence, relaxed feel",
    "punk": "DIY aesthetic, torn paper collage, safety pins, anarchic typography, high contrast black and white with color accents",
}


def build_prompt(args):
    """Compose the generation prompt from parameters."""
    
    prompt_parts = [
        "Professional album cover art, square format, print-ready quality, centered composition.",
    ]
    
    # Genre styling
    if args.genre:
        style = GENRE_STYLES.get(args.genre.lower(), args.genre)
        prompt_parts.append(f"Style: {style}.")
    
    # Custom style override
    if args.style:
        prompt_parts.append(f"Visual direction: {args.style}.")
    
    # Title - important for text rendering
    if args.title:
        prompt_parts.append(f'Album title "{args.title}" prominently displayed with clear, legible typography.')
    
    # Artist
    if args.artist:
        prompt_parts.append(f'Artist name "{args.artist}" integrated into the design.')
    
    # Colors
    if args.colors:
        prompt_parts.append(f"Color palette: {args.colors}.")
    
    # Logo
    if args.logo:
        prompt_parts.append(f"Include logo element: {args.logo}.")
    
    # Subject/imagery
    if args.subject:
        prompt_parts.append(f"Main visual subject: {args.subject}.")
    
    # Quality markers
    prompt_parts.append("High resolution, no watermarks, professional album cover composition, suitable for streaming platforms and print.")
    
    return " ".join(prompt_parts)


def generate_cover(prompt, api_key, resolution="1K", num_images=1):
    """Call fal.ai Nano Banana Pro API."""
    
    payload = {
        "prompt": prompt,
        "aspect_ratio": "1:1",  # Album covers are square
        "resolution": resolution,
        "num_images": num_images,
        "output_format": "png"
    }
    
    headers = {
        "Authorization": f"Key {api_key}",
        "Content-Type": "application/json"
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(FAL_API_URL, data=data, headers=headers, method='POST')
    
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8') if e.fp else str(e)
        print(f"API Error {e.code}: {error_body}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Connection Error: {e.reason}", file=sys.stderr)
        sys.exit(1)


def download_image(url, output_path):
    """Download generated image to local path."""
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=60) as response:
        with open(output_path, 'wb') as f:
            f.write(response.read())
    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="Generate album cover art using Nano Banana Pro",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --title "Midnight Drive" --artist "Neon Collective" --genre synthwave
  %(prog)s --title "Urban Tales" --artist "MC Flow" --genre hip-hop --colors "gold, black"
  %(prog)s --title "Quiet Hours" --artist "Lofi Girl" --genre lo-fi --style "anime girl studying"
        """
    )
    
    parser.add_argument("--title", required=True, help="Album/single title")
    parser.add_argument("--artist", required=True, help="Artist name")
    parser.add_argument("--genre", help=f"Genre preset: {', '.join(GENRE_STYLES.keys())}")
    parser.add_argument("--style", help="Custom style description (overrides/adds to genre)")
    parser.add_argument("--colors", help="Color palette description")
    parser.add_argument("--logo", help="Logo description to include")
    parser.add_argument("--subject", help="Main visual subject/imagery")
    parser.add_argument("--resolution", default="1K", choices=["1K", "2K", "4K"],
                        help="Output resolution (4K costs 2x)")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--output-dir", default=".", help="Output directory (default: current)")
    parser.add_argument("--num", type=int, default=1, help="Number of variations (1-4)")
    parser.add_argument("--prompt-only", action="store_true", help="Only output the prompt, don't generate")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    
    args = parser.parse_args()
    
    # Validate num
    if args.num < 1 or args.num > 4:
        print("Error: --num must be between 1 and 4", file=sys.stderr)
        sys.exit(1)
    
    # Build prompt
    prompt = build_prompt(args)
    
    if args.prompt_only:
        print(prompt)
        return
    
    # Load environment variables from .env file
    env_file = Path(__file__).parent.parent / '.env'
    load_dotenv(env_file)
    
    # Get API key
    api_key = os.environ.get("FAL_KEY")
    if not api_key:
        print("Error: FAL_KEY not found", file=sys.stderr)
        print("Please create a .env file with your API key (see .env.example)", file=sys.stderr)
        print("Get your key at: https://fal.ai/dashboard/keys", file=sys.stderr)
        sys.exit(1)
    
    if not args.json:
        print(f"🎨 Generating cover art for '{args.title}' by {args.artist}...", file=sys.stderr)
        print(f"📝 Prompt: {prompt[:100]}...", file=sys.stderr)
    
    # Generate
    result = generate_cover(prompt, api_key, args.resolution, args.num)
    
    # Handle output
    images = result.get("images", [])
    if not images:
        print("Error: No images returned from API", file=sys.stderr)
        sys.exit(1)
    
    # Prepare output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Download images
    downloaded = []
    for i, img in enumerate(images):
        url = img.get("url")
        if url:
            # Generate safe filename
            safe_title = "".join(c if c.isalnum() or c in "- " else "" for c in args.title)
            safe_title = safe_title.replace(" ", "-").lower()[:30]
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            
            if args.output and len(images) == 1:
                out_path = Path(args.output)
            else:
                suffix = f"-{i+1}" if len(images) > 1 else ""
                out_path = output_dir / f"cover-{safe_title}-{timestamp}{suffix}.png"
            
            download_image(url, out_path)
            downloaded.append(str(out_path.absolute()))
            
            if not args.json:
                print(f"✅ Saved: {out_path}")
    
    # Calculate cost
    cost = 0.15 * len(downloaded)
    if args.resolution == "4K":
        cost *= 2
    
    # Output summary
    output_data = {
        "title": args.title,
        "artist": args.artist,
        "genre": args.genre,
        "prompt": prompt,
        "resolution": args.resolution,
        "images": downloaded,
        "count": len(downloaded),
        "cost": f"${cost:.2f}"
    }
    
    if args.json:
        print(json.dumps(output_data, indent=2))
    else:
        print(f"\n🎵 Generated {len(downloaded)} cover(s) for '{args.title}'")
        print(f"💰 Estimated cost: ${cost:.2f}")


if __name__ == "__main__":
    main()
