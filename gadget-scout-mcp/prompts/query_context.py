"""
Query Context Generator - Creates brilliant context for each query
"""

from typing import Dict, Any, List
import re


class QueryContextGenerator:
    """Generates intelligent, query-specific context for the LLM"""
    
    def __init__(self, conversation_tracker, tool_registry):
        self.conversation = conversation_tracker
        self.tools = tool_registry
    
    def generate_context(self, query: str) -> str:
        """Generate brilliant context for the current query"""
        
        # Analyze the query
        query_type = self._classify_query(query)
        missing_info = self._identify_missing_info(query)
        
        # Get conversation history
        history = self.conversation.get_context()
        
        # Generate smart suggestions
        suggestions = self._generate_suggestions(query, query_type, history)
        
        # Get relevant data
        relevant_data = self._get_relevant_data(query, history)
        
        # Recommend approach
        approach = self._recommend_approach(query, query_type, history)
        
        # Build context
        context = f"""
🔍 QUERY ANALYSIS:
- Type: {query_type}
- Missing Info: {missing_info or "None - query is complete"}
- User History: {self._summarize_history(history)}
- Conversation Theme: {history.get('conversation_theme', 'initial_exploration')}

💡 SMART SUGGESTIONS:
{suggestions}

📊 RELEVANT DATA:
{relevant_data}

🎯 RECOMMENDED APPROACH:
{approach}
"""
        return context.strip()
    
    def _classify_query(self, query: str) -> str:
        """Classify the query type"""
        query_lower = query.lower()
        
        # Comparison
        if any(word in query_lower for word in ["compare", "vs", "versus", "which is better", "difference between"]):
            return "comparison"
        
        # Recommendation
        if any(word in query_lower for word in ["best", "recommend", "suggest", "should i", "which phone"]):
            return "recommendation"
        
        # Specific info
        if any(word in query_lower for word in ["what is", "tell me about", "specs", "price", "cost", "review"]):
            return "specific_information"
        
        # Budget search
        if any(word in query_lower for word in ["under", "below", "budget", "₹", "inr"]):
            return "budget_search"
        
        # Feature search
        if any(word in query_lower for word in ["camera", "battery", "performance", "display"]):
            return "feature_search"
        
        return "general_inquiry"
    
    def _identify_missing_info(self, query: str) -> str:
        """Identify what information is missing from the query"""
        query_lower = query.lower()
        missing = []
        
        # Check for comparison without phone names
        if "compare" in query_lower or "vs" in query_lower:
            # Check if we have phone names
            phones = self._extract_phone_names(query)
            if len(phones) < 2:
                missing.append("Need two phone names to compare")
        
        # Check for vague "better" questions
        if "better" in query_lower and not any(word in query_lower for word in ["camera", "battery", "performance", "price"]):
            # Check if context provides the phones
            history = self.conversation.get_context()
            last_queries = history.get("last_3_queries", [])
            if not last_queries:
                missing.append("Need to know which phones to compare")
        
        # Check for budget without amount
        if "budget" in query_lower and not re.search(r'\d+', query):
            missing.append("Budget amount not specified")
        
        return "; ".join(missing) if missing else None
    
    def _extract_phone_names(self, query: str) -> List[str]:
        """Extract phone names from query"""
        # Simple extraction - look for known brands/models
        known_phones = [
            "samsung galaxy s24 ultra", "samsung s24 ultra", "s24 ultra",
            "iphone 15 pro max", "iphone 15", "iphone",
            "oneplus 12", "oneplus",
            "pixel 8 pro", "pixel",
            "xiaomi 14", "xiaomi"
        ]
        
        found = []
        query_lower = query.lower()
        for phone in known_phones:
            if phone in query_lower:
                found.append(phone)
        
        return found
    
    def _summarize_history(self, history: Dict[str, Any]) -> str:
        """Summarize conversation history"""
        query_count = history.get("query_count", 0)
        
        if query_count == 0:
            return "This is the first query"
        
        last_queries = history.get("last_3_queries", [])
        if not last_queries:
            return f"{query_count} queries so far"
        
        # Summarize last query
        last = last_queries[-1]
        summary = f"Last query was about: {last['query'][:50]}..."
        
        return summary
    
    def _generate_suggestions(self, query: str, query_type: str, history: Dict[str, Any]) -> str:
        """Generate smart suggestions based on query and history"""
        
        suggestions = []
        
        if query_type == "comparison":
            phones = self._extract_phone_names(query)
            if len(phones) >= 2:
                suggestions.append(f"1. Call compare_specs('{phones[0]}', '{phones[1]}')")
                suggestions.append(f"2. Call get_price for both to show price difference")
                suggestions.append(f"3. Call get_reviews for both to validate with user feedback")
            else:
                # Check history for context
                last_queries = history.get("last_3_queries", [])
                if last_queries:
                    suggestions.append("1. User might be referring to previously discussed phones")
                    suggestions.append("2. Ask clarifying question OR use context to infer phones")
        
        elif query_type == "recommendation":
            suggestions.append("1. Call search_devices to find matching phones")
            suggestions.append("2. Get specs, prices, and reviews for top matches")
            suggestions.append("3. Suggest 2-3 best options with clear reasoning")
        
        elif query_type == "budget_search":
            suggestions.append("1. Extract budget amount from query")
            suggestions.append("2. Call search_devices to find phones")
            suggestions.append("3. Filter by price using get_price")
            suggestions.append("4. Recommend best value options")
        
        else:
            suggestions.append("1. Understand user intent")
            suggestions.append("2. Call appropriate tools")
            suggestions.append("3. Provide helpful, conversational response")
        
        return "\n".join(suggestions) if suggestions else "No specific suggestions"
    
    def _get_relevant_data(self, query: str, history: Dict[str, Any]) -> str:
        """Get relevant data from history or database"""
        
        # Check if query mentions phones from history
        prefs = history.get("inferred_preferences", {})
        brands = prefs.get("brands_interested", [])
        
        if brands:
            return f"User has shown interest in: {', '.join(brands)}"
        
        # Check for budget
        budget = prefs.get("budget_range")
        if budget:
            return f"User's budget range: {budget}"
        
        return "No specific relevant data from history"
    
    def _recommend_approach(self, query: str, query_type: str, history: Dict[str, Any]) -> str:
        """Recommend the best approach for this query"""
        
        if query_type == "comparison":
            phones = self._extract_phone_names(query)
            if len(phones) >= 2:
                return f"Directly compare {phones[0]} and {phones[1]} using compare_specs, then enhance with pricing and reviews"
            else:
                last_queries = history.get("last_3_queries", [])
                if last_queries and "compare" in last_queries[-1].get("query", "").lower():
                    return "User is likely continuing previous comparison - use context to infer phones"
                else:
                    return "Ask clarifying question: 'Which phones would you like me to compare?'"
        
        elif query_type == "recommendation":
            return "Search database for matches, get full details (specs/price/reviews), then provide 2-3 personalized recommendations with reasoning"
        
        elif query_type == "budget_search":
            return "Filter phones by budget, rank by value (specs vs price), highlight best deals"
        
        else:
            return "Provide helpful, conversational response using appropriate tools"
