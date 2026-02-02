#!/usr/bin/env python3
"""
Create a simple test image to use as reference for API testing.
"""

import os
from pathlib import Path

try:
    # Try to import PIL for image creation
    from PIL import Image, ImageDraw
    
    # Create output directory
    output_dir = Path(__file__).parent.parent / "test_output"
    output_dir.mkdir(exist_ok=True)
    
    # Create a blue 400x400 image with a white circle
    img = Image.new('RGB', (400, 400), color=(0, 100, 200))
    draw = ImageDraw.Draw(img)
    
    # Draw a white circle
    circle_x = 200
    circle_y = 200
    circle_radius = 100
    draw.ellipse(
        (circle_x - circle_radius, circle_y - circle_radius, 
         circle_x + circle_radius, circle_y + circle_radius), 
        fill=(255, 255, 255)
    )
    
    # Save the image
    output_path = output_dir / "reference_test_image.png"
    img.save(output_path)
    
    print(f"Created test image: {output_path}")
except ImportError:
    print("PIL/Pillow is not installed. Installing...")
    import subprocess
    import sys
    subprocess.call([sys.executable, "-m", "pip", "install", "pillow"])
    print("Please run this script again after installation.")