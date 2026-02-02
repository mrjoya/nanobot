#!/usr/bin/env python3
"""
Simple test for fal.ai API connectivity.
"""

import sys
import os
import json
import time
import urllib.request
import urllib.error
from pathlib import Path

def load_api_key():
    """Load API key from .env file."""
    env_path = Path(__file__).parent.parent / ".env"
    with open(env_path, 'r') as f:
        for line in f:
            if line.startswith('FAL_KEY='):
                return line.strip().split('=', 1)[1]
    raise ValueError("FAL_KEY not found in .env file")

def main():
    try:
        # Load API key
        api_key = load_api_key()
        key_parts = api_key.split(':')
        masked_key = f"{key_parts[0]}:{'*' * 10}"
        print(f"API key loaded: {masked_key}")
        
        # Endpoint for a simple API test
        endpoint = "https://queue.fal.run/fal-ai/nano-banana-pro"
        
        # Simple payload for testing
        payload = {
            "prompt": "A simple test image with blue background and white circle",
            "resolution": "1K",
            "num_images": 1,
            "aspect_ratio": "1:1",
            "output_format": "png",
            "limit_generations": True,
        }
        
        # Set up headers
        headers = {
            "Authorization": f"Key {api_key}",
            "Content-Type": "application/json"
        }
        
        # Encode the payload
        data = json.dumps(payload).encode('utf-8')
        
        # Make the request
        print("Sending API request...")
        req = urllib.request.Request(endpoint, data=data, headers=headers, method='POST')
        
        with urllib.request.urlopen(req, timeout=20) as response:
            initial_response = json.loads(response.read().decode('utf-8'))
            
        print(f"Initial response: {json.dumps(initial_response, indent=2)}")
        
        # Check if queued
        if "status" in initial_response and initial_response["status"] == "IN_QUEUE":
            print("Request is queued. Checking status...")
            
            # Poll for status
            status_url = initial_response.get("status_url")
            if not status_url:
                raise ValueError("Status URL not found in response")
                
            # Poll up to 20 times, waiting 5 seconds between each attempt
            for i in range(20):
                print(f"Poll attempt {i+1}...")
                status_req = urllib.request.Request(status_url, headers=headers, method='GET')
                
                with urllib.request.urlopen(status_req, timeout=10) as status_response:
                    status_data = json.loads(status_response.read().decode('utf-8'))
                
                print(f"Status: {status_data.get('status')}")
                
                if status_data.get("status") == "COMPLETED":
                    print("Request completed!")
                    
                    # Get the final result
                    response_url = initial_response.get("response_url")
                    result_req = urllib.request.Request(response_url, headers=headers, method='GET')
                    
                    with urllib.request.urlopen(result_req, timeout=10) as result_response:
                        result = json.loads(result_response.read().decode('utf-8'))
                        
                    print(f"Final result: {json.dumps(result, indent=2)}")
                    
                    # Check for images
                    if "images" in result and len(result["images"]) > 0:
                        print("✅ Image generation successful!")
                        return True
                    else:
                        print("❌ No images found in response")
                        return False
                        
                elif status_data.get("status") in ["FAILED", "CANCELED"]:
                    print(f"❌ Request {status_data.get('status').lower()}")
                    return False
                    
                # Wait before next poll
                time.sleep(5)
                
            print("❌ Timed out waiting for completion")
            return False
            
        else:
            # Direct response (not queued)
            if "images" in initial_response and len(initial_response["images"]) > 0:
                print("✅ Image generation successful!")
                return True
            else:
                print("❌ No images found in response")
                return False
                
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)