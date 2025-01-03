from typing import Dict, Any
import json
from openai import AzureOpenAI

class BaseAgent:
    def __init__(self, name: str, instructions:str):
        self.name = name
        self.instructions = instructions
        self.openai = AzureOpenAI()

    async def run(self, messages:list) -> Dict[str, Any]:
        """Default run method to be overridden by child classes"""
        raise NotImplementedError("subclass must implement run()")
    
    def query_model(self, prompt:str) -> str:
        """"Query the LLM with the given prompt"""
        try:
            response = self.openai.query(prompt)
            model="gpt-4"
            messages = [
                {"role":"system", "content": self.instructions},
                {"role":"user", "content":prompt},
            ]
            temperature = 0.7
            max_tokens = 2000

            return response
        except Exception as e:
            print(f"Error querying model: {str(e)}")
            raise

    def parse_json_safely(self, text: str) -> Dict[str, Any]:
        """"Safely parse JSON from text, handling potential errors"""
        try:
            start = text.find("{")
            end = text.rfind("}") 
            if start != -1 and end != -1:
                json_str = text[start : end+1]
                return json.loads(json_str)
            return {"error" : "No JSON content found"}
        except json.JSONDecodeError:
            return {"error": "Invalid JSON content"}