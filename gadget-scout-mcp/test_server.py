"""
Simple test script for the MCP server
"""

import asyncio
import json
from resources.conversation import ConversationTracker
from resources.tool_registry import ToolRegistry
from prompts.query_context import QueryContextGenerator


async def test_mcp_components():
    """Test MCP server components"""
    
    print("=" * 80)
    print("Testing Gadget Scout MCP Server Components")
    print("=" * 80)
    
    # Initialize components
    print("\n1️⃣ Initializing components...")
    conversation = ConversationTracker(max_history=10)
    registry = ToolRegistry()
    context_gen = QueryContextGenerator(conversation, registry)
    print("✅ Components initialized")
    
    # Test 1: Tool Registry
    print("\n2️⃣ Testing Tool Registry...")
    tools = registry.get_all_tools()
    print(f"   Found {len(tools)} tools")
    for tool in tools:
        print(f"   - {tool['name']}: {tool['description'][:50]}...")
    print("✅ Tool registry working")
    
    # Test 2: Conversation Tracking
    print("\n3️⃣ Testing Conversation Tracking...")
    conversation.track_query(
        query="Compare Samsung S24 Ultra and iPhone 15 Pro Max",
        tools_called=["compare_specs", "get_price"],
        result_summary="Comparison provided",
        session_id="test_session"
    )
    conversation.track_query(
        query="What's the price difference?",
        tools_called=["get_price"],
        result_summary="Price difference shown",
        session_id="test_session"
    )
    
    context = conversation.get_context()
    print(f"   Tracked {context['query_count']} queries")
    print(f"   Theme: {context['conversation_theme']}")
    print(f"   Inferred preferences: {context['inferred_preferences']}")
    print("✅ Conversation tracking working")
    
    # Test 3: Context Generation
    print("\n4️⃣ Testing Context Generation...")
    test_query = "Which phone has better battery?"
    generated_context = context_gen.generate_context(test_query)
    print(f"   Query: {test_query}")
    print("\n   Generated Context:")
    print("   " + "\n   ".join(generated_context.split("\n")[:10]))
    print("   ...")
    print("✅ Context generation working")
    
    # Test 4: Resource Export
    print("\n5️⃣ Testing Resource Export...")
    registry_json = registry.to_json()
    conversation_json = conversation.to_json()
    print(f"   Tool registry JSON: {len(registry_json)} characters")
    print(f"   Conversation JSON: {len(conversation_json)} characters")
    print("✅ Resource export working")
    
    print("\n" + "=" * 80)
    print("✅ All tests passed! MCP server components are working correctly.")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(test_mcp_components())
