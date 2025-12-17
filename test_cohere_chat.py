#!/usr/bin/env python3
"""
Test script to verify the Cohere chat functionality
"""
import os
import sys
import asyncio
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from dotenv import load_dotenv
load_dotenv()

async def test_cohere_chat():
    """Test the Cohere chat functionality."""
    try:
        from backend.src.chat.cohere_chat_client import CohereChatClient
        from backend.src.utils.config import Config

        print("[INFO] Testing Cohere chat functionality...")

        # Initialize configuration
        config = Config()
        print(f"[INFO] Configuration loaded successfully")

        # Initialize Cohere chat client
        cohere_client = CohereChatClient(config)
        print(f"[INFO] Cohere client initialized")

        # Test query and context
        query = "What is Physical AI?"
        context = """
        Physical AI is an emerging field that combines artificial intelligence with real-world physics.
        This interdisciplinary approach enables AI systems to understand and interact with the physical world.
        Key concepts include embodied intelligence, sensorimotor learning, and physics-informed neural networks.
        Applications range from robotics and autonomous vehicles to material science and drug discovery.
        The field represents a convergence of machine learning, physics, and engineering disciplines.
        """

        print(f"[INFO] Generating answer for query: {query}")

        # Generate answer
        answer = await cohere_client.generate_answer(query, context)

        if answer:
            print(f"[SUCCESS] Generated answer: {answer}")
        else:
            print(f"[ERROR] Failed to generate answer")

        return answer is not None

    except ImportError as e:
        print(f"[ERROR] Import error: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Error during Cohere chat test: {e}")
        import traceback
        traceback.print_exc()
        return False

# Run the async test
if __name__ == "__main__":
    success = asyncio.run(test_cohere_chat())
    if not success:
        sys.exit(1)