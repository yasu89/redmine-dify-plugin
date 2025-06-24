# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Running the Plugin
```bash
python -m main
```

### Installing Dependencies
```bash
pip install -r requirements.txt
```

### Packaging the Plugin
```bash
dify-plugin plugin package ./
```

### Testing/Debugging Setup
1. Copy `.env.example` to `.env` and configure:
   - `INSTALL_METHOD=remote`
   - `REMOTE_INSTALL_URL=debug.dify.ai:5003` (or your Dify instance)
   - `REMOTE_INSTALL_KEY=<your-debug-key>`

## Architecture Overview

This is a Dify plugin that provides comprehensive Redmine integration as a tool provider. The plugin follows Dify's plugin architecture and supports full CRUD operations for Redmine issues and users with complete API compliance.

### Core Components
- **main.py**: Plugin entry point using `dify_plugin.Plugin`
- **manifest.yaml**: Plugin configuration and metadata
- **provider/**: Tool provider implementation
  - `redmine.py`: Provider class with credential validation
  - `redmine.yaml`: Provider configuration with 8 tools and productivity tag
- **tools/**: Individual tool implementations (8 tools total)
  - `get_issues.py`: List/search multiple issues (`RedmineTool` class)
  - `get_issue.py`: Retrieve single issue with attachments (`RedmineIssueTool` class)
  - `create_issue.py`: Create new issues (`RedmineCreateIssueTool` class)
  - `update_issue.py`: Update existing issues (`RedmineUpdateIssueTool` class)
  - `get_users.py`: List/search multiple users (`RedmineUsersTool` class)
  - `get_user.py`: Retrieve single user with details (`RedmineUserTool` class)
  - `create_user.py`: Create new users (`RedmineCreateUserTool` class)
  - `update_user.py`: Update existing users (`RedmineUpdateUserTool` class)

### Plugin Structure
- Python 3.12 runtime with `dify_plugin` SDK
- Tool-type plugin (extends Dify with Redmine functionality)
- Generator-based tool invoke pattern returning `ToolInvokeMessage`
- Credential validation in provider class
- Standardized naming convention: get_*, create_*, update_*
- Full API compliance with Redmine REST API documentation

### Current Implementation Status
- ✅ Complete CRUD operations for Redmine issues and users
- ✅ Multi-language support (English, Chinese, Portuguese, Japanese) for all tools
- ✅ Comprehensive error handling and API validation
- ✅ Attachment download support with `create_blob_message`
- ✅ Raw JSON output (no data reformatting)
- ✅ Consistent tool naming and structure
- ✅ Full API parameter coverage following official documentation order
- ✅ Advanced filtering, sorting, and pagination
- ✅ Custom fields and watcher support
- ✅ User management with admin privileges
- ✅ Project configuration with productivity tag

## Available Tools

### 1. Get Issues (`tools/get_issues.yaml`)
**Purpose**: Retrieve multiple issues with comprehensive filtering and pagination
**Parameters** (following API documentation order):
- `offset`: Skip this number of issues for pagination
- `limit`: Maximum number of issues to retrieve (default: 25, max: 100)
- `sort`: Column to sort with (select dropdown with predefined options)
- `include`: Additional data to fetch (attachments, relations)
- `issue_id`: Specific issue ID(s) - comma-separated for multiple
- `project_id`: Filter by project ID or identifier
- `subproject_id`: Filter by subproject ID
- `tracker_id`: Filter by tracker ID
- `status_id`: Filter by issue status (1=New, 2=In Progress, 3=Resolved, etc.)
- `assigned_to_id`: Filter by assignee user ID (supports "me")
- `parent_id`: Filter by parent issue ID
- `created_on`: Date range filter for creation date (>=, <=, ><)
- `updated_on`: Date range filter for update date (>=, <=, ><)
- `custom_fields`: Custom field filters as query parameters (cf_x=value format)

**Features**:
- Automatic attachment download when `attachments` is included
- `create_blob_message` for file attachments with proper MIME types
- Full pagination support
- Advanced date range filtering
- Custom field filtering

### 2. Get Issue (`tools/get_issue.yaml`)
**Purpose**: Retrieve single issue with detailed information
**Parameters**:
- `issue_id`: Required - The numeric ID of the issue
- `include`: Optional - Additional data (journals, children, attachments, relations, changesets, watchers)

**Features**:
- Automatic attachment download when `attachments` is included
- `create_blob_message` for file attachments with proper MIME types

### 3. Create Issue (`tools/create_issue.yaml`)
**Purpose**: Create new Redmine issues
**Parameters** (following API documentation order):
- `project_id`: Required - Project ID or identifier
- `tracker_id`: Tracker ID (1=Bug, 2=Feature, 3=Support)
- `status_id`: Status ID (1=New, 2=In Progress, etc.)
- `priority_id`: Priority ID (1=Low, 2=Normal, 3=High, etc.)
- `subject`: Required - Issue title/subject
- `description`: Detailed description
- `category_id`: Category ID for the issue
- `fixed_version_id`: Target version ID
- `assigned_to_id`: User ID to assign to
- `parent_issue_id`: Parent issue ID for subtasks
- `custom_fields`: Custom fields as JSON array
- `watcher_user_ids`: Comma-separated user IDs to add as watchers
- `is_private`: Whether the issue should be private
- `estimated_hours`: Estimated hours to complete

### 4. Update Issue (`tools/update_issue.yaml`)
**Purpose**: Update existing Redmine issues
**Parameters** (following API documentation order):
- `issue_id`: Required - The numeric ID of the issue to update
- `project_id`: Move issue to different project
- `tracker_id`: Change tracker type
- `status_id`: Update status
- `priority_id`: Change priority
- `subject`: Update title/subject
- `description`: Update detailed description
- `category_id`: Change category
- `fixed_version_id`: Update target version
- `assigned_to_id`: Reassign to different user
- `parent_issue_id`: Change parent issue
- `custom_fields`: Update custom fields as JSON array
- `watcher_user_ids`: Add watchers (comma-separated user IDs)
- `is_private`: Change privacy setting
- `estimated_hours`: Update estimated hours
- `notes`: Comments about the update
- `private_notes`: Whether notes should be private
- `done_ratio`: Completion percentage (0-100)

## User Management Tools

### 5. Get Users (`tools/get_users.yaml`)
**Purpose**: Retrieve list of users with filtering options (Admin privileges required)
**Parameters** (following API documentation order):
- `status`: User status filter (1=Active can login, 2=Registered not confirmed, 3=Locked cannot login)
- `name`: Filter by login, firstname, lastname, or email
- `group_id`: Filter users who are members of specified group

**Features**:
- Admin privilege validation
- Comprehensive status-based filtering
- Name-based search across multiple fields

### 6. Get User (`tools/get_user.yaml`)
**Purpose**: Retrieve single user with detailed information
**Parameters**:
- `user_id`: Required - User ID (numeric) or 'current' for authenticated user
- `include`: Optional - Additional data (memberships, groups)

**Features**:
- Support for 'current' user retrieval
- Flexible include parameter validation
- Admin and non-admin access with different response details

### 7. Create User (`tools/create_user.yaml`)
**Purpose**: Create new Redmine users (Admin privileges required)
**Parameters** (following API documentation order):
- `login`: Required - User login name (unique identifier)
- `password`: User password (optional if using auth_source_id or generate_password)
- `firstname`: Required - User's first name
- `lastname`: Required - User's last name
- `mail`: Required - User's email address
- `auth_source_id`: Authentication source ID (for LDAP or external auth)
- `mail_notification`: Email notification preference (only_my_events, none, all, selected, only_assigned, only_owner)
- `must_change_passwd`: Whether user must change password on first login
- `generate_password`: Whether to automatically generate a password
- `custom_fields`: Custom fields as JSON array
- `send_information`: Whether to send account information via email (top-level parameter)

**Features**:
- Complete user creation with all API parameters
- Password generation and change requirements
- External authentication source support
- Email notification configuration

### 8. Update User (`tools/update_user.yaml`)
**Purpose**: Update existing Redmine users (Admin privileges required)
**Parameters** (following API documentation order):
- `user_id`: Required - The numeric ID of the user to update
- `login`: New user login name
- `password`: New user password (secret-input type)
- `firstname`: New first name
- `lastname`: New last name
- `mail`: New email address
- `auth_source_id`: New authentication source ID
- `mail_notification`: New email notification preference
- `must_change_passwd`: Whether user must change password on next login
- `generate_password`: Whether to automatically generate a new password
- `custom_fields`: Updated custom fields as JSON array
- `admin`: Whether to grant or revoke admin rights (top-level parameter)

**Features**:
- Flexible user attribute updates
- Admin privilege management
- All user creation parameters supported for updates

## Key Files

### Issue Management
- `tools/get_issues.py` - Multiple issue retrieval with comprehensive filtering
- `tools/get_issue.py` - Single issue retrieval with attachment download
- `tools/create_issue.py` - Issue creation with full API compliance
- `tools/update_issue.py` - Issue updating with complete field support

### User Management
- `tools/get_users.py` - Multiple user retrieval with filtering (admin required)
- `tools/get_user.py` - Single user retrieval with details
- `tools/create_user.py` - User creation with complete API compliance (admin required)
- `tools/update_user.py` - User updating with admin privilege management (admin required)

### Core Components
- `provider/redmine.py` - Provider with credential validation
- `provider/redmine.yaml` - Provider configuration with productivity tag
- `.editorconfig` - Code style configuration

## Recent Changes

### User Management Implementation (Latest)
- **Complete User CRUD Operations**: Added comprehensive user management tools
  - `get_users`: List users with status, name, and group filtering (admin required)
  - `get_user`: Retrieve single user with 'current' support and include options
  - `create_user`: Full user creation with password generation and external auth
  - `update_user`: User updates with admin privilege management
- **API Documentation Compliance**: All user tools follow exact Redmine Users API documentation
- **Admin Privilege Handling**: Proper admin privilege validation and error handling
- **Password Management**: Support for password generation, must-change flags, and external auth
- **Parameter Structure**: Correct top-level vs user-object parameter placement (send_information, admin)

### Previous Issue Management Enhancements
- **API Compliance**: Updated all tools to follow exact Redmine API documentation order
- **Enhanced Filtering**: Added comprehensive filtering options to get_issues
  - Date range filtering (created_on, updated_on)
  - Custom field filtering with query parameter format
  - Subproject and parent issue filtering
- **UI Improvements**: 
  - Sort parameter changed to select dropdown with predefined options
  - Added placeholders for all parameters in all languages
- **Advanced Features**:
  - Custom fields support (JSON format)
  - Watcher management (comma-separated format)
  - Parent issue relationships
  - Progress tracking (done_ratio)
- **Attachment Support**: Automatic download in both get_issues and get_issue
- **Multi-language Enhancement**: Complete translation for all new parameters
- **Provider Configuration**: Added productivity tag and proper Japanese translations
- **Code Quality**: Added .editorconfig for consistent formatting

## Tool Configuration Details

### Provider Configuration (`provider/redmine.yaml`)
**Credentials required**:
- `redmine_host`: Your Redmine server URL (e.g., https://redmine.example.com)
- `api_key`: Your Redmine API key (available in account settings)

**Tags**: `productivity` (categorizes as productivity tool)

**All tools support**:
- **Multi-language UI**: English, Chinese (Simplified), Portuguese (Brazil), Japanese
- **Comprehensive Error Handling**: Network errors, authentication, validation
- **Raw JSON Output**: No data transformation, preserves original API structure
- **Type Safety**: Parameter validation and conversion
- **API Compliance**: Follows exact Redmine REST API documentation

### Parameter Types and Validation
- **Numeric Parameters**: Automatic validation and conversion for IDs
- **Date Filters**: Support for operators (>=, <=, ><) with ISO format
- **Custom Fields**: JSON array format with id/value pairs
- **Watchers**: Comma-separated integer format
- **Boolean Parameters**: Proper boolean handling for private flags
- **Select Parameters**: Dropdown UI for sort options

## Troubleshooting

### Common Issues
1. **YAML Syntax Errors**: Ensure colons in string values are properly quoted
2. **API Connection**: Verify Redmine host URL and API key are correct
3. **Tool Not Found**: Check that `provider/redmine.yaml` references all 8 tool files
4. **Admin Privileges**: Ensure API key has admin privileges for user management operations
5. **Attachment Download**: Ensure `attachments` is included in the `include` parameter
6. **Custom Fields**: Ensure JSON format is valid for custom_fields parameter
7. **Date Filters**: Use proper operators and ISO date format (YYYY-MM-DD)
8. **User Status**: Check user status values (1=Active, 2=Registered, 3=Locked) for filtering

### Testing the Plugin
```bash
# Validate YAML syntax for all tools (issues + users)
python -c "import yaml; [yaml.safe_load(open(f'tools/{tool}.yaml', 'r')) for tool in ['get_issues', 'get_issue', 'create_issue', 'update_issue', 'get_users', 'get_user', 'create_user', 'update_user']]"

# Test plugin locally
python -m main
```

### API Testing Examples
```bash
# Test comprehensive issue filtering
GET /issues.xml?project_id=1&status_id=1&sort=updated_on:desc&limit=10

# Test custom field filtering
GET /issues.xml?cf_1=value&cf_2=~substring

# Test date range filtering
GET /issues.xml?created_on=>=2024-01-01&updated_on=><2024-01-01|2024-12-31

# Test user management (admin required)
GET /users.xml?status=1&name=john
GET /users/current.xml?include=memberships,groups
POST /users.xml (with user creation data)
PUT /users/123.xml (with user update data)
```

## Documentation References
- **Dify Plugin Development**: https://docs.dify.ai/plugin-dev-en/0111-getting-started-dify-plugin
- **Redmine REST API**: https://www.redmine.org/projects/redmine/wiki/Rest_api
- **Redmine Issues API**: https://www.redmine.org/projects/redmine/wiki/Rest_Issues
- **Redmine Users API**: https://www.redmine.org/projects/redmine/wiki/Rest_Users