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

            if text.strip().startswith('```') and '```' in text:
                # Extract content between markdown code blocks
                match = re.search(r'```(?:json)?\s*\n([\s\S]+?)\n\s*```', text)
                if match:
                    text = match.group(1)
                else:
                    # If regex fails, just strip the backticks
                    text = text.strip().strip('`')
            # Replace "not stated" with "not_stated" before parsing
            text = text.replace('"not stated"', '"not_stated"')

            return json.loads(text)
        
        except Exception as e:
            print(f"Error parsing JSON-like content: {e} in text: {text}") 
            return None
        

        

