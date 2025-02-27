#GIT
from typing import Dict, Any
from openai import OpenAI
from swarm_config import LLM_MODEL, TEMPERATURE, MAX_TOKENS
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
                match = re.search(r"\{.*\}", text, re.DOTALL)
                
                if match:
                    json_str = match.group(0)  #get the matched JSON string
                    return json.loads(json_str)
                
                return {"error": "No JSON content found"}

            except json.JSONDecodeError as e:
                print(f"Invalid JSON: {e}")
                return None