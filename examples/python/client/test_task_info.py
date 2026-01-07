#!/usr/bin/env python3
"""
Test script for ARC Protocol task.info method

Tests the task.info method of the ARC Protocol SDK against a test server.
Requires a valid task ID (can be created using test_task_create.py).
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

async def test_task_info(client, target_agent, task_id, include_messages=True, include_artifacts=True, verbose=False):
    """Test task.info method"""
    print(f"\n=== Testing task.info with task {task_id} ===")
    try:
        response = await client.task.info(
            target_agent=target_agent,
            task_id=task_id,
            include_messages=include_messages,
            include_artifacts=include_artifacts
        )
        
        if verbose:
            print("Full response:")
            print(json.dumps(response, indent=2))
        
        # Extract and display task information
        task = response["result"]["task"]
        status = task["status"]
        
        print(f" Task info retrieved successfully")
        print(f"Task ID: {task['taskId']}")
        print(f"Status: {status}")
        print(f"Created at: {task.get('createdAt', 'N/A')}")
        print(f"Updated at: {task.get('updatedAt', 'N/A')}")
        
        # Display messages if included
        if include_messages and "messages" in task:
            print(f"\nMessages ({len(task['messages'])}):")
            for i, msg in enumerate(task["messages"]):
                role = msg.get("role", "unknown")
                timestamp = msg.get("timestamp", "N/A")
                
                # Extract content from parts
                content = "No content"
                if "parts" in msg and len(msg["parts"]) > 0:
                    part = msg["parts"][0]
                    if "content" in part:
                        content = part["content"]
                        if isinstance(content, str) and len(content) > 50:
                            content = content[:50] + "..."
                
                print(f"  {i+1}. [{role}] {content}")
        
        # Display artifacts if included
        if include_artifacts and "artifacts" in task and task["artifacts"]:
            print(f"\nArtifacts ({len(task['artifacts'])}):")
            for i, artifact in enumerate(task["artifacts"]):
                name = artifact.get("name", "Unnamed")
                artifact_id = artifact.get("artifactId", "unknown")
                mime_type = artifact.get("mimeType", "unknown")
                created_at = artifact.get("createdAt", "N/A")
                
                print(f"  {i+1}. {name} (ID: {artifact_id}, Type: {mime_type})")
        
        # Display metadata if available
        if "metadata" in task and task["metadata"]:
            print(f"\nMetadata: {json.dumps(task['metadata'], indent=2)}")
        
        return status
    except ARCException as e:
        print(f" Error: {e}")
        if verbose and hasattr(e, 'details') and e.details:
            print(f"Details: {e.details}")
        return None
    except Exception as e:
        print(f" Unexpected error: {e}")
        return None

async def main():
    parser = argparse.ArgumentParser(description='Test ARC Protocol task.info method')
    parser.add_argument('task_id', help='Task ID to retrieve information for')
    parser.add_argument('--url', default=SERVER_URL, help='ARC server endpoint URL')
    parser.add_argument('--agent', default=SERVER_AGENT_ID, help='Target agent ID')
    parser.add_argument('--client-id', default=CLIENT_AGENT_ID, help='Client agent ID')
    parser.add_argument('--no-messages', action='store_true', help='Exclude messages from results')
    parser.add_argument('--no-artifacts', action='store_true', help='Exclude artifacts from results')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
    
    args = parser.parse_args()
    
    print(f"ARC Protocol task.info Test")
    print(f"Server URL: {args.url}")
    print(f"Target agent: {args.agent}")
    print(f"Client agent: {args.client_id}")
    print(f"Task ID: {args.task_id}")
    
    # Create client
    client = ARCClient(
        endpoint=args.url,
        request_agent=args.client_id,
        timeout=30.0
    )
    
    try:
        status = await test_task_info(
            client, 
            args.agent, 
            args.task_id, 
            not args.no_messages, 
            not args.no_artifacts,
            args.verbose
        )
        
        if status:
            print("\nTest completed successfully!")
            return 0
        else:
            print("\nTest failed!")
            return 1
    finally:
        await client.close()

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))