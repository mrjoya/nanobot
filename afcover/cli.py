#!/usr/bin/env python3
"""
afcover CLI - Afghan Music Cover Art Generator

Command-line interface for generating Afghan music cover art.
"""

import argparse
import json
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from afcover.generator import generate_cover
from afcover.styles import get_style_names, get_regional_names, describe_style, STYLES


def main():
    parser = argparse.ArgumentParser(
        description="Generate Afghan music cover art using AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic generation with reference images
  %(prog)s --ref cover1.jpg --ref cover2.jpg --title "Dilbar" --artist "Ahmad Zahir"
  
  # Modern style with regional modifier
  %(prog)s --ref reference.jpg --title "Kabul Nights" --artist "Aryana" --style modern --regional kabuli
  
  # Multiple variations
  %(prog)s --ref ref1.jpg --ref ref2.jpg --title "Watan" --style traditional --num 4
  
  # Custom prompt additions
  %(prog)s --ref cover.jpg --title "Ghazal" --style ghazal --custom "include poetry verses in background"

Available Styles:
  traditional  - Classic Afghan with ornate details and gold accents
  modern       - Contemporary pop style, clean and polished
  fusion       - East-West blend, bilingual appeal
  romantic     - Soft, emotional for love songs
  folk         - Rustic, earthy, homeland imagery
  ghazal       - Poetic, calligraphic, literary

Regional Modifiers:
  kabuli       - Urban, cosmopolitan Kabul aesthetic
  herati       - Artistic, Persian classical influences
  kandahari    - Bold, traditional Pashtun style
  mazari       - Colorful, festive Turkic influences
  panjshiri    - Mountain imagery, natural beauty
        """
    )
    
    # Reference images (required for generation, not for --list-styles)
    parser.add_argument(
        "--ref", "--reference",
        dest="references",
        action="append",
        help="Reference image(s) for style (can use multiple times)"
    )
    
    # Content arguments
    parser.add_argument("--title", help="Album/single title")
    parser.add_argument("--artist", help="Artist name")
    
    # Style arguments
    parser.add_argument(
        "--style", "-s",
        default="traditional",
        choices=get_style_names(),
        help="Style preset (default: traditional)"
    )
    parser.add_argument(
        "--regional", "-r",
        choices=get_regional_names(),
        help="Regional style modifier"
    )
    parser.add_argument(
        "--custom",
        help="Additional custom prompt instructions"
    )
    
    # Output arguments
    parser.add_argument(
        "--resolution",
        default="1K",
        choices=["1K", "2K", "4K"],
        help="Output resolution (default: 1K, 4K costs 2x)"
    )
    parser.add_argument(
        "--num", "-n",
        type=int,
        default=1,
        help="Number of variations to generate (1-4)"
    )
    parser.add_argument(
        "--format",
        dest="output_format",
        default="png",
        choices=["png", "jpeg", "webp"],
        help="Output format (default: png, jpeg for smaller files)"
    )
    parser.add_argument(
        "--seed",
        type=int,
        help="Random seed for reproducibility"
    )
    parser.add_argument(
        "--output-dir", "-o",
        default=".",
        help="Output directory"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )
    
    # Cost control arguments
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show cost estimate without generating"
    )
    parser.add_argument(
        "--no-limit",
        action="store_true",
        help="Disable generation limit (allows prompt to request more images - NOT RECOMMENDED)"
    )
    
    # Info arguments
    parser.add_argument(
        "--list-styles",
        action="store_true",
        help="List available styles and exit"
    )
    
    args = parser.parse_args()
    
    # Handle --list-styles
    if args.list_styles:
        print("\nAvailable Styles:\n")
        for name in get_style_names():
            style = STYLES[name]
            print(f"  {name:12} - {style['description']}")
        print("\nRegional Modifiers:\n")
        for name in get_regional_names():
            from afcover.styles import REGIONAL_STYLES
            print(f"  {name:12} - {REGIONAL_STYLES[name]['name']}")
        return
    
    # Validate arguments
    if not args.references:
        print("Error: At least one reference image is required (--ref)", file=sys.stderr)
        parser.print_usage()
        sys.exit(1)
    
    if args.num < 1 or args.num > 4:
        print("Error: --num must be between 1 and 4", file=sys.stderr)
        sys.exit(1)
    
    # Check that reference files exist (for local files)
    for ref in args.references:
        if not ref.startswith(("http://", "https://", "data:")):
            if not Path(ref).exists():
                print(f"Error: Reference file not found: {ref}", file=sys.stderr)
                sys.exit(1)
    
    # Generate
    if not args.json:
        print(f"\n🎨 Generating Afghan music cover art...", file=sys.stderr)
        if args.title:
            print(f"   Title: {args.title}", file=sys.stderr)
        if args.artist:
            print(f"   Artist: {args.artist}", file=sys.stderr)
        print(f"   Style: {args.style}", file=sys.stderr)
        if args.regional:
            print(f"   Regional: {args.regional}", file=sys.stderr)
        print(f"   References: {len(args.references)} image(s)", file=sys.stderr)
        print(f"   Generating {args.num} variation(s)...\n", file=sys.stderr)
    
    try:
        result = generate_cover(
            reference_images=args.references,
            title=args.title,
            artist=args.artist,
            style=args.style,
            regional=args.regional,
            custom_prompt=args.custom,
            resolution=args.resolution,
            num_variations=args.num,
            output_format=args.output_format,
            seed=args.seed,
            limit_generations=not args.no_limit,
            dry_run=args.dry_run,
            output_dir=args.output_dir,
        )
        
        if args.json:
            print(json.dumps(result, indent=2))
        elif args.dry_run:
            print(f"\n💰 Cost Estimate: {result['estimated_cost']}")
            print(f"   {result['message']}")
            print("\n   Remove --dry-run to generate.")
        else:
            print("✅ Generation complete!\n")
            for img in result["images"]:
                print(f"   📀 {img}")
            print(f"\n💰 Cost: {result['cost']}")
    
    except Exception as e:
        if args.json:
            print(json.dumps({"error": str(e)}))
        else:
            print(f"\n❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
