from jira_api import issue, children, memorized_jira
from dataclasses import dataclass
from jira import Issue
from typing import List


@dataclass
class TuiJira:
    value: Issue
    children: List | None

    @staticmethod
    def from_issue(issue, children):
        return TuiJira(
            value=issue,
            children=children,
        )


class TuiState:
    def __init__(self):
        self.jiras = []
        self.selected = None
        self.jira_map = {}
        for jira_key in memorized_jira():
            self.add_jira(jira_key)

    def add_jira(self, jira_key: str):
        if jira_key not in self.jiras:
            j = self.build_jira(issue(jira_key))
            self.jiras.append(j)

    def build_jira(self, issue) -> TuiJira:
        child_issues = children(issue)
        if child_issues is None:
            child_jiras = None
        else:
            child_jiras = [self.build_jira(child) for child in child_issues]
        tui_jira = TuiJira.from_issue(issue, child_jiras)
        self.jira_map[issue.key] = tui_jira
        return tui_jira


def to_md(tui_jira: TuiJira):
    issue = tui_jira.value
    md = [
        f"## {issue.key} {issue.fields.summary}",
        f"Priority: [{issue.fields.priority}]\n",
        f"Status: {issue.fields.status}\n",
        f"Assignee: {issue.fields.assignee}\n",
        "### Description",
        f"{issue.fields.description}",
    ]
    return "\n".join(md)
