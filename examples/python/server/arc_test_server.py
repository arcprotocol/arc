#!/usr/bin/env python3
"""
ARC Protocol Test Server

A fully functional ARC protocol server that responds to all standard methods
with realistic mock data. Used for testing the ARC SDK.
"""

import asyncio
import uuid
import os
import sys
import logging
import json
from datetime import datetime
from typing import Dict, Any, AsyncGenerator

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from arc.server.arc_server import create_server
from arc.server.decorators import validate_params, trace_method, error_handler
from arc.core.chat import ChatManager
from arc.utils.logging import configure_root_logger, create_logger
from arc.server.sse import create_sse_response
from arc.core.streaming import create_chat_stream_generator

# Configure logging
configure_root_logger(level=logging.INFO)
logger = create_logger("arc-test-server", level=logging.INFO)

# Initialize multi-agent server with ChatManager
server = create_server(
    server_id="travel-booking-platform",
    name="Travel & Booking Test Server",
    version="1.0.0",
    server_description="Full-featured travel booking test server for ARC protocol",
    enable_cors=True,
    enable_logging=True,
    enable_chat_manager=True,
    chat_manager_agent_id="travel-booking-platform"
)

# In-memory storage for tasks and subscriptions
tasks = {}
subscriptions = {}

# Simulate task progression
async def process_task_async(task_id):
    """Background task to simulate task progression"""
    await asyncio.sleep(2)
    
    # Move to WORKING state
    if task_id in tasks and tasks[task_id]["status"] == "SUBMITTED":
        tasks[task_id]["status"] = "WORKING"
        tasks[task_id]["updatedAt"] = datetime.utcnow().isoformat() + "Z"
        logger.info(f"Task {task_id} status changed to WORKING")
        
        # Notify subscribers
        await notify_subscribers(task_id, "TASK_STARTED", {
            "status": "WORKING",
            "message": "Task processing started",
            "startedAt": tasks[task_id]["updatedAt"]
        })
    
    # Simulate processing time
    await asyncio.sleep(5)
    
    # Generate artifact and complete task
    if task_id in tasks and tasks[task_id]["status"] == "WORKING":
        # Add artifact
        artifact = {
            "artifactId": f"artifact-{uuid.uuid4().hex[:8]}",
            "name": "Analysis Results",
            "description": "Generated results from the task execution",
            "mimeType": "application/json",
            "createdAt": datetime.utcnow().isoformat() + "Z",
            "parts": [{
                "type": "DataPart",
                "content": {"results": "Some analysis results", "timestamp": datetime.utcnow().isoformat()},
                "mimeType": "application/json"
            }]
        }
        
        tasks[task_id]["artifacts"] = tasks[task_id].get("artifacts", []) + [artifact]
        
        # Notify about new artifact
        await notify_subscribers(task_id, "NEW_ARTIFACT", {
            "status": "WORKING",
            "message": "New artifact generated",
            "artifact": artifact
        })
        
        # Add agent message
        agent_message = {
            "role": "agent",
            "parts": [{
                "type": "TextPart",
                "content": "I've completed the analysis and generated results."
            }],
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        tasks[task_id]["messages"].append(agent_message)
        
        # Notify about new message
        await notify_subscribers(task_id, "NEW_MESSAGE", {
            "status": "WORKING",
            "message": "New message added",
            "messageContent": agent_message
        })
        
        await asyncio.sleep(2)
        
        # Complete task
        tasks[task_id]["status"] = "COMPLETED"
        tasks[task_id]["completedAt"] = datetime.utcnow().isoformat() + "Z"
        tasks[task_id]["updatedAt"] = tasks[task_id]["completedAt"]
        
        # Notify subscribers
        await notify_subscribers(task_id, "TASK_COMPLETED", {
            "status": "COMPLETED",
            "message": "Task processing completed successfully",
            "completedAt": tasks[task_id]["completedAt"],
            "artifactCount": len(tasks[task_id].get("artifacts", [])),
            "messageCount": len(tasks[task_id].get("messages", [])),
            "duration": 7000  # simulated 7 seconds duration
        })
        
        logger.info(f"Task {task_id} completed with status COMPLETED")

async def notify_subscribers(task_id, event, data):
    """Send notifications to all subscribers of a task"""
    if task_id not in tasks:
        return
    
    task_subs = [s for s in subscriptions.values() 
                if s["taskId"] == task_id and s["active"] and 
                (event in s["events"] or "STATUS_CHANGE" in s["events"])]
    
    if not task_subs:
        return
    
    logger.info(f"Sending {event} notifications for task {task_id} to {len(task_subs)} subscribers")
    
    # In a production server, this would make HTTP requests to the callback URLs
    # Here we just log that we would have sent notifications
    for sub in task_subs:
        logger.info(f"Would send notification to {sub['callbackUrl']}: {event}")
        # In real implementation: await send_notification_webhook(sub["callbackUrl"], task_id, event, data)

# Task methods for test agent
@server.agent_handler("test-arc-server", "task.create")
@trace_method
@error_handler
@validate_params()
async def handle_task_create(params, context):
    """Handle task.create method with realistic mock behavior"""
    task_id = f"task-{uuid.uuid4().hex[:8]}"
    initial_message = params["initialMessage"]
    priority = params.get("priority", "NORMAL")
    metadata = params.get("metadata", {})
    
    created_at = datetime.utcnow().isoformat() + "Z"
    
    # Create and store task
    task = {
        "taskId": task_id,
        "status": "SUBMITTED",
        "createdAt": created_at,
        "updatedAt": created_at,
        "priority": priority,
        "messages": [initial_message],
        "artifacts": [],
        "metadata": metadata
    }
    
    tasks[task_id] = task
    
    # Start background processing of task
    asyncio.create_task(process_task_async(task_id))
    
    logger.info(f"Created task {task_id} with priority {priority}")
    
    return {
        "type": "task",
        "task": {
            "taskId": task_id,
            "status": "SUBMITTED",
            "createdAt": created_at,
            "priority": priority
        }
    }

@server.agent_handler("test-arc-server", "task.send")
@trace_method
@error_handler
@validate_params()
async def handle_task_send(params, context):
    """Handle task.send method"""
    task_id = params["taskId"]
    message = params["message"]
    
    # Check if task exists
    if task_id not in tasks:
        raise ValueError(f"Task not found: {task_id}")
    
    # Check if task is in proper state
    if tasks[task_id]["status"] != "INPUT_REQUIRED":
        # For the test server, we'll be lenient and accept messages in any state
        logger.warning(f"Task {task_id} is not in INPUT_REQUIRED state, but accepting message anyway")
    
    # Add message to task
    message["timestamp"] = datetime.utcnow().isoformat() + "Z"
    tasks[task_id]["messages"].append(message)
    tasks[task_id]["updatedAt"] = datetime.utcnow().isoformat() + "Z"
    
    logger.info(f"Added message to task {task_id}")
    
    # Notify subscribers
    await notify_subscribers(task_id, "NEW_MESSAGE", {
        "status": tasks[task_id]["status"],
        "message": "New message added to task",
        "messageContent": message
    })
    
    return {
        "success": True,
        "message": "Message sent to task successfully"
    }

@server.agent_handler("test-arc-server", "task.info")
@trace_method
@error_handler
@validate_params()
async def handle_task_info(params, context):
    """Handle task.info method"""
    task_id = params["taskId"]
    include_messages = params.get("includeMessages", True)
    include_artifacts = params.get("includeArtifacts", True)
    
    # Check if task exists
    if task_id not in tasks:
        raise ValueError(f"Task not found: {task_id}")
    
    # Create a copy for response
    task_copy = tasks[task_id].copy()
    
    # Filter out messages and artifacts if not requested
    if not include_messages and "messages" in task_copy:
        task_copy["messages"] = []
    
    if not include_artifacts and "artifacts" in task_copy:
        task_copy["artifacts"] = []
    
    logger.info(f"Retrieved info for task {task_id}")
    
    return {
        "type": "task",
        "task": task_copy
    }

@server.agent_handler("test-arc-server", "task.cancel")
@trace_method
@error_handler
@validate_params()
async def handle_task_cancel(params, context):
    """Handle task.cancel method"""
    task_id = params["taskId"]
    reason = params.get("reason", "User requested cancellation")
    
    # Check if task exists
    if task_id not in tasks:
        raise ValueError(f"Task not found: {task_id}")
    
    # Check if task is already completed or canceled
    if tasks[task_id]["status"] in ["COMPLETED", "FAILED", "CANCELED"]:
        raise ValueError(f"Cannot cancel task in {tasks[task_id]['status']} state")
    
    # Cancel task
    old_status = tasks[task_id]["status"]
    canceled_at = datetime.utcnow().isoformat() + "Z"
    
    tasks[task_id]["status"] = "CANCELED"
    tasks[task_id]["canceledAt"] = canceled_at
    tasks[task_id]["updatedAt"] = canceled_at
    tasks[task_id]["reason"] = reason
    
    logger.info(f"Canceled task {task_id} with reason: {reason}")
    
    # Notify subscribers
    await notify_subscribers(task_id, "TASK_CANCELED", {
        "status": "CANCELED",
        "message": f"Task was canceled: {reason}",
        "canceledAt": canceled_at,
        "previousStatus": old_status,
        "reason": reason
    })
    
    return {
        "type": "task",
        "task": {
            "taskId": task_id,
            "status": "CANCELED",
            "canceledAt": canceled_at,
            "reason": reason
        }
    }

@server.agent_handler("test-arc-server", "task.subscribe")
@trace_method
@error_handler
@validate_params()
async def handle_task_subscribe(params, context):
    """Handle task.subscribe method"""
    task_id = params["taskId"]
    callback_url = params["callbackUrl"]
    events = params.get("events", ["TASK_COMPLETED", "TASK_FAILED"])
    
    # Check if task exists
    if task_id not in tasks:
        raise ValueError(f"Task not found: {task_id}")
    
    # Create subscription
    subscription_id = f"sub-{uuid.uuid4().hex[:8]}"
    created_at = datetime.utcnow().isoformat() + "Z"
    
    subscription = {
        "subscriptionId": subscription_id,
        "taskId": task_id,
        "callbackUrl": callback_url,
        "events": events,
        "createdAt": created_at,
        "active": True
    }
    
    # Store subscription
    subscriptions[subscription_id] = subscription
    
    logger.info(f"Created subscription {subscription_id} for task {task_id} with events: {events}")
    
    return {
        "type": "subscription",
        "subscription": subscription
    }

# Chat methods for test agent
@server.agent_handler("test-arc-server", "chat.start")
@trace_method
@error_handler
@validate_params()
async def handle_chat_start(params, context):
    """Handle chat.start method"""
    initial_message = params["initialMessage"]
    chat_id = params.get("chatId") or f"chat-{uuid.uuid4().hex[:8]}"
    metadata = params.get("metadata", {})
    stream = params.get("stream", False)
    
    # Create chat using ChatManager from context
    chat_manager = context["chat_manager"]
    if not chat_manager:
        raise ValueError("ChatManager not available - enable_chat_manager=True required for chat methods")
    
    chat_info = chat_manager.create_chat(
        target_agent=context["request_agent"],
        chat_id=chat_id,
        metadata=metadata
    )
    
    # No need to store initial message - agent handles its own history
    
    # Handle streaming if requested - generate content dynamically
    if stream:
        logger.info(f"Streaming response for chat {chat_id}")
        
        # Create a generator that simulates real agent streaming
        async def agent_content_stream():
            # This simulates what a real agent would do - generate content as it processes
            response_parts = [
                "Hello! ", "This is ", "a test ", "response ", "from the ", 
                "ARC server. ", "I'm here ", "to help ", "with your ", "request."
            ]
            
            for part in response_parts:
                # Simulate real agent processing time (LLM token generation, etc.)
                await asyncio.sleep(0.2)
                yield part
        
        return create_sse_response(create_chat_stream_generator(
            chat_id=chat_id,
            content_generator=agent_content_stream(),
            request_id=context.get("request_id", "unknown")
        ))
    
    # For non-streaming, create complete response
    response_text = "Hello! This is a test response from the ARC server. I'm here to help with your request."
    agent_message = {
        "role": "agent",
        "parts": [{
            "type": "TextPart",
            "content": response_text
        }],
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    
    # No need to store agent response - agent handles its own history
    
    logger.info(f"Started chat {chat_id} with initial message")
    
    # Get session info (no messages stored)
    chat = chat_manager.get_chat(chat_id)
    
    # Return standard response - message is optional but useful for client
    return {
        "type": "chat",
        "chat": {
            "chatId": chat_id,
            "status": "ACTIVE", 
            "createdAt": chat["createdAt"],
            "message": agent_message  # Optional but contains agent response
        }
    }

@server.agent_handler("test-arc-server", "chat.message")
@trace_method
@error_handler
@validate_params()
async def handle_chat_message(params, context):
    """Handle chat.message method"""
    chat_id = params["chatId"]
    message = params["message"]
    stream = params.get("stream", False)
    
    # Check if chat exists using ChatManager from context
    chat_manager = context["chat_manager"]
    if not chat_manager:
        raise ValueError("ChatManager not available - enable_chat_manager=True required for chat methods")
    
    try:
        chat = chat_manager.get_chat(chat_id)
    except Exception as e:
        raise ValueError(f"Chat not found: {chat_id}")
    
    # No need to store message - agent handles its own history
    
    # Handle streaming if requested - generate content dynamically
    if stream:
        logger.info(f"Streaming response for chat message in chat {chat_id}")
        
        # Create a generator that simulates real agent streaming
        async def agent_content_stream():
            # Simulate dynamic content generation with varied responses
            content_options = [
                ["I understand ", "your request. ", "Let me provide ", "some information ", "about that."],
                ["Thanks for ", "your message. ", "Here's my ", "response to ", "your query."],
                ["I've processed ", "your input. ", "Let me know ", "if you need ", "more details."]
            ]
            import random
            response_parts = random.choice(content_options)
            
            for part in response_parts:
                # Simulate real agent processing time
                await asyncio.sleep(0.15)
                yield part
        
        return create_sse_response(create_chat_stream_generator(
            chat_id=chat_id,
            content_generator=agent_content_stream(),
            request_id=context.get("request_id", "unknown")
        ))
    
    # For non-streaming, create complete response
    content_options = [
        "I understand your request. Let me provide some information about that.",
        "Thanks for your message. Here's my response to your query.",
        "I've processed your input. Let me know if you need more details."
    ]
    import random
    response_text = random.choice(content_options)
    
    agent_message = {
        "role": "agent",
        "parts": [{
            "type": "TextPart",
            "content": response_text
        }],
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    
    # No need to store agent response - agent handles its own history
    
    logger.info(f"Handled message in chat {chat_id}")
    
    # Return standard response - message is optional but useful for client
    return {
        "type": "chat",
        "chat": {
            "chatId": chat_id,
            "status": "ACTIVE",
            "createdAt": chat["createdAt"],
            "message": agent_message  # Optional but contains agent response
        }
    }

@server.agent_handler("test-arc-server", "chat.end")
@trace_method
@error_handler
@validate_params()
async def handle_chat_end(params, context):
    """Handle chat.end method"""
    chat_id = params["chatId"]
    reason = params.get("reason", "Chat ended by user")
    
    # Close the chat using ChatManager from context
    chat_manager = context["chat_manager"]
    if not chat_manager:
        raise ValueError("ChatManager not available - enable_chat_manager=True required for chat methods")
    
    try:
        chat_result = chat_manager.close_chat(chat_id, reason)
        logger.info(f"Ended chat {chat_id} with reason: {reason}")
        
        return {
            "type": "chat",
            "chat": chat_result
        }
    except Exception as e:
        raise ValueError(f"Failed to end chat: {e}")

if __name__ == "__main__":
    print(f"Starting ARC Protocol Multi-Agent Test Server")
    print(f"Server ID: test-arc-server")
    print(f"Registered agents: {', '.join(server.supported_agents)}")
    print(f"Total methods: {sum(len(methods) for methods in server.agents.values())}")
    print(f"Listening at: http://localhost:8000/arc")
    print(f"Press Ctrl+C to stop the server")
    server.run(host="0.0.0.0", port=8000)