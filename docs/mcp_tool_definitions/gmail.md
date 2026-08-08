1. GMAIL (20 tools)
   Server: gmail | smithery.ai/server/gmail
================================================================================

GMAIL_ADD_LABEL_TO_EMAIL
  Description: Adds and/or removes specified gmail labels for a message; ensure message id and all label ids are valid
  Parameters:
    - user_id (string): User's email or 'me'; default "me"
    - message_id (string, required): Immutable message identifier
    - add_label_ids (array): Label IDs to add; default []
    - remove_label_ids (array): Label IDs to remove; default []

GMAIL_CREATE_EMAIL_DRAFT
  Description: Creates a gmail email draft, supporting to/cc/bcc, subject, plain/html body
  Parameters:
    - user_id (string): User's email or 'me'; default "me"
    - recipient_email (string, required): Primary recipient
    - extra_recipients (array): Additional 'To' addresses; default []
    - cc (array): Carbon copy recipients; default []
    - bcc (array): Blind carbon copy recipients; default []
    - subject (string, required): Email subject line
    - body (string, required): Email content (plain text or HTML)
    - is_html (boolean): True if body is HTML; default false
    - thread_id (string|null): Existing thread ID for replies
    - attachment (object|null): File with name, s3key, mimetype

GMAIL_CREATE_LABEL
  Description: Creates a new label with a unique name in the specified user's gmail account
  Parameters:
    - user_id (string): User's email; default "me"
    - label_name (string, required): Unique label name (max 225 chars)
    - text_color (string|null): Hex color code
    - background_color (string|null): Hex color code
    - label_list_visibility (string): labelShow/labelShowIfUnread/labelHide; default "labelShow"
    - message_list_visibility (string): show/hide; default "show"

GMAIL_DELETE_DRAFT
  Description: Permanently deletes a specific gmail draft using its id
  Parameters:
    - user_id (string): User's email or 'me'; default "me"
    - draft_id (string, required): Immutable draft identifier

GMAIL_DELETE_MESSAGE
  Description: Permanently deletes a specific email message by its id from a gmail mailbox
  Parameters:
    - user_id (string): User's email or 'me'; default "me"
    - message_id (string, required): Email message identifier

GMAIL_FETCH_EMAILS
  Description: Fetches a list of email messages from a gmail account, supporting filtering, pagination, and optional full content retrieval
  Parameters:
    - user_id (string): User's email or 'me'; default "me"
    - query (string|null): Gmail search query (from:, subject:, label:, etc.)
    - label_ids (array): Filter by specific labels
    - max_results (integer): 1-500 messages per page; default 1
    - page_token (string|null): Pagination token
    - verbose (boolean): True for detailed fetching; default true
    - ids_only (boolean): True for message IDs only; default false
    - include_payload (boolean): Include full message payload; default true
    - include_spam_trash (boolean): Include spam/trash messages; default false

GMAIL_FETCH_MESSAGE_BY_MESSAGE_ID
  Description: Fetches a specific email message by its id, provided the message id exists and is accessible
  Parameters:
    - user_id (string): User's email or 'me'; default "me"
    - message_id (string, required): Unique message identifier
    - format (string): minimal/full/raw/metadata; default "full"

GMAIL_FETCH_MESSAGE_BY_THREAD_ID
  Description: Retrieves messages from a gmail thread using its thread id
  Parameters:
    - user_id (string): User's email; default "me"
    - thread_id (string, required): Unique thread identifier
    - page_token (string): Pagination token; default ""

GMAIL_GET_ATTACHMENT
  Description: Retrieves a specific attachment by id from a message in a user's gmail mailbox
  Parameters:
    - user_id (string): User's email or 'me'; default "me"
    - message_id (string, required): Message containing attachment
    - attachment_id (string, required): Specific attachment identifier
    - file_name (string, required): Desired filename for download

GMAIL_GET_CONTACTS
  Description: Fetches contacts (connections) for the authenticated google account
  Parameters:
    - resource_name (string): Person resource identifier; default "people/me"
    - person_fields (string): Comma-separated fields to retrieve; default "emailAddresses,names,birthdays,genders"
    - page_token (string|null): Pagination token
    - include_other_contacts (boolean): Include interacted-with contacts; default true

GMAIL_GET_PEOPLE
  Description: Retrieves either a specific person's details or lists 'other contacts'
  Parameters:
    - resource_name (string): Person resource identifier; default "people/me"
    - person_fields (string): Field mask for returned data; default "emailAddresses,names,birthdays,genders"
    - other_contacts (boolean): Retrieve 'Other Contacts'; default false
    - page_size (integer): Results per page (1-1000); default 10
    - page_token (string): Pagination token; default ""
    - sync_token (string): Token for syncing changes; default ""

GMAIL_GET_PROFILE
  Description: Retrieves key gmail profile information (email address, message/thread totals, history id)
  Parameters:
    - user_id (string): User's email or 'me'; default "me"

GMAIL_LIST_DRAFTS
  Description: Retrieves a paginated list of email drafts from a user's gmail account
  Parameters:
    - user_id (string): User's mailbox ID or 'me'; default "me"
    - verbose (boolean): True for full details; default false
    - max_results (integer): 1-500 drafts per page; default 1
    - page_token (string): Pagination token; default ""

GMAIL_LIST_LABELS
  Description: Retrieves a list of all system and user-created labels for the specified gmail account
  Parameters:
    - user_id (string): User's email or 'me'; default "me"

GMAIL_LIST_THREADS
  Description: Retrieves a list of email threads from a gmail account, supporting filtering and pagination
  Parameters:
    - user_id (string): User's email or 'me'; default "me"
    - query (string): Gmail search query filter; default ""
    - verbose (boolean): True for complete message details; default false
    - max_results (integer): 1-500 threads per page; default 10
    - page_token (string): Pagination token; default ""

GMAIL_MODIFY_THREAD_LABELS
  Description: Adds or removes specified existing label ids from a gmail thread, affecting all its messages
  Parameters:
    - user_id (string): User's email or 'me'; default "me"
    - thread_id (string, required): Immutable thread identifier
    - add_label_ids (array|null): Labels to add
    - remove_label_ids (array|null): Labels to remove

GMAIL_MOVE_TO_TRASH
  Description: Moves an existing, non-deleted email message to the trash for the specified user
  Parameters:
    - user_id (string): User's email or 'me'; default "me"
    - message_id (string, required): Message identifier

GMAIL_PATCH_LABEL
  Description: Patches the specified label
  Parameters:
    - userId (string, required): User's email or 'me'
    - id (string, required): Label ID to update
    - name (string|null): Updated display name
    - labelListVisibility (string|null): labelShow/labelShowIfUnread/labelHide
    - messageListVisibility (string|null): show/hide
    - color (object|null): Contains textColor and backgroundColor (hex)

GMAIL_REMOVE_LABEL
  Description: Permanently deletes a specific, existing user-created gmail label by its id
  Parameters:
    - user_id (string): User's email or 'me'; default "me"
    - label_id (string, required): User-created label identifier

GMAIL_REPLY_TO_THREAD
  Description: Sends a reply within a specific gmail thread using the original thread's subject
  Parameters:
    - user_id (string): User's email or 'me'; default "me"
    - thread_id (string, required): Gmail thread identifier
    - recipient_email (string, required): Primary recipient
    - extra_recipients (array): Additional 'To' recipients; default []
    - cc (array): CC recipients; default []
    - bcc (array): BCC recipients; default []
    - message_body (string, required): Reply content (plain text or HTML)
    - is_html (boolean): True if message_body is HTML; default false
    - attachment (object|null): File with name, s3key, mimetype


================================================================================
