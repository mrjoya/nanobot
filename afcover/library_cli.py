#!/usr/bin/env python3
"""
Reference Library CLI for Afghan Cover Art Generator

Command-line tool for managing the reference library.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Any

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from afcover.library import (
    list_references, 
    get_artist_references,
    get_style_references,
    add_artist_reference,
    add_style_reference,
    batch_add_artist_references,
    batch_add_style_references,
    search_references,
    export_collection,
    import_collection,
)


def main():
    parser = argparse.ArgumentParser(
        description="Manage reference images for the Afghan Cover Art Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List all references
  %(prog)s list
  
  # List references for a specific artist
  %(prog)s list-artist "Ahmad Zahir"
  
  # List references for a specific style
  %(prog)s list-style modern
  
  # Add a reference image to an artist
  %(prog)s add-artist "Ahmad Zahir" path/to/image.jpg
  
  # Add a reference image to a style with metadata
  %(prog)s add-style traditional path/to/image.jpg --meta '{"source": "original album", "year": 1975}'
  
  # Add multiple references to a style
  %(prog)s batch-add-style modern image1.jpg image2.jpg image3.jpg
  
  # Search for references
  %(prog)s search "traditional" --collection-type all
  
  # Export a collection
  %(prog)s export artists "Ahmad Zahir" --output ahmad_zahir_refs.zip
  
  # Import a collection
  %(prog)s import styles "traditional" traditional_refs.zip
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List all references")
    list_parser.add_argument(
        "--collection-type", "-t",
        choices=["artists", "styles", "all"],
        default="all",
        help="Type of collections to list (default: all)"
    )
    
    # List artist command
    list_artist_parser = subparsers.add_parser("list-artist", help="List references for a specific artist")
    list_artist_parser.add_argument("artist", help="Artist name")
    
    # List style command
    list_style_parser = subparsers.add_parser("list-style", help="List references for a specific style")
    list_style_parser.add_argument("style", help="Style name")
    
    # Add artist command
    add_artist_parser = subparsers.add_parser("add-artist", help="Add a reference image to an artist")
    add_artist_parser.add_argument("artist", help="Artist name")
    add_artist_parser.add_argument("image", help="Path to the image file")
    add_artist_parser.add_argument(
        "--meta", "--metadata",
        type=json.loads,
        help="Metadata for the image (JSON string)"
    )
    add_artist_parser.add_argument(
        "--move",
        action="store_true",
        help="Move the file instead of copying it"
    )
    
    # Add style command
    add_style_parser = subparsers.add_parser("add-style", help="Add a reference image to a style")
    add_style_parser.add_argument("style", help="Style name")
    add_style_parser.add_argument("image", help="Path to the image file")
    add_style_parser.add_argument(
        "--meta", "--metadata",
        type=json.loads,
        help="Metadata for the image (JSON string)"
    )
    add_style_parser.add_argument(
        "--move",
        action="store_true",
        help="Move the file instead of copying it"
    )
    
    # Batch add artist command
    batch_add_artist_parser = subparsers.add_parser("batch-add-artist", help="Add multiple reference images to an artist")
    batch_add_artist_parser.add_argument("artist", help="Artist name")
    batch_add_artist_parser.add_argument("images", nargs="+", help="Paths to image files")
    batch_add_artist_parser.add_argument(
        "--move",
        action="store_true",
        help="Move the files instead of copying them"
    )
    
    # Batch add style command
    batch_add_style_parser = subparsers.add_parser("batch-add-style", help="Add multiple reference images to a style")
    batch_add_style_parser.add_argument("style", help="Style name")
    batch_add_style_parser.add_argument("images", nargs="+", help="Paths to image files")
    batch_add_style_parser.add_argument(
        "--move",
        action="store_true",
        help="Move the files instead of copying them"
    )
    
    # Search command
    search_parser = subparsers.add_parser("search", help="Search for references")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument(
        "--collection-type", "-t",
        choices=["artists", "styles", "all"],
        default="all",
        help="Type of collections to search (default: all)"
    )
    search_parser.add_argument(
        "--skip-metadata", "-s",
        action="store_true",
        help="Skip searching in metadata"
    )
    
    # Export command
    export_parser = subparsers.add_parser("export", help="Export a collection")
    export_parser.add_argument(
        "collection_type",
        choices=["artists", "styles"],
        help="Type of collection"
    )
    export_parser.add_argument("collection_name", help="Name of the collection")
    export_parser.add_argument(
        "--output", "-o",
        help="Output path for the zip file"
    )
    
    # Import command
    import_parser = subparsers.add_parser("import", help="Import a collection")
    import_parser.add_argument(
        "collection_type",
        choices=["artists", "styles"],
        help="Type of collection"
    )
    import_parser.add_argument("collection_name", help="Name of the collection")
    import_parser.add_argument("zip_file", help="Path to the zip file")
    import_parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing files"
    )
    
    args = parser.parse_args()
    
    # Handle no command
    if args.command is None:
        parser.print_help()
        return
    
    # Handle list command
    if args.command == "list":
        collections = list_references(args.collection_type)
        print(f"\nReference Library ({args.collection_type}):\n")
        
        if "artists" in collections and collections["artists"]:
            print("Artists:")
            for artist, references in collections["artists"].items():
                count = len(references)
                print(f"  {artist:15} - {count} reference(s)")
            print()
        
        if "styles" in collections and collections["styles"]:
            print("Styles:")
            for style, references in collections["styles"].items():
                count = len(references)
                print(f"  {style:15} - {count} reference(s)")
        
        return
    
    # Handle list-artist command
    if args.command == "list-artist":
        references = get_artist_references(args.artist)
        count = len(references)
        print(f"\nReferences for artist '{args.artist}' ({count}):\n")
        
        for i, ref in enumerate(references, 1):
            print(f"  {i}. {ref}")
        
        return
    
    # Handle list-style command
    if args.command == "list-style":
        references = get_style_references(args.style)
        count = len(references)
        print(f"\nReferences for style '{args.style}' ({count}):\n")
        
        for i, ref in enumerate(references, 1):
            print(f"  {i}. {ref}")
        
        return
    
    # Handle add-artist command
    if args.command == "add-artist":
        try:
            ref_path = add_artist_reference(
                artist_name=args.artist,
                image_path=args.image,
                metadata=args.meta,
                copy_file=not args.move,
            )
            print(f"\n✅ Added reference to artist '{args.artist}'")
            print(f"  {ref_path}")
        except Exception as e:
            print(f"\n❌ Error: {e}", file=sys.stderr)
            sys.exit(1)
        
        return
    
    # Handle add-style command
    if args.command == "add-style":
        try:
            ref_path = add_style_reference(
                style_name=args.style,
                image_path=args.image,
                metadata=args.meta,
                copy_file=not args.move,
            )
            print(f"\n✅ Added reference to style '{args.style}'")
            print(f"  {ref_path}")
        except Exception as e:
            print(f"\n❌ Error: {e}", file=sys.stderr)
            sys.exit(1)
        
        return
    
    # Handle batch-add-artist command
    if args.command == "batch-add-artist":
        try:
            ref_paths = batch_add_artist_references(
                artist_name=args.artist,
                image_paths=args.images,
                copy_files=not args.move,
            )
            print(f"\n✅ Added {len(ref_paths)} references to artist '{args.artist}'")
            for ref_path in ref_paths:
                print(f"  {ref_path}")
        except Exception as e:
            print(f"\n❌ Error: {e}", file=sys.stderr)
            sys.exit(1)
        
        return
    
    # Handle batch-add-style command
    if args.command == "batch-add-style":
        try:
            ref_paths = batch_add_style_references(
                style_name=args.style,
                image_paths=args.images,
                copy_files=not args.move,
            )
            print(f"\n✅ Added {len(ref_paths)} references to style '{args.style}'")
            for ref_path in ref_paths:
                print(f"  {ref_path}")
        except Exception as e:
            print(f"\n❌ Error: {e}", file=sys.stderr)
            sys.exit(1)
        
        return
    
    # Handle search command
    if args.command == "search":
        results = search_references(
            query=args.query,
            collection_type=args.collection_type,
            search_metadata=not args.skip_metadata,
        )
        
        total_matches = sum(len(refs) for refs in results.values())
        print(f"\nSearch results for '{args.query}' ({total_matches} matches):\n")
        
        for collection, references in results.items():
            print(f"{collection} ({len(references)} matches):")
            for i, ref in enumerate(references, 1):
                print(f"  {i}. {ref}")
            print()
        
        return
    
    # Handle export command
    if args.command == "export":
        try:
            output_path = export_collection(
                collection_type=args.collection_type,
                collection_name=args.collection_name,
                output_path=args.output,
            )
            print(f"\n✅ Exported collection '{args.collection_type}/{args.collection_name}'")
            print(f"  {output_path}")
        except Exception as e:
            print(f"\n❌ Error: {e}", file=sys.stderr)
            sys.exit(1)
        
        return
    
    # Handle import command
    if args.command == "import":
        try:
            imported, skipped = import_collection(
                collection_type=args.collection_type,
                collection_name=args.collection_name,
                zip_path=args.zip_file,
                overwrite=args.overwrite,
            )
            print(f"\n✅ Imported collection '{args.collection_type}/{args.collection_name}'")
            print(f"  Imported: {imported} files")
            print(f"  Skipped: {skipped} files")
        except Exception as e:
            print(f"\n❌ Error: {e}", file=sys.stderr)
            sys.exit(1)
        
        return


if __name__ == "__main__":
    main()