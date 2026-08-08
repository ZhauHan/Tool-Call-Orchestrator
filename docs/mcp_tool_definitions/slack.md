3. SLACK (10 tools)
   Server: jtalk22/slack-mcp-server | smithery.ai/server/jtalk22/slack-mcp-server
================================================================================

slack_token_status
  Description: Check token health, age, and auto-refresh status
  Parameters: (none)

slack_health_check
  Description: Check if Slack API connection is working and show workspace info
  Parameters: (none)

slack_list_conversations
  Description: List all DMs and channels with user names resolved
  Parameters:
    - limit (number): Max results (default 100)
    - types (string): Comma-separated: public_channel,private_channel,mpim,im
    - discover_dms (boolean): Actively discover all DMs (slower but complete)

slack_conversations_history
  Description: Get messages from a channel or DM with user names resolved
  Parameters:
    - limit (number): Messages to fetch (max 100, default 50)
    - latest (string): Unix timestamp - get messages before this time
    - oldest (string): Unix timestamp - get messages after this time
    - channel (string): Channel or DM ID (e.g., D063M4403MW)

slack_get_full_conversation
  Description: Export full conversation history with all messages, threads, and user names
  Parameters:
    - latest (string): Unix timestamp end
    - oldest (string): Unix timestamp start
    - channel (string): Channel or DM ID
    - max_messages (number): Maximum messages (default 2000, max 10000)
    - include_threads (boolean): Fetch thread replies (default true)

slack_search_messages
  Description: Search messages across the Slack workspace
  Parameters:
    - count (number): Number of results (max 100, default 20)
    - query (string): Search query (supports from:@user, in:#channel)

slack_send_message
  Description: Send a message to a channel or DM
  Parameters:
    - text (string): Message text (supports Slack markdown)
    - channel (string): Channel or DM ID to send to
    - thread_ts (string): Thread timestamp to reply to (optional)

slack_get_thread
  Description: Get all replies in a message thread
  Parameters:
    - channel (string): Channel or DM ID
    - thread_ts (string): Thread parent message timestamp

slack_users_info
  Description: Get detailed information about a Slack user
  Parameters:
    - user (string): Slack user ID

slack_list_users
  Description: List all users in the workspace with pagination support
  Parameters:
    - limit (number): Maximum users to return (default 500)


================================================================================
