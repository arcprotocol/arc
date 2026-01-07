#!/usr/bin/env python3
"""
FastAPI Integration Example

This example demonstrates how to integrate ARC protocol with an existing
FastAPI application using a single agent with proper chat logic.
"""

import sys
import os
import asyncio
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

try:
    from fastapi import FastAPI, Depends
    from fastapi.middleware.cors import CORSMiddleware
    from arc.fastapi import ARCRouter
    from arc.server.sse import create_sse_response
    from arc.core.streaming import create_chat_stream_generator
    from arc.exceptions import InternalError, InvalidRequestError
except ImportError:
    print("FastAPI integration requires FastAPI to be installed.")
    print("Install with: pip install arc-sdk[fastapi]")
    sys.exit(1)

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
        try:
            # This is where you'd connect to your actual AI service
            # For example: OpenAI, Anthropic, local LLM, etc.
            
            # Simulate agent processing and streaming response
            response_parts = [
                "I understand your request about: ", 
                f'"{user_content}". ',
                "Let me process this information... ",
                "Based on my analysis, ",
                "I can provide you with the following insights: ",
                "This appears to be a valid request that I can help with. ",
                "Is there anything specific you'd like me to focus on?"
            ]
            
            for part in response_parts:
                # Simulate processing time (real agent would stream as it generates)
                await asyncio.sleep(0.3)
                yield part
                
        except Exception as e:
            # Fallback streaming content
            fallback_text = f"Error processing your request: {e}. Please try again."
            for chunk in [fallback_text[i:i+10] for i in range(0, len(fallback_text), 10)]:
                await asyncio.sleep(0.1)
                yield chunk
    
    return create_sse_response(create_chat_stream_generator(
        chat_id=chat_id,
        content_generator=agent_content_stream(),
        request_id="streaming"
    ))

async def process_agent_non_streaming(user_content: str, chat_id: str) -> str:
    """Process agent request and return complete response"""
    try:
        # This is where you'd connect to your actual AI service
        # For example:
        # response = await openai_client.chat.completions.create(...)
        # response = await anthropic_client.messages.create(...)
        # response = await your_local_llm.generate(...)
        
        # Simulate agent processing
        await asyncio.sleep(0.5)  # Simulate processing time
        
        response_text = f"I've processed your request about: '{user_content}'. Based on my analysis, I can help you with this. What would you like to know more about?"
        
        return response_text
        
    except Exception as e:
        return f"Error processing your request: {e}. Please try again."

# Create FastAPI application
app = FastAPI(
    title="Enterprise API Gateway with ARC",
    description="Example of integrating ARC protocol into existing FastAPI app",
    version="1.0.0"
)

# Add CORS middleware (enterprise requirement)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Example: Custom authentication middleware
async def get_current_user():
    """Example dependency for user authentication."""
    # In real enterprise app, this would validate JWT tokens, etc.
    return {"user_id": "enterprise_user", "scopes": ["arc.agent.caller"]}

# Existing business routes
@app.get("/")
async def root():
    return {"message": "Enterprise API Gateway", "status": "active"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "services": ["api", "arc-agents"]}

@app.get("/users/me")
async def get_user_profile(current_user: dict = Depends(get_current_user)):
    return {"user": current_user, "profile": "enterprise_profile"}

# Create SINGLE ARC router for multi-agent routing with ChatManager
arc_router = ARCRouter(
    enable_chat_manager=True,
    chat_manager_agent_id="enterprise-server"
)

# Single agent with full chat capabilities
@arc_router.agent_handler("my-chat-agent", "chat.start")
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

@arc_router.agent_handler("my-chat-agent", "chat.message")
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

@arc_router.agent_handler("my-chat-agent", "chat.end")
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
        
        # Here you could do additional cleanup logic:
        # - Save final chat history to your database
        # - Clean up resources
        # - Log chat completion
        # - Send analytics events
        
        return {
            "type": "chat",
            "chat": chat_result
        }
    except Exception as e:
        raise InvalidRequestError(f"Failed to end chat: {e}")

# Include SINGLE ARC router - all agents route through /arc
app.include_router(arc_router, prefix="/arc", tags=["ARC Protocol"])

# Example: Protected route that uses ARC agents
@app.post("/enterprise/chat")
async def start_enterprise_chat(
    message_data: dict,
    current_user: dict = Depends(get_current_user)
):
    """
    Enterprise endpoint that shows how to integrate with ARC agents.
    """
    return {
        "message": "Chat initiated via enterprise endpoint",
        "user": current_user["user_id"],
        "arc_endpoint": "/arc",
        "target_agent": "my-chat-agent",
        "status": "ready"
    }

if __name__ == "__main__":
    import uvicorn
    
    print(" Starting Enterprise FastAPI App with ARC Integration")
    print(" Available endpoints:")
    print("   • GET  /              - Root endpoint")
    print("   • GET  /health        - Health check")
    print("   • GET  /users/me      - User profile")
    print("   • POST /arc/          - SINGLE ARC endpoint for ALL agents")
    print("   • GET  /arc/info      - ARC router information")
    print("   • GET  /docs          - FastAPI OpenAPI docs")
    print()
    print("🤖 Registered Agent:")
    print("   • my-chat-agent: chat.start, chat.message, chat.end")
    print("   • ChatManager: enabled (enterprise-server)")
    print("   • Chat lifecycle: managed automatically")
    print()
    print("📝 Example ARC Requests:")
    print('   # Start chat (non-streaming)')
    print('   POST /arc/ {')
    print('     "arc": "1.0",')
    print('     "id": "req-001",')
    print('     "method": "chat.start",')
    print('     "requestAgent": "client",')
    print('     "targetAgent": "my-chat-agent",')
    print('     "params": {')
    print('       "initialMessage": {')
    print('         "role": "user",')
    print('         "parts": [{"type": "TextPart", "content": "Hello!"}]')
    print('       },')
    print('       "stream": false')
    print('     }')
    print('   }')
    print()
    print('   # Start chat (streaming)')
    print('   POST /arc/ {..., "params": {"stream": true}}')
    print()
    print("🌐 Access at: http://localhost:8000")
    print("📚 API docs: http://localhost:8000/docs")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)