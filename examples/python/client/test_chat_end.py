#!/usr/bin/env python3
"""
Test script for ARC Protocol chat.end method

Tests the chat.end method of the ARC Protocol SDK against a test server.
Requires a valid chat ID (can be created using test_chat_start.py).
"""

import asyncio
import sys
import os
import json
import argparse

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from arc.client.arc_client import ARCClient
from arc.exceptions import ARCException

# Default configuration
SERVER_URL = "http://localhost:8000/arc"
SERVER_AGENT_ID = "price-tracker"
CLIENT_AGENT_ID = "travel-app-client"

async def test_chat_end(client, target_agent, chat_id, reason=None, verbose=False):
    """Test chat.end method"""
    print(f"\n=== Testing chat.end with chat {chat_id} ===")
    try:
        params = {
            "target_agent": target_agent,
            "chat_id": chat_id
        }
        
        if reason:
            params["reason"] = reason
        
        response = await client.chat.end(**params)
        
        if verbose:
            print("Full response:")
            print(json.dumps(response, indent=2))
        
        # Extract and display chat information
        if "result" in response and "chat" in response["result"]:
            chat = response["result"]["chat"]
            status = chat.get("status")
            
            if status == "CLOSED":
                print(f" Chat ended successfully")
                print(f"Chat ID: {chat['chatId']}")
                print(f"Status: {status}")
                
                if "reason" in chat:
                    print(f"Reason: {chat['reason']}")
                
                return True
            else:
                print(f" Chat not closed (status: {status})")
                return False
        else:
            print(f" Invalid response format")
            return False
            
    except ARCException as e:
        print(f" Error: {e}")
        if verbose and hasattr(e, 'details') and e.details:
            print(f"Details: {e.details}")
        return False
    except Exception as e:
        print(f" Unexpected error: {e}")
        return False

async def main():
    parser = argparse.ArgumentParser(description='Test ARC Protocol chat.end method')
    parser.add_argument('chat_id', help='Chat ID to end')
    parser.add_argument('--reason', '-r', default="Test chat ended by SDK test script", 
                      help='Reason for ending the chat')
    parser.add_argument('--url', default=SERVER_URL, help='ARC server endpoint URL')
    parser.add_argument('--agent', default=SERVER_AGENT_ID, help='Target agent ID')
    parser.add_argument('--client-id', default=CLIENT_AGENT_ID, help='Client agent ID')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
    
    args = parser.parse_args()
    
    print(f"ARC Protocol chat.end Test")
    print(f"Server URL: {args.url}")
    print(f"Target agent: {args.agent}")
    print(f"Client agent: {args.client_id}")
    print(f"Chat ID: {args.chat_id}")
    print(f"Reason: {args.reason}")
    
    # Create client
    client = ARCClient(
        endpoint=args.url,
        request_agent=args.client_id,
        timeout=30.0
    )
    
    try:
        success = await test_chat_end(
            client, args.agent, args.chat_id, args.reason, args.verbose
        )
        
        if success:
            print("\nTest completed successfully!")
            return 0
        else:
            print("\nTest failed!")
            return 1
    finally:
        await client.close()

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))