#!/usr/bin/env python3
"""
Test script for ARC Protocol task.cancel method

Tests the task.cancel method of the ARC Protocol SDK against a test server.
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

async def test_task_cancel(client, target_agent, task_id, reason=None, verbose=False):
    """Test task.cancel method"""
    print(f"\n=== Testing task.cancel with task {task_id} ===")
    try:
        # Build parameters
        params = {}
        if reason:
            params["reason"] = reason
        
        response = await client.task.cancel(
            target_agent=target_agent,
            task_id=task_id,
            reason=reason
        )
        
        if verbose:
            print("Full response:")
            print(json.dumps(response, indent=2))
        
        # Extract and display task information
        task = response["result"]["task"]
        status = task["status"]
        
        if status == "CANCELED":
            print(f" Task canceled successfully")
            print(f"Task ID: {task['taskId']}")
            print(f"Status: {status}")
            
            if "canceledAt" in task:
                print(f"Canceled at: {task['canceledAt']}")
                
            if "reason" in task:
                print(f"Reason: {task['reason']}")
            
            return True
        else:
            print(f" Task not canceled (status: {status})")
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
    parser = argparse.ArgumentParser(description='Test ARC Protocol task.cancel method')
    parser.add_argument('task_id', help='Task ID to cancel')
    parser.add_argument('--reason', '-r', default="Test cancellation via SDK", 
                      help='Reason for cancellation')
    parser.add_argument('--url', default=SERVER_URL, help='ARC server endpoint URL')
    parser.add_argument('--agent', default=SERVER_AGENT_ID, help='Target agent ID')
    parser.add_argument('--client-id', default=CLIENT_AGENT_ID, help='Client agent ID')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
    
    args = parser.parse_args()
    
    print(f"ARC Protocol task.cancel Test")
    print(f"Server URL: {args.url}")
    print(f"Target agent: {args.agent}")
    print(f"Client agent: {args.client_id}")
    print(f"Task ID: {args.task_id}")
    print(f"Reason: {args.reason}")
    
    # Create client
    client = ARCClient(
        endpoint=args.url,
        request_agent=args.client_id,
        timeout=30.0
    )
    
    try:
        success = await test_task_cancel(client, args.agent, args.task_id, args.reason, args.verbose)
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