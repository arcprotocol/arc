#!/usr/bin/env python3
"""
Test script for ARC Protocol task.send method

Tests the task.send method of the ARC Protocol SDK against a test server.
Requires a valid task ID (can be created using test_task_create.py).
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
SERVER_AGENT_ID = "flight-finder"
CLIENT_AGENT_ID = "travel-app-client"

async def test_task_send(client, target_agent, task_id, message_content, verbose=False):
    """Test task.send method"""
    print(f"\n=== Testing task.send with task {task_id} ===")
    try:
        response = await client.task.send(
            target_agent=target_agent,
            task_id=task_id,
            message={
                "role": "user",
                "parts": [{"type": "TextPart", "content": message_content}]
            }
        )
        
        if verbose:
            print("Full response:")
            print(json.dumps(response, indent=2))
        
        # Validate response
        if "result" in response and "success" in response["result"]:
            success = response["result"]["success"]
            message = response["result"].get("message", "No message provided")
            
            if success:
                print(f" Message sent successfully")
                print(f"Response: {message}")
                return True
            else:
                print(f" Server reported failure")
                print(f"Message: {message}")
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
    parser = argparse.ArgumentParser(description='Test ARC Protocol task.send method')
    parser.add_argument('task_id', help='Task ID to send a message to')
    parser.add_argument('--message', '-m', default="This is a test message from task.send test script", 
                      help='Message content to send')
    parser.add_argument('--url', default=SERVER_URL, help='ARC server endpoint URL')
    parser.add_argument('--agent', default=SERVER_AGENT_ID, help='Target agent ID')
    parser.add_argument('--client-id', default=CLIENT_AGENT_ID, help='Client agent ID')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
    
    args = parser.parse_args()
    
    print(f"ARC Protocol task.send Test")
    print(f"Server URL: {args.url}")
    print(f"Target agent: {args.agent}")
    print(f"Client agent: {args.client_id}")
    print(f"Task ID: {args.task_id}")
    print(f"Message: {args.message}")
    
    # Create client
    client = ARCClient(
        endpoint=args.url,
        request_agent=args.client_id,
        timeout=30.0
    )
    
    try:
        success = await test_task_send(client, args.agent, args.task_id, args.message, args.verbose)
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