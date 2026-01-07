"""
Example: Using ChatManager with PostgreSQL storage for persistent chat sessions.

This example demonstrates:
1. Setting up PostgreSQL connection pool
2. Initializing database schema
3. Initializing ChatManager with PostgreSQLChatStorage
4. Creating and managing chats with automatic persistence
5. Manual cleanup of expired chats (PostgreSQL doesn't have automatic TTL)
"""

import asyncio
import logging
import uuid
import asyncpg
from arc.core.chat import ChatManager
from arc.server.storage import PostgreSQLChatStorage

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def main():
    logger.info("Starting PostgreSQL ChatManager example...")
    
    # Step 1: Create PostgreSQL connection pool
    # Users provide their own database credentials
    try:
        db_pool = await asyncpg.create_pool(
            host='localhost',
            port=5432,
            user='your_db_user',  # Change to your PostgreSQL user
            password='your_db_password',  # Change to your PostgreSQL password
            database='your_db_name',  # Change to your database name
            min_size=2,
            max_size=10,
            command_timeout=60
        )
        logger.info("Connected to PostgreSQL successfully")
        
        # Step 2: Create PostgreSQLChatStorage with the connection pool
        storage = PostgreSQLChatStorage(db_pool, table_name="arc_chats")
        
        # Step 3: Initialize database schema (creates table and indexes if they don't exist)
        logger.info("\n--- Initializing database schema ---")
        await storage.initialize_schema()
        logger.info("Database schema initialized")
        
        # Step 4: Initialize ChatManager with PostgreSQL storage
        chat_manager = ChatManager(agent_id="agent-server-1", storage=storage)
        
        # Step 5: Create a chat (stored in both RAM and PostgreSQL)
        logger.info("\n--- Creating a new chat ---")
        chat_result = await chat_manager.create_chat(
            target_agent="agent-A",
            metadata={"user_id": "user-456", "topic": "billing_inquiry"}
        )
        chat_id = chat_result["chatId"]
        logger.info(f"Created chat: {chat_id}")
        
        # Step 6: Update metadata (e.g., add framework thread_id)
        logger.info("\n--- Updating chat metadata ---")
        framework_thread_id = str(uuid.uuid4())
        await chat_manager.update_metadata(chat_id, {
            "framework": "langchain",
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
        
        # Step 9: Close the chat (marks as CLOSED with closedAt timestamp)
        logger.info("\n--- Closing chat ---")
        close_result = await chat_manager.close_chat(chat_id, reason="Issue resolved")
        logger.info(f"Chat {chat_id} closed: {close_result['status']}")
        logger.info("Chat will be kept in PostgreSQL for 24 hours (requires manual cleanup)")
        
        # Step 10: Verify chat is still accessible (but CLOSED)
        logger.info("\n--- Verifying closed chat is still accessible ---")
        closed_chat = await chat_manager.get_chat(chat_id)
        logger.info(f"Closed chat status: {closed_chat['status']}")
        logger.info("Chat data (metadata mapping) is preserved for debugging/analytics")
        
        # Step 11: Demonstrate cleanup (removes expired CLOSED chats from both RAM and PostgreSQL)
        logger.info("\n--- Running cleanup (removes chats closed >24 hours ago) ---")
        cleanup_count = await chat_manager.cleanup_old_chats(max_age_seconds=86400)
        logger.info(f"Cleaned up {cleanup_count} old chats from RAM and PostgreSQL")
        logger.info("NOTE: For production, run cleanup_old_chats() periodically (cron job or scheduler)")
        
        # Step 12: Create another chat to demonstrate persistence
        logger.info("\n--- Creating second chat to show persistence ---")
        chat_result_2 = await chat_manager.create_chat(
            target_agent="agent-B",
            metadata={"framework": "llamaindex", "framework_thread_id": str(uuid.uuid4())}
        )
        chat_id_2 = chat_result_2["chatId"]
        logger.info(f"Created second chat: {chat_id_2}")
        
        # Clear RAM to simulate server restart
        logger.info("\n--- Simulating server restart (clearing RAM) ---")
        chat_manager.active_chats.clear()
        logger.info("RAM cache cleared")
        
        # Retrieve chat from PostgreSQL (should still exist)
        logger.info("\n--- Retrieving chat from PostgreSQL after 'restart' ---")
        recovered_chat = await chat_manager.get_chat(chat_id_2)
        logger.info(f"Successfully recovered chat {chat_id_2} from PostgreSQL")
        logger.info(f"Chat status: {recovered_chat['status']}")
        
        # Step 13: Query database directly to show stored data
        logger.info("\n--- Querying PostgreSQL directly ---")
        async with db_pool.acquire() as conn:
            count = await conn.fetchval("SELECT COUNT(*) FROM arc_chats")
            logger.info(f"Total chats in database: {count}")
            
            active_count = await conn.fetchval("SELECT COUNT(*) FROM arc_chats WHERE status != 'CLOSED'")
            logger.info(f"Active chats in database: {active_count}")
        
        logger.info("\n PostgreSQL ChatManager example completed successfully")
        logger.info("\n📝 PRODUCTION NOTES:")
        logger.info("   1. Set up a cron job or scheduler to call cleanup_old_chats() periodically")
        logger.info("   2. Consider adding indexes on frequently queried fields")
        logger.info("   3. Configure connection pool size based on your load")
        logger.info("   4. Use environment variables for database credentials")
        
    except asyncpg.PostgresError as e:
        logger.error(f"PostgreSQL error: {e}")
        logger.error("Make sure PostgreSQL is running and credentials are correct")
    except Exception as e:
        logger.error(f"Error in example: {e}", exc_info=True)
    finally:
        # Close database connection pool
        if 'db_pool' in locals():
            await db_pool.close()
            logger.info("PostgreSQL connection pool closed")


if __name__ == "__main__":
    asyncio.run(main())

