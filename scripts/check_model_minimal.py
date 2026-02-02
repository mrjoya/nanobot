#!/usr/bin/env python3
"""
Minimal check for nano-banana-pro model access.
Using the documented POST endpoint with minimal payload.
"""

import sys
import os
import json
import urllib.request
import urllib.error
from pathlib import Path
from dotenv import load_dotenv

def check_minimal():
    """
    Minimal check for nano-banana-pro model access.
    """
    try:
        # Load the .env file
        dotenv_path = Path(__file__).parent.parent / ".env"
        if dotenv_path.exists():
            load_dotenv(dotenv_path)
            print(f"Loaded environment from {dotenv_path}")
        
        # Get the API key
        api_key = os.environ.get("FAL_KEY")
        if not api_key:
            print("❌ FAL_KEY not found in environment variables or .env file")
            return False
        
        # Mask the key for display
        key_parts = api_key.split(':')
        if len(key_parts) == 2:
            masked_key = f"{key_parts[0]}:{'*' * 10}"
        else:
            masked_key = f"{'*' * 10}"
        print(f"API key loaded: {masked_key}")
        
        # Model endpoint
        endpoint = "https://queue.fal.run/fal-ai/nano-banana-pro"
        
        # Minimal payload 
        payload = {
            "prompt": "test",
            "num_images": 1,
            "resolution": "1K"
        }
        
        # Set up headers
        headers = {
            "Authorization": f"Key {api_key}",
            "Content-Type": "application/json"
        }
        
        # Encode the payload
        data = json.dumps(payload).encode('utf-8')
        
        # Make a request to check model access
        print("Testing model access with minimal payload...")
        req = urllib.request.Request(endpoint, data=data, headers=headers, method='POST')
        
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                result = json.loads(response.read().decode('utf-8'))
                print(f"✅ Successfully submitted request to model!")
                print(f"Response: {json.dumps(result, indent=2)}")
                
                if "status" in result and result["status"] == "IN_QUEUE":
                    print("✅ Request accepted and queued (this is good!)")
                    print(f"Queue position: {result.get('queue_position', 'unknown')}")
                    print(f"Request ID: {result.get('request_id', 'unknown')}")
                    return True
                else:
                    print("Response format is unexpected, but we got a 200 OK response")
                    return True
                
        except urllib.error.HTTPError as e:
            if e.code == 401:
                print("❌ API key is invalid (401 Unauthorized)")
            elif e.code == 403:
                print("❌ API key is valid but lacks permission (403 Forbidden)")
            else:
                print(f"❌ HTTP Error: {e.code} - {e.reason}")
            
            error_body = e.read().decode('utf-8') if e.fp else ""
            print(f"Error details: {error_body}")
            return False
            
        except urllib.error.URLError as e:
            print(f"❌ Connection Error: {e.reason}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = check_minimal()
    sys.exit(0 if success else 1)