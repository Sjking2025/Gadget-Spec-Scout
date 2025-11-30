"""
Gadget Scout MCP Server - Main server implementation
"""

import asyncio
import json
import logging
from typing import Any, Sequence
from mcp.server import Server
from mcp.types import Resource, Tool, Prompt, TextContent, ImageContent, EmbeddedResource
from mcp.server.stdio import stdio_server

# Import our components
from resources.conversation import ConversationTracker
from resources.tool_registry import ToolRegistry
from prompts.query_context import QueryContextGenerator
import config

# Setup logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(config.LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize components
conversation_tracker = ConversationTracker(max_history=config.MAX_HISTORY_LENGTH)
tool_registry = ToolRegistry()
context_generator = QueryContextGenerator(conversation_tracker, tool_registry)

# Create MCP server
server = Server(config.SERVER_NAME)

logger.info(f"Initializing {config.SERVER_NAME} v{config.SERVER_VERSION}")


@server.list_resources()
async def list_resources() -> list[Resource]:
    """List available resources"""
    logger.info("Listing resources")
    
    return [
        Resource(
            uri="gadget-scout://tools/registry",
            name="Tool Registry",
            description="Complete registry of all available tools with metadata and usage patterns",
            mimeType="application/json"
        ),
        Resource(
            uri="gadget-scout://conversation/current",
            name="Current Conversation Context",
            description="Context from current conversation including history and inferred preferences",
            mimeType="application/json"
        ),
        Resource(
            uri="gadget-scout://analytics/tools",
            name="Tool Analytics",
            description="Usage statistics and patterns for all tools",
            mimeType="application/json"
        )
    ]


@server.read_resource()
async def read_resource(uri: str) -> str:
    """Read a resource by URI"""
    logger.info(f"Reading resource: {uri}")
    
    if uri == "gadget-scout://tools/registry":
        return tool_registry.to_json()
    
    elif uri == "gadget-scout://conversation/current":
        return conversation_tracker.to_json()
    
    elif uri == "gadget-scout://analytics/tools":
        analytics = {
            "most_used_tools": tool_registry.get_most_used_tools(),
            "common_sequences": tool_registry.get_common_sequences(),
            "tool_stats": tool_registry.tool_stats
        }
        return json.dumps(analytics, indent=2)
    
    else:
        raise ValueError(f"Unknown resource URI: {uri}")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools"""
    logger.info("Listing tools")
    
    tools = []
    for tool_meta in tool_registry.get_all_tools():
        tools.append(Tool(
            name=tool_meta["name"],
            description=tool_meta["description"],
            inputSchema=tool_meta["input_schema"]
        ))
    
    return tools


@server.call_tool()
async def call_tool(name: str, arguments: Any) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    """Call a tool (placeholder - actual tools are in the notebook)"""
    logger.info(f"Tool call: {name} with args: {arguments}")
    
    # Record the call
    tool_registry.record_tool_call(name, success=True)
    
    # Return a message indicating tools are handled by the notebook
    return [
        TextContent(
            type="text",
            text=f"Tool '{name}' should be called by the notebook. MCP server tracks metadata only."
        )
    ]


@server.list_prompts()
async def list_prompts() -> list[Prompt]:
    """List available prompts"""
    logger.info("Listing prompts")
    
    return [
        Prompt(
            name="get_query_context",
            description="Generate intelligent context for a user query",
            arguments=[
                {
                    "name": "query",
                    "description": "The user's query",
                    "required": True
                }
            ]
        ),
        Prompt(
            name="get_conversation_summary",
            description="Get a summary of the current conversation",
            arguments=[]
        )
    ]


@server.get_prompt()
async def get_prompt(name: str, arguments: dict[str, str] | None = None) -> str:
    """Get a prompt with arguments"""
    logger.info(f"Getting prompt: {name} with args: {arguments}")
    
    if name == "get_query_context":
        query = arguments.get("query", "") if arguments else ""
        if not query:
            return "Error: query argument is required"
        
        # Generate context
        context = context_generator.generate_context(query)
        return context
    
    elif name == "get_conversation_summary":
        # Get conversation context
        ctx = conversation_tracker.get_context()
        
        summary = f"""
CONVERSATION SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 Queries So Far: {ctx['query_count']}

"""
        # Add last queries
        for i, query_record in enumerate(ctx.get('last_3_queries', []), 1):
            summary += f"{i}️⃣ \"{query_record['query']}\"\n"
            summary += f"   Tools Used: {', '.join(query_record['tools_called'])}\n\n"
        
        # Add inferred preferences
        prefs = ctx.get('inferred_preferences', {})
        if prefs:
            summary += "🎯 Inferred Preferences:\n"
            if prefs.get('budget_range'):
                summary += f"   Budget: {prefs['budget_range']}\n"
            if prefs.get('priority_features'):
                summary += f"   Features: {', '.join(prefs['priority_features'])}\n"
            if prefs.get('brands_interested'):
                summary += f"   Brands: {', '.join(prefs['brands_interested'])}\n"
        
        summary += f"\n🔑 Conversation Theme: {ctx.get('conversation_theme', 'general')}\n"
        
        return summary.strip()
    
    else:
        raise ValueError(f"Unknown prompt: {name}")


async def main():
    """Main entry point"""
    logger.info(f"Starting {config.SERVER_NAME} server")
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
