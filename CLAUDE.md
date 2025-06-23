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
  - `redmine.py`: Main tool logic (`RedmineTool` class)
  - `redmine.yaml`: Tool parameter definitions

### Plugin Structure
- Python 3.12 runtime with `dify_plugin` SDK
- Tool-type plugin (extends Dify with Redmine functionality)
- Generator-based tool invoke pattern returning `ToolInvokeMessage`
- Credential validation in provider class

### Current Implementation Status
- Basic plugin structure is in place
- Tool currently returns placeholder "Hello, world!" response
- Provider credential validation is not implemented (placeholder comment)
- Plugin accepts a "query" string parameter

## Key Files to Modify
- `tools/redmine.py:8-11` - Implement actual Redmine API integration
- `provider/redmine.py:10-13` - Implement credential validation for Redmine API
- Tool parameters can be extended in `tools/redmine.yaml:14-26`

## Documentation References
- **Dify Plugin Development**: https://docs.dify.ai/plugin-dev-en/0111-getting-started-dify-plugin
- **Redmine REST API**: https://www.redmine.org/projects/redmine/wiki/Rest_api