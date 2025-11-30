"""
Conversation Tracker - Manages conversation history and context
"""

from datetime import datetime
from typing import List, Dict, Any, Optional
import json
from collections import defaultdict


class ConversationTracker:
    """Tracks conversation history and generates intelligent context"""
    
    def __init__(self, max_history: int = 10):
        self.max_history = max_history
        self.query_history: List[Dict[str, Any]] = []
        self.tool_usage_stats = defaultdict(int)
        self.current_session_id: Optional[str] = None
        
    def track_query(
        self,
        query: str,
        tools_called: List[str],
        result_summary: str,
        session_id: str
    ):
        """Track a query and its tool usage"""
        
        # Update session
        if self.current_session_id != session_id:
            self.current_session_id = session_id
            self.query_history = []  # Reset for new session
        
        # Add to history
        query_record = {
            "query": query,
            "tools_called": tools_called,
            "result_summary": result_summary,
            "timestamp": datetime.now().isoformat(),
            "session_id": session_id
        }
        
        self.query_history.append(query_record)
        
        # Trim history
        if len(self.query_history) > self.max_history:
            self.query_history = self.query_history[-self.max_history:]
        
        # Update stats
        for tool in tools_called:
            self.tool_usage_stats[tool] += 1
    
    def get_last_n_queries(self, n: int = 3) -> List[Dict[str, Any]]:
        """Get last N queries"""
        return self.query_history[-n:] if self.query_history else []
    
    def infer_preferences(self) -> Dict[str, Any]:
        """Infer user preferences from conversation history"""
        
        if not self.query_history:
            return {}
        
        preferences = {
            "budget_range": self._extract_budget_range(),
            "priority_features": self._extract_features(),
            "brands_interested": self._extract_brands(),
            "comparison_history": self._extract_comparisons()
        }
        
        return preferences
    
    def _extract_budget_range(self) -> Optional[str]:
        """Extract budget mentions from queries"""
        budget_keywords = ["budget", "under", "below", "₹", "inr", "price"]
        
        for record in reversed(self.query_history):
            query_lower = record["query"].lower()
            if any(kw in query_lower for kw in budget_keywords):
                # Try to extract number
                import re
                numbers = re.findall(r'₹?\s*(\d+(?:,\d+)*)', query_lower)
                if numbers:
                    # Clean and convert
                    amount = int(numbers[0].replace(',', ''))
                    return f"Under ₹{amount:,}"
        
        return None
    
    def _extract_features(self) -> List[str]:
        """Extract feature priorities from queries"""
        feature_keywords = {
            "camera": ["camera", "photography", "photo", "video"],
            "battery": ["battery", "charging", "power"],
            "performance": ["performance", "speed", "processor", "gaming"],
            "display": ["display", "screen", "amoled"],
            "storage": ["storage", "memory", "gb"]
        }
        
        mentioned_features = set()
        
        for record in self.query_history:
            query_lower = record["query"].lower()
            for feature, keywords in feature_keywords.items():
                if any(kw in query_lower for kw in keywords):
                    mentioned_features.add(feature)
        
        return list(mentioned_features)
    
    def _extract_brands(self) -> List[str]:
        """Extract brand interests from queries"""
        brands = ["samsung", "apple", "iphone", "oneplus", "google", "pixel", "xiaomi"]
        
        mentioned_brands = set()
        
        for record in self.query_history:
            query_lower = record["query"].lower()
            for brand in brands:
                if brand in query_lower:
                    mentioned_brands.add(brand.title())
        
        return list(mentioned_brands)
    
    def _extract_comparisons(self) -> List[Dict[str, str]]:
        """Extract phone comparisons from history"""
        comparisons = []
        
        for record in self.query_history:
            if "compare_specs" in record["tools_called"]:
                # This was a comparison query
                comparisons.append({
                    "query": record["query"],
                    "timestamp": record["timestamp"]
                })
        
        return comparisons[-3:]  # Last 3 comparisons
    
    def get_conversation_theme(self) -> str:
        """Identify the overall conversation theme"""
        
        if not self.query_history:
            return "initial_exploration"
        
        # Check for patterns
        tool_counts = defaultdict(int)
        for record in self.query_history:
            for tool in record["tools_called"]:
                tool_counts[tool] += 1
        
        # Determine theme
        if tool_counts.get("compare_specs", 0) >= 2:
            return "comparison_shopping"
        elif tool_counts.get("get_price", 0) >= 3:
            return "price_focused"
        elif tool_counts.get("get_reviews", 0) >= 2:
            return "review_research"
        elif tool_counts.get("search_devices", 0) >= 2:
            return "discovery_exploration"
        else:
            return "general_inquiry"
    
    def get_context(self) -> Dict[str, Any]:
        """Generate complete conversation context"""
        
        return {
            "session_id": self.current_session_id,
            "query_count": len(self.query_history),
            "last_3_queries": self.get_last_n_queries(3),
            "inferred_preferences": self.infer_preferences(),
            "conversation_theme": self.get_conversation_theme(),
            "tool_usage_stats": dict(self.tool_usage_stats)
        }
    
    def to_json(self) -> str:
        """Export context as JSON"""
        return json.dumps(self.get_context(), indent=2)
