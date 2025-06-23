from collections.abc import Generator
from typing import Any
import requests
import json

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

class RedmineCreateIssueTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        # Get credentials
        redmine_host = self.runtime.credentials.get("redmine_host")
        api_key = self.runtime.credentials.get("api_key")
        
        if not redmine_host or not api_key:
            yield self.create_text_message("Error: Redmine host and API key are required")
            return
            
        # Remove trailing slash from host if present
        redmine_host = redmine_host.rstrip('/')
        
        # Get required parameters
        project_id = tool_parameters.get("project_id")
        subject = tool_parameters.get("subject")
        
        if not project_id:
            yield self.create_text_message("Error: Project ID is required")
            return
            
        if not subject:
            yield self.create_text_message("Error: Subject is required")
            return
        
        # Build API URL
        api_url = f"{redmine_host}/issues.json"
        
        # Prepare headers
        headers = {
            "X-Redmine-API-Key": api_key,
            "Content-Type": "application/json"
        }
        
        # Build issue data
        issue_data = {
            "project_id": project_id,
            "subject": subject
        }
        
        # Add optional parameters
        optional_params = [
            "description", "tracker_id", "status_id", "priority_id", 
            "assigned_to_id", "category_id", "fixed_version_id", "estimated_hours"
        ]
        
        for param in optional_params:
            value = tool_parameters.get(param)
            if value:
                # Convert numeric string parameters to integers where appropriate
                if param in ["tracker_id", "status_id", "priority_id", "assigned_to_id", "category_id", "fixed_version_id"]:
                    try:
                        issue_data[param] = int(value)
                    except ValueError:
                        yield self.create_text_message(f"Warning: Invalid {param} '{value}', must be numeric")
                        continue
                elif param == "estimated_hours":
                    try:
                        issue_data[param] = float(value)
                    except ValueError:
                        yield self.create_text_message(f"Warning: Invalid estimated_hours '{value}', must be numeric")
                        continue
                else:
                    issue_data[param] = value
        
        # Handle boolean parameter
        is_private = tool_parameters.get("is_private")
        if is_private is not None:
            issue_data["is_private"] = bool(is_private)
        
        # Handle project_id conversion
        try:
            issue_data["project_id"] = int(project_id)
        except ValueError:
            # Keep as string if it's a project identifier
            pass
        
        # Prepare request payload
        payload = {
            "issue": issue_data
        }
        
        try:
            # Make API request
            response = requests.post(api_url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 201:
                # Success - issue created
                data = response.json()
                result = data
                
                # Output success message and JSON data
                created_issue = data.get("issue", {})
                issue_id = created_issue.get("id")
                issue_subject = created_issue.get("subject")
                
                success_message = f"Issue created successfully: #{issue_id} - {issue_subject}"
                yield self.create_text_message(success_message)
                yield self.create_json_message(result)
                
            elif response.status_code == 422:
                # Validation errors
                try:
                    error_data = response.json()
                    errors = error_data.get("errors", [])
                    if errors:
                        error_message = "Validation errors:\n" + "\n".join([f"- {error}" for error in errors])
                        yield self.create_text_message(error_message)
                    else:
                        yield self.create_text_message("Validation error occurred but no details provided")
                except json.JSONDecodeError:
                    yield self.create_text_message("Validation error occurred")
                return
                
            elif response.status_code == 403:
                yield self.create_text_message("Error: Access denied. Check your API key permissions or project access")
                return
                
            elif response.status_code == 404:
                yield self.create_text_message("Error: Project not found. Check the project ID")
                return
                
            else:
                response.raise_for_status()
            
        except requests.exceptions.RequestException as e:
            yield self.create_text_message(f"Error connecting to Redmine: {str(e)}")
        except json.JSONDecodeError as e:
            yield self.create_text_message(f"Error parsing Redmine response: {str(e)}")
        except Exception as e:
            yield self.create_text_message(f"Unexpected error: {str(e)}")