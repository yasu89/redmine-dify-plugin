from collections.abc import Generator
from typing import Any
import requests
import json

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

class RedmineTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        # Get credentials
        redmine_host = self.runtime.credentials.get("redmine_host")
        api_key = self.runtime.credentials.get("api_key")
        
        if not redmine_host or not api_key:
            yield self.create_text_message("Error: Redmine host and API key are required")
            return
            
        # Remove trailing slash from host if present
        redmine_host = redmine_host.rstrip('/')
        
        # Build API URL
        api_url = f"{redmine_host}/issues.json"
        
        # Prepare headers
        headers = {
            "X-Redmine-API-Key": api_key,
            "Content-Type": "application/json"
        }
        
        # Build query parameters
        params = {}
        
        if tool_parameters.get("project_id"):
            params["project_id"] = tool_parameters["project_id"]
            
        if tool_parameters.get("status_id"):
            params["status_id"] = tool_parameters["status_id"]
            
        if tool_parameters.get("assigned_to_id"):
            params["assigned_to_id"] = tool_parameters["assigned_to_id"]
            
        # Set limit (default 25, max 100)
        limit = tool_parameters.get("limit", "25")
        try:
            limit_int = int(limit)
            if limit_int > 100:
                limit_int = 100
            elif limit_int < 1:
                limit_int = 25
            params["limit"] = str(limit_int)
        except ValueError:
            params["limit"] = "25"
        
        try:
            # Make API request
            response = requests.get(api_url, headers=headers, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            result = data
            
            # Output JSON as text string
            yield self.create_text_message(json.dumps(result, ensure_ascii=False))
            yield self.create_json_message(result)
            
        except requests.exceptions.RequestException as e:
            yield self.create_text_message(f"Error connecting to Redmine: {str(e)}")
        except json.JSONDecodeError as e:
            yield self.create_text_message(f"Error parsing Redmine response: {str(e)}")
        except Exception as e:
            yield self.create_text_message(f"Unexpected error: {str(e)}")
