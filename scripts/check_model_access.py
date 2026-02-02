#!/usr/bin/env python3
"""
Check access to the nano-banana-pro model using the API key.
This script tests basic auth against the model's endpoint.
"""

import sys
import os
import json
import urllib.request
import urllib.error
from pathlib import Path
from dotenv import load_dotenv

def check_model_access():
    """
    Check if we have access to the nano-banana-pro model.
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
        endpoint = "https://queue.fal.run/fal-ai/nano-banana-pro/info"
        
        # Set up headers
        headers = {
            "Authorization": f"Key {api_key}",
            "Content-Type": "application/json"
        }
        
        # Make a request to check model access
        print("Checking model access...")
        req = urllib.request.Request(endpoint, headers=headers, method='GET')
        
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                print(f"✅ Successfully connected to model endpoint! Status code: {response.status}")
                try:
                    result = json.loads(response.read().decode('utf-8'))
                    print(f"Model info: {json.dumps(result, indent=2)}")
                except:
                    # Response might not be JSON
                    print("Response is not JSON format")
                return True
                
        except urllib.error.HTTPError as e:
            if e.code == 401:
                print("❌ API key is invalid or lacks permission for this model (401 Unauthorized)")
            elif e.code == 403:
                print("❌ API key is valid but lacks permission for this model (403 Forbidden)")
            elif e.code == 404:
                print("❌ Model endpoint not found (404 Not Found)")
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
    success = check_model_access()
    sys.exit(0 if success else 1)