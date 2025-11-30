"""
Colab-Compatible MCP Client (Direct Import Version)

This version directly imports and uses MCP components without stdio,
which is compatible with Google Colab environment.
"""

import sys
import os
from typing import Optional, Dict, Any


class ColabMCPClient:
    """Simplified MCP Client for Google Colab"""
    
    def __init__(self):
        # Import MCP components directly
        sys.path.append('/content/gadget-scout-mcp')
        
        from resources.conversation import ConversationTracker
        from resources.tool_registry import ToolRegistry
        from prompts.query_context import QueryContextGenerator
        
        # Initialize components
        self.conversation = ConversationTracker(max_history=10)
        self.registry = ToolRegistry()
        self.context_gen = QueryContextGenerator(self.conversation, self.registry)
        
        print("✅ MCP components loaded (Colab mode)")
    
    def get_query_context(self, query: str) -> str:
        """Get intelligent context for a query"""
        try:
            context = self.context_gen.generate_context(query)
            return context
        except Exception as e:
            print(f"Warning: Context generation failed: {e}")
            return ""
    
    def get_conversation_summary(self) -> str:
        """Get conversation summary"""
        try:
            ctx = self.conversation.get_context()
            
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
        except Exception as e:
            print(f"Warning: Summary generation failed: {e}")
            return ""
    
    def track_query(
        self,
        query: str,
        tools_called: list,
        result_summary: str,
        session_id: str
    ):
        """Track a query for future context"""
        try:
            self.conversation.track_query(
                query=query,
                tools_called=tools_called,
                result_summary=result_summary,
                session_id=session_id
            )
        except Exception as e:
            print(f"Warning: Query tracking failed: {e}")


# Global instance
_colab_mcp_client: Optional[ColabMCPClient] = None


def initialize_colab_mcp():
    """Initialize the Colab-compatible MCP client"""
    global _colab_mcp_client
    
    try:
        _colab_mcp_client = ColabMCPClient()
        return _colab_mcp_client
    except Exception as e:
        print(f"Failed to initialize MCP: {e}")
        return None


def get_colab_mcp_client() -> Optional[ColabMCPClient]:
    """Get the global MCP client"""
    return _colab_mcp_client
