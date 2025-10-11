from crewai.tools import tool
from typing import Type
from pydantic import BaseModel, Field
import requests
import os
from github import Github
from github import Auth


@tool("get_github_issues")
def get_github_issues(repo: str) -> str:
    """
    Fetches issues from a GitHub repository. It takes a repository name in 
    the format 'owner/repo' and returns a list of issues. The tool uses the 
    GitHub API to fetch the issues.
    Example: 'web2project/web2project' will return issues from the web2project repository.
    
    Args:
        repo: The GitHub repository in the format 'owner/repo'.
    
    Returns:
        str: A string representation of the issues.
    """
    print(f"Fetching issues for repository: {repo}")
    url = f"https://api.github.com/repos/{repo}/issues"
    response = requests.get(url)
    
    if response.status_code == 200:
        # get only the first 5 issues, to avoid hitting the rate limit of the LLM
        issues = response.json()[:5]
        return str(issues)
    else:
        return f"Error fetching issues: {response.status_code}"
    

@tool("update_github_issues")
def update_github_issues(repo: str, issueId: int, labels: list) -> str:
    """
    Updates issues in a GitHub repository.
    
    Args:
        repo (str): The GitHub repository in the format 'owner/repo'
        issueId (int): the id of the issue to update
        labels (list): the labels to add to the issue
    """
    #token = os.environ.get("GITHUB_TOKEN")
    #auth = Auth.Token(token)
    #g = Github(auth=auth)
    #repo = g.get_repo(repo)
    #issue = repo.get_issue(number=issueId)
    #issue.add_to_labels(labels)

    #lets pretend we are updating the issue with the labels
    print(f"Updating issue {issueId} with labels: {labels}")
