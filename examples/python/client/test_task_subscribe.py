#!/usr/bin/env python3
"""
Test script for ARC Protocol task.subscribe method

Tests the task.subscribe method of the ARC Protocol SDK against a test server.
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

async def test_task_subscribe(client, target_agent, task_id, callback_url, events=None, verbose=False):
    """Test task.subscribe method"""
    print(f"\n=== Testing task.subscribe with task {task_id} ===")
    
    # Default events if not specified
    if events is None:
        events = ["TASK_COMPLETED", "TASK_FAILED"]
    
    try:
        response = await client.task.subscribe(
            target_agent=target_agent,
            task_id=task_id,
            callback_url=callback_url,
            events=events
        )
        
        if verbose:
            print("Full response:")
            print(json.dumps(response, indent=2))
        
        # Extract and display subscription information
        if "result" in response and "subscription" in response["result"]:
            subscription = response["result"]["subscription"]
            
            print(f" Subscription created successfully")
            print(f"Subscription ID: {subscription['subscriptionId']}")
            print(f"Task ID: {subscription['taskId']}")
            print(f"Callback URL: {subscription['callbackUrl']}")
            print(f"Events: {', '.join(subscription['events'])}")
            print(f"Created at: {subscription.get('createdAt', 'N/A')}")
            print(f"Active: {subscription.get('active', True)}")
            
            return subscription["subscriptionId"]
        else:
            print(f" Invalid response format")
            return None
            
    except ARCException as e:
        print(f" Error: {e}")
        if verbose and hasattr(e, 'details') and e.details:
            print(f"Details: {e.details}")
        return None
    except Exception as e:
        print(f" Unexpected error: {e}")
        return None

async def main():
    parser = argparse.ArgumentParser(description='Test ARC Protocol task.subscribe method')
    parser.add_argument('task_id', help='Task ID to subscribe to')
    parser.add_argument('--callback', '-c', 
                      default="https://example.com/webhook", 
                      help='Callback URL for notifications')
    parser.add_argument('--events', '-e', nargs='+',
                      default=["TASK_COMPLETED", "TASK_FAILED", "NEW_ARTIFACT"],
                      help='Events to subscribe to')
    parser.add_argument('--url', default=SERVER_URL, help='ARC server endpoint URL')
    parser.add_argument('--agent', default=SERVER_AGENT_ID, help='Target agent ID')
    parser.add_argument('--client-id', default=CLIENT_AGENT_ID, help='Client agent ID')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
    
    args = parser.parse_args()
    
    print(f"ARC Protocol task.subscribe Test")
    print(f"Server URL: {args.url}")
    print(f"Target agent: {args.agent}")
    print(f"Client agent: {args.client_id}")
    print(f"Task ID: {args.task_id}")
    print(f"Callback URL: {args.callback}")
    print(f"Events: {', '.join(args.events)}")
    
    # Create client
    client = ARCClient(
        endpoint=args.url,
        request_agent=args.client_id,
        timeout=30.0
    )
    
    try:
        subscription_id = await test_task_subscribe(
            client, args.agent, args.task_id, args.callback, args.events, args.verbose
        )
        
        if subscription_id:
            print("\nTest completed successfully!")
            return 0
        else:
            print("\nTest failed!")
            return 1
    finally:
        await client.close()

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))