from dotenv import load_dotenv
import os
from langchain.tools import tool
from jira import JIRA


# Load environment variables from .env file
load_dotenv(override=True)

def get_jira_client():
    """
    Returns a JIRA client authenticated with environment variables:
    JIRA_URL, JIRA_USER, JIRA_TOKEN.
    """
    jira_url = os.environ.get("JIRA_URL")
    jira_user = os.environ.get("JIRA_USER")
    jira_token = os.environ.get("JIRA_TOKEN")
    if not (jira_url and jira_user and jira_token):
        raise Exception("Jira credentials not set in environment variables.")
    return JIRA(server=jira_url, basic_auth=(jira_user, jira_token))

@tool
def authenticate_jira(_: str = "") -> str:
    """
    Authenticates with Jira and returns a success or error message.
    """
    try:
        client = get_jira_client()
        user = client.current_user()
        return f"✅ Jira authentication successful. Logged as: {user}"
    except Exception as e:
        return f"❌ Jira authentication failed: {str(e)}"

@tool
def create_jira_issue(data: str) -> str:
    """
    Creates a Jira issue. Input is a pipe-separated string:
    'project:PC | summary:Test ticket | description:Ticket body | issuetype:Task'
    Returns Jira issue key and summary.
    """
    try:
        parts = dict(p.strip().split(":", 1) for p in data.split("|"))
        project = parts.get("project", "PC").strip()
        summary = parts["summary"].strip()
        description = parts.get("description", "").strip()
        issuetype = parts.get("issuetype", "Task").strip()
        client = get_jira_client()
        issue = client.create_issue(fields={
            'project': {'key': project},
            'summary': summary,
            'description': description,
            'issuetype': {'name': issuetype}
        })
        return f"✅ Issue created: [{issue.key}] {summary}"
    except Exception as e:
        return f"❌ Error creating Jira issue: {str(e)}"

@tool
def search_jira_issues(query: str) -> str:
    """
    Searches for Jira issues using JQL. Example input:
    'project=PC AND status!=Done ORDER BY created DESC'
    Returns up to 5 issues with key and summary.
    """
    try:
        client = get_jira_client()
        issues = client.search_issues(query, maxResults=5)
        if not issues:
            return "🔎 No issues found."
        result = []
        for i in issues:
            result.append(f"{i.key}: {i.fields.summary}") # type: ignore
        return "\n".join(result)
    except Exception as e:
        return f"❌ Error searching Jira: {str(e)}"

@tool
def add_jira_comment(data: str) -> str:
    """
    Adds a comment to a Jira issue. Input is a pipe-separated string:
    'issue_key:PC-123 | comment:This is a comment'
    Returns confirmation.
    """
    try:
        parts = dict(p.strip().split(":", 1) for p in data.split("|"))
        issue_key = parts["issue_key"].strip()
        comment = parts["comment"].strip()
        client = get_jira_client()
        client.add_comment(issue_key, comment)
        return f"💬 Comment added to {issue_key}."
    except Exception as e:
        return f"❌ Error adding comment: {str(e)}"