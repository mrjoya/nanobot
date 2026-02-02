#!/usr/bin/env python3
"""
Test script to validate fal.ai API connectivity.
Tests both text-to-image and image-to-image endpoints.
"""

import sys
import os
import time
from pathlib import Path
import tempfile
import urllib.request

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.api import generate_image, edit_image, download_image, preview_cost
from dotenv import load_dotenv

# Check if required packages are installed, install if missing
def check_dependencies():
    try:
        import dotenv
        print("✅ python-dotenv is installed")
    except ImportError:
        print("❌ python-dotenv is missing. Installing...")
        import subprocess
        subprocess.call([sys.executable, "-m", "pip", "install", "python-dotenv"])

def test_api_connectivity():
    """
    Test fal.ai API connectivity using both endpoints.
    """
    print("\n🧪 Testing fal.ai API connectivity\n")
    
    # Test key loading
    try:
        from shared.api import load_api_key
        api_key = load_api_key()
        key_parts = api_key.split(':')
        masked_key = f"{key_parts[0]}:{'*' * 10}"
        print(f"✅ API key loaded: {masked_key}")
    except Exception as e:
        print(f"❌ API key error: {e}")
        return False
    
    # Show cost estimate
    print("\n💰 Cost estimate for tests:")
    preview_cost(num_images=1, resolution="1K")
    
    # Create output directory for test results
    test_output_dir = Path(__file__).parent.parent / "test_output"
    test_output_dir.mkdir(exist_ok=True)
    
    # Test text-to-image endpoint
    print("\n🖼️ Testing text-to-image generation...")
    try:
        # Use a simple prompt for testing
        result = generate_image(
            prompt="A simple test image with blue background and white circle in the center",
            resolution="1K",
            num_images=1,
            output_format="png"
        )
        
        if "images" in result and len(result["images"]) > 0:
            print(f"✅ Text-to-image generation successful")
            
            # Download the test image to our output directory
            test_image_path = test_output_dir / "test_output_text2img.png"
            url = result["images"][0]["url"]
            
            print(f"Downloading image from URL: {url}")
            downloaded_path = download_image(url, test_image_path)
            
            print(f"Image saved to: {downloaded_path}")
            
            if os.path.exists(test_image_path):
                print(f"✅ Image download successful")
                
                # Use the generated image for the image-to-image test
                print("\n🖼️ Testing image-to-image generation...")
                try:
                    edit_result = edit_image(
                        prompt="Same image but with a red background instead of blue",
                        image_urls=[str(test_image_path)],
                        resolution="1K",
                        num_images=1
                    )
                    
                    if "images" in edit_result and len(edit_result["images"]) > 0:
                        print(f"✅ Image-to-image generation successful")
                        
                        # Download the edited image
                        edit_image_path = test_output_dir / "test_output_img2img.png"
                        edit_url = edit_result["images"][0]["url"]
                        
                        print(f"Downloading edited image from URL: {edit_url}")
                        downloaded_edit_path = download_image(edit_url, edit_image_path)
                        
                        print(f"Edited image saved to: {downloaded_edit_path}")
                        
                        return True
                    else:
                        print(f"❌ Image-to-image generation failed: Unexpected response")
                        print(f"Response: {edit_result}")
                        return False
                        
                except Exception as e:
                    print(f"❌ Image-to-image generation error: {e}")
                    return False
            else:
                print(f"❌ Image download failed")
                return False
        else:
            print(f"❌ Text-to-image generation failed: Unexpected response")
            print(f"Response: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Text-to-image generation error: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    return True


if __name__ == "__main__":
    # Check and install dependencies
    check_dependencies()
    
    # Load .env file
    dotenv_path = Path(__file__).parent.parent / ".env"
    if dotenv_path.exists():
        load_dotenv(dotenv_path)
        print(f"Loaded environment from {dotenv_path}")
    else:
        print(f"⚠️ Warning: .env file not found at {dotenv_path}")
        
    # Create output directory for test images if needed
    test_output_dir = Path(__file__).parent.parent / "test_output"
    test_output_dir.mkdir(exist_ok=True)
    print(f"Test output will be saved to: {test_output_dir}")
    
    # Run the test
    success = test_api_connectivity()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)