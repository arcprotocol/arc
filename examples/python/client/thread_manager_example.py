"""
Example: Using ThreadManager for CLIENT-side thread management

This example shows how to use ThreadManager in a WebSocket handler
to automatically manage chat_id mappings for agent conversations.
"""

import asyncio
from arc import Client, ThreadManager


async def websocket_handler_example():
    """
    Example WebSocket handler using ThreadManager.
    
    This would typically be in your Platform's WebSocket handler.
    """
    
    # Initialize ARC client
    arc_client = Client(
        endpoint="https://agents.example.com/arc",
        token="your-oauth2-token"
    )
    
    # Initialize thread manager (scoped to this WebSocket session)
    thread_manager = ThreadManager(arc_client)
    
    try:
        # Simulate user messages
        
        # First message to agent-A - creates new thread
        print("=== First contact with agent-A ===")
        response1 = await thread_manager.send_to_agent(
            agent_id="financial-agent",
            message={
                "role": "user",
                "parts": [{"type": "TextPart", "content": "Analyze Q4 revenue"}]
            },
            trace_id="workflow-123"
        )
        print(f"Response: {response1['result']['chat']['chatId']}")
        print(f"Active threads: {thread_manager.get_thread_count()}")
        
        # Second message to agent-A - reuses thread
        print("\n=== Second contact with agent-A (reuses thread) ===")
        response2 = await thread_manager.send_to_agent(
            agent_id="financial-agent",
            message={
                "role": "user",
                "parts": [{"type": "TextPart", "content": "Focus on operating expenses"}]
            },
            trace_id="workflow-123"
        )
        print(f"Reused thread: {response2['result']['chat']['chatId']}")
        
        # First message to agent-B - creates new thread
        print("\n=== First contact with agent-B ===")
        response3 = await thread_manager.send_to_agent(
            agent_id="marketing-agent",
            message={
                "role": "user",
                "parts": [{"type": "TextPart", "content": "Summarize campaign metrics"}]
            },
            trace_id="workflow-123"
        )
        print(f"Response: {response3['result']['chat']['chatId']}")
        print(f"Active threads: {thread_manager.get_thread_count()}")
        print(f"Agents with threads: {thread_manager.get_all_agents()}")
        
        # Check if thread exists
        print(f"\nHas thread with financial-agent: {thread_manager.has_thread('financial-agent')}")
        print(f"Thread ID: {thread_manager.get_thread_id('financial-agent')}")
        
        # End specific thread
        print("\n=== Ending thread with marketing-agent ===")
        await thread_manager.end_thread("marketing-agent", reason="Task complete")
        print(f"Active threads: {thread_manager.get_thread_count()}")
        
    finally:
        # Cleanup on disconnect
        print("\n=== WebSocket disconnecting - cleanup all threads ===")
        results = await thread_manager.cleanup_all(reason="Session ended")
        print(f"Cleanup results: {results}")
        print(f"Active threads: {thread_manager.get_thread_count()}")
        
        # Close client
        await arc_client.close()


async def simple_usage_example():
    """
    Simpler example showing basic usage.
    """
    
    # Setup
    client = Client(endpoint="https://agent.example.com/arc", token="token")
    manager = ThreadManager(client)
    
    try:
        # Send to agent - automatically creates thread on first call
        response = await manager.send_to_agent(
            "agent-A",
            {"role": "user", "parts": [{"type": "TextPart", "content": "Hello"}]}
        )
        
        # Send again - automatically reuses thread
        response = await manager.send_to_agent(
            "agent-A",
            {"role": "user", "parts": [{"type": "TextPart", "content": "Follow up"}]}
        )
        
    finally:
        # Clean up all threads on disconnect
        await manager.cleanup_all()
        await client.close()


async def manual_control_example():
    """
    Example with manual thread control.
    """
    
    client = Client(endpoint="https://agent.example.com/arc", token="token")
    manager = ThreadManager(client)
    
    try:
        # Send messages
        await manager.send_to_agent("agent-A", {...})
        await manager.send_to_agent("agent-B", {...})
        
        # Check state
        if manager.has_thread("agent-A"):
            chat_id = manager.get_thread_id("agent-A")
            print(f"Thread with agent-A: {chat_id}")
        
        # End specific thread manually
        await manager.end_thread("agent-A", reason="Done with this agent")
        
        # agent-B thread still active
        print(f"Remaining threads: {manager.get_all_agents()}")
        
    finally:
        await manager.cleanup_all()
        await client.close()


if __name__ == "__main__":
    # Run examples
    print("=" * 60)
    print("ThreadManager Example - WebSocket Handler Pattern")
    print("=" * 60)
    asyncio.run(websocket_handler_example())
    
    print("\n\n")
    print("=" * 60)
    print("ThreadManager Example - Simple Usage")
    print("=" * 60)
    asyncio.run(simple_usage_example())

