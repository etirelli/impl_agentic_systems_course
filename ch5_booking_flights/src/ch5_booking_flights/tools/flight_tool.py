from crewai.tools import BaseTool
from typing import Type, Any
from pydantic import BaseModel, Field
import requests
import os

class FlightToolInput(BaseModel):
    """Input schema for FlightTool."""
    departure: str = ("This is our starting airport")
    arrival: str = ("This is our destination airport")
    departure_date: str = ("This the date of the outbound flight")
    return_date: str = ("This is our return date")

class FlightTool(BaseTool):
    name: str = "Flight Finder"
    description: str = (
        "This tool lets my agent query to find flights according to specific parameters."
    )
    args_schema: Type[BaseModel] = FlightToolInput

    def _run(self, **kwargs: Any) -> str:
        # Implementation goes here
        self.get_flights(kwargs["departure"], kwargs["arrival"], kwargs["departure_date"], kwargs["return_date"])

    def get_flights(self, departure: str, arrival: str, departure_date: str, return_date: str) -> str:
        """
        Fetches flights from the API
        
        Args:
            none
        
        Returns:
            str: A string representation of the flights.
        """
        print(f"Looking for flights from {departure} to {arrival} leaving on {departure_date} and returning on {return_date}")

        api_key = os.getenv("SERPAPI_KEY")
        url = f"https://serpapi.com/search?engine=google_flights&departure_id={departure}&arrival_id={arrival}&api_key={api_key}&outbound_date={departure_date}&return_date={return_date}"
        response = requests.get(url)
        
        if response.status_code == 200:
            issues = response.json()
            return str(issues)
        else:
            return f"Error fetching issues: {response.status_code}"