#!/usr/bin/env python3
"""
ARC Protocol Client Test Suite

A comprehensive test suite for the ARC Protocol SDK client implementation.
Tests all standard methods against a test server with detailed reporting.
"""

import asyncio
import sys
import os
import json
import argparse
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from arc.client.arc_client import ARCClient
from arc.exceptions import ARCException
from arc.utils.logging import configure_root_logger, create_logger

# Configuration
SERVER_URL = "http://localhost:8000/arc"
SERVER_AGENT_ID = "flight-finder"  # Using flight-finder as primary test agent
CLIENT_AGENT_ID = "travel-app-client"

# Configure logging
configure_root_logger(level=logging.INFO)
logger = create_logger("arc-client-test")

class TestResult:
    """Track test results for reporting"""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.skipped = 0
        self.tests = []
    
    def add_result(self, name: str, passed: bool, error: Optional[Exception] = None, skipped: bool = False):
        """Add a test result"""
        if skipped:
            self.skipped += 1
            status = "SKIPPED"
        elif passed:
            self.passed += 1
            status = "PASSED"
        else:
            self.failed += 1
            status = "FAILED"
            
        self.tests.append({
            "name": name,
            "status": status,
            "error": str(error) if error else None,
            "timestamp": datetime.now().isoformat()
        })
    
    def print_summary(self):
        """Print test result summary"""
        print("\n========== TEST RESULTS ==========")
        print(f"Passed:  {self.passed}")
        print(f"Failed:  {self.failed}")
        print(f"Skipped: {self.skipped}")
        print(f"Total:   {self.passed + self.failed + self.skipped}")
        
        if self.failed > 0:
            print("\nFailed Tests:")
            for test in self.tests:
                if test["status"] == "FAILED":
                    print(f"- {test['name']}: {test['error']}")
        
        print("================================\n")
        
        return self.failed == 0

# Task Tests
async def test_task_create(client: ARCClient, results: TestResult) -> Optional[str]:
    """Test task.create method"""
    test_name = "task.create"
    print(f"\n=== Testing {test_name} ===")
    
    try:
        response = await client.task.create(
            target_agent=SERVER_AGENT_ID,
            initial_message={
                "role": "user",
                "parts": [{"type": "TextPart", "content": "Find flights from New York (JFK) to Los Angeles (LAX) for next Friday"}]
            },
            priority="HIGH",
            metadata={"route": "JFK-LAX", "purpose": "flight search"}
        )
        
        # Validate response
        assert "result" in response, "Missing 'result' field in response"
        assert "type" in response["result"], "Missing 'type' field in result"
        assert response["result"]["type"] == "task", "Invalid result type"
        assert "task" in response["result"], "Missing 'task' field in result"
        assert "taskId" in response["result"]["task"], "Missing 'taskId' in task"
        assert "status" in response["result"]["task"], "Missing 'status' in task"
        
        task_id = response["result"]["task"]["taskId"]
        status = response["result"]["task"]["status"]
        
        print(f"Task created successfully with ID: {task_id}")
        print(f"Initial status: {status}")
        
        results.add_result(test_name, True)
        return task_id
    except Exception as e:
        print(f"Error in {test_name}: {e}")
        results.add_result(test_name, False, e)
        return None

async def test_task_send(client: ARCClient, results: TestResult, task_id: str) -> bool:
    """Test task.send method"""
    test_name = "task.send"
    print(f"\n=== Testing {test_name} ===")
    
    if not task_id:
        print(f"Skipping {test_name}: No task ID available")
        results.add_result(test_name, False, skipped=True)
        return False
    
    try:
        response = await client.task.send(
            target_agent=SERVER_AGENT_ID,
            task_id=task_id,
            message={
                "role": "user",
                "parts": [{"type": "TextPart", "content": "Please also include connecting flights with one stop"}]
            }
        )
        
        # Validate response
        assert "result" in response, "Missing 'result' field in response"
        assert "success" in response["result"], "Missing 'success' field in result"
        assert response["result"]["success"] is True, "Task message not sent successfully"
        
        print(f"Message sent successfully to task {task_id}")
        print(f"Response: {json.dumps(response['result'], indent=2)}")
        
        results.add_result(test_name, True)
        return True
    except Exception as e:
        print(f"Error in {test_name}: {e}")
        results.add_result(test_name, False, e)
        return False

async def test_task_info(client: ARCClient, results: TestResult, task_id: str) -> Optional[str]:
    """Test task.info method"""
    test_name = "task.info"
    print(f"\n=== Testing {test_name} ===")
    
    if not task_id:
        print(f"Skipping {test_name}: No task ID available")
        results.add_result(test_name, False, skipped=True)
        return None
    
    try:
        response = await client.task.info(
            target_agent=SERVER_AGENT_ID,
            task_id=task_id,
            include_messages=True,
            include_artifacts=True
        )
        
        # Validate response
        assert "result" in response, "Missing 'result' field in response"
        assert "type" in response["result"], "Missing 'type' field in result"
        assert response["result"]["type"] == "task", "Invalid result type"
        assert "task" in response["result"], "Missing 'task' field in result"
        assert "status" in response["result"]["task"], "Missing 'status' field in task"
        
        task = response["result"]["task"]
        status = task["status"]
        
        print(f"Task info retrieved successfully")
        print(f"Status: {status}")
        
        # Print messages if available
        if "messages" in task:
            print(f"Messages: {len(task['messages'])}")
            for i, msg in enumerate(task["messages"]):
                content = "No content"
                if "parts" in msg and len(msg["parts"]) > 0:
                    content = msg["parts"][0].get("content", "")
                    if isinstance(content, str) and len(content) > 50:
                        content = content[:50] + "..."
                print(f"  Message {i+1}: {msg['role']} - {content}")
        
        # Print artifacts if available
        if "artifacts" in task and task["artifacts"]:
            print(f"Artifacts: {len(task['artifacts'])}")
            for i, artifact in enumerate(task["artifacts"]):
                print(f"  Artifact {i+1}: {artifact['name']}")
                
        results.add_result(test_name, True)
        return status
    except Exception as e:
        print(f"Error in {test_name}: {e}")
        results.add_result(test_name, False, e)
        return None

async def test_task_cancel(client: ARCClient, results: TestResult, task_id: str) -> bool:
    """Test task.cancel method"""
    test_name = "task.cancel"
    print(f"\n=== Testing {test_name} ===")
    
    if not task_id:
        print(f"Skipping {test_name}: No task ID available")
        results.add_result(test_name, False, skipped=True)
        return False
    
    try:
        response = await client.task.cancel(
            target_agent=SERVER_AGENT_ID,
            task_id=task_id,
            reason="Travel plans changed"
        )
        
        # Validate response
        assert "result" in response, "Missing 'result' field in response"
        assert "type" in response["result"], "Missing 'type' field in result"
        assert response["result"]["type"] == "task", "Invalid result type"
        assert "task" in response["result"], "Missing 'task' field in result"
        assert "status" in response["result"]["task"], "Missing 'status' field in task"
        assert response["result"]["task"]["status"] == "CANCELED", "Task not canceled properly"
        
        print(f"Task {task_id} canceled successfully")
        print(f"Reason: {response['result']['task'].get('reason', 'No reason provided')}")
        
        results.add_result(test_name, True)
        return True
    except Exception as e:
        print(f"Error in {test_name}: {e}")
        results.add_result(test_name, False, e)
        return False

async def test_task_subscribe(client: ARCClient, results: TestResult, task_id: str) -> bool:
    """Test task.subscribe method"""
    test_name = "task.subscribe"
    print(f"\n=== Testing {test_name} ===")
    
    if not task_id:
        print(f"Skipping {test_name}: No task ID available")
        results.add_result(test_name, False, skipped=True)
        return False
    
    try:
        response = await client.task.subscribe(
            target_agent=SERVER_AGENT_ID,
            task_id=task_id,
            callback_url="https://travel-app.com/webhook",
            events=["TASK_COMPLETED", "TASK_FAILED", "TASK_CANCELED", "NEW_ARTIFACT"]
        )
        
        # Validate response
        assert "result" in response, "Missing 'result' field in response"
        assert "type" in response["result"], "Missing 'type' field in result"
        assert response["result"]["type"] == "subscription", "Invalid result type"
        assert "subscription" in response["result"], "Missing 'subscription' field in result"
        assert "subscriptionId" in response["result"]["subscription"], "Missing 'subscriptionId' in subscription"
        
        subscription_id = response["result"]["subscription"]["subscriptionId"]
        events = response["result"]["subscription"]["events"]
        
        print(f"Subscription {subscription_id} created successfully")
        print(f"Subscribed to events: {', '.join(events)}")
        
        results.add_result(test_name, True)
        return True
    except Exception as e:
        print(f"Error in {test_name}: {e}")
        results.add_result(test_name, False, e)
        return False

# Chat Tests
async def test_chat_start(client: ARCClient, results: TestResult) -> Optional[str]:
    """Test chat.start method"""
    test_name = "chat.start"
    print(f"\n=== Testing {test_name} ===")
    
    try:
        response = await client.chat.start(
            target_agent="price-tracker",
            initial_message={
                "role": "user",
                "parts": [{"type": "TextPart", "content": "I want to track prices for JFK to LAX route"}]
            },
            metadata={"route": "JFK-LAX", "purpose": "price monitoring"}
        )
        
        # Validate response
        assert "result" in response, "Missing 'result' field in response"
        assert "type" in response["result"], "Missing 'type' field in result"
        assert response["result"]["type"] == "chat", "Invalid result type"
        assert "chat" in response["result"], "Missing 'chat' field in result"
        assert "chatId" in response["result"]["chat"], "Missing 'chatId' in chat"
        assert "status" in response["result"]["chat"], "Missing 'status' in chat"
        
        chat_id = response["result"]["chat"]["chatId"]
        status = response["result"]["chat"]["status"]
        
        print(f"Chat started successfully with ID: {chat_id}")
        print(f"Status: {status}")
        
        # Print agent response if available
        if "message" in response["result"]["chat"]:
            message = response["result"]["chat"]["message"]
            if "parts" in message and len(message["parts"]) > 0:
                content = message["parts"][0].get("content", "No content")
                print(f"Agent response: {content}")
        
        results.add_result(test_name, True)
        return chat_id
    except Exception as e:
        print(f"Error in {test_name}: {e}")
        results.add_result(test_name, False, e)
        return None

async def test_chat_message(client: ARCClient, results: TestResult, chat_id: str) -> bool:
    """Test chat.message method"""
    test_name = "chat.message"
    print(f"\n=== Testing {test_name} ===")
    
    if not chat_id:
        print(f"Skipping {test_name}: No chat ID available")
        results.add_result(test_name, False, skipped=True)
        return False
    
    try:
        response = await client.chat.message(
            target_agent="price-tracker",
            chat_id=chat_id,
            message={
                "role": "user",
                "parts": [{"type": "TextPart", "content": "Alert me when the price drops below $400"}]
            }
        )
        
        # Validate response
        assert "result" in response, "Missing 'result' field in response"
        assert "type" in response["result"], "Missing 'type' field in result"
        assert response["result"]["type"] == "chat", "Invalid result type"
        assert "chat" in response["result"], "Missing 'chat' field in result"
        assert "chatId" in response["result"]["chat"], "Missing 'chatId' in chat"
        
        print(f"Message sent to chat {chat_id} successfully")
        
        # Print agent response if available
        if "message" in response["result"]["chat"]:
            message = response["result"]["chat"]["message"]
            if "parts" in message and len(message["parts"]) > 0:
                content = message["parts"][0].get("content", "No content")
                print(f"Agent response: {content}")
        
        results.add_result(test_name, True)
        return True
    except Exception as e:
        print(f"Error in {test_name}: {e}")
        results.add_result(test_name, False, e)
        return False

async def test_chat_end(client: ARCClient, results: TestResult, chat_id: str) -> bool:
    """Test chat.end method"""
    test_name = "chat.end"
    print(f"\n=== Testing {test_name} ===")
    
    if not chat_id:
        print(f"Skipping {test_name}: No chat ID available")
        results.add_result(test_name, False, skipped=True)
        return False
    
    try:
        response = await client.chat.end(
            target_agent="price-tracker",
            chat_id=chat_id,
            reason="Price alert configured"
        )
        
        # Validate response
        assert "result" in response, "Missing 'result' field in response"
        assert "type" in response["result"], "Missing 'type' field in result"
        assert response["result"]["type"] == "chat", "Invalid result type"
        assert "chat" in response["result"], "Missing 'chat' field in result"
        assert "status" in response["result"]["chat"], "Missing 'status' field in chat"
        assert response["result"]["chat"]["status"] == "CLOSED", "Chat not closed properly"
        
        print(f"Chat {chat_id} ended successfully")
        print(f"Reason: {response['result']['chat'].get('reason', 'No reason provided')}")
        
        results.add_result(test_name, True)
        return True
    except Exception as e:
        print(f"Error in {test_name}: {e}")
        results.add_result(test_name, False, e)
        return False

async def test_chat_with_streaming(client: ARCClient, results: TestResult) -> bool:
    """Test chat with streaming enabled"""
    test_name = "chat.streaming"
    print(f"\n=== Testing {test_name} ===")
    
    try:
        print("Starting chat with streaming enabled...")
        response = await client.chat.start(
            target_agent="hotel-booking",
            initial_message={
                "role": "user",
                "parts": [{"type": "TextPart", "content": "Find hotels in Los Angeles for 3 nights"}]
            },
            stream=True
        )
        
        # With a real streaming server, this would be an AsyncIterator
        # Our test server doesn't implement streaming, so we just get a regular response
        
        # Test if we can handle both streaming and non-streaming responses
        if isinstance(response, dict):
            # Non-streaming response
            print("Server returned non-streaming response (expected in test server)")
            chat_id = response["result"]["chat"]["chatId"]
            
            # Send another message with streaming
            print("Sending follow-up message with streaming...")
            message_response = await client.chat.message(
                target_agent="hotel-booking",
                chat_id=chat_id,
                message={
                    "role": "user",
                    "parts": [{"type": "TextPart", "content": "I prefer hotels with a pool and gym"}]
                },
                stream=True
            )
            
            # End the chat
            await client.chat.end(
                target_agent="hotel-booking",
                chat_id=chat_id,
                reason="Hotel preferences collected"
            )
            
            print("Streaming test completed successfully")
            results.add_result(test_name, True)
            return True
        else:
            # Streaming response (would be handled differently with a real streaming server)
            print("Streaming response received")
            # We would process chunks here
            results.add_result(test_name, True)
            return True
    except Exception as e:
        print(f"Error in {test_name}: {e}")
        results.add_result(test_name, False, e)
        return False

async def run_task_tests(client: ARCClient, results: TestResult) -> None:
    """Run all task-related tests"""
    print("\n=== RUNNING TASK TESTS ===")
    
    # Create a task
    task_id = await test_task_create(client, results)
    
    # Test task operations
    if task_id:
        await test_task_send(client, results, task_id)
        
        # Wait for task to progress
        print("\nWaiting for task to progress...")
        await asyncio.sleep(3)
        
        # Check task info
        await test_task_info(client, results, task_id)
        
        # Subscribe to task updates
        await test_task_subscribe(client, results, task_id)
        
        # Cancel task
        await test_task_cancel(client, results, task_id)
    else:
        print("Skipping remaining task tests: Failed to create task")

async def run_chat_tests(client: ARCClient, results: TestResult) -> None:
    """Run all chat-related tests"""
    print("\n=== RUNNING CHAT TESTS ===")
    
    # Start a chat
    chat_id = await test_chat_start(client, results)
    
    # Test chat operations
    if chat_id:
        await test_chat_message(client, results, chat_id)
        await test_chat_end(client, results, chat_id)
    else:
        print("Skipping remaining chat tests: Failed to start chat")
    
    # Test streaming chat
    await test_chat_with_streaming(client, results)

async def run_all_tests(client: ARCClient) -> bool:
    """Run all tests and return True if all passed"""
    results = TestResult()
    
    try:
        # Run task tests
        await run_task_tests(client, results)
        
        # Run chat tests
        await run_chat_tests(client, results)
        
        # Print test summary
        return results.print_summary()
    except Exception as e:
        print(f"Unexpected error during tests: {e}")
        results.add_result("all_tests", False, e)
        results.print_summary()
        return False

async def main():
    parser = argparse.ArgumentParser(description='ARC Protocol Client Test Suite')
    parser.add_argument('--url', default=SERVER_URL, help='ARC server endpoint URL')
    parser.add_argument('--agent', default=SERVER_AGENT_ID, help='Server agent ID')
    parser.add_argument('--client-id', default=CLIENT_AGENT_ID, help='Client agent ID')
    parser.add_argument('--tests', choices=['all', 'task', 'chat'], default='all',
                        help='Which test suite to run')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
    
    args = parser.parse_args()
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    # Create client
    async with ARCClient(
        endpoint=args.url,
        request_agent=args.client_id,
        timeout=30.0
    ) as client:
        print(f"ARC Protocol Client Test Suite - Travel & Booking Platform")
        print(f"Server URL: {args.url}")
        print(f"Testing agents: flight-finder, hotel-booking, itinerary-planner, price-tracker")
        print(f"Client agent: {args.client_id}")
        
        results = TestResult()
        
        if args.tests == 'all':
            success = await run_all_tests(client)
        elif args.tests == 'task':
            await run_task_tests(client, results)
            success = results.print_summary()
        elif args.tests == 'chat':
            await run_chat_tests(client, results)
            success = results.print_summary()
        
        # Return appropriate exit code
        return 0 if success else 1

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))