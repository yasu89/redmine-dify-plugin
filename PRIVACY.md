# Privacy Policy

**Last Updated:** 2025-06-27
**Version:** 0.1.0

## Introduction

The Redmine Plugin for Dify enables integration with Redmine project management systems through Dify workflows. This policy explains how we handle your data.

## Information We Collect

### Authentication Data
- **Redmine Host URL**: Your Redmine server address
- **API Key**: Your Redmine API authentication key

### Redmine Data Access
When you use the plugin, it accesses:
- Request data you send to Redmine via the Plugin
- Response data you consume from Redmine via the Plugin
- File attachments (when requested)

## How We Handle Your Data

### Data Processing
- All data processing happens within the Dify platform
- Direct communication between Dify and your Redmine instance
- No data sent to external third parties

### Security
- **Encryption**: HTTPS encryption is used only when you specify an HTTPS URL for your Redmine instance
    - **Important**: HTTP URLs will result in unencrypted communication - always use HTTPS in production
- Secure credential storage within Dify
- Access limited to your API key permissions

### Data Retention
- Authentication credentials you provide are securely stored by the Dify platform
- No permanent storage of Redmine data by the plugin
- Attached files are not stored within the plugin itself, but rather on the Dify platform

## Your Rights

- **Full Control**: You control all data access through your Redmine permissions
- **Removal**: Uninstalling removes all stored authentication data

## Third-Party Services

This plugin only communicates with:
- Your specified Redmine instance
- The Dify platform (where the plugin runs)

No data is shared with other external services.

## Privacy Policy Updates

This Privacy Policy may be updated periodically.
The latest version will be published in our GitHub repository and distributed with future plugin updates.

## Contact

For questions about this privacy policy:
- **Repository**: [https://github.com/yasu89/redmine-dify-plugin](https://github.com/yasu89/redmine-dify-plugin)
- **Issues**: [https://github.com/yasu89/redmine-dify-plugin/issues](https://github.com/yasu89/redmine-dify-plugin/issues)
- **Author**: yasu89

## Disclaimer

This Plugin is provided "as is" without warranties of any kind. Users are responsible for:
- Ensuring compliance with their organization's data policies
- Proper configuration and security of their Redmine instance
    - **Using HTTPS URLs for secure communication** - HTTP URLs will transmit data unencrypted
- Managing API key permissions and access controls
- Reviewing and understanding Redmine's own privacy policies

By using this plugin, you accept these terms and agree to this privacy policy.
