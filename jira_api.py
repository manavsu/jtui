from dataclasses import fields
from jira import JIRA
from jira.client import ResultList
from jira.resources import Issue
import tomllib

# Some Authentication Methods
with open("config.toml", "rb") as f:
    config = tomllib.load(f)

jir = JIRA(
    config["url"],
    token_auth=config["access_token"],
)


def issue(id: str):
    return jir.issue(id)


def children(issue: Issue):
    jql = f'"Epic Link" = {issue.key}'
    child_issues = jir.search_issues(jql, maxResults=False)
    assert isinstance(child_issues, ResultList)

    return child_issues


def memorized_jira():
    return config["jiras"]


def get_available_transitions(issue_key: str):
    """Get all available transitions for an issue."""
    issue = jir.issue(issue_key)
    transitions = jir.transitions(issue)

    print(f"Available transitions for {issue_key}:")
    for transition in transitions:
        print(f"  ID: {transition['id']}, Name: {transition['name']}")

    return transitions
