from textual.app import App, ComposeResult
from textual.widgets import Tree, Footer, Static, Input, Button, Label
from textual.containers import Horizontal, Container, Center, Vertical
from textual.screen import ModalScreen
from state import TuiState
from jira import Issue

state = TuiState()
print("State initialized with Jiras:", state.jiras)


class TreeApp(App):
    CSS = """
    Footer {
        border: round $accent;
        background: $background;
        height: 3;
    }

    * {
        background: $background;
    }

    Container {
        border: round $accent;
        padding: 1;
        height: 100%;
        }
    """
    BINDINGS = [("q", "quit", "Quit"), ("a", "add_jira", "+jira")]

    def action_add_jira(self):
        self.push_screen(JiraInputScreen(), callback=self._on_jira_input)

    def _on_jira_input(self, jira_key: str | None):
        print(f"Jira key entered: {jira_key}")
        if jira_key:
            state.add_jira(jira_key)
            tree = self.query_one("#jira_tree", expect_type=JiraTree)
            tree.load_tree()

    def compose(self) -> ComposeResult:
        jira_info = JiraInfo("Jira Info", id="jira_info")
        tree_container = Container()
        tree_container.border_title = "Jiras"
        description_container = Container()
        description_container.border_title = "Description"
        with Horizontal():
            with tree_container:
                yield JiraTree("", jira_info, id="jira_tree")
            with description_container:
                yield jira_info
        yield Footer()


class JiraInfo(Static):
    def update_content(self, tui_jira: Issue):
        text = "\n".join(
            [
                f"Key - {tui_jira.value.key}",
                f"Priority - {tui_jira.value.fields.priority}",
                f"Summary - {tui_jira.value.fields.summary}",
                f"Status - {tui_jira.value.fields.status}",
                f"Assignee - {tui_jira.value.fields.assignee}",
                f"Description - {tui_jira.value.fields.description}",
            ]
        )
        self.update(text)


class JiraTree(Tree):
    def __init__(self, label: str, jira_info: JiraInfo, id=None):
        super().__init__(label, id=id)
        self.jira_info = jira_info
        self.load_tree()
        self.show_root = False

    def load_tree(self):
        self.clear()
        self.root.expand()
        for jira in state.jiras:
            self.add_jira(self.root, jira)
        self.refresh(layout=True)

    def on_tree_node_highlighted(self, event):
        if not event.node.label:
            return
        state.selected = event.node.label
        self.jira_info.update_content(state.jira_map[str(state.selected)])
        self.refresh()

    def add_jira(self, node, issue):
        leaf = node.add_leaf(issue.value.key)
        if issue.children is not None:
            for child in issue.children:
                self.add_jira(leaf, child)
        leaf.expand()


class JiraInputScreen(ModalScreen[str]):
    CSS = """
    #popup {
        width: auto;
        height: auto;
        padding: 1 2;
        border: round $accent;
        background: $background;
        align: center middle;
        content-align: center middle;
    }
    """

    def compose(self) -> ComposeResult:
        with Center():
            with Vertical(id="popup"):
                yield Label("Enter new Jira key:")
                yield Input(placeholder="e.g. CCS-123", id="jira_input")
                yield Button("Submit", id="submit_btn")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        input_widget = self.query_one("#jira_input", Input)
        self.dismiss(input_widget.value.strip())

    def on_input_submitted(self, event: Input.Submitted) -> None:
        self.dismiss(event.value.strip())


if __name__ == "__main__":
    TreeApp().run()
