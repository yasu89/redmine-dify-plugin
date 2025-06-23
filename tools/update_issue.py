from collections.abc import Generator
from typing import Any
import requests
import json

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

class RedmineUpdateIssueTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        # Get credentials
        redmine_host = self.runtime.credentials.get("redmine_host")
        api_key = self.runtime.credentials.get("api_key")
        
        if not redmine_host or not api_key:
            yield self.create_text_message("Error: Redmine host and API key are required")
            return
            
        # Remove trailing slash from host if present
        redmine_host = redmine_host.rstrip('/')
        
        # Get required parameter
        issue_id = tool_parameters.get("issue_id")
        
        if not issue_id:
            yield self.create_text_message("Error: Issue ID is required")
            return
            
        # Validate issue ID is numeric
        try:
            int(issue_id)
        except ValueError:
            yield self.create_text_message("Error: Issue ID must be a numeric value")
            return
        
        # Build API URL
        api_url = f"{redmine_host}/issues/{issue_id}.json"
        
        # Prepare headers
        headers = {
            "X-Redmine-API-Key": api_key,
            "Content-Type": "application/json"
        }
        
        # Build issue data
        issue_data = {}
        
        # Check if there are any parameters to update
        update_params = [
            "subject", "description", "notes", "project_id", "tracker_id", "status_id", 
            "priority_id", "assigned_to_id", "category_id", "fixed_version_id", 
            "estimated_hours", "done_ratio"
        ]
        
        has_updates = False
        
        for param in update_params:
            value = tool_parameters.get(param)
            if value is not None and value != "":
                has_updates = True
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
                elif param == "done_ratio":
                    try:
                        done_ratio_int = int(value)
                        if 0 <= done_ratio_int <= 100:
                            issue_data[param] = done_ratio_int
                        else:
                            yield self.create_text_message(f"Warning: Invalid done_ratio '{value}', must be between 0 and 100")
                            continue
                    except ValueError:
                        yield self.create_text_message(f"Warning: Invalid done_ratio '{value}', must be numeric")
                        continue
                elif param == "project_id":
                    # Try to convert to integer, but keep as string if it's a project identifier
                    try:
                        issue_data[param] = int(value)
                    except ValueError:
                        issue_data[param] = value
                else:
                    issue_data[param] = value
        
        # Handle boolean parameters
        private_notes = tool_parameters.get("private_notes")
        if private_notes is not None:
            issue_data["private_notes"] = bool(private_notes)
            has_updates = True
            
        is_private = tool_parameters.get("is_private")
        if is_private is not None:
            issue_data["is_private"] = bool(is_private)
            has_updates = True
        
        if not has_updates:
            yield self.create_text_message("Error: No parameters provided for update. At least one field must be specified.")
            return
        
        # Prepare request payload
        payload = {
            "issue": issue_data
        }
        
        try:
            # Make API request
            response = requests.put(api_url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                # Success - issue updated
                success_message = f"Issue #{issue_id} updated successfully"
                yield self.create_text_message(success_message)
                
                # Try to get the updated issue details
                try:
                    get_response = requests.get(api_url, headers=headers, timeout=30)
                    if get_response.status_code == 200:
                        updated_data = get_response.json()
                        yield self.create_json_message(updated_data)
                    else:
                        yield self.create_json_message({"message": f"Issue #{issue_id} updated successfully", "updated_fields": list(issue_data.keys())})
                except:
                    yield self.create_json_message({"message": f"Issue #{issue_id} updated successfully", "updated_fields": list(issue_data.keys())})
                
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
                yield self.create_text_message("Error: Access denied. Check your API key permissions or issue access")
                return
                
            elif response.status_code == 404:
                yield self.create_text_message(f"Error: Issue #{issue_id} not found")
                return
                
            else:
                response.raise_for_status()
            
        except requests.exceptions.RequestException as e:
            yield self.create_text_message(f"Error connecting to Redmine: {str(e)}")
        except json.JSONDecodeError as e:
            yield self.create_text_message(f"Error parsing Redmine response: {str(e)}")
        except Exception as e:
            yield self.create_text_message(f"Unexpected error: {str(e)}")