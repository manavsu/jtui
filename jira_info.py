from textual.app import App, ComposeResult
from textual.widgets import Tree, Footer, Static, Input, Button, Label, Markdown
from textual.containers import Horizontal, Container, Center, Vertical
from textual.screen import ModalScreen
from state import TuiState, TuiJira, to_md
from jira import Issue


class JiraInfo(Markdown):
    def update_content(self, tui_jira: TuiJira):
        self.update(to_md(tui_jira))
