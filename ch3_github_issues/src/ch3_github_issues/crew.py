from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from ch3_github_issues.tools.custom_tool import get_github_issues, update_github_issues
import os

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class Ch3GithubIssues():
    """Ch3GithubIssues crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools    
    @agent
    def team_lead(self) -> Agent:
        # Configure Claude model from environment variables
        claude_llm = LLM(
            model=os.getenv("MODEL", "anthropic/claude-sonnet-4-5-20250929"),
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )

        return Agent(
            config=self.agents_config['team_lead'],
            tools=[get_github_issues, update_github_issues],
            llm=claude_llm,
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def retrieval_task(self) -> Task:
        return Task(
            config=self.tasks_config['retrieval_task'],
            output_file='output/issues.md'
        )
    
    @task
    def categorization_task(self) -> Task:
        return Task(
            config=self.tasks_config['categorization_task'],
            output_file='output/categorized.md'
        )
    
    @task
    def update_task(self) -> Task:
        return Task(
            config=self.tasks_config['update_task']
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Ch3GithubIssues crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        # Configure Claude model for the entire crew
        claude_llm = LLM(
            model=os.getenv("MODEL", "anthropic/claude-sonnet-4-5-20250929"),
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            llm=claude_llm,  # This LLM will be used for planning as well
            planning_llm=claude_llm,
            verbose=True,
            planning=True  # Enabled planning with Claude model
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
    