from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import requests

class SlackToolInput(BaseModel):
    """Input schema for SlackTool."""
    slack_channel: str = ("This is our target slack channel.")
    message: str = ("This is the message to post.")

class SlackTool(BaseTool):
    name: str = "SlackTool"
    description: str = (
        "This tool posts issues to a Slack channel."
    )
    argument: str = Field('slack_channel', description="This is the Slack channel ID where the message will be posted.")
    argument: str = Field('message', description="This is the message that will be posted to the Slack channel.")
    args_schema: Type[BaseModel] = SlackToolInput

    def _run(self, slack_channel: str, message: str) -> str:
        # Implementation goes here
        self.post_to_channel(slack_channel, message)
    
    def post_to_channel(self, slack_channel: str, message: str) -> str:
        token = os.environ.get("SLACK_BOT_TOKEN")

        """
        Posts a message to a Slack channel
        """
        url = "https://slack.com/api/chat.postMessage"
        headers = {
            "Content-type": "application/json; charset=utf-8",
            "Authorization": f"Bearer {token}"
        }
        data = {
            "channel": slack_channel,
            "text": message
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code != 200:
            raise Exception(f"Failed to post message: {response.text}")
        # Assuming the response is successful, return a success message        
        return "Message posted successfully to Slack channel."
