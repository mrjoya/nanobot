"""
Shared fal.ai API utilities for NanoBot tools.

COST REFERENCE (as of 2026):
- Base cost: $0.15 per image
- 4K resolution: 2x cost ($0.30 per image)
- num_images: Multiplied by base cost

COST CONTROL TIPS:
- Use 1K resolution for drafts/testing
- Use limit_generations=True to prevent prompt injection
- Generate 1 image first, then variations if needed
- Use jpeg format for smaller file sizes (no cost difference)
"""

import json
import os
import base64
import mimetypes
import urllib.request
import urllib.error
from pathlib import Path
from dotenv import load_dotenv

# API Endpoints
ENDPOINTS = {
    "text_to_image": "https://queue.fal.run/fal-ai/nano-banana-pro",
    "image_to_image": "https://queue.fal.run/fal-ai/nano-banana-pro/edit",
}

# Cost constants
COST_PER_IMAGE = 0.15  # Base cost in USD
COST_4K_MULTIPLIER = 2.0  # 4K costs 2x


def estimate_cost(num_images=1, resolution="1K"):
    """
    Estimate the cost for a generation request.
    
    Args:
        num_images: Number of images to generate (1-4)
        resolution: "1K", "2K", or "4K"
    
    Returns:
        Estimated cost in USD
    """
    base = COST_PER_IMAGE * num_images
    if resolution == "4K":
        base *= COST_4K_MULTIPLIER
    return base


def load_api_key():
    """Load API key from environment or .env file."""
    # Try to find .env in parent directories
    current = Path(__file__).parent
    for _ in range(3):  # Check up to 3 levels
        env_file = current / '.env'
        if env_file.exists():
            load_dotenv(env_file)
            break
        current = current.parent
    
    api_key = os.environ.get("FAL_KEY")
    if not api_key:
        raise ValueError(
            "FAL_KEY not found. Please create a .env file with your API key.\n"
            "Get your key at: https://fal.ai/dashboard/keys"
        )
    return api_key


def image_to_data_uri(image_path):
    """Convert a local image file to a data URI."""
    with open(image_path, "rb") as f:
        file_data = f.read()
    
    file_type = mimetypes.guess_type(image_path)[0] or "application/octet-stream"
    file_ext = os.path.splitext(image_path)[1].lstrip(".")
    if not file_type.startswith("image/"):
        file_type = f"image/{file_ext}"
    
    return f"data:{file_type};base64,{base64.b64encode(file_data).decode('utf-8')}"


def prepare_image_urls(image_paths):
    """
    Convert a list of image paths/URLs to URLs suitable for the API.
    Handles local files, URLs, and data URIs.
    """
    urls = []
    for path in image_paths:
        if isinstance(path, str):
            if path.startswith(("http://", "https://", "data:")):
                urls.append(path)
            else:
                # Local file
                urls.append(image_to_data_uri(path))
        else:
            raise ValueError(f"Invalid image path type: {type(path)}")
    return urls


def call_api(endpoint, payload, timeout=120):
    """Make an API call to fal.ai."""
    api_key = load_api_key()
    
    headers = {
        "Authorization": f"Key {api_key}",
        "Content-Type": "application/json"
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(endpoint, data=data, headers=headers, method='POST')
    
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8') if e.fp else str(e)
        raise RuntimeError(f"API Error {e.code}: {error_body}")
    except urllib.error.URLError as e:
        raise RuntimeError(f"Connection Error: {e.reason}")


def download_image(url, output_path):
    """Download an image from a URL to a local path."""
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=60) as response:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'wb') as f:
            f.write(response.read())
    return str(output_path)


def generate_image(
    prompt,
    resolution="1K",
    aspect_ratio="1:1",
    num_images=1,
    output_format="png",
    seed=None,
    limit_generations=True,
    enable_web_search=False,
    sync_mode=False,
):
    """
    Generate images from text prompt.
    
    Args:
        prompt: Text description for image generation
        resolution: "1K" (default, cheapest), "2K", or "4K" (2x cost)
        aspect_ratio: Image ratio (default "1:1" for album covers)
        num_images: Number to generate (1-4, each costs $0.15)
        output_format: "png" (default), "jpeg", or "webp"
        seed: Random seed for reproducibility (optional)
        limit_generations: If True, ignore prompt instructions for multiple images (RECOMMENDED for cost control)
        enable_web_search: Allow model to search web (default False)
        sync_mode: Return as data URI instead of URL (default False)
    
    Returns:
        API response with generated images
    
    Cost: $0.15/image (1K/2K), $0.30/image (4K)
    """
    payload = {
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "resolution": resolution,
        "num_images": num_images,
        "output_format": output_format,
        "limit_generations": limit_generations,
        "enable_web_search": enable_web_search,
        "sync_mode": sync_mode,
    }
    
    if seed is not None:
        payload["seed"] = seed
    
    return call_api(ENDPOINTS["text_to_image"], payload)


def edit_image(
    prompt,
    image_urls,
    resolution="1K",
    aspect_ratio="auto",
    num_images=1,
    output_format="png",
    seed=None,
    limit_generations=True,
    enable_web_search=False,
    sync_mode=False,
):
    """
    Edit/transform images using reference images and a prompt.
    
    Args:
        prompt: Instructions for editing/transformation
        image_urls: List of reference image paths/URLs (up to 14)
        resolution: "1K" (default, cheapest), "2K", or "4K" (2x cost)
        aspect_ratio: "auto" (keeps original) or specific ratio
        num_images: Number of variations (1-4, each costs $0.15)
        output_format: "png" (default), "jpeg", or "webp"
        seed: Random seed for reproducibility (optional)
        limit_generations: If True, ignore prompt instructions for multiple images (RECOMMENDED)
        enable_web_search: Allow model to search web (default False)
        sync_mode: Return as data URI instead of URL (default False)
    
    Returns:
        API response with edited images
    
    Cost: $0.15/image (1K/2K), $0.30/image (4K)
    """
    # Ensure image_urls are properly formatted
    prepared_urls = prepare_image_urls(image_urls) if image_urls else []
    
    payload = {
        "prompt": prompt,
        "image_urls": prepared_urls,
        "aspect_ratio": aspect_ratio,
        "resolution": resolution,
        "num_images": num_images,
        "output_format": output_format,
        "limit_generations": limit_generations,
        "enable_web_search": enable_web_search,
        "sync_mode": sync_mode,
    }
    
    if seed is not None:
        payload["seed"] = seed
    
    return call_api(ENDPOINTS["image_to_image"], payload)


# Convenience function to show cost before generating
def preview_cost(num_images=1, resolution="1K"):
    """
    Print estimated cost for a generation.
    
    Usage:
        preview_cost(num_images=4, resolution="2K")
        # Output: Estimated cost: $0.60 (4 images at 2K)
    """
    cost = estimate_cost(num_images, resolution)
    print(f"Estimated cost: ${cost:.2f} ({num_images} image(s) at {resolution})")
    return cost
