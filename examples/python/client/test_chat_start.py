#!/usr/bin/env python3
"""
Test script for ARC Protocol chat.start method

Tests the chat.start method of the ARC Protocol SDK against a test server.
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
from arc.core.streaming import SSEParser

# Default configuration
SERVER_URL = "http://localhost:8000/arc"
SERVER_AGENT_ID = "price-tracker"
CLIENT_AGENT_ID = "travel-app-client"

async def test_chat_start(client, target_agent, message_content, chat_id=None, stream=False, verbose=False):
    """Test chat.start method"""
    print(f"\n=== Testing chat.start ===")
    try:
        params = {
            "target_agent": target_agent,
            "initial_message": {
                "role": "user",
                "parts": [{"type": "TextPart", "content": message_content}]
            },
            "metadata": {"test": True, "purpose": "SDK validation"}
        }
        
        if chat_id:
            params["chat_id"] = chat_id
            
        if stream:
            params["stream"] = True
            print("Note: Using streaming mode")
        
        response = await client.chat.start(**params)
        
        # Handle both streaming and non-streaming responses
        if isinstance(response, dict):
            # Non-streaming response
            if verbose:
                print("Full response:")
                print(json.dumps(response, indent=2))
            
            # Extract and display chat information
            if "result" in response and "chat" in response["result"]:
                chat = response["result"]["chat"]
                
                print(f" Chat started successfully")
                print(f"Chat ID: {chat['chatId']}")
                print(f"Status: {chat['status']}")
                
                # Display agent response if available
                if "message" in chat:
                    message = chat["message"]
                    if "parts" in message and len(message["parts"]) > 0:
                        content = message["parts"][0].get("content", "No content")
                        print(f"Agent response: {content}")
                
                return chat["chatId"]
            else:
                print(f" Invalid response format")
                return None
        else:
            # Streaming response - process the async iterator
            print(" Received streaming response")
            print("\nStreaming content:")
            chat_id = None
            full_content = ""
            
            try:
                # Process each chunk as it arrives
                # Show a waiting message
                print("Receiving message: ", end="", flush=True)
                first_content = True
                
                async for chunk in response:
                    # Use the SSEParser to parse the chunk
                    try:
                        event_type, event_data = SSEParser.parse_chunk(chunk)
                        
                        if event_type == "stream":
                            # Extract chat ID if we don't have it yet
                            if not chat_id and "chatId" in event_data:
                                chat_id = event_data["chatId"]
                            
                            # Use SSEParser to extract content
                            content = SSEParser.extract_content(event_data)
                            
                            if content:
                                # Only print if content has changed
                                if content != full_content:
                                    full_content = content
                                    # Clear the line and print the new content
                                    if first_content:
                                        print("\r" + " " * 20, end="\r", flush=True)  # Clear "Receiving message"
                                        first_content = False
                                    print(f"\r{content}", end="", flush=True)
                        elif event_type == "done":
                            print("\n\nChat completed ✓")
                            
                    except json.JSONDecodeError:
                        print(f"Raw chunk: {chunk}")
                
                print("\n")
                return chat_id
                
            except Exception as e:
                print(f"\n Error processing stream: {e}")
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
    parser = argparse.ArgumentParser(description='Test ARC Protocol chat.start method')
    parser.add_argument('--message', '-m', default="Hello, this is a test chat from the SDK test script", 
                      help='Initial message content')
    parser.add_argument('--chat-id', help='Optional chat ID to use (if not provided, server generates one)')
    parser.add_argument('--stream', '-s', action='store_true', help='Use streaming mode')
    parser.add_argument('--url', default=SERVER_URL, help='ARC server endpoint URL')
    parser.add_argument('--agent', default=SERVER_AGENT_ID, help='Target agent ID')
    parser.add_argument('--client-id', default=CLIENT_AGENT_ID, help='Client agent ID')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
    
    args = parser.parse_args()
    
    print(f"ARC Protocol chat.start Test")
    print(f"Server URL: {args.url}")
    print(f"Target agent: {args.agent}")
    print(f"Client agent: {args.client_id}")
    print(f"Message: {args.message}")
    if args.chat_id:
        print(f"Using chat ID: {args.chat_id}")
    
    # Create client
    client = ARCClient(
        endpoint=args.url,
        request_agent=args.client_id,
        timeout=30.0
    )
    
    try:
        chat_id = await test_chat_start(
            client, args.agent, args.message, args.chat_id, args.stream, args.verbose
        )
        
        if chat_id or args.stream:
            print("\nTest completed successfully!")
            if chat_id:
                print(f"Created chat ID: {chat_id}")
                print(f"Use this ID for testing chat.message and chat.end")
            return 0
        else:
            print("\nTest failed!")
            return 1
    finally:
        await client.close()

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))