# 🚀 Gadget Scout MCP Server

Intelligent context management server for Gadget Spec Scout using the Model Context Protocol (MCP).

## 🎯 What This Does

This MCP server provides **super-intelligent context** to the Gadget Scout agent by:

- **Tracking Conversation History** - Remembers what user asked before
- **Inferring Preferences** - Learns budget, features, brands from queries
- **Generating Smart Context** - Provides brilliant suggestions to the LLM
- **Managing Tool Metadata** - Rich information about each tool
- **Analytics** - Tracks tool usage patterns

## 📦 Components

### Resources (Read-Only Data)
- `gadget-scout://tools/registry` - All tools with metadata
- `gadget-scout://conversation/current` - Current conversation context
- `gadget-scout://analytics/tools` - Tool usage statistics

### Prompts (Dynamic Context Generators)
- `get_query_context(query)` - Generate smart context for a query
- `get_conversation_summary()` - Summarize conversation so far

### Tools
All 5 Gadget Scout tools exposed via MCP:
- `search_devices`
- `get_specs`
- `get_price`
- `get_reviews`
- `compare_specs`

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd gadget-scout-mcp
pip install -r requirements.txt
```

### 2. Run the Server
```bash
python server.py
```

### 3. Test with MCP Inspector
```bash
npx @modelcontextprotocol/inspector python server.py
```

## 🔧 How It Works

### Example: Smart Context Generation

**User Query**: "Which phone has better battery?"

**MCP Server Generates**:
```
🔍 QUERY ANALYSIS:
- Type: comparison (implicit)
- Missing Info: None if previous comparison exists
- User History: Last query compared Samsung S24 Ultra vs iPhone 15 Pro Max
- Conversation Theme: comparison_shopping

💡 SMART SUGGESTIONS:
1. User likely continuing previous comparison
2. Get battery specs for both phones
3. Provide direct answer with context

📊 RELEVANT DATA:
- Samsung S24 Ultra: 5000mAh
- iPhone 15 Pro Max: 4441mAh

🎯 RECOMMENDED APPROACH:
Answer directly using context from previous comparison
```

**Result**: Agent provides instant, context-aware answer without asking clarifying questions!

## 📊 Features

### Conversation Tracking
- Tracks last 10 queries
- Infers user preferences (budget, features, brands)
- Identifies conversation themes
- Provides query summaries

### Tool Registry
- Rich metadata for each tool
- Usage examples and patterns
- Success rate tracking
- Common tool sequences

### Context Generation
- Query classification
- Missing information detection
- Smart suggestions
- Relevant data extraction
- Approach recommendations

## 🎓 Usage Example

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Connect to MCP server
server_params = StdioServerParameters(
    command="python",
    args=["gadget-scout-mcp/server.py"]
)

async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
        # Initialize
        await session.initialize()
        
        # Get query context
        context = await session.call_prompt(
            "get_query_context",
            arguments={"query": "Which phone has better battery?"}
        )
        
        print(context)
```

## 📁 File Structure

```
gadget-scout-mcp/
├── server.py                 # Main MCP server
├── config.py                 # Configuration
├── requirements.txt          # Dependencies
├── resources/
│   ├── conversation.py       # Conversation tracker
│   └── tool_registry.py      # Tool metadata
└── prompts/
    └── query_context.py      # Context generator
```

## 🔍 Testing

### Test Resource Reading
```python
# Read tool registry
registry = await session.read_resource("gadget-scout://tools/registry")

# Read conversation context
context = await session.read_resource("gadget-scout://conversation/current")

# Read analytics
analytics = await session.read_resource("gadget-scout://analytics/tools")
```

### Test Prompts
```python
# Get query context
context = await session.call_prompt(
    "get_query_context",
    arguments={"query": "Best phone under 70000"}
)

# Get conversation summary
summary = await session.call_prompt("get_conversation_summary")
```

## 🎯 Next Steps

1. ✅ **Phase 1 Complete**: MCP server foundation
2. ⏳ **Phase 2**: Integrate with notebook
3. ⏳ **Phase 3**: Add advanced features (predictive loading, caching)
4. ⏳ **Phase 4**: Polish and optimize

## 📚 Resources

- [MCP Documentation](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Gadget Scout Notebook](../gadget_spec_scout_complete.ipynb)

---

**Built with ❤️ for super-intelligent agents**
