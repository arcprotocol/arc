#!/usr/bin/env python3
"""
Test script for ARC Protocol task.create method

Tests the task.create method of the ARC Protocol SDK against a test server.
"""

import asyncio
import sys
import os
import json
import argparse
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from arc.client.arc_client import ARCClient
from arc.exceptions import ARCException

# Default configuration
SERVER_URL = "http://localhost:8000/arc"
SERVER_AGENT_ID = "flight-finder"
CLIENT_AGENT_ID = "travel-app-client"

async def test_task_create(client, target_agent, verbose=False):
    """Test task.create method"""
    print("\n=== Testing task.create ===")
    try:
        response = await client.task.create(
            target_agent=target_agent,
            initial_message={
                "role": "user",
                "parts": [{"type": "TextPart", "content": "Find flights from New York (JFK) to Los Angeles (LAX) for next Friday"}]
            },
            priority="HIGH",
            metadata={"route": "JFK-LAX", "purpose": "flight search"}
        )
        
        if verbose:
            print("Full response:")
            print(json.dumps(response, indent=2))
        
        # Extract and display task information
        task = response["result"]["task"]
        task_id = task["taskId"]
        status = task["status"]
        
        print(f"Task created successfully")
        print(f"Task ID: {task_id}")
        print(f"Status: {status}")
        print(f"Created at: {task.get('createdAt', 'N/A')}")
        print(f"Priority: {task.get('priority', 'NORMAL')}")
        
        return task_id
    except ARCException as e:
        print(f"Error: {e}")
        if verbose and hasattr(e, 'details') and e.details:
            print(f"Details: {e.details}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

async def main():
    parser = argparse.ArgumentParser(description='Test ARC Protocol task.create method')
    parser.add_argument('--url', default=SERVER_URL, help='ARC server endpoint URL')
    parser.add_argument('--agent', default=SERVER_AGENT_ID, help='Target agent ID')
    parser.add_argument('--client-id', default=CLIENT_AGENT_ID, help='Client agent ID')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
    
    args = parser.parse_args()
    
    print(f"ARC Protocol task.create Test")
    print(f"Server URL: {args.url}")
    print(f"Target agent: {args.agent}")
    print(f"Client agent: {args.client_id}")
    
    # Create client
    client = ARCClient(
        endpoint=args.url,
        request_agent=args.client_id,
        timeout=30.0
    )
    
    try:
        task_id = await test_task_create(client, args.agent, args.verbose)
        if task_id:
            print("\nTest completed successfully!")
            return 0
        else:
            print("\nTest failed!")
            return 1
    finally:
        await client.close()

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))