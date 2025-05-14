from crewai_tools import GithubSearchTool

# Initialize the tool for semantic searches within a specific GitHub repository
tool = GithubSearchTool(
	github_repo='https://github.com/web2project/web2project',
	gh_token='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',
	content_types=['code', 'issue'] # Options: code, repo, pr, issue
)