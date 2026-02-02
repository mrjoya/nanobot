#!/usr/bin/env python3
"""
Simple script to validate the fal.ai API key.
This script only tests that the key is valid by making a minimal API call.
"""

import sys
import os
import json
import urllib.request
import urllib.error
from pathlib import Path
from dotenv import load_dotenv

def validate_api_key():
    """
    Validate the fal.ai API key with a simple request.
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
        
        # Basic test endpoint (may need to be updated based on fal.ai docs)
        endpoint = "https://api.fal.ai/auth/validate"
        
        # Set up headers
        headers = {
            "Authorization": f"Key {api_key}",
            "Content-Type": "application/json"
        }
        
        # Make a simple request to validate the key
        print("Validating API key...")
        req = urllib.request.Request(endpoint, headers=headers, method='GET')
        
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                print(f"✅ API key is valid! Status code: {response.status}")
                try:
                    result = json.loads(response.read().decode('utf-8'))
                    print(f"Response: {json.dumps(result, indent=2)}")
                except:
                    # Response might not be JSON
                    print("Response is not JSON format (this is OK)")
                return True
                
        except urllib.error.HTTPError as e:
            if e.code == 401:
                print("❌ API key is invalid (401 Unauthorized)")
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
    success = validate_api_key()
    sys.exit(0 if success else 1)