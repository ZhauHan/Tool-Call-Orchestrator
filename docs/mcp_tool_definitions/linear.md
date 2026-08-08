4. LINEAR (25 tools)
   Server: linear | smithery.ai/server/linear
================================================================================

list_comments
  Description: List comments for a specific Linear issue
  Parameters:
    - issueId (string, required): The issue ID

create_comment
  Description: Create a comment on a specific Linear issue
  Parameters:
    - body (string, required): The content of the comment as Markdown
    - issueId (string, required): The issue ID
    - parentId (string, optional): A parent comment ID to reply to

list_cycles
  Description: Retrieve cycles for a specific Linear team
  Parameters:
    - type (enum, optional): "current", "previous", "next", or all cycles
    - teamId (string, required): The team ID

get_document
  Description: Retrieve a Linear document by ID or slug
  Parameters:
    - id (string, required): The document ID or slug

list_documents
  Description: List documents in the user's Linear workspace
  Parameters:
    - after (string, optional): Pagination cursor (after)
    - before (string, optional): Pagination cursor (before)
    - limit (number, optional, default 50, max 250): Results to return
    - query (string, optional): Search query
    - orderBy (enum, optional, default "updatedAt"): "createdAt" or "updatedAt"
    - createdAt (string, optional): ISO-8601 datetime or duration filter
    - updatedAt (string, optional): ISO-8601 datetime or duration filter
    - creatorId (string, optional): Filter by creator ID
    - projectId (string, optional): Filter by project ID
    - initiativeId (string, optional): Filter by initiative ID
    - includeArchived (boolean, optional, default false): Include archived documents

create_document
  Description: Create a new document in Linear
  Parameters:
    - title (string, required): The title
    - content (string, optional): Markdown content
    - icon (string, optional): Icon emoji
    - color (string, optional): Hex color code
    - project (string, optional): Project name or ID

update_document
  Description: Update an existing Linear document
  Parameters:
    - id (string, required): Document ID
    - title (string, optional): Updated title
    - content (string, optional): Updated Markdown content
    - icon (string, optional): Updated icon emoji
    - color (string, optional): Updated hex color code
    - project (string, optional): Updated project name or ID

get_issue
  Description: Retrieve detailed information about an issue by ID
  Parameters:
    - id (string, required): The issue ID
    - includeRelations (boolean, optional, default false): Include blocking/related/duplicate relations

list_issues
  Description: List issues in the user's Linear workspace. Use 'me' for personal issues
  Parameters:
    - team (string, optional): Team name or ID filter
    - cycle (string, optional): Cycle filter
    - label (string, optional): Label filter
    - state (string, optional): State filter
    - project (string, optional): Project filter
    - assignee (string, optional): Assignee filter
    - delegate (string, optional): Delegate filter
    - parentId (string, optional): Filter by parent issue
    - after (string, optional): Pagination cursor (after)
    - before (string, optional): Pagination cursor (before)
    - limit (number, optional, default 50, max 250): Results to return
    - query (string, optional): Search title/description
    - orderBy (enum, optional, default "updatedAt"): "createdAt" or "updatedAt"
    - createdAt (string, optional): Time filter
    - updatedAt (string, optional): Time filter
    - includeArchived (boolean, optional, default true): Include archived issues

create_issue
  Description: Create a new Linear issue
  Parameters:
    - title (string, required): Issue title
    - team (string, required): Team name or ID
    - description (string, optional): Markdown description
    - state (string, optional): Issue state
    - assignee (string, optional): Assignee
    - delegate (string, optional): Delegate
    - cycle (string, optional): Cycle
    - project (string, optional): Project
    - milestone (string, optional): Milestone
    - parentId (string, optional): Parent issue ID (for sub-issues)
    - priority (number, optional): 0-4 scale
    - dueDate (string, optional): ISO format date
    - labels (array, optional): Label names or IDs
    - links (array, optional): Objects with url and title
    - blocks (array, optional): Issue IDs this blocks
    - blockedBy (array, optional): Issue IDs blocking this
    - relatedTo (array, optional): Related issue IDs
    - duplicateOf (string, optional): Duplicate relation

update_issue
  Description: Update an existing Linear issue
  Parameters:
    - id (string, required): Issue ID
    - (All fields from create_issue are optional for updates)
    - Note: blocks, blockedBy, relatedTo REPLACE existing relations
    - duplicateOf (string|null, optional): Replace or remove duplicate relation

list_issue_statuses
  Description: List available issue statuses in a Linear team
  Parameters:
    - team (string, required): Team name or ID

get_issue_status
  Description: Retrieve detailed information about an issue status
  Parameters:
    - id (string, optional): Status ID
    - name (string, optional): Status name
    - team (string, optional): Team name or ID

list_issue_labels
  Description: List available issue labels in workspace or team
  Parameters:
    - name (string, optional): Filter by label name
    - team (string, optional): Team name or ID
    - after (string, optional): Pagination cursor
    - before (string, optional): Pagination cursor
    - limit (number, optional, default 50, max 250): Results
    - orderBy (enum, optional, default "updatedAt"): "createdAt" or "updatedAt"

create_issue_label
  Description: Create a new Linear issue label
  Parameters:
    - name (string, required): Label name
    - color (string, optional): Hex color code
    - teamId (string, optional): Team UUID; omit for workspace label
    - isGroup (boolean, optional, default false): Label group flag
    - parentId (string, optional): Parent label UUID for child labels
    - description (string, optional): Label description

list_projects
  Description: List projects in the user's Linear workspace
  Parameters:
    - team (string, optional): Team filter
    - state (string, optional): State filter
    - member (string, optional): Member filter
    - initiative (string, optional): Initiative filter
    - after (string, optional): Pagination cursor
    - before (string, optional): Pagination cursor
    - limit (number, optional, default 50, max 250): Results
    - query (string, optional): Search project names
    - orderBy (enum, optional, default "updatedAt"): "createdAt" or "updatedAt"
    - createdAt (string, optional): Time filter
    - updatedAt (string, optional): Time filter
    - includeArchived (boolean, optional, default false): Include archived

get_project
  Description: Retrieve details of a specific project in Linear
  Parameters:
    - query (string, required): Project ID or name

create_project
  Description: Create a new project in Linear
  Parameters:
    - name (string, required): Project name
    - team (string, required): Team name or ID
    - lead (string, optional): User ID, name, email, or "me"
    - summary (string, optional): Plaintext summary (max 255 chars)
    - description (string, optional): Markdown description
    - state (string, optional): Project state
    - priority (integer, optional, 0-4): Priority level
    - icon (string, optional): Icon emoji
    - color (string, optional): Hex color
    - labels (array, optional): Label names or IDs
    - startDate (string, optional): ISO format date
    - targetDate (string, optional): ISO format date
    - initiative (string, optional): Initiative ID or name

update_project
  Description: Update an existing Linear project
  Parameters:
    - id (string, required): Project ID
    - (All create_project fields optional except id)
    - initiatives (array, optional): Initiative IDs or names (replaces existing)

list_project_labels
  Description: List available project labels in the Linear workspace
  Parameters:
    - name (string, optional): Filter by label name
    - after (string, optional): Pagination cursor
    - before (string, optional): Pagination cursor
    - limit (number, optional, default 50, max 250): Results
    - orderBy (enum, optional, default "updatedAt"): "createdAt" or "updatedAt"

list_teams
  Description: List teams in the user's Linear workspace
  Parameters:
    - after (string, optional): Pagination cursor
    - before (string, optional): Pagination cursor
    - limit (number, optional, default 50, max 250): Results
    - query (string, optional): Search query
    - orderBy (enum, optional, default "updatedAt"): "createdAt" or "updatedAt"
    - createdAt (string, optional): Time filter
    - updatedAt (string, optional): Time filter
    - includeArchived (boolean, optional, default false): Include archived

get_team
  Description: Retrieve details of a specific Linear team
  Parameters:
    - query (string, required): Team UUID, key, or name

list_users
  Description: Retrieve users in the Linear workspace
  Parameters:
    - team (string, optional): Team name or ID for filtering members
    - query (string, optional): Filter users by name or email

get_user
  Description: Retrieve details of a specific Linear user
  Parameters:
    - query (string, required): User ID, name, email, or "me"

search_documentation
  Description: Search Linear's documentation to learn about features and usage
  Parameters:
    - query (string, required): Search query
    - page (number, optional, default 0): Page number


================================================================================
