"""
Example: Using ChatManager with Redis storage for persistent chat sessions.

This example demonstrates:
1. Setting up Redis connection
2. Initializing ChatManager with RedisChatStorage
3. Creating and managing chats with automatic persistence
4. 24-hour TTL for closed chats (automatic cleanup by Redis)
"""

import asyncio
import logging
import uuid
import redis.asyncio as redis
from arc.core.chat import ChatManager
from arc.server.storage import RedisChatStorage

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def main():
    logger.info("Starting Redis ChatManager example...")
    
    # Step 1: Create Redis client
    # Users provide their own Redis connection with their credentials
    redis_client = redis.Redis(
        host='localhost',
        port=6379,
        password=None,  # Set your Redis password if required
        db=0,
        decode_responses=False,  # We handle JSON serialization
        socket_connect_timeout=5,
        socket_timeout=5
    )
    
    try:
        # Test connection
        await redis_client.ping()
        logger.info("Connected to Redis successfully")
        
        # Step 2: Create RedisChatStorage with the Redis client
        storage = RedisChatStorage(redis_client)
        
        # Step 3: Initialize ChatManager with Redis storage
        chat_manager = ChatManager(agent_id="agent-server-1", storage=storage)
        
        # Step 4: Create a chat (stored in both RAM and Redis)
        logger.info("\n--- Creating a new chat ---")
        chat_result = await chat_manager.create_chat(
            target_agent="agent-A",
            metadata={"user_id": "user-123", "topic": "technical_support"}
        )
        chat_id = chat_result["chatId"]
        logger.info(f"Created chat: {chat_id}")
        
        # Step 5: Update metadata (e.g., add framework thread_id)
        logger.info("\n--- Updating chat metadata ---")
        framework_thread_id = str(uuid.uuid4())
        await chat_manager.update_metadata(chat_id, {
            "framework": "custom",
            "framework_thread_id": framework_thread_id
        })
        logger.info(f"Updated metadata with framework_thread_id: {framework_thread_id}")
        
        # Step 6: Retrieve chat information
        logger.info("\n--- Retrieving chat info ---")
        chat_info = await chat_manager.get_chat(chat_id)
        logger.info(f"Chat status: {chat_info['status']}")
        logger.info(f"Chat metadata: {chat_info['metadata']}")
        logger.info(f"Framework thread_id: {chat_info['metadata'].get('framework_thread_id')}")
        
        # Step 7: List active chats
        logger.info("\n--- Listing active chats ---")
        active_chats = await chat_manager.get_active_chats()
        logger.info(f"Active chats: {len(active_chats)}")
        for chat in active_chats:
            logger.info(f"  - {chat['chatId']} with {chat['targetAgent']}")
        
        # Step 8: Close the chat (sets 24-hour TTL in Redis)
        logger.info("\n--- Closing chat ---")
        close_result = await chat_manager.close_chat(chat_id, reason="Issue resolved")
        logger.info(f"Chat {chat_id} closed: {close_result['status']}")
        logger.info("Redis will automatically delete this chat after 24 hours")
        
        # Step 9: Verify chat is still accessible (but CLOSED)
        logger.info("\n--- Verifying closed chat is still accessible ---")
        closed_chat = await chat_manager.get_chat(chat_id)
        logger.info(f"Closed chat status: {closed_chat['status']}")
        logger.info("Chat data (metadata mapping) is preserved for 24 hours for debugging/analytics")
        
        # Step 10: Demonstrate cleanup (removes from RAM, Redis auto-handles TTL)
        logger.info("\n--- Running cleanup ---")
        cleanup_count = await chat_manager.cleanup_old_chats(max_age_seconds=86400)
        logger.info(f"Cleaned up {cleanup_count} old chats from RAM")
        logger.info("Redis TTL will handle persistent storage cleanup automatically")
        
        # Step 11: Create another chat to demonstrate persistence
        logger.info("\n--- Creating second chat to show persistence ---")
        chat_result_2 = await chat_manager.create_chat(
            target_agent="agent-B",
            metadata={"framework": "langchain", "framework_thread_id": str(uuid.uuid4())}
        )
        chat_id_2 = chat_result_2["chatId"]
        logger.info(f"Created second chat: {chat_id_2}")
        
        # Clear RAM to simulate server restart
        logger.info("\n--- Simulating server restart (clearing RAM) ---")
        chat_manager.active_chats.clear()
        logger.info("RAM cache cleared")
        
        # Retrieve chat from Redis (should still exist)
        logger.info("\n--- Retrieving chat from Redis after 'restart' ---")
        recovered_chat = await chat_manager.get_chat(chat_id_2)
        logger.info(f"Successfully recovered chat {chat_id_2} from Redis")
        logger.info(f"Chat status: {recovered_chat['status']}")
        
        logger.info("\n Redis ChatManager example completed successfully")
        
    except redis.ConnectionError as e:
        logger.error(f"Failed to connect to Redis: {e}")
        logger.error("Make sure Redis is running on localhost:6379")
    except Exception as e:
        logger.error(f"Error in example: {e}", exc_info=True)
    finally:
        # Close Redis connection
        await redis_client.close()
        logger.info("Redis connection closed")


if __name__ == "__main__":
    asyncio.run(main())

