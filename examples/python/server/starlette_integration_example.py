#!/usr/bin/env python3
"""
Starlette Integration Example

This example demonstrates how to integrate ARC protocol with a Starlette
application using the ARCRouter with complete method support.
"""

import sys
import os
import asyncio
import logging
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

try:
    from starlette.applications import Starlette
    from starlette.middleware import Middleware
    from starlette.middleware.cors import CORSMiddleware
    from arc.starlette import ARCRouter
    from arc.server.sse import create_sse_response
    from arc.core.streaming import create_chat_stream_generator
    from arc.exceptions import InternalError, InvalidRequestError
except ImportError:
    print("Starlette integration requires Starlette to be installed.")
    print("Install with: pip install arc-sdk[starlette]")
    sys.exit(1)

# Configure logging
logger = logging.getLogger(__name__)

# Helper functions for agent processing
def extract_message_content(message) -> str:
    """Extract text content from message parts"""
    user_content = ""
    for part in message.get("parts", []):
        if part.get("type") == "TextPart":
            user_content += part.get("content", "")
    return user_content

def create_agent_message(content: str) -> dict:
    """Create standardized agent message response"""
    return {
        "role": "agent",
        "parts": [{
            "type": "TextPart",
            "content": content
        }],
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

async def process_agent_streaming(user_content: str, chat_id: str):
    """Create a streaming generator for agent responses"""
    async def agent_content_stream():
        response_parts = [
            "I understand ", "your message: ", f'"{user_content}". ',
            "Let me help ", "you with ", "that request."
        ]
        for part in response_parts:
            await asyncio.sleep(0.1)  # Simulate processing
            yield part
    
    return create_sse_response(create_chat_stream_generator(
        chat_id=chat_id,
        content_generator=agent_content_stream()
    ))

async def process_agent_non_streaming(user_content: str, chat_id: str) -> str:
    """Process agent response without streaming"""
    return f'I understand your message: "{user_content}". Let me help you with that request.'

# Create Starlette app with CORS middleware
middleware = [
    Middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
]

app = Starlette(middleware=middleware)

# Create ARC router with ChatManager
arc_router = ARCRouter(
    enable_chat_manager=True,
    chat_manager_agent_id="starlette-server"
)

# Chat methods for the agent
@arc_router.agent_handler("my-starlette-agent", "chat.start")
async def handle_chat_start(params, context):
    """Handle chat.start method with streaming and non-streaming support"""
    initial_message = params["initialMessage"]
    chat_id = params.get("chatId", f"chat-{context['request_id'][:8]}")
    stream = params.get("stream", False)
    metadata = params.get("metadata", {})
    
    # Create chat session using ChatManager
    chat_manager = context["chat_manager"]
    if not chat_manager:
        raise InternalError("ChatManager not available - enable_chat_manager=True required for chat methods")
    
    chat_info = chat_manager.create_chat(
        target_agent=context["request_agent"],
        chat_id=chat_id,
        metadata=metadata
    )
    
    # Extract user content from message
    user_content = extract_message_content(initial_message)
    
    # Handle streaming if requested
    if stream:
        # Return streaming response directly
        return await process_agent_streaming(user_content, chat_id)
    
    # For non-streaming, process and return complete response
    response_text = await process_agent_non_streaming(user_content, chat_id)
    agent_message = create_agent_message(response_text)
    
    return {
        "type": "chat",
        "chat": {
            "chatId": chat_id,
            "status": "ACTIVE",
            "createdAt": chat_info["createdAt"],
            "message": agent_message
        }
    }

@arc_router.agent_handler("my-starlette-agent", "chat.message")
async def handle_chat_message(params, context):
    """Handle chat.message method for follow-up messages"""
    chat_id = params["chatId"]
    message = params["message"]
    stream = params.get("stream", False)
    
    # Validate chat exists and is active using ChatManager
    chat_manager = context["chat_manager"]
    if not chat_manager:
        raise InternalError("ChatManager not available - enable_chat_manager=True required for chat methods")
    
    try:
        chat = chat_manager.get_chat(chat_id)
    except Exception as e:
        raise InvalidRequestError(f"Chat not found: {chat_id}")
    
    # Extract user content from message
    user_content = extract_message_content(message)
    
    # Handle streaming if requested
    if stream:
        # Return streaming response directly
        return await process_agent_streaming(user_content, chat_id)
    
    # For non-streaming, process and return complete response
    response_text = await process_agent_non_streaming(user_content, chat_id)
    agent_message = create_agent_message(response_text)
    
    return {
        "type": "chat",
        "chat": {
            "chatId": chat_id,
            "status": "ACTIVE",
            "createdAt": chat["createdAt"],
            "message": agent_message
        }
    }

@arc_router.agent_handler("my-starlette-agent", "chat.end")
async def handle_chat_end(params, context):
    """Handle chat.end method to terminate chat"""
    chat_id = params["chatId"]
    reason = params.get("reason", "Chat ended by user")
    
    # Close chat using ChatManager
    chat_manager = context["chat_manager"]
    if not chat_manager:
        raise InternalError("ChatManager not available - enable_chat_manager=True required for chat methods")
    
    try:
        chat_result = chat_manager.close_chat(chat_id, reason)
        
        return {
            "type": "chat",
            "chat": chat_result
        }
    except Exception as e:
        raise InvalidRequestError(f"Failed to end chat: {e}")

# Task methods for the same agent
@arc_router.agent_handler("my-starlette-agent", "task.create")
async def handle_task_create(params, context):
    """Handle task.create method"""
    import uuid
    
    task_id = f"task-{uuid.uuid4().hex[:8]}"
    initial_message = params["initialMessage"]
    priority = params.get("priority", "NORMAL")
    metadata = params.get("metadata", {})
    
    created_at = datetime.utcnow().isoformat() + "Z"
    
    return {
        "type": "task",
        "task": {
            "taskId": task_id,
            "status": "SUBMITTED",
            "createdAt": created_at,
            "priority": priority,
            "metadata": metadata
        }
    }

@arc_router.agent_handler("my-starlette-agent", "task.info")
async def handle_task_info(params, context):
    """Handle task.info method"""
    task_id = params["taskId"]
    include_messages = params.get("includeMessages", True)
    include_artifacts = params.get("includeArtifacts", True)
    
    # Mock task for demo
    mock_task = {
        "taskId": task_id,
        "status": "COMPLETED",
        "createdAt": "2024-01-01T12:00:00Z",
        "updatedAt": "2024-01-01T12:05:00Z",
        "completedAt": "2024-01-01T12:05:00Z",
        "priority": "NORMAL",
        "messages": [
            {
                "role": "user",
                "parts": [{"type": "TextPart", "content": "Process this document"}],
                "timestamp": "2024-01-01T12:00:00Z"
            }
        ] if include_messages else [],
        "artifacts": [
            {
                "artifactId": f"artifact-{task_id}",
                "name": "Processed Document",
                "description": "The processed document result",
                "mimeType": "application/json",
                "createdAt": "2024-01-01T12:05:00Z",
                "parts": [{
                    "type": "DataPart",
                    "content": {"result": "Document processing complete"},
                    "mimeType": "application/json"
                }]
            }
        ] if include_artifacts else [],
        "metadata": {}
    }
    
    return {
        "type": "task",
        "task": mock_task
    }

# Mount the ARC router
app.mount("/arc", arc_router)

# Add a simple health check
@app.route("/health")
async def health_check(request):
    from starlette.responses import JSONResponse
    return JSONResponse({"status": "ok", "framework": "starlette"})

if __name__ == "__main__":
    import uvicorn
    
    print("Starting Starlette ARC Server")
    print("Registered agents:")
    for agent_id, methods in arc_router.agents.items():
        print(f"  - {agent_id}: {', '.join(methods.keys())}")
    print("Endpoints:")
    print("  - ARC Protocol: http://localhost:8000/arc/")
    print("  - Agent Info: http://localhost:8000/arc/info")
    print("  - Health Check: http://localhost:8000/health")
    print("Press Ctrl+C to stop the server")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
