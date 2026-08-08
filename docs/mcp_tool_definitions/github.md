6. GITHUB (86 tools)
   Server: github | smithery.ai/server/github
================================================================================

--- Actions Management ---

actions_get
  Description: Retrieves details about GitHub Actions resources (workflows, runs, jobs, artifacts)
  Parameters:
    - repo (string): Repository name
    - owner (string): Repository owner
    - method (string): get_workflow, get_workflow_run, get_workflow_job, download_workflow_run_artifact, get_workflow_run_usage, get_workflow_run_logs_url
    - resource_id (string): Resource identifier

actions_list
  Description: Lists GitHub Actions resources with filtering and pagination
  Parameters:
    - repo (string): Repository name
    - owner (string): Repository owner
    - method (string): list_workflows, list_workflow_runs, list_workflow_jobs, list_workflow_run_artifacts
    - resource_id (string): Resource identifier
    - page (integer): Page number
    - per_page (integer): Results per page
    - workflow_jobs_filter (string): Filter for workflow jobs
    - workflow_runs_filter (string): Filter for workflow runs

actions_run_trigger
  Description: Executes workflow operations (run, rerun, cancel, delete logs)
  Parameters:
    - repo (string): Repository name
    - owner (string): Repository owner
    - workflow_id (string): Workflow identifier
    - ref (string): Git reference (branch/tag)
    - run_id (string): Run identifier
    - inputs (object): Workflow inputs
    - method (string): run_workflow, rerun_workflow_run, rerun_failed_jobs, cancel_workflow_run, delete_workflow_run_logs

--- Pull Request Operations ---

add_comment_to_pending_review
  Description: Adds comments to existing pending PR reviews
  Parameters:
    - repo (string, required): Repository name
    - owner (string, required): Repository owner
    - pullNumber (integer, required): PR number
    - path (string, required): File path
    - line (integer, required): Line number
    - body (string, required): Comment body
    - side (string, required): "LEFT" or "RIGHT"

add_reply_to_pull_request_comment
  Description: Replies to specific PR comments
  Parameters:
    - repo (string, required): Repository name
    - owner (string, required): Repository owner
    - pullNumber (integer, required): PR number
    - commentId (integer, required): Comment ID
    - body (string, required): Reply body

create_pull_request
  Description: Creates new PRs with customizable options
  Parameters:
    - repo (string, required): Repository name
    - owner (string, required): Repository owner
    - base (string, required): Base branch
    - head (string, required): Head branch
    - title (string, required): PR title
    - body (string, optional): PR description
    - draft (boolean, optional): Create as draft
    - maintainer_can_modify (boolean, optional): Allow maintainer edits

create_pull_request_with_copilot
  Description: Delegates implementation tasks to GitHub Copilot
  Parameters:
    - repo (string, required): Repository name
    - owner (string, required): Repository owner
    - title (string, required): PR title
    - problem_statement (string, required): Task description
    - base_ref (string, optional): Base branch reference

merge_pull_request
  Description: Merges PRs with specified merge strategy
  Parameters:
    - repo (string, required): Repository name
    - owner (string, required): Repository owner
    - pullNumber (integer, required): PR number
    - merge_method (string, optional): merge, squash, or rebase
    - commit_title (string, optional): Merge commit title
    - commit_message (string, optional): Merge commit message

pull_request_read
  Description: Retrieves PR data and metadata
  Parameters:
    - repo (string, required): Repository name
    - owner (string, required): Repository owner
    - pullNumber (integer, required): PR number
    - method (string): get, get_diff, get_status, get_files, get_review_comments, get_reviews, get_comments, get_check_runs

pull_request_review_write
  Description: Creates, submits, or deletes PR reviews
  Parameters:
    - repo (string, required): Repository name
    - owner (string, required): Repository owner
    - pullNumber (integer, required): PR number
    - method (string): create, submit_pending, delete_pending

update_pull_request
  Description: Modifies existing PR properties
  Parameters:
    - repo (string, required): Repository name
    - owner (string, required): Repository owner
    - pullNumber (integer, required): PR number
    - title (string, optional): Updated title
    - body (string, optional): Updated description
    - state (string, optional): open or closed
    - base (string, optional): Updated base branch
    - draft (boolean, optional): Draft status
    - reviewers (array, optional): Reviewer usernames
    - maintainer_can_modify (boolean, optional): Allow maintainer edits

update_pull_request_branch
  Description: Syncs PR branch with base branch changes
  Parameters:
    - repo (string, required): Repository name
    - owner (string, required): Repository owner
    - pullNumber (integer, required): PR number

list_pull_requests
  Description: Lists pull requests with filtering
  Parameters:
    - repo (string, required): Repository name
    - owner (string, required): Repository owner
    - state (string, optional): open, closed, all
    - head (string, optional): Filter by head branch
    - base (string, optional): Filter by base branch
    - sort (string, optional): Sort field
    - direction (string, optional): Sort direction
    - page (integer, optional): Page number
    - perPage (integer, optional): Results per page

--- Issue Management ---

add_issue_comment
  Description: Posts comments on issues and PRs
  Parameters:
    - repo (string, required): Repository name
    - owner (string, required): Repository owner
    - issue_number (integer, required): Issue number
    - body (string, required): Comment body

assign_copilot_to_issue
  Description: Delegates issue resolution to Copilot agent
  Parameters:
    - repo (string, required): Repository name
    - owner (string, required): Repository owner
    - issue_number (integer, required): Issue number
    - base_ref (string, optional): Base branch reference
    - custom_instructions (string, optional): Custom instructions

issue_read
  Description: Retrieves issue information and related data
  Parameters:
    - repo (string, required): Repository name
    - owner (string, required): Repository owner
    - issue_number (integer, required): Issue number
    - method (string): get, get_comments, get_sub_issues, get_labels

issue_write
  Description: Creates or updates issues with metadata
  Parameters:
    - repo (string, required): Repository name
    - owner (string, required): Repository owner
    - method (string): create, update
    - title (string): Issue title
    - body (string): Issue body
    - labels (array, optional): Label names
    - assignees (array, optional): Assignee usernames
    - milestone (integer, optional): Milestone number
    - state (string, optional): open or closed
    - state_reason (string, optional): Reason for state change
    - type (string, optional): Issue type

list_issues
  Description: Lists repository issues with filtering
  Parameters:
    - repo (string, required): Repository name
    - owner (string, required): Repository owner
    - state (string, optional): open, closed, all
    - labels (string, optional): Comma-separated label names
    - sort (string, optional): Sort field
    - direction (string, optional): Sort direction
    - page (integer, optional): Page number
    - perPage (integer, optional): Results per page

sub_issue_write
  Description: Manages issue hierarchies
  Parameters:
    - repo (string, required): Repository name
    - owner (string, required): Repository owner
    - issue_number (integer, required): Parent issue number
    - method (string): add, remove, reprioritize

triage_issue
  Description: Categorizes issues with rationale and metadata
  Parameters:
    - repo (string, required): Repository name
    - owner (string, required): Repository owner
    - issue_number (integer, required): Issue number
    - triage_rationale (string, required): Rationale for categorization
    - labels (array, optional): Labels to apply
    - type (string, optional): Issue type
    - fields (object, optional): Custom fields

list_issue_types
  Description: Lists organization issue types
  Parameters:
    - owner (string, required): Organization name

--- Code and File Operations ---

create_branch
  Description: Creates repository branches
  Parameters:
    - repo (string, required): Repository name
    - owner (string, required): Repository owner
    - branch (string, required): New branch name
    - from_branch (string, optional): Source branch

create_or_update_file
  Description: Creates/modifies single files with commit control
  Parameters:
    - repo (string, required): Repository name
    - owner (string, required): Repository owner
    - path (string, required): File path
    - branch (string, required): Target branch
    - content (string, required): File content
    - message (string, required): Commit message
    - sha (string, optional): Required for updates

delete_file
  Description: Removes files from repository
  Parameters:
    - repo (string, required): Repository name
    - owner (string, required): Repository owner
    - path (string, required): File path
    - branch (string, required): Target branch
    - message (string, required): Commit message

get_file_contents
  Description: Retrieves file/directory contents
  Parameters:
    - repo (string, required): Repository name
    - owner (string, required): Repository owner
    - path (string, optional): File or directory path
    - ref (string, optional): Git reference
    - sha (string, optional): Commit SHA

get_repository_tree
  Description: Displays repository structure
  Parameters:
    - repo (string, required): Repository name
    - owner (string, required): Repository owner
    - tree_sha (string, optional): Tree SHA (default: HEAD)
    - recursive (boolean, optional): Recursive listing
    - path_filter (string, optional): Filter by path prefix

push_files
  Description: Commits multiple files in single operation
  Parameters:
    - repo (string, required): Repository name
    - owner (string, required): Repository owner
    - branch (string, required): Target branch
    - message (string, required): Commit message
    - files (array, required): Array of {path, content} objects

search_code
  Description: Searches across all repositories using GitHub syntax
  Parameters:
    - query (string, required): Search query
    - page (integer, optional): Page number
    - perPage (integer, optional): Results per page
    - sort (string, optional): Sort field
    - order (string, optional): Sort order

--- Repository Management ---

create_repository
  Description: Initializes new repositories
  Parameters:
    - name (string, required): Repository name
    - private (boolean, optional): Private repo flag
    - description (string, optional): Repo description
    - autoInit (boolean, optional): Initialize with README
    - organization (string, optional): Org owner

fork_repository
  Description: Creates repository copies
  Parameters:
    - repo (string, required): Repository name
    - owner (string, required): Repository owner
    - organization (string, optional): Target organization

star_repository
  Description: Marks repositories as favorites
  Parameters:
    - repo (string, required): Repository name
    - owner (string, required): Repository owner

unstar_repository
  Description: Removes favorite status
  Parameters:
    - repo (string, required): Repository name
    - owner (string, required): Repository owner

list_starred_repositories
  Description: Lists user's starred repositories
  Parameters:
    - sort (string, optional): Sort field
    - direction (string, optional): Sort direction
    - page (integer, optional): Page number
    - perPage (integer, optional): Results per page

get_latest_release
  Description: Retrieves most recent release
  Parameters:
    - repo (string, required): Repository name
    - owner (string, required): Repository owner

--- Notifications ---

dismiss_notification
  Description: Updates notification status
  Parameters:
    - threadID (string, required): Notification thread ID
    - state (string, required): read or done

get_notification_details
  Description: Retrieves specific notification info
  Parameters:
    - notificationID (string, required): Notification ID

list_notifications
  Description: Lists all notifications with filtering
  Parameters:
    - repo (string, optional): Repository name
    - owner (string, optional): Repository owner
    - since (string, optional): ISO timestamp filter
    - before (string, optional): ISO timestamp filter
    - filter (string, optional): Filter type
    - perPage (integer, optional): Results per page
    - page (integer, optional): Page number

manage_notification_subscription
  Description: Controls notification subscriptions
  Parameters:
    - notificationID (string, required): Notification ID
    - action (string, required): ignore, watch, or delete

manage_repository_notification_subscription
  Description: Repository-level notification control
  Parameters:
    - repo (string, required): Repository name
    - owner (string, required): Repository owner
    - action (string, required): ignore, watch, or unwatch

mark_all_notifications_read
  Description: Marks notifications as read
  Parameters:
    - repo (string, optional): Repository name
    - owner (string, optional): Repository owner
    - lastReadAt (string, optional): ISO timestamp

--- Security and Scanning ---

get_code_scanning_alert
  Description: Retrieves specific code scanning alerts
  Parameters:
    - repo (string, required): Repository name
    - owner (string, required): Repository owner
    - alertNumber (integer, required): Alert number

list_code_scanning_alerts
  Description: Lists code scanning alerts with filtering
  Parameters:
    - repo (string, required): Repository name
    - owner (string, required): Repository owner
    - ref (string, optional): Git reference
    - state (string, optional): Alert state
    - severity (string, optional): Severity level
    - tool_name (string, optional): Tool name filter

get_dependabot_alert
  Description: Retrieves dependency vulnerability alerts
  Parameters:
    - repo (string, required): Repository name
    - owner (string, required): Repository owner
    - alertNumber (integer, required): Alert number

list_dependabot_alerts
  Description: Lists dependency alerts with filtering
  Parameters:
    - repo (string, required): Repository name
    - owner (string, required): Repository owner
    - state (string, optional): Alert state
    - severity (string, optional): Severity level

get_secret_scanning_alert
  Description: Retrieves exposed credential alerts
  Parameters:
    - repo (string, required): Repository name
    - owner (string, required): Repository owner
    - alertNumber (integer, required): Alert number

list_secret_scanning_alerts
  Description: Lists secret detection alerts
  Parameters:
    - repo (string, required): Repository name
    - owner (string, required): Repository owner
    - state (string, optional): Alert state
    - resolution (string, optional): Resolution status
    - secret_type (string, optional): Secret type filter

run_secret_scanning
  Description: Scans files for exposed credentials
  Parameters:
    - repo (string, required): Repository name
    - owner (string, required): Repository owner
    - files (array, required): Array of file content objects

--- Releases and Tags ---

get_release_by_tag
  Description: Retrieves specific release by tag
  Parameters:
    - repo (string, required): Repository name
    - owner (string, required): Repository owner
    - tag (string, required): Tag name

list_releases
  Description: Lists repository releases with pagination
  Parameters:
    - repo (string, required): Repository name
    - owner (string, required): Repository owner
    - page (integer, optional): Page number
    - perPage (integer, optional): Results per page

get_tag
  Description: Retrieves tag information
  Parameters:
    - repo (string, required): Repository name
    - owner (string, required): Repository owner
    - tag (string, required): Tag name

list_tags
  Description: Lists repository tags
  Parameters:
    - repo (string, required): Repository name
    - owner (string, required): Repository owner
    - page (integer, optional): Page number
    - perPage (integer, optional): Results per page

--- Commits and History ---

get_commit
  Description: Retrieves commit details and diffs
  Parameters:
    - repo (string, required): Repository name
    - owner (string, required): Repository owner
    - sha (string, required): Commit SHA
    - include_diff (boolean, optional): Include diff
    - page (integer, optional): Page number
    - perPage (integer, optional): Results per page

list_commits
  Description: Lists commits with filtering options
  Parameters:
    - repo (string, required): Repository name
    - owner (string, required): Repository owner
    - sha (string, optional): Branch/tag/SHA
    - author (string, optional): Author filter
    - page (integer, optional): Page number
    - perPage (integer, optional): Results per page

--- Discussions ---

get_discussion
  Description: Retrieves specific discussion
  Parameters:
    - repo (string, required): Repository name
    - owner (string, required): Repository owner
    - discussionNumber (integer, required): Discussion number

get_discussion_comments
  Description: Retrieves discussion replies
  Parameters:
    - repo (string, required): Repository name
    - owner (string, required): Repository owner
    - discussionNumber (integer, required): Discussion number
    - after (string, optional): Pagination cursor
    - perPage (integer, optional): Results per page

list_discussions
  Description: Lists discussions with filtering
  Parameters:
    - repo (string, optional): Repository name
    - owner (string, optional): Repository owner
    - category (string, optional): Category filter
    - orderBy (string, optional): Sort field
    - direction (string, optional): Sort direction
    - perPage (integer, optional): Results per page
    - after (string, optional): Pagination cursor

list_discussion_categories
  Description: Lists discussion categories
  Parameters:
    - repo (string, required): Repository name
    - owner (string, required): Repository owner

--- Gists ---

create_gist
  Description: Creates code snippets/gists
  Parameters:
    - content (string, required): Gist content
    - filename (string, required): File name
    - description (string, optional): Gist description
    - public (boolean, optional): Public visibility

get_gist
  Description: Retrieves gist content
  Parameters:
    - gist_id (string, required): Gist identifier

list_gists
  Description: Lists user gists
  Parameters:
    - username (string, optional): GitHub username
    - since (string, optional): ISO timestamp filter
    - perPage (integer, optional): Results per page
    - page (integer, optional): Page number

update_gist
  Description: Modifies existing gist
  Parameters:
    - gist_id (string, required): Gist identifier
    - filename (string, required): File name
    - content (string, required): Updated content
    - description (string, optional): Updated description

--- Search ---

search_issues
  Description: Finds issues using GitHub syntax
  Parameters:
    - repo (string, optional): Repository name
    - owner (string, optional): Repository owner
    - query (string, optional): Search query
    - sort (string, optional): Sort field
    - order (string, optional): Sort order
    - page (integer, optional): Page number
    - perPage (integer, optional): Results per page

search_pull_requests
  Description: Searches PRs with filtering
  Parameters:
    - repo (string, optional): Repository name
    - owner (string, optional): Repository owner
    - query (string, optional): Search query
    - sort (string, optional): Sort field
    - order (string, optional): Sort order
    - page (integer, optional): Page number
    - perPage (integer, optional): Results per page

search_repositories
  Description: Discovers repositories
  Parameters:
    - query (string, required): Search query
    - sort (string, optional): Sort field
    - order (string, optional): Sort order
    - page (integer, optional): Page number
    - perPage (integer, optional): Results per page
    - minimal_output (boolean, optional): Minimal output flag

search_users
  Description: Locates GitHub users
  Parameters:
    - query (string, required): Search query
    - sort (string, optional): Sort field
    - order (string, optional): Sort order
    - page (integer, optional): Page number
    - perPage (integer, optional): Results per page

search_orgs
  Description: Finds organizations
  Parameters:
    - query (string, required): Search query
    - sort (string, optional): Sort field
    - order (string, optional): Sort order
    - page (integer, optional): Page number
    - perPage (integer, optional): Results per page

--- Labels ---

get_label
  Description: Retrieves label properties
  Parameters:
    - repo (string, required): Repository name
    - owner (string, required): Repository owner
    - name (string, required): Label name

list_label
  Description: Lists repository labels
  Parameters:
    - repo (string, required): Repository name
    - owner (string, required): Repository owner

label_write
  Description: Creates/modifies/deletes labels
  Parameters:
    - repo (string, required): Repository name
    - owner (string, required): Repository owner
    - method (string): create, update, delete
    - name (string, required): Label name
    - color (string, optional): Label color
    - description (string, optional): Label description
    - new_name (string, optional): Renamed label name

--- Security Advisories ---

get_global_security_advisory
  Description: Retrieves security advisory
  Parameters:
    - ghsaId (string, required): GHSA identifier

list_global_security_advisories
  Description: Lists security advisories with filtering
  Parameters:
    - ghsaId (string, optional): GHSA identifier
    - cveId (string, optional): CVE identifier
    - cwes (array, optional): CWE identifiers
    - ecosystem (string, optional): Package ecosystem
    - severity (string, optional): Severity level

list_repository_security_advisories
  Description: Lists repo-specific advisories
  Parameters:
    - repo (string, required): Repository name
    - owner (string, required): Repository owner
    - sort (string, optional): Sort field
    - state (string, optional): Advisory state
    - direction (string, optional): Sort direction

list_org_repository_security_advisories
  Description: Lists organizational advisories
  Parameters:
    - org (string, required): Organization name
    - sort (string, optional): Sort field
    - state (string, optional): Advisory state
    - direction (string, optional): Sort direction

--- Projects ---

projects_get
  Description: Retrieves project resources
  Parameters:
    - repo (string): Repository name
    - owner (string): Repository owner
    - method (string): get_project, get_project_field, get_project_item, get_project_status_update

projects_list
  Description: Lists project resources with filtering
  Parameters:
    - repo (string): Repository name
    - owner (string): Repository owner
    - method (string): list_projects, list_project_fields, list_project_items, list_project_status_updates

projects_write
  Description: Modifies project items/status
  Parameters:
    - repo (string): Repository name
    - owner (string): Repository owner
    - method (string): add_project_item, update_project_item, delete_project_item, create_project_status_update

--- User and Organization ---

get_me
  Description: Retrieves authenticated user profile
  Parameters: (none)

get_teams
  Description: Retrieves user team memberships
  Parameters:
    - user (string, optional): GitHub username

get_team_members
  Description: Lists team member usernames
  Parameters:
    - org (string, required): Organization name
    - team_slug (string, required): Team slug

list_branches
  Description: Lists repository branches
  Parameters:
    - repo (string, required): Repository name
    - owner (string, required): Repository owner
    - page (integer, optional): Page number
    - perPage (integer, optional): Results per page

--- Copilot ---

get_copilot_job_status
  Description: Monitors Copilot task progress
  Parameters:
    - id (string, required): Job ID
    - repo (string, required): Repository name
    - owner (string, required): Repository owner

get_copilot_space
  Description: Provides context from Copilot spaces
  Parameters:
    - name (string, required): Space name
    - owner (string, required): Organization owner

list_copilot_spaces
  Description: Lists accessible spaces
  Parameters: (none)

request_copilot_review
  Description: Requests automated PR review
  Parameters:
    - repo (string, required): Repository name
    - owner (string, required): Repository owner
    - pullNumber (integer, required): PR number

--- Miscellaneous ---

get_job_logs
  Description: Retrieves logs for a workflow job
  Parameters:
    - repo (string, required): Repository name
    - owner (string, required): Repository owner
    - job_id (integer, required): Job ID

github_support_docs_search
  Description: Searches GitHub documentation
  Parameters:
    - query (string, required): Search query


================================================================================
