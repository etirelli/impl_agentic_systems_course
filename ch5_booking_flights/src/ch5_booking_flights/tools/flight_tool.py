from crewai.tools import BaseTool
from typing import Type, Any
from pydantic import BaseModel, Field
import requests
import os

class FlightToolInput(BaseModel):
    """Input schema for FlightTool."""
    argument: str = Field(..., description="Description of the argument.")
    departure: str = ("This is our starting airport")
    arrival: str = ("This is our destination airport")

class FlightTool(BaseTool):
    name: str = "Flight Finder"
    description: str = (
        "This tool lets my agent query to find flights according to specific parameters."
    )
    args_schema: Type[BaseModel] = FlightToolInput

    def _run(self, **kwargs: Any) -> str:
        # Implementation goes here
        self.get_flights(kwargs["departure"], kwargs["arrival"])

    def get_flights(self, departure: str, arrival: str) -> str:
        """
        Fetches flights from the API
        
        Args:
            none
        
        Returns:
            str: A string representation of the flights.
        """
        print(f"Looking for flights from {departure} to {arrival}")
        api_key = os.getenv("SERPAPI_KEY")
        url = f"https://serpapi.com/search?engine=google_flights&departure_id={departure}&arrival_id={arrival}&api_key={api_key}&outbound_date=2025-06-01&return_date=2025-06-08"
        response = requests.get(url)
        
        if response.status_code == 200:
            issues = response.json()
            return str(issues)
        else:
            return f"Error fetching issues: {response.status_code}"