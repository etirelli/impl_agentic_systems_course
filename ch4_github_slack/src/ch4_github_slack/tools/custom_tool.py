from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import requests
from github import Github
from github import Auth

class MyCustomToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    argument: str = Field('repo', description="Repository name in the format 'owner/repo'.")

class MyCustomTool(BaseTool):
    name: str = "MyCustomTool"
    description: str = (
        "This tool fetches issues from a GitHub repository. It takes a repository name in the format 'owner/repo' "
        "and returns a list of issues. The tool uses the GitHub API to fetch the issues."
        "Example: 'web2project/web2project' will return issues from the web2project repository."
    )
    args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self, argument: str) -> str:
        # Implementation goes here
        self.get_github_issues(argument)

    def get_github_issues(self, repo: str) -> str:
        """
        Fetches issues from a GitHub repository.
        
        Args:
            repo (str): The GitHub repository in the format 'owner/repo'.
        
        Returns:
            str: A string representation of the issues.
        """
        print(f"Fetching issues for repository: {repo}")
        url = f"https://api.github.com/repos/{repo}/issues"
        response = requests.get(url)
        
        if response.status_code == 200:
            issues = response.json()
            return str(issues)
        else:
            return f"Error fetching issues: {response.status_code}"
        

    def update_github_issues(self, repo: str, issueId: int, labels: dict) -> str:
        """
        Updates issues in a GitHub repository.
        
        Args:
            repo (str): The GitHub repository in the format 'owner/repo'.
            labels (dict): 
        Returns:
            str: A string representation of the issues.
        """
        token = os.environ.get("GITHUB_TOKEN")
        auth = Auth.Token(token)
        g = Github(auth=auth)
        repo = g.get_repo(repo)
        issue = repo.get_issue(number=issueId)
        issue.add_to_labels(labels)
