from typing import Dict, Any
from datetime import datetime
import json
from .base_agent import BaseAgent

class ScreenerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Screener",
            instructions=""" Screen candidates based on :
            - Qualifications
            - Relevant experience
            - Skills match percentage
            - Cultural fit indicators
            - Red flags or concerns
            Provide comprehensive screening reports."""
        )

    async def run(self, messages:list)-> Dict[str, Any]:
        """"Screen the candidate"""
        print("👥 Screener: Conducting initial screening")

        try:
            workflow_context = json.loads(messages[-1]["content"])
        except json.JSONDecodeError:
            return {"error": "Invalid JSON content in messages"}

        #query the model
        screening_results = self.query_model(str(workflow_context))

        #generate dynamic timestamp
        screening_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return {
            "screening report": screening_results,
            "screening_timestamp": screening_timestamp,
            "screening_score": 85   
        }