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

This is a Dify plugin that provides Redmine integration as a tool provider. The plugin follows Dify's plugin architecture:

### Core Components
- **main.py**: Plugin entry point using `dify_plugin.Plugin`
- **manifest.yaml**: Plugin configuration and metadata
- **provider/**: Tool provider implementation
  - `redmine.py`: Provider class with credential validation
  - `redmine.yaml`: Provider configuration
- **tools/**: Individual tool implementations
  - `issues.py`: Main tool logic (`RedmineTool` class)
  - `issues.yaml`: Tool parameter definitions

### Plugin Structure
- Python 3.12 runtime with `dify_plugin` SDK
- Tool-type plugin (extends Dify with Redmine functionality)
- Generator-based tool invoke pattern returning `ToolInvokeMessage`
- Credential validation in provider class

### Current Implementation Status
- ✅ Basic plugin structure is in place
- ✅ Redmine API integration implemented with full credential validation
- ✅ Tool renamed from `redmine` to `issues` for better clarity
- ✅ Multi-language support (English, Chinese, Portuguese, Japanese)
- ✅ Comprehensive parameter support:
  - `project_id`: Filter by project ID or identifier
  - `status_id`: Filter by issue status (1=New, 2=In Progress, 3=Resolved, etc.)
  - `assigned_to_id`: Filter by assignee user ID
  - `limit`: Maximum number of issues to retrieve (default: 25, max: 100)
- ✅ Dual output format: JSON data + formatted text summary
- ✅ Error handling for API connection, authentication, and response parsing

## Key Files
- `tools/issues.py` - Redmine API integration with comprehensive issue retrieval
- `tools/issues.yaml` - Tool configuration with 4-language support
- `provider/redmine.py` - Provider with credential validation
- `provider/redmine.yaml` - Provider configuration with credentials setup

## Recent Changes
- Fixed YAML syntax errors in tool configuration
- Renamed tool from `redmine` to `issues` for better naming
- Added Japanese language support to all UI texts
- Implemented dual output (JSON + text) for better user experience
- Added comprehensive error handling and parameter validation

## Tool Configuration Details

### Issues Tool (`tools/issues.yaml`)
The main tool configuration supports:
- **Multi-language UI**: English, Chinese (Simplified), Portuguese (Brazil), Japanese
- **Flexible Filtering**: Project, status, assignee-based filtering
- **Configurable Limits**: 1-100 issues per request
- **Comprehensive Output**: Both structured JSON and readable text format

### Provider Configuration (`provider/redmine.yaml`)
Credentials required:
- `redmine_host`: Your Redmine server URL (e.g., https://redmine.example.com)
- `api_key`: Your Redmine API key (available in account settings)

## Troubleshooting

### Common Issues
1. **YAML Syntax Errors**: Ensure colons in string values are properly quoted
2. **API Connection**: Verify Redmine host URL and API key are correct
3. **Tool Not Found**: Check that `provider/redmine.yaml` references `tools/issues.yaml`

### Testing the Plugin
```bash
# Validate YAML syntax
python -c "import yaml; yaml.safe_load(open('tools/issues.yaml', 'r'))"

# Test plugin locally
python -m main
```

## Documentation References
- **Dify Plugin Development**: https://docs.dify.ai/plugin-dev-en/0111-getting-started-dify-plugin
- **Redmine REST API**: https://www.redmine.org/projects/redmine/wiki/Rest_api