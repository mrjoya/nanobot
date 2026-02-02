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
from afcover.library import list_references, get_artist_references, get_style_references


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
  
  # Using reference library
  %(prog)s --artist-ref "Ahmad Zahir" --title "New Release" --style traditional
  %(prog)s --style-ref "modern" --title "Summer Hit" --artist "Aryana"
  %(prog)s --list-references   # Show all available references in the library

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
    
    # Reference Library arguments
    parser.add_argument(
        "--use-library",
        action="store_true",
        help="Use stored references from the library"
    )
    parser.add_argument(
        "--artist-ref",
        help="Use references for a specific artist from the library"
    )
    parser.add_argument(
        "--style-ref",
        help="Use references for a specific style from the library"
    )
    parser.add_argument(
        "--list-references",
        action="store_true",
        help="List available references in the library and exit"
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
    
    # Handle --list-references
    if args.list_references:
        ref_collections = list_references()
        
        print("\nReference Library:\n")
        
        if "artists" in ref_collections and ref_collections["artists"]:
            print("Artists:")
            for artist, references in ref_collections["artists"].items():
                count = len(references)
                print(f"  {artist:15} - {count} reference(s)")
        else:
            print("  No artist references found")
        
        print()
        
        if "styles" in ref_collections and ref_collections["styles"]:
            print("Styles:")
            for style, references in ref_collections["styles"].items():
                count = len(references)
                print(f"  {style:15} - {count} reference(s)")
        else:
            print("  No style references found")
        
        return
    
    # Handle library references
    reference_images = args.references or []
    using_library = False
    library_source = None
    
    if args.use_library or args.artist_ref or args.style_ref:
        if args.artist_ref:
            artist_refs = get_artist_references(args.artist_ref)
            if artist_refs:
                reference_images.extend(artist_refs)
                using_library = True
                library_source = f"artist '{args.artist_ref}'"
            else:
                print(f"Warning: No references found for artist: {args.artist_ref}", file=sys.stderr)
        
        if args.style_ref:
            style_refs = get_style_references(args.style_ref)
            if style_refs:
                reference_images.extend(style_refs)
                using_library = True
                library_source = f"style '{args.style_ref}'"
            else:
                print(f"Warning: No references found for style: {args.style_ref}", file=sys.stderr)
    
    # Validate arguments
    if not reference_images:
        print("Error: At least one reference image is required (--ref, --artist-ref, or --style-ref)", file=sys.stderr)
        parser.print_usage()
        sys.exit(1)
    
    if args.num < 1 or args.num > 4:
        print("Error: --num must be between 1 and 4", file=sys.stderr)
        sys.exit(1)
    
    # Check that reference files exist (for local files)
    for ref in reference_images:
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
        print(f"   References: {len(reference_images)} image(s)", file=sys.stderr)
        if using_library:
            print(f"   Using library references from {library_source}", file=sys.stderr)
        print(f"   Generating {args.num} variation(s)...\n", file=sys.stderr)
    
    try:
        result = generate_cover(
            reference_images=reference_images,
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
