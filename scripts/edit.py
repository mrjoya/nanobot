#!/usr/bin/env python3
"""
Cover Art Editor - Nano Banana Pro Edit via fal.ai
Usage: python edit.py --prompt "Make it blue with sparkles" --image image.jpg [options]
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
import base64
import mimetypes
from datetime import datetime
from pathlib import Path

FAL_API_URL = "https://queue.fal.run/fal-ai/nano-banana-pro/edit"

def upload_image(image_path):
    """Upload image to fal.ai storage service."""
    # This is a simplified approach - in a more robust implementation,
    # we would use the fal_client library for uploads
    with open(image_path, "rb") as f:
        file_data = f.read()
    
    file_type = mimetypes.guess_type(image_path)[0] or "application/octet-stream"
    file_ext = os.path.splitext(image_path)[1].lstrip(".")
    if not file_type.startswith("image/"):
        file_type = f"image/{file_ext}"
    
    # Convert to data URI - easier than separate upload for this script
    data_uri = f"data:{file_type};base64,{base64.b64encode(file_data).decode('utf-8')}"
    return data_uri

def edit_image(prompt, image_paths, api_key, resolution="1K", aspect_ratio="auto", num_images=1):
    """Call fal.ai Nano Banana Pro Edit API."""
    
    # Convert local file paths to data URIs or use as-is if they're already URLs
    image_urls = []
    for path in image_paths:
        if path.startswith(("http://", "https://", "data:")):
            image_urls.append(path)
        else:
            # Local file, upload it
            image_urls.append(upload_image(path))
    
    payload = {
        "prompt": prompt,
        "image_urls": image_urls,
        "aspect_ratio": aspect_ratio,
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
        description="Edit images using Nano Banana Pro",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --prompt "Make it blue with sparkles" --image album_cover.jpg
  %(prog)s --prompt "Add a vintage filter and grain" --image cover1.jpg --image cover2.jpg
  %(prog)s --prompt "Add a bright cyberpunk neon glow" --image input.png --aspect-ratio 1:1 --resolution 2K
        """
    )
    
    parser.add_argument("--prompt", required=True, help="Editing instructions")
    parser.add_argument("--image", dest="images", action="append", required=True, 
                        help="Input image(s) to edit (local file or URL, can use multiple times)")
    parser.add_argument("--aspect-ratio", default="auto", 
                        choices=["auto", "21:9", "16:9", "3:2", "4:3", "5:4", "1:1", "4:5", "3:4", "2:3", "9:16"],
                        help="Output aspect ratio (default: auto - keeps original)")
    parser.add_argument("--resolution", default="1K", choices=["1K", "2K", "4K"],
                        help="Output resolution (4K costs 2x)")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--output-dir", default=".", help="Output directory (default: current)")
    parser.add_argument("--num", type=int, default=1, help="Number of variations (1-4)")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    
    args = parser.parse_args()
    
    # Validate num
    if args.num < 1 or args.num > 4:
        print("Error: --num must be between 1 and 4", file=sys.stderr)
        sys.exit(1)
    
    # Get API key
    api_key = os.environ.get("FAL_KEY")
    if not api_key:
        print("Error: FAL_KEY environment variable not set", file=sys.stderr)
        print("Get your key at: https://fal.ai/dashboard/keys", file=sys.stderr)
        sys.exit(1)
    
    if not args.json:
        print(f"🖌️ Editing image(s) with prompt: {args.prompt}", file=sys.stderr)
        for img in args.images:
            print(f"📷 Input: {img}", file=sys.stderr)
    
    # Generate
    result = edit_image(args.prompt, args.images, api_key, args.resolution, args.aspect_ratio, args.num)
    
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
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            
            if args.output and len(images) == 1:
                out_path = args.output
            else:
                base_name = Path(args.images[0]).stem if args.images else "edit"
                out_path = output_dir / f"{base_name}-edited-{timestamp}-{i+1}.png"
            
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
        "prompt": args.prompt,
        "inputs": args.images,
        "aspect_ratio": args.aspect_ratio,
        "resolution": args.resolution,
        "outputs": downloaded,
        "count": len(downloaded),
        "cost": f"${cost:.2f}"
    }
    
    if args.json:
        print(json.dumps(output_data, indent=2))
    else:
        print(f"\n✨ Edited {len(downloaded)} image(s)")
        print(f"💰 Estimated cost: ${cost:.2f}")


if __name__ == "__main__":
    main()