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

This is a Dify plugin that provides comprehensive Redmine integration as a tool provider. The plugin follows Dify's plugin architecture and supports full CRUD operations for Redmine issues.

### Core Components
- **main.py**: Plugin entry point using `dify_plugin.Plugin`
- **manifest.yaml**: Plugin configuration and metadata
- **provider/**: Tool provider implementation
  - `redmine.py`: Provider class with credential validation
  - `redmine.yaml`: Provider configuration with 4 tools
- **tools/**: Individual tool implementations (4 tools total)
  - `get_issues.py`: List/search multiple issues (`RedmineTool` class)
  - `get_issue.py`: Retrieve single issue with attachments (`RedmineIssueTool` class)
  - `create_issue.py`: Create new issues (`RedmineCreateIssueTool` class)
  - `update_issue.py`: Update existing issues (`RedmineUpdateIssueTool` class)

### Plugin Structure
- Python 3.12 runtime with `dify_plugin` SDK
- Tool-type plugin (extends Dify with Redmine functionality)
- Generator-based tool invoke pattern returning `ToolInvokeMessage`
- Credential validation in provider class
- Standardized naming convention: get_*, create_*, update_*

### Current Implementation Status
- ✅ Complete CRUD operations for Redmine issues
- ✅ Multi-language support (English, Chinese, Portuguese, Japanese) for all tools
- ✅ Comprehensive error handling and API validation
- ✅ Attachment download support with `create_blob_message`
- ✅ Raw JSON output (no data reformatting)
- ✅ Consistent tool naming and structure

## Available Tools

### 1. Get Issues (`tools/get_issues.yaml`)
**Purpose**: Retrieve multiple issues with filtering
**Parameters**:
- `project_id`: Filter by project ID or identifier
- `status_id`: Filter by issue status (1=New, 2=In Progress, 3=Resolved, etc.)
- `assigned_to_id`: Filter by assignee user ID
- `limit`: Maximum number of issues to retrieve (default: 25, max: 100)

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
**Required Parameters**:
- `project_id`: Project ID or identifier
- `subject`: Issue title/subject
**Optional Parameters**:
- `description`, `tracker_id`, `status_id`, `priority_id`, `assigned_to_id`, `category_id`, `fixed_version_id`, `estimated_hours`, `is_private`

### 4. Update Issue (`tools/update_issue.yaml`)
**Purpose**: Update existing Redmine issues
**Required Parameters**:
- `issue_id`: The numeric ID of the issue to update
**Optional Parameters**:
- `subject`, `description`, `notes`, `private_notes`, `project_id`, `tracker_id`, `status_id`, `priority_id`, `assigned_to_id`, `category_id`, `fixed_version_id`, `estimated_hours`, `done_ratio`, `is_private`

## Key Files
- `tools/get_issues.py` - Multiple issue retrieval with filtering
- `tools/get_issue.py` - Single issue retrieval with attachment download
- `tools/create_issue.py` - Issue creation with validation
- `tools/update_issue.py` - Issue updating with field validation
- `provider/redmine.py` - Provider with credential validation
- `provider/redmine.yaml` - Provider configuration referencing all 4 tools

## Recent Changes
- Implemented complete CRUD operations for Redmine issues
- Added attachment download functionality with `create_blob_message`
- Standardized file naming: get_issues, get_issue, create_issue, update_issue
- Removed data reformatting - now outputs raw Redmine API responses
- Fixed YAML syntax errors with proper string quoting
- Enhanced error handling for all HTTP status codes (404, 403, 422)
- Added parameter validation and type conversion

## Tool Configuration Details

### Provider Configuration (`provider/redmine.yaml`)
Credentials required:
- `redmine_host`: Your Redmine server URL (e.g., https://redmine.example.com)
- `api_key`: Your Redmine API key (available in account settings)

All tools support:
- **Multi-language UI**: English, Chinese (Simplified), Portuguese (Brazil), Japanese
- **Comprehensive Error Handling**: Network errors, authentication, validation
- **Raw JSON Output**: No data transformation, preserves original API structure
- **Type Safety**: Parameter validation and conversion

## Troubleshooting

### Common Issues
1. **YAML Syntax Errors**: Ensure colons in string values are properly quoted
2. **API Connection**: Verify Redmine host URL and API key are correct
3. **Tool Not Found**: Check that `provider/redmine.yaml` references all 4 tool files
4. **Attachment Download**: Ensure `attachments` is included in the `include` parameter

### Testing the Plugin
```bash
# Validate YAML syntax for all tools
python -c "import yaml; [yaml.safe_load(open(f'tools/{tool}.yaml', 'r')) for tool in ['get_issues', 'get_issue', 'create_issue', 'update_issue']]"

# Test plugin locally
python -m main
```

## Documentation References
- **Dify Plugin Development**: https://docs.dify.ai/plugin-dev-en/0111-getting-started-dify-plugin
- **Redmine REST API**: https://www.redmine.org/projects/redmine/wiki/Rest_api