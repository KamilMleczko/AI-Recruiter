import json
from typing import Dict, Any
import re
def parse_json( text: str) -> Dict[str, Any]:
        try:
            # First, try to parse the entire input as JSON
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                pass
            
            # If that fails, look for JSON-like structures
            # Use a less complex regex to find potential JSON
            json_matches = re.findall(r'\{[^{}]*\}', text)
            
            for match in json_matches:
                try:
                    return json.loads(match)
                except json.JSONDecodeError:
                    continue
            
            # If no valid JSON found, try to extract JSON-like content
            try:
                # Remove single quotes and try to parse
                cleaned_text = text.replace("'", '"')
                return json.loads(cleaned_text)
            except json.JSONDecodeError:
                pass
            
            return {"error": "No valid JSON content found"}
        
        except Exception as e:
            print(f"Error parsing JSON: {e}")
            return {"error": f"Parsing error: {str(e)}"}
