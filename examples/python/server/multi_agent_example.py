#!/usr/bin/env python3
"""
Multi-Agent ARC Server Example - Travel & Booking Platform

Demonstrates how to create a server with multiple specialized agents:
- Flight Finder: task.create, chat.start (flight search)
- Hotel Booking: task.create, chat.start (hotel search)
- Itinerary Planner: task.create, chat.start (trip planning)
- Price Tracker: task.create, chat.start, chat.message (price monitoring)

Shows how different agents can handle different method sets and specializations.
"""

import asyncio
import uuid
import os
import sys
import json
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from arc.server.arc_server import create_server
from arc.server.decorators import validate_params, trace_method, error_handler
from arc.utils.logging import configure_root_logger, create_logger
from arc.server.sse import create_sse_response
from arc.core.streaming import create_chat_stream_generator

# Configure logging
configure_root_logger()
logger = create_logger("travel-booking-server")

# Create multi-agent server with ChatManager
server = create_server(
    server_id="travel-booking-platform",
    name="Travel & Booking Multi-Agent Server",
    version="1.0.0",
    server_description="Travel booking platform with specialized agents",
    enable_cors=True,
    enable_logging=True,
    enable_chat_manager=True,
    chat_manager_agent_id="travel-booking-platform"
)

# Flight Finder Agent - Searches for flights
@server.agent_handler("flight-finder", "task.create")
@trace_method
@error_handler
@validate_params()
async def handle_flight_task_create(params, context):
    """Flight finder task creation handler"""
    task_id = f"flight_{int(datetime.utcnow().timestamp() * 1000)}"
    initial_message = params["initialMessage"]
    priority = params.get("priority", "NORMAL")
    
    created_at = datetime.utcnow().isoformat() + "Z"
    completed_at = datetime.utcnow().isoformat() + "Z"
    
    # Simulate flight search results
    flights = [
        {"airline": "Delta", "price": 450, "departure": "10:30 AM", "arrival": "2:45 PM", "duration": "4h 15m"},
        {"airline": "United", "price": 420, "departure": "1:15 PM", "arrival": "5:30 PM", "duration": "4h 15m"},
        {"airline": "Southwest", "price": 380, "departure": "6:00 AM", "arrival": "10:15 AM", "duration": "4h 15m"},
    ]
    
    logger.info(f"Flight finder created task {task_id} for flight search")
    
    return {
        "type": "task",
        "task": {
            "taskId": task_id,
            "status": "COMPLETED",
            "createdAt": created_at,
            "completedAt": completed_at,
            "artifacts": [
                {
                    "artifactId": f"artifact_{int(datetime.utcnow().timestamp() * 1000)}",
                    "name": "Flight Search Results",
                    "parts": [{
                        "type": "DataPart",
                        "content": json.dumps(flights),
                        "mimeType": "application/json"
                    }],
                    "createdAt": created_at
                }
            ]
        }
    }

@server.agent_handler("flight-finder", "chat.start")
@trace_method
@error_handler
@validate_params()
async def handle_flight_chat_start(params, context):
    """Flight finder chat handler"""
    initial_message = params["initialMessage"]
    chat_id = params.get("chatId", f"flight_chat_{uuid.uuid4().hex[:8]}")
    stream = params.get("stream", False)
    
    # Use ChatManager from context
    chat_manager = context["chat_manager"]
    chat_info = chat_manager.create_chat(
        target_agent=context["request_agent"],
        chat_id=chat_id,
        metadata={"agent_type": "flight-finder", "specialization": "flight_search"}
    )
    
    if stream:
        async def flight_content_stream():
            response_parts = [
                "Flight Search Assistant: ", "Where would you like to fly? ",
                "I can help you ", "find the best flights ", "by price, time, ", 
                "or airline."
            ]
            for part in response_parts:
                await asyncio.sleep(0.15)
                yield part
        
        return create_sse_response(create_chat_stream_generator(
            chat_id=chat_id,
            content_generator=flight_content_stream(),
            request_id=context.get("request_id", "unknown")
        ))
    
    # Non-streaming response
    response_text = "Flight Search Assistant: Where would you like to fly? I can help you find the best flights by price, time, or airline."
    agent_message = {
        "role": "agent",
        "parts": [{
            "type": "TextPart",
            "content": response_text
        }],
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    
    return {
        "type": "chat",
        "chat": {
            "chatId": chat_id,
            "status": "ACTIVE",
            "createdAt": chat_info["createdAt"],
            "message": agent_message
        }
    }

# Hotel Booking Agent - Searches for hotels
@server.agent_handler("hotel-booking", "task.create")
@trace_method
@error_handler
@validate_params()
async def handle_hotel_task_create(params, context):
    """Hotel booking task creation handler"""
    task_id = f"hotel_{int(datetime.utcnow().timestamp() * 1000)}"
    initial_message = params["initialMessage"]
    priority = params.get("priority", "NORMAL")
    
    created_at = datetime.utcnow().isoformat() + "Z"
    completed_at = datetime.utcnow().isoformat() + "Z"
    
    # Simulate hotel search results
    hotels = [
        {"name": "Grand Plaza Hotel", "rating": 4.5, "price": 189, "amenities": ["WiFi", "Pool", "Gym"]},
        {"name": "City Center Inn", "rating": 4.2, "price": 149, "amenities": ["WiFi", "Breakfast"]},
        {"name": "Airport Suites", "rating": 3.8, "price": 99, "amenities": ["WiFi", "Shuttle"]},
    ]
    
    logger.info(f"Hotel booking created task {task_id} for hotel search")
    
    return {
        "type": "task",
        "task": {
            "taskId": task_id,
            "status": "COMPLETED",
            "createdAt": created_at,
            "completedAt": completed_at,
            "artifacts": [
                {
                    "artifactId": f"artifact_{int(datetime.utcnow().timestamp() * 1000)}",
                    "name": "Hotel Options",
                    "parts": [{
                        "type": "DataPart",
                        "content": json.dumps(hotels),
                        "mimeType": "application/json"
                    }],
                    "createdAt": created_at
                }
            ]
        }
    }

@server.agent_handler("hotel-booking", "chat.start")
@trace_method
@error_handler
@validate_params()
async def handle_hotel_chat_start(params, context):
    """Hotel booking chat handler"""
    initial_message = params["initialMessage"]
    chat_id = params.get("chatId", f"hotel_chat_{uuid.uuid4().hex[:8]}")
    stream = params.get("stream", False)
    
    # Use ChatManager from context
    chat_manager = context["chat_manager"]
    chat_info = chat_manager.create_chat(
        target_agent=context["request_agent"],
        chat_id=chat_id,
        metadata={"agent_type": "hotel-booking", "specialization": "hotel_search"}
    )
    
    if stream:
        async def hotel_content_stream():
            response_parts = [
                "Hotel Booking Agent: ", "I'll help you ", "find the perfect ",
                "accommodation. ", "What city and dates ", "are you looking for?"
            ]
            for part in response_parts:
                await asyncio.sleep(0.12)
                yield part
        
        return create_sse_response(create_chat_stream_generator(
            chat_id=chat_id,
            content_generator=hotel_content_stream(),
            request_id=context.get("request_id", "unknown")
        ))
    
    # Non-streaming response
    response_text = "Hotel Booking Agent: I'll help you find the perfect accommodation. What city and dates are you looking for?"
    agent_message = {
        "role": "agent",
        "parts": [{
            "type": "TextPart",
            "content": response_text
        }],
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    
    return {
        "type": "chat",
        "chat": {
            "chatId": chat_id,
            "status": "ACTIVE",
            "createdAt": chat_info["createdAt"],
            "message": agent_message
        }
    }

# Itinerary Planner Agent - Creates travel plans
@server.agent_handler("itinerary-planner", "task.create")
@trace_method
@error_handler
@validate_params()
async def handle_itinerary_task_create(params, context):
    """Itinerary planner task creation handler"""
    task_id = f"itinerary_{int(datetime.utcnow().timestamp() * 1000)}"
    initial_message = params["initialMessage"]
    priority = params.get("priority", "NORMAL")
    
    created_at = datetime.utcnow().isoformat() + "Z"
    completed_at = datetime.utcnow().isoformat() + "Z"
    
    # Simulate itinerary creation
    itinerary = {
        "destination": "Paris, France",
        "days": 5,
        "schedule": [
            {"day": 1, "activities": ["Arrive", "Eiffel Tower", "Seine River Cruise"]},
            {"day": 2, "activities": ["Louvre Museum", "Notre-Dame", "Latin Quarter"]},
            {"day": 3, "activities": ["Versailles Palace", "Shopping", "Moulin Rouge"]},
            {"day": 4, "activities": ["Montmartre", "Sacré-Cœur", "Arc de Triomphe"]},
            {"day": 5, "activities": ["Last minute shopping", "Departure"]},
        ],
        "estimatedBudget": 2500,
    }
    
    logger.info(f"Itinerary planner created task {task_id} for trip planning")
    
    return {
        "type": "task",
        "task": {
            "taskId": task_id,
            "status": "COMPLETED",
            "createdAt": created_at,
            "completedAt": completed_at,
            "artifacts": [
                {
                    "artifactId": f"artifact_{int(datetime.utcnow().timestamp() * 1000)}",
                    "name": "5-Day Paris Itinerary",
                    "parts": [{
                        "type": "DataPart",
                        "content": json.dumps(itinerary),
                        "mimeType": "application/json"
                    }],
                    "createdAt": created_at
                }
            ]
        }
    }

@server.agent_handler("itinerary-planner", "chat.start")
@trace_method
@error_handler
@validate_params()
async def handle_itinerary_chat_start(params, context):
    """Itinerary planner chat handler"""
    initial_message = params["initialMessage"]
    chat_id = params.get("chatId", f"itinerary_chat_{uuid.uuid4().hex[:8]}")
    stream = params.get("stream", False)
    
    # Use ChatManager from context
    chat_manager = context["chat_manager"]
    chat_info = chat_manager.create_chat(
        target_agent=context["request_agent"],
        chat_id=chat_id,
        metadata={"agent_type": "itinerary-planner", "specialization": "trip_planning"}
    )
    
    if stream:
        async def itinerary_content_stream():
            response_parts = [
                "Travel Planner: ", "I'll create ", "a personalized ",
                "itinerary ", "for your trip! ", "What's your destination ", 
                "and how many days?"
            ]
            for part in response_parts:
                await asyncio.sleep(0.12)
                yield part
        
        return create_sse_response(create_chat_stream_generator(
            chat_id=chat_id,
            content_generator=itinerary_content_stream(),
            request_id=context.get("request_id", "unknown")
        ))
    
    # Non-streaming response
    response_text = "Travel Planner: I'll create a personalized itinerary for your trip! What's your destination and how many days?"
    agent_message = {
        "role": "agent",
        "parts": [{
            "type": "TextPart",
            "content": response_text
        }],
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    
    return {
        "type": "chat",
        "chat": {
            "chatId": chat_id,
            "status": "ACTIVE",
            "createdAt": chat_info["createdAt"],
            "message": agent_message
        }
    }

# Price Tracker Agent - Monitors travel prices
@server.agent_handler("price-tracker", "task.create")
@trace_method
@error_handler
@validate_params()
async def handle_tracker_task_create(params, context):
    """Price tracker task creation handler"""
    task_id = f"tracker_{int(datetime.utcnow().timestamp() * 1000)}"
    initial_message = params["initialMessage"]
    priority = params.get("priority", "NORMAL")
    
    created_at = datetime.utcnow().isoformat() + "Z"
    
    # Simulate price tracking setup
    price_history = [
        {"date": "2024-01-01", "price": 520},
        {"date": "2024-01-08", "price": 480},
        {"date": "2024-01-15", "price": 450},
        {"date": "2024-01-22", "price": 420},
    ]
    
    logger.info(f"Price tracker created task {task_id} for price monitoring")
    
    return {
        "type": "task",
        "task": {
            "taskId": task_id,
            "status": "SUBMITTED",
            "createdAt": created_at,
            "metadata": {
                "tracking": "JFK → LAX",
                "currentPrice": 420,
                "lowestPrice": 380,
                "priceDropAlert": True,
                "alertThreshold": 400,
            },
            "artifacts": [
                {
                    "artifactId": f"artifact_{int(datetime.utcnow().timestamp() * 1000)}",
                    "name": "Price History",
                    "parts": [{
                        "type": "DataPart",
                        "content": json.dumps(price_history),
                        "mimeType": "application/json"
                    }],
                    "createdAt": created_at
                }
            ]
        }
    }

@server.agent_handler("price-tracker", "chat.start")
@trace_method
@error_handler
@validate_params()
async def handle_tracker_chat_start(params, context):
    """Price tracker chat handler"""
    initial_message = params["initialMessage"]
    chat_id = params.get("chatId", f"tracker_chat_{uuid.uuid4().hex[:8]}")
    stream = params.get("stream", False)
    
    # Use ChatManager from context
    chat_manager = context["chat_manager"]
    chat_info = chat_manager.create_chat(
        target_agent=context["request_agent"],
        chat_id=chat_id,
        metadata={"agent_type": "price-tracker", "specialization": "price_monitoring"}
    )
    
    if stream:
        async def tracker_content_stream():
            response_parts = [
                "Price Tracker: ", "I'll monitor prices ", "and alert you ",
                "when they drop! ", "What route and price point ", 
                "are you interested in?"
            ]
            for part in response_parts:
                await asyncio.sleep(0.12)
                yield part
        
        return create_sse_response(create_chat_stream_generator(
            chat_id=chat_id,
            content_generator=tracker_content_stream(),
            request_id=context.get("request_id", "unknown")
        ))
    
    # Non-streaming response
    response_text = "Price Tracker: I'll monitor prices and alert you when they drop! What route and price point are you interested in?"
    agent_message = {
        "role": "agent",
        "parts": [{
            "type": "TextPart",
            "content": response_text
        }],
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    
    return {
        "type": "chat",
        "chat": {
            "chatId": chat_id,
            "status": "ACTIVE",
            "createdAt": chat_info["createdAt"],
            "message": agent_message
        }
    }

@server.agent_handler("price-tracker", "chat.message")
@trace_method
@error_handler
@validate_params()
async def handle_tracker_chat_message(params, context):
    """Price tracker chat message handler"""
    chat_id = params["chatId"]
    message = params["message"]
    stream = params.get("stream", False)
    
    # Validate chat exists
    chat_manager = context["chat_manager"]
    try:
        chat = chat_manager.get_chat(chat_id)
    except Exception as e:
        raise ValueError(f"Chat not found: {chat_id}")
    
    if stream:
        async def tracker_message_stream():
            response_parts = [
                "Great! ", "I've set up ", "a price alert. ",
                "You'll get notified ", "when the price drops ",
                "below $400. ", "Current price: $420."
            ]
            for part in response_parts:
                await asyncio.sleep(0.1)
                yield part
        
        return create_sse_response(create_chat_stream_generator(
            chat_id=chat_id,
            content_generator=tracker_message_stream(),
            request_id=context.get("request_id", "unknown")
        ))
    
    # Non-streaming response
    response_text = "Great! I've set up a price alert. You'll get notified when the price drops below $400. Current price: $420."
    agent_message = {
        "role": "agent",
        "parts": [{
            "type": "TextPart",
            "content": response_text
        }],
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    
    return {
        "type": "chat",
        "chat": {
            "chatId": chat_id,
            "status": "ACTIVE",
            "createdAt": chat["createdAt"],
            "message": agent_message
        }
    }

# Add chat.end handlers for all chat agents
for agent_id in ["flight-finder", "hotel-booking", "itinerary-planner", "price-tracker"]:
    @server.agent_handler(agent_id, "chat.end")
    @trace_method
    @error_handler
    @validate_params()
    async def handle_chat_end(params, context):
        """Generic chat end handler"""
        chat_id = params["chatId"]
        reason = params.get("reason", "Chat ended by user")
        
        # Close chat
        chat_manager = context["chat_manager"]
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
    print(f"Starting Travel & Booking Multi-Agent Server")
    print(f"Server ID: travel-booking-platform")
    print(f"Registered agents:")
    for agent_id, methods in server.agents.items():
        print(f"  - {agent_id}: {', '.join(methods.keys())}")
    print(f"Total agents: {len(server.agents)}")
    print(f"Total methods: {sum(len(methods) for methods in server.agents.values())}")
    print(f"Listening at: http://localhost:8000/arc")
    print(f"Health check: http://localhost:8000/health")
    print(f"Agent info: http://localhost:8000/agent-info")
    print(f"Press Ctrl+C to stop the server")
    server.run(host="0.0.0.0", port=8000)
