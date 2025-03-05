#GIT
from typing import Dict, Any
from openai import OpenAI
from .swarm_config import LLM_MODEL, TEMPERATURE, MAX_TOKENS
import json
import re

class BaseAgent:
    def __init__(self, name: str, instructions: str):
        self.name = name
        self.instructions = instructions
        self.ollama_client =  OpenAI(
            base_url="http://localhost:11434/v1",
            api_key="ollama"
        )
        
    async def run(self, messages: list) -> Dict[str, Any]:
        """Method to be overriden by child classes"""
        raise NotImplementedError
        
    def query_ollama(self, prompt) -> Dict[str, Any]:
        try:
            res = self.ollama_client.chat.completions.create(
                model = LLM_MODEL,
                messages = [
                    {"role": "system", "content": self.instructions},
                    {"role": "user", "content": prompt},
                ],
                temperature = TEMPERATURE,
                max_tokens = MAX_TOKENS
            )

            return res.choices[0].message.content
        except Exception as e:
            print("Error while querying Ollama: ", e)
            return None
            
    def parse_json(self, text: str) -> Dict[str, Any]:
            try:
                try:
                    return json.loads(text)
                except json.JSONDecodeError:
                    pass
                
                json_matches = re.findall(r'\{[^{}]*\}', text)
                
                for match in json_matches:
                    try:
                        return json.loads(match)
                    except json.JSONDecodeError:
                        continue
                
                try:
                    cleaned_text = text.replace("'", '"')
                    return json.loads(cleaned_text)
                except json.JSONDecodeError:
                    pass
                
                return {"error": "No valid JSON content found"}
            
            except Exception as e:
                print(f"Error parsing JSON: {e}")
                return {"error": f"Parsing error: {str(e)}"}