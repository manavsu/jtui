"""Some simple authentication examples."""

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
    basic_auth=(config["email"], config["api_key"]),
)

# print(editor_epic.fields.summary)
# print(editor_epic.fields.status)
# print(editor_epic.fields.assignee)
#
# # jql = f'"Epic Link" = {editor_epic.key}'
# jql = f'"parent" = {editor_epic.key}'
#
# child_issues = jir.search_issues(jql, maxResults=False)
# assert isinstance(child_issues, ResultList)
#
# for i, issue in enumerate(child_issues):
#     print(
#         i,
#         issue.fields.priority,
#         issue.fields.summary,
#         issue.fields.status,
#         issue.fields.assignee,
#     )
#


def issue(id: str):
    return jir.issue(id)


def children(issue: Issue):
    jql = f'"parent" = {issue.key}'
    child_issues = jir.search_issues(jql, maxResults=False)
    assert isinstance(child_issues, ResultList)

    return child_issues


def memorized_jira():
    return config["jiras"]


def md(issue: Issue):
    md = [
        f"#{issue.fields.key} {issue.fields.summary}\n",
        "## Description\n",
        f"{issue.fields.description}\n",
    ]
    return "\n".join(md)
