#!/usr/bin/env python3
"""
Debug script for ARC Protocol client request

Analyzes the request format sent to the server for debugging.
"""

import asyncio
import sys
import os
import json
import httpx

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from arc.client.arc_client import ARCClient

# Default configuration
SERVER_URL = "http://localhost:8000/arc"
SERVER_AGENT_ID = "flight-finder"
CLIENT_AGENT_ID = "travel-app-client"

async def debug_request():
    """Debug ARC client request format"""
    # Create a debug version of httpx.AsyncClient
    class DebugClient(httpx.AsyncClient):
        async def post(self, *args, **kwargs):
            print("\n=== REQUEST DETAILS ===")
            print(f"URL: {args[0]}")
            print("Headers:")
            for key, value in kwargs.get("headers", {}).items():
                print(f"  {key}: {value}")
            
            print("\nRequest Body:")
            body = kwargs.get("content", kwargs.get("json", {}))
            if isinstance(body, bytes):
                body = body.decode('utf-8')
                try:
                    body = json.loads(body)
                except:
                    pass
            
            print(json.dumps(body, indent=2))
            
            # Make the actual request but catch errors
            try:
                response = await super().post(*args, **kwargs)
                print("\n=== RESPONSE DETAILS ===")
                print(f"Status: {response.status_code}")
                print("Headers:")
                for key, value in response.headers.items():
                    print(f"  {key}: {value}")
                
                if response.status_code < 300:
                    try:
                        print("\nResponse Body:")
                        print(json.dumps(response.json(), indent=2))
                    except:
                        print("\nRaw Response Body:")
                        print(response.text[:500])
                else:
                    print("\nError Response Body:")
                    print(response.text[:500])
                
                return response
            except Exception as e:
                print(f"\nException: {e}")
                raise
    
    # Create client with debug httpx client
    client = ARCClient(
        endpoint=SERVER_URL,
        request_agent=CLIENT_AGENT_ID,
        timeout=30.0
    )
    
    # Replace the http client with our debug version
    client.http_client = DebugClient()
    
    print("Sending task.create request...")
    try:
        response = await client.task.create(
            target_agent=SERVER_AGENT_ID,
            initial_message={
                "role": "user",
                "parts": [{"type": "TextPart", "content": "Debug test task"}]
            }
        )
        print("\nRequest completed successfully!")
    except Exception as e:
        print(f"\nError in request: {e}")
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(debug_request())