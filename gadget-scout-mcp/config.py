# MCP Server Configuration

# Server Info
SERVER_NAME = "gadget-scout-mcp"
SERVER_VERSION = "1.0.0"
SERVER_DESCRIPTION = "Intelligent context management for Gadget Spec Scout"

# Database
SMARTPHONE_DB_PATH = "../smartphone_db.json"  # Will be created from notebook data

# Conversation Settings
MAX_HISTORY_LENGTH = 10  # Keep last 10 queries in context
CONTEXT_WINDOW_SIZE = 3  # Show last 3 queries in summaries

# Analytics
ENABLE_ANALYTICS = True
ANALYTICS_DB_PATH = "./analytics.db"

# Tool Metadata
TOOL_METADATA_PATH = "./tools/tool_metadata.json"

# Logging
LOG_LEVEL = "INFO"
LOG_FILE = "./mcp_server.log"
