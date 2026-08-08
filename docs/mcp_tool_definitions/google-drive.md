7. GOOGLE DRIVE (20 tools)
   Server: googledrive | smithery.ai/server/googledrive
================================================================================

GOOGLEDRIVE_ADD_FILE_SHARING_PREFERENCE
  Description: Modifies sharing permissions for an existing google drive file, granting a specified role to a user, group, domain, or 'anyone'
  Parameters:
    - role (string, required): Permission level. Pattern: ^(owner|organizer|fileOrganizer|writer|commenter|reader)$
    - type (string, required): Grantee category. Pattern: ^(user|group|domain|anyone)$
    - file_id (string, required): Unique file identifier
    - email_address (string|null): Email for user/group grantees
    - domain (string|null): Domain for domain-type permissions

GOOGLEDRIVE_COPY_FILE
  Description: Duplicates an existing file in google drive, identified by its file id
  Parameters:
    - file_id (string, required): Unique identifier for source file
    - new_title (string|null): Title for copied file; defaults to "Copy of [original]"

GOOGLEDRIVE_CREATE_COMMENT
  Description: Create a comment on a file. Use when you need to add a new comment to a specific file
  Parameters:
    - file_id (string, required): File identifier
    - content (string, required): Plain text comment content
    - anchor (string|null): JSON-formatted document region (e.g., {"type": "line", "line": 12})
    - quoted_file_content_value (string|null): Quoted text excerpt
    - quoted_file_content_mime_type (string|null): MIME type of quoted content

GOOGLEDRIVE_CREATE_DRIVE
  Description: Create a new shared drive for collaboration
  Parameters:
    - name (string, required): Shared drive name
    - requestId (string, required): Unique UUID for idempotent creation
    - hidden (boolean|null): Hide from default view
    - themeId (string|null): Theme identifier for background
    - colorRgb (string|null): Hex color code (e.g., #FF0000)
    - backgroundImageFile (object|null): Image file with cropping parameters (sub-fields: id, width, xCoordinate, yCoordinate)

GOOGLEDRIVE_CREATE_FILE
  Description: Creates a new file or folder with metadata. Use to create empty files or folders, or files with content
  Parameters:
    - name (string|null): File name
    - mimeType (string|null): MIME type designation
    - parents (array|null): Parent folder IDs
    - starred (boolean|null): Star status
    - description (string|null): File description
    - fields (string|null): Comma-separated response fields

GOOGLEDRIVE_CREATE_FILE_FROM_TEXT
  Description: Creates a new file in google drive from provided text content (up to 10mb), supporting various formats
  Parameters:
    - file_name (string, required): Desired file name
    - text_content (string, required): Plain text content (max 10MB)
    - mime_type (string, default "text/plain"): Format type for new file
    - parent_id (string|null): Parent folder identifier

GOOGLEDRIVE_CREATE_FOLDER
  Description: Creates a new folder in google drive, optionally within a parent folder specified by its id or name
  Parameters:
    - folder_name (string, required): Folder name
    - parent_id (string|null): Parent folder ID or name; omit for root creation

GOOGLEDRIVE_CREATE_REPLY
  Description: Create a reply to a comment in google drive
  Parameters:
    - file_id (string, required): File identifier
    - comment_id (string, required): Comment identifier
    - content (string, required): Plain text reply content
    - action (string|null): Action on parent comment (resolve or reopen)
    - fields (string|null): Response field selector

GOOGLEDRIVE_CREATE_SHORTCUT_TO_FILE
  Description: Create a shortcut to a file or folder in google drive
  Parameters:
    - name (string, required): Shortcut name
    - target_id (string, required): ID of target file/folder
    - target_mime_type (string|null): MIME type of target
    - includeLabels (string|null): Comma-separated label IDs
    - supportsAllDrives (boolean|null): Support for shared drives
    - keepRevisionForever (boolean|null): Preserve head revision
    - ignoreDefaultVisibility (boolean|null): Override domain defaults
    - includePermissionsForView (string|null): Additional view permissions

GOOGLEDRIVE_DELETE_COMMENT
  Description: Deletes a comment from a file
  Parameters:
    - file_id (string, required): File identifier
    - comment_id (string, required): Comment identifier

GOOGLEDRIVE_DELETE_DRIVE
  Description: Permanently delete a shared drive and its contents
  Parameters:
    - driveId (string, required): Shared drive identifier
    - allowItemDeletion (boolean|null): Delete contents within drive
    - useDomainAdminAccess (boolean|null): Request as domain administrator

GOOGLEDRIVE_DELETE_PERMISSION
  Description: Deletes a permission from a file by permission id to revoke access
  Parameters:
    - file_id (string, required): File or shared drive identifier
    - permission_id (string, required): Permission identifier
    - supportsAllDrives (boolean|null): Support both drive types
    - useDomainAdminAccess (boolean|null): Domain admin request mode

GOOGLEDRIVE_DELETE_REPLY
  Description: Delete a specific reply by reply id from a comment
  Parameters:
    - file_id (string, required): File identifier
    - comment_id (string, required): Comment identifier
    - reply_id (string, required): Reply identifier

GOOGLEDRIVE_DOWNLOAD_FILE
  Description: Downloads a file from google drive by its id. For Google Workspace documents, optionally exports to specified format
  Parameters:
    - file_id (string, required): File identifier for download
    - mime_type (string|null): Export format for Workspace documents (PDF, DOCX, CSV, etc.)

GOOGLEDRIVE_EDIT_FILE
  Description: Updates an existing google drive file by overwriting its entire content with new text (max 10mb)
  Parameters:
    - file_id (string, required): File identifier to update
    - content (string, required): New text content (UTF-8, max 10MB)
    - mime_type (string, default "text/plain"): Content format type

GOOGLEDRIVE_EMPTY_TRASH
  Description: Permanently delete all of the user's trashed files
  Parameters:
    - driveId (string|null): Shared drive identifier for drive-specific trash
    - enforceSingleParent (boolean|null): Deprecated parameter

GOOGLEDRIVE_FILES_MODIFY_LABELS
  Description: Modifies the set of labels applied to a file. Returns a list of the labels that were added or modified
  Parameters:
    - file_id (string, required): File identifier
    - label_modifications (array, required): Label modification objects containing label_id (required), remove_label (boolean|null), field_modifications (array|null)
    - kind (string, default "drive#modifyLabelsRequest"): Request type identifier

GOOGLEDRIVE_FIND_FILE
  Description: List or search for files and folders in google drive based on query criteria
  Parameters:
    - q (string|null): Query filter (Google Drive API query syntax)
    - spaces (string, default "drive"): Comma-separated spaces to query
    - corpora (enum|null): Search scope (user, drive, domain, allDrives)
    - driveId (string|null): Shared drive ID (required if corpora is "drive")
    - orderBy (string|null): Sort keys and direction
    - pageSize (integer, default 100, max 1000): Results per page
    - pageToken (string|null): Pagination token
    - fields (string, default "*"): Response field selector
    - supportsAllDrives (boolean, default true): Support both drive types
    - includeItemsFromAllDrives (boolean, default false): Include all drives in results

GOOGLEDRIVE_FIND_FOLDER
  Description: Find a folder in google drive by its name and optionally a parent folder
  Parameters:
    - name_exact (string|null): Exact folder name (case-sensitive)
    - name_contains (string|null): Substring in name (case-insensitive)
    - name_not_contains (string|null): Exclude substring from name
    - modified_after (string|null): RFC 3339 timestamp filter
    - starred (boolean|null): Filter by star status
    - full_text_contains (string|null): Text within folder contents
    - full_text_not_contains (string|null): Exclude text from contents

GOOGLEDRIVE_GENERATE_IDS
  Description: Generates a set of file ids which can be provided in create or copy requests
  Parameters:
    - type (string|null): Item type for IDs (e.g., files, shortcuts)
    - count (integer|null, min 1, max 1000): Number of IDs to generate
    - space (string|null): Space for ID usage (drive or appDataFolder)


================================================================================
SUMMARY
================================================================================

Service              | Tool Count
---------------------|----------
Gmail                | 20
Google Calendar      | 29
Slack                | 10
Linear               | 25
Perplexity           | 1
GitHub               | 86
Google Drive         | 20
---------------------|----------
TOTAL                | 191
