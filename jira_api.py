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

