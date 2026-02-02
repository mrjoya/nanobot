#!/usr/bin/env python3
"""
Test fal.ai API with a reference image (image-to-image functionality).
"""

import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.api import edit_image, download_image, preview_cost
from dotenv import load_dotenv

def test_api_with_reference():
    """
    Test the image-to-image endpoint with our reference image.
    """
    print("\n🧪 Testing fal.ai API with reference image\n")
    
    # Load .env file
    dotenv_path = Path(__file__).parent.parent / ".env"
    if dotenv_path.exists():
        load_dotenv(dotenv_path)
        print(f"Loaded environment from {dotenv_path}")
    
    # Define the reference image path
    test_output_dir = Path(__file__).parent.parent / "test_output"
    reference_image_path = test_output_dir / "reference_test_image.png"
    
    if not reference_image_path.exists():
        print(f"❌ Reference image not found at {reference_image_path}")
        print("Please run create_test_image.py first.")
        return False
    
    # Show cost estimate
    print("\n💰 Cost estimate for image-to-image test:")
    preview_cost(num_images=1, resolution="1K")
    
    # Test image-to-image endpoint
    print(f"\n🖼️ Testing image-to-image generation with reference: {reference_image_path}")
    try:
        edit_result = edit_image(
            prompt="Transform this into an Afghan music album cover with traditional style, keep the circular shape as a central element",
            image_urls=[str(reference_image_path)],
            resolution="1K",
            num_images=1
        )
        
        print(f"\nAPI Response: {edit_result}")
        
        if "images" in edit_result and len(edit_result["images"]) > 0:
            print(f"✅ Image-to-image generation successful")
            
            # Download the edited image
            output_image_path = test_output_dir / "afghan_cover_test.png"
            edit_url = edit_result["images"][0]["url"]
            
            print(f"Downloading image from URL: {edit_url}")
            downloaded_path = download_image(edit_url, output_image_path)
            
            print(f"Image saved to: {downloaded_path}")
            
            return True
        else:
            print(f"❌ Image-to-image generation failed: Unexpected response")
            print(f"Response: {edit_result}")
            return False
            
    except Exception as e:
        print(f"❌ Image-to-image generation error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_api_with_reference()
    sys.exit(0 if success else 1)