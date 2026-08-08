2. GOOGLE CALENDAR (29 tools)
   Server: googlecalendar | smithery.ai/server/googlecalendar
================================================================================

GOOGLECALENDAR_ACL_PATCH
  Description: Updates an access control rule for a calendar using patch semantics
  Parameters:
    - role (string|null): Permission level - "none", "freeBusyReader", "reader", "writer", "owner"
    - scope (object|null): Access extent with type ("default", "user", "group", "domain") and optional value
    - rule_id (string, required): ACL identifier (e.g., "user:test.user@example.com")
    - calendar_id (string, required): Calendar ID or "primary"
    - send_notifications (boolean|null): Whether to notify of sharing changes

GOOGLECALENDAR_CALENDAR_LIST_INSERT
  Description: Inserts an existing calendar into the user's calendar list
  Parameters:
    - id (string, required): Calendar identifier
    - hidden (boolean|null): Hide from list (default: false)
    - color_id (string|null): Color palette reference
    - selected (boolean|null): Visibility status (default: true)
    - background_color (string|null): Hex color code
    - color_rgb_format (boolean|null): Use RGB format
    - foreground_color (string|null): Hex foreground
    - summary_override (string|null): Custom calendar name
    - default_reminders (array|null): EventReminder objects
    - notification_settings (object|null): Notification configuration

GOOGLECALENDAR_CALENDAR_LIST_UPDATE
  Description: Updates an existing entry on the user's calendar list
  Parameters:
    - calendar_id (string, required): Actual calendar ID (not "primary")
    - hidden (boolean|null): Hide status
    - colorId (string|null): Color identifier
    - selected (boolean|null): Display in UI
    - colorRgbFormat (boolean|null): RGB format flag
    - backgroundColor (string|null): Hex background
    - foregroundColor (string|null): Hex foreground
    - summaryOverride (string|null): User-set name
    - defaultReminders (array|null): Reminder objects
    - notificationSettings (object|null): Notification setup

GOOGLECALENDAR_CALENDARS_DELETE
  Description: Deletes a secondary calendar (use clear for primary calendars)
  Parameters:
    - calendar_id (string, required): Calendar to delete

GOOGLECALENDAR_CALENDARS_UPDATE
  Description: Updates metadata for a calendar
  Parameters:
    - summary (string, required): Calendar title
    - calendarId (string, required): Calendar identifier
    - location (string|null): Geographic location
    - timeZone (string|null): IANA timezone name
    - description (string|null): Calendar description

GOOGLECALENDAR_CLEAR_CALENDAR
  Description: Clears a primary calendar. This operation deletes all events associated with the primary calendar
  Parameters:
    - calendar_id (string, required): Target calendar (typically "primary")

GOOGLECALENDAR_CREATE_EVENT
  Description: Create a Google Calendar event using start_datetime plus event_duration_hour and event_duration_minutes fields
  Parameters:
    - summary (string|null): Event title
    - location (string|null): Physical/virtual location
    - timezone (string|null): IANA timezone
    - attendees (array|null): Attendee email strings
    - eventType (enum): "birthday", "default", "focusTime", "outOfOffice", "workingLocation"
    - recurrence (array|null): RRULE/EXRULE lines
    - visibility (enum): "default", "public", "private", "confidential"
    - calendar_id (string, default: "primary"): Target calendar
    - description (string|null): Event description (HTML allowed)
    - send_updates (boolean|null): Notify attendees
    - transparency (enum): "opaque" or "transparent"
    - start_datetime (string, required): YYYY-MM-DDTHH:MM:SS format
    - exclude_organizer (boolean, default: false): Exclude organizer as attendee
    - guests_can_modify (boolean, default: false): Modification permission
    - event_duration_hour (integer, 0-24, default: 0): Hours
    - event_duration_minutes (integer, 0-59, default: 30): Minutes
    - create_meeting_room (boolean|null): Add Google Meet link
    - birthdayProperties (object|null): Birthday event config
    - focusTimeProperties (object|null): Focus time settings
    - outOfOfficeProperties (object|null): Out-of-office config
    - workingLocationProperties (object|null): Work location details
    - guestsCanInviteOthers (boolean|null): Invitation permission
    - guestsCanSeeOtherGuests (boolean|null): Attendee visibility

GOOGLECALENDAR_DELETE_EVENT
  Description: Deletes a specified event (idempotent, raises 404 if not found)
  Parameters:
    - event_id (string, required): Event identifier
    - calendar_id (string, default: "primary"): Source calendar

GOOGLECALENDAR_DUPLICATE_CALENDAR
  Description: Creates a new, empty Google Calendar with specified title
  Parameters:
    - summary (string, required, minLength: 1): New calendar name

GOOGLECALENDAR_EVENTS_INSTANCES
  Description: Returns instances of the specified recurring event
  Parameters:
    - eventId (string, required): Recurring event ID
    - calendarId (string, required): Calendar identifier
    - timeMin (string|null): Lower bound (RFC3339 with timezone)
    - timeMax (string|null): Upper bound (RFC3339 with timezone)
    - timeZone (string|null): Response timezone
    - maxResults (integer|null, 1-2500): Results per page
    - pageToken (string|null): Pagination token
    - showDeleted (boolean|null): Include cancelled instances
    - maxAttendees (integer|null): Attendee limit
    - originalStart (string|null): Instance original start time

GOOGLECALENDAR_EVENTS_LIST
  Description: Returns events on the specified calendar
  Parameters:
    - calendarId (string, required): Calendar identifier
    - q (string|null): Free text search
    - iCalUID (string|null): iCalendar format event ID
    - orderBy (string|null): "startTime" or "updated"
    - timeMin (string|null): RFC3339 lower bound
    - timeMax (string|null): RFC3339 upper bound
    - timeZone (string|null): Response timezone
    - maxResults (integer|null): Results limit
    - pageToken (string|null): Pagination token
    - syncToken (string|null): Incremental sync token
    - eventTypes (string|null): Filter by event type
    - updatedMin (string|null): Last modification lower bound
    - showDeleted (boolean|null): Include cancelled events
    - maxAttendees (integer|null, >=1): Attendee limit
    - singleEvents (boolean|null): Expand recurring events
    - alwaysIncludeEmail (boolean|null): Deprecated
    - showHiddenInvitations (boolean|null): Include hidden invitations
    - sharedExtendedProperty (string|null): Extended property constraint
    - privateExtendedProperty (string|null): Private property constraint

GOOGLECALENDAR_EVENTS_MOVE
  Description: Moves an event to another calendar (changes organizer)
  Parameters:
    - event_id (string, required): Event identifier
    - calendar_id (string, required): Source calendar
    - destination (string, required): Target calendar
    - send_updates (string|null): "all", "externalOnly", or "none"

GOOGLECALENDAR_EVENTS_WATCH
  Description: Watch for changes to Events resources
  Parameters:
    - calendarId (string, required): Calendar identifier
    - id (string, required): Channel UUID
    - type (string, default: "web_hook"): Delivery mechanism
    - address (string, required): Notification address
    - token (string|null): Arbitrary delivery string
    - params (object|null): Delivery channel behavior
    - payload (boolean|null): Include payload flag

GOOGLECALENDAR_FIND_EVENT
  Description: Finds events in a specified Google Calendar using text query, time ranges, and event types
  Parameters:
    - calendar_id (string, default: "primary"): Target calendar
    - query (string|null): Free-text search terms
    - timeMin (string|null): Lower bound (multiple formats accepted)
    - timeMax (string|null): Upper bound (multiple formats accepted)
    - order_by (string|null): "startTime" or "updated"
    - event_types (array, default: all types): Filter by type
    - max_results (integer, default: 10): Results per page
    - page_token (string|null): Pagination token
    - updated_min (string|null): Last modification lower bound
    - show_deleted (boolean|null): Include cancelled events
    - single_events (boolean, default: true): Expand recurring events

GOOGLECALENDAR_FIND_FREE_SLOTS
  Description: Finds both free and busy time slots in Google Calendars for specified calendars within a defined time range
  Parameters:
    - items (array, default: ["primary"]): Calendar identifiers
    - time_min (string|null): Start datetime
    - time_max (string|null): End datetime
    - timezone (string, default: "UTC"): IANA timezone
    - group_expansion_max (integer, default: 100): Max group calendars
    - calendar_expansion_max (integer, default: 50): Max calendars for FreeBusy

GOOGLECALENDAR_FREE_BUSY_QUERY
  Description: Returns free/busy information for a set of calendars
  Parameters:
    - items (array, required): FreeBusyQueryItem objects with id
    - timeMin (string, required): RFC3339 start interval
    - timeMax (string, required): RFC3339 end interval
    - timeZone (string|null): Response timezone
    - groupExpansionMax (integer|null): Max group members (max 100)
    - calendarExpansionMax (integer|null): Max calendars (max 50)

GOOGLECALENDAR_GET_CALENDAR
  Description: Retrieves a specific Google Calendar accessible to authenticated user
  Parameters:
    - calendar_id (string, default: "primary"): Calendar identifier

GOOGLECALENDAR_GET_CURRENT_DATE_TIME
  Description: Gets the current date and time with optional timezone offset
  Parameters:
    - timezone (number, default: 0): UTC offset in hours

GOOGLECALENDAR_LIST_ACL_RULES
  Description: Retrieves the list of access control rules (ACLs) for a specified calendar
  Parameters:
    - calendar_id (string, required): Calendar identifier
    - max_results (integer|null): Results limit (default: 100)
    - page_token (string|null): Pagination token
    - sync_token (string|null): Incremental sync token
    - show_deleted (boolean|null): Include deleted ACLs

GOOGLECALENDAR_LIST_CALENDARS
  Description: Retrieves a paginated list of calendars from user's calendar list
  Parameters:
    - maxResults (integer, default: 100, max: 250): Results per page
    - pageToken (string|null): Pagination token
    - syncToken (string|null): Incremental sync token
    - showHidden (boolean, default: false): Include hidden calendars
    - showDeleted (boolean, default: false): Include deleted entries
    - minAccessRole (enum|null): "freeBusyReader", "owner", "reader", "writer"

GOOGLECALENDAR_PATCH_CALENDAR
  Description: Partially updates (PATCHes) an existing Google Calendar, modifying only the fields provided
  Parameters:
    - calendar_id (string, required): Calendar identifier
    - summary (string, required): New title (non-empty)
    - description (string|null): New description
    - location (string|null): Geographic location
    - timezone (string|null): IANA timezone

GOOGLECALENDAR_PATCH_EVENT
  Description: Update specified fields of an existing event using patch semantics
  Parameters:
    - calendar_id (string, required): Calendar identifier
    - event_id (string, required): Event identifier
    - summary (string|null): New title
    - start_time (string|null): New start (RFC3339 or YYYY-MM-DD)
    - end_time (string|null): New end (RFC3339 or YYYY-MM-DD)
    - location (string|null): New location
    - description (string|null): New description
    - attendees (array|null): Email list (replaces existing)
    - timezone (string|null): IANA timezone
    - send_updates (string|null): "all", "externalOnly", or "none"
    - max_attendees (integer|null, >0): Attendee limit
    - rsvp_response (string|null): "accepted", "declined", "tentative", "needsAction"
    - supports_attachments (boolean|null): Attachment support flag
    - conference_data_version (integer|null, 0-1): Conference support version

GOOGLECALENDAR_QUICK_ADD
  Description: Parses natural language text to quickly create a basic Google Calendar event
  Parameters:
    - text (string, default: ""): Natural language event description
    - calendar_id (string, default: "primary"): Target calendar
    - send_updates (enum): "all", "externalOnly", or "none"

GOOGLECALENDAR_REMOVE_ATTENDEE
  Description: Removes an attendee from a specified event
  Parameters:
    - calendar_id (string, default: "primary"): Event's calendar
    - event_id (string, required): Event identifier
    - attendee_email (string, required, format: email): Email to remove

GOOGLECALENDAR_SETTINGS_LIST
  Description: Returns all user settings for the authenticated user
  Parameters:
    - maxResults (integer|null, 1-250): Results limit
    - pageToken (string|null): Pagination token
    - syncToken (string|null): Incremental sync token

GOOGLECALENDAR_SETTINGS_WATCH
  Description: Watch for changes to Settings resources
  Parameters:
    - id (string, required): Channel UUID
    - type (string, required): "web_hook" or "webhook"
    - address (string, required): Notification endpoint
    - token (string|null): Arbitrary delivery string
    - params (object|null): TTL and delivery controls

GOOGLECALENDAR_SYNC_EVENTS
  Description: Synchronizes Google Calendar events, performing full or incremental sync
  Parameters:
    - calendar_id (string, default: "primary"): Calendar identifier
    - sync_token (string|null): Incremental sync token
    - pageToken (string|null): Pagination token
    - event_types (array|null): Filter by type
    - max_results (integer|null, max: 2500): Results limit
    - single_events (boolean|null): Expand recurring events

GOOGLECALENDAR_UPDATE_ACL_RULE
  Description: Updates an access control rule for the specified calendar
  Parameters:
    - calendar_id (string, required): Calendar identifier
    - rule_id (string, required): ACL rule identifier
    - role (string, required): "none", "freeBusyReader", "reader", "writer", "owner"
    - send_notifications (boolean|null, default: true): Notification flag

GOOGLECALENDAR_UPDATE_EVENT
  Description: Updates an existing event; this is a full PUT replacement
  Parameters:
    - calendar_id (string, default: "primary"): Event's calendar
    - event_id (string, required): Event to update
    - summary (string|null): Event title
    - start_datetime (string, required): YYYY-MM-DDTHH:MM:SS format
    - location (string|null): Event location
    - description (string|null): Event description
    - timezone (string|null): IANA timezone
    - attendees (array|null): Attendee emails
    - eventType (enum): Event classification
    - recurrence (array|null): RRULE/EXRULE lines
    - visibility (enum): "default", "public", "private", "confidential"
    - transparency (enum): "opaque" or "transparent"
    - send_updates (boolean|null): Notify attendees
    - guests_can_modify (boolean, default: false): Edit permission
    - event_duration_hour (integer, 0-24): Duration hours
    - event_duration_minutes (integer, 0-59): Duration minutes
    - create_meeting_room (boolean|null): Add Google Meet
    - birthdayProperties (object|null): Birthday configuration
    - focusTimeProperties (object|null): Focus time settings
    - outOfOfficeProperties (object|null): Out-of-office config
    - workingLocationProperties (object|null): Work location details
    - guestsCanInviteOthers (boolean|null): Invitation permission
    - guestsCanSeeOtherGuests (boolean|null): Attendee visibility


================================================================================
