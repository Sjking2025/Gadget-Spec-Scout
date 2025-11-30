"""
Tool Registry - Manages tool metadata and usage patterns
"""

from typing import List, Dict, Any
import json


class ToolRegistry:
    """Central registry for all tools with rich metadata"""
    
    def __init__(self):
        self.tools = self._initialize_tools()
        self.tool_stats = {tool["name"]: {"calls": 0, "successes": 0, "failures": 0} 
                          for tool in self.tools}
    
    def _initialize_tools(self) -> List[Dict[str, Any]]:
        """Initialize tool metadata"""
        
        return [
            {
                "name": "search_devices",
                "description": "Search smartphone database by name, brand, or features",
                "category": "discovery",
                "when_to_use": [
                    "User asks for recommendations",
                    "User mentions budget or specific features",
                    "User wants to explore options",
                    "User asks 'what phones...' or 'show me...'"
                ],
                "example_queries": [
                    "Best phone under ₹70,000",
                    "Phones with good camera",
                    "Show me Samsung phones",
                    "What phones have 5000mAh battery?"
                ],
                "typical_next_tools": ["get_specs", "get_price", "get_reviews"],
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query (brand, model, or keywords)"
                        }
                    },
                    "required": ["query"]
                },
                "output_format": "List of matching device names",
                "avg_execution_time_ms": 12,
                "cost": "low"
            },
            {
                "name": "get_specs",
                "description": "Get detailed technical specifications for a specific device",
                "category": "information",
                "when_to_use": [
                    "User asks about specific phone features",
                    "User wants technical details",
                    "After search_devices to get details",
                    "For comparison preparation"
                ],
                "example_queries": [
                    "What are the specs of Samsung S24 Ultra?",
                    "Tell me about iPhone 15 Pro Max camera",
                    "How much RAM does OnePlus 12 have?"
                ],
                "typical_next_tools": ["get_price", "get_reviews", "compare_specs"],
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "device_name": {
                            "type": "string",
                            "description": "Exact device name"
                        }
                    },
                    "required": ["device_name"]
                },
                "output_format": "Device specifications (processor, RAM, camera, etc.)",
                "avg_execution_time_ms": 8,
                "cost": "low"
            },
            {
                "name": "get_price",
                "description": "Get pricing information from multiple retailers (Amazon, Flipkart, Croma)",
                "category": "pricing",
                "when_to_use": [
                    "User asks about price",
                    "User mentions budget",
                    "User wants to know cheapest option",
                    "For value comparison"
                ],
                "example_queries": [
                    "How much does iPhone 15 Pro Max cost?",
                    "What's the cheapest place to buy Samsung S24?",
                    "Price of OnePlus 12?",
                    "Where can I get the best deal?"
                ],
                "typical_next_tools": ["get_reviews", "compare_specs"],
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "device_name": {
                            "type": "string",
                            "description": "Exact device name"
                        }
                    },
                    "required": ["device_name"]
                },
                "output_format": "Prices from Amazon, Flipkart, Croma with lowest price highlighted",
                "avg_execution_time_ms": 10,
                "cost": "low"
            },
            {
                "name": "get_reviews",
                "description": "Get aggregated user reviews, ratings, pros and cons",
                "category": "social_proof",
                "when_to_use": [
                    "User asks about user opinions",
                    "User wants to know pros/cons",
                    "User asks 'is it good?'",
                    "For final decision validation"
                ],
                "example_queries": [
                    "What do users say about Samsung S24 Ultra?",
                    "Is iPhone 15 Pro Max worth it?",
                    "Pros and cons of OnePlus 12?",
                    "User reviews for Pixel 8 Pro?"
                ],
                "typical_next_tools": ["get_price", "compare_specs"],
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "device_name": {
                            "type": "string",
                            "description": "Exact device name"
                        }
                    },
                    "required": ["device_name"]
                },
                "output_format": "Rating, review count, pros list, cons list",
                "avg_execution_time_ms": 15,
                "cost": "low"
            },
            {
                "name": "compare_specs",
                "description": "Side-by-side comparison of two devices",
                "category": "comparison",
                "when_to_use": [
                    "User explicitly asks to compare",
                    "User mentions 'vs' or 'versus'",
                    "User asks 'which is better'",
                    "User is deciding between two phones"
                ],
                "example_queries": [
                    "Compare Samsung S24 Ultra and iPhone 15 Pro Max",
                    "Samsung vs iPhone for photography",
                    "Which is better: OnePlus 12 or Xiaomi 14?",
                    "Pixel 8 Pro vs iPhone 15 Pro Max"
                ],
                "typical_next_tools": ["get_price", "get_reviews"],
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "device1": {
                            "type": "string",
                            "description": "First device name"
                        },
                        "device2": {
                            "type": "string",
                            "description": "Second device name"
                        }
                    },
                    "required": ["device1", "device2"]
                },
                "output_format": "Side-by-side spec comparison for all features",
                "avg_execution_time_ms": 18,
                "cost": "low"
            }
        ]
    
    def get_tool(self, name: str) -> Dict[str, Any]:
        """Get tool metadata by name"""
        for tool in self.tools:
            if tool["name"] == name:
                return tool
        return None
    
    def get_all_tools(self) -> List[Dict[str, Any]]:
        """Get all tools"""
        return self.tools
    
    def record_tool_call(self, tool_name: str, success: bool):
        """Record a tool call for analytics"""
        if tool_name in self.tool_stats:
            self.tool_stats[tool_name]["calls"] += 1
            if success:
                self.tool_stats[tool_name]["successes"] += 1
            else:
                self.tool_stats[tool_name]["failures"] += 1
    
    def get_success_rate(self, tool_name: str) -> float:
        """Get success rate for a tool"""
        stats = self.tool_stats.get(tool_name, {})
        calls = stats.get("calls", 0)
        if calls == 0:
            return 0.0
        successes = stats.get("successes", 0)
        return successes / calls
    
    def get_most_used_tools(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get most frequently used tools"""
        sorted_tools = sorted(
            self.tool_stats.items(),
            key=lambda x: x[1]["calls"],
            reverse=True
        )
        
        return [
            {
                "tool": name,
                "calls": stats["calls"],
                "success_rate": self.get_success_rate(name)
            }
            for name, stats in sorted_tools[:limit]
        ]
    
    def get_common_sequences(self) -> List[List[str]]:
        """Get common tool call sequences (placeholder for now)"""
        # This would analyze actual usage patterns
        # For now, return typical sequences based on tool metadata
        return [
            ["search_devices", "get_specs", "get_price"],
            ["search_devices", "get_price", "get_reviews"],
            ["compare_specs", "get_price", "get_reviews"],
            ["get_specs", "get_reviews"],
            ["search_devices", "compare_specs"]
        ]
    
    def to_json(self) -> str:
        """Export registry as JSON"""
        return json.dumps({
            "tools": self.tools,
            "stats": self.tool_stats,
            "most_used": self.get_most_used_tools(),
            "common_sequences": self.get_common_sequences()
        }, indent=2)
