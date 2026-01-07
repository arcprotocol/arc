"""
Example: Using ChatManager with MongoDB storage for persistent chat sessions.

This example demonstrates:
1. Setting up MongoDB connection
2. Initializing TTL indexes for automatic cleanup
3. Initializing ChatManager with MongoChatStorage
4. Creating and managing chats with automatic persistence
5. Automatic cleanup via MongoDB TTL index (expires 24 hours after closedAt)
"""

import asyncio
import logging
import uuid
from motor.motor_asyncio import AsyncIOMotorClient
from arc.core.chat import ChatManager
from arc.server.storage import MongoChatStorage

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def main():
    logger.info("Starting MongoDB ChatManager example...")
    
    # Step 1: Create MongoDB client and database
    # Users provide their own MongoDB connection string
    try:
        mongo_client = AsyncIOMotorClient(
            'mongodb://localhost:27017',  # Change to your MongoDB URI
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=5000
        )
        
        # Get database
        db = mongo_client['arc_chat_db']  # Change to your database name
        
        # Test connection
        await mongo_client.admin.command('ping')
        logger.info("Connected to MongoDB successfully")
        
        # Step 2: Create MongoChatStorage with the database
        storage = MongoChatStorage(db, collection_name="arc_chats")
        
        # Step 3: Initialize indexes (creates TTL index for automatic cleanup)
        logger.info("\n--- Initializing MongoDB indexes ---")
        await storage.initialize_indexes()
        logger.info("MongoDB indexes initialized (TTL index will auto-delete closed chats after 24h)")
        
        # Step 4: Initialize ChatManager with MongoDB storage
        chat_manager = ChatManager(agent_id="agent-server-1", storage=storage)
        
        # Step 5: Create a chat (stored in both RAM and MongoDB)
        logger.info("\n--- Creating a new chat ---")
        chat_result = await chat_manager.create_chat(
            target_agent="agent-A",
            metadata={"user_id": "user-789", "topic": "product_demo"}
        )
        chat_id = chat_result["chatId"]
        logger.info(f"Created chat: {chat_id}")
        
        # Step 6: Update metadata (e.g., add framework thread_id)
        logger.info("\n--- Updating chat metadata ---")
        framework_thread_id = str(uuid.uuid4())
        await chat_manager.update_metadata(chat_id, {
            "framework": "custom",
            "framework_thread_id": framework_thread_id
        })
        logger.info(f"Updated metadata with framework_thread_id: {framework_thread_id}")
        
        # Step 7: Retrieve chat information
        logger.info("\n--- Retrieving chat info ---")
        chat_info = await chat_manager.get_chat(chat_id)
        logger.info(f"Chat status: {chat_info['status']}")
        logger.info(f"Chat metadata: {chat_info['metadata']}")
        logger.info(f"Framework thread_id: {chat_info['metadata'].get('framework_thread_id')}")
        
        # Step 8: List active chats
        logger.info("\n--- Listing active chats ---")
        active_chats = await chat_manager.get_active_chats()
        logger.info(f"Active chats: {len(active_chats)}")
        for chat in active_chats:
            logger.info(f"  - {chat['chatId']} with {chat['targetAgent']}")
        
        # Step 9: Close the chat (sets closedAt timestamp, TTL index will auto-delete after 24h)
        logger.info("\n--- Closing chat ---")
        close_result = await chat_manager.close_chat(chat_id, reason="Demo completed")
        logger.info(f"Chat {chat_id} closed: {close_result['status']}")
        logger.info("MongoDB TTL index will automatically delete this chat 24 hours after closedAt")
        
        # Step 10: Verify chat is still accessible (but CLOSED)
        logger.info("\n--- Verifying closed chat is still accessible ---")
        closed_chat = await chat_manager.get_chat(chat_id)
        logger.info(f"Closed chat status: {closed_chat['status']}")
        logger.info("Chat data (metadata mapping) is preserved for 24 hours for debugging/analytics")
        
        # Step 11: Demonstrate cleanup (MongoDB TTL handles this automatically)
        logger.info("\n--- Running cleanup ---")
        cleanup_count = await chat_manager.cleanup_old_chats(max_age_seconds=86400)
        logger.info(f"Cleaned up {cleanup_count} old chats from RAM")
        logger.info("MongoDB TTL index handles persistent storage cleanup automatically")
        
        # Step 12: Create another chat to demonstrate persistence
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
        
        # Retrieve chat from MongoDB (should still exist)
        logger.info("\n--- Retrieving chat from MongoDB after 'restart' ---")
        recovered_chat = await chat_manager.get_chat(chat_id_2)
        logger.info(f"Successfully recovered chat {chat_id_2} from MongoDB")
        logger.info(f"Chat status: {recovered_chat['status']}")
        
        # Step 13: Query MongoDB directly to show stored data
        logger.info("\n--- Querying MongoDB directly ---")
        collection = db['arc_chats']
        total_count = await collection.count_documents({})
        logger.info(f"Total chats in MongoDB: {total_count}")
        
        active_count = await collection.count_documents({"status": {"$ne": "CLOSED"}})
        logger.info(f"Active chats in MongoDB: {active_count}")
        
        # Show indexes
        logger.info("\n--- MongoDB Indexes ---")
        indexes = await collection.index_information()
        for index_name, index_info in indexes.items():
            logger.info(f"  - {index_name}: {index_info}")
        
        logger.info("\n MongoDB ChatManager example completed successfully")
        logger.info("\n📝 PRODUCTION NOTES:")
        logger.info("   1. MongoDB TTL index handles automatic cleanup (no cron job needed)")
        logger.info("   2. TTL background thread runs every 60 seconds by default")
        logger.info("   3. Consider sharding for very high volume")
        logger.info("   4. Use connection pooling (Motor handles this automatically)")
        logger.info("   5. Use environment variables for MongoDB URI and credentials")
        
    except Exception as e:
        logger.error(f"Error in example: {e}", exc_info=True)
        if 'ConnectionError' in str(type(e).__name__):
            logger.error("Make sure MongoDB is running on localhost:27017")
    finally:
        # Close MongoDB connection
        if 'mongo_client' in locals():
            mongo_client.close()
            logger.info("MongoDB connection closed")


if __name__ == "__main__":
    asyncio.run(main())

