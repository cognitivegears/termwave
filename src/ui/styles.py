"""CSS styles for TermWave UI."""

APP_CSS = """
Screen {
    background: #1f1d2e;
}

#app-grid {
    layout: grid;
    grid-size: 2 1;
    grid-columns: 1fr 4fr;
    height: 100%;
}

#sidebar {
    background: #2d2b3a;
    border-right: solid #3d3b4a;
}

#main-area {
    layout: grid;
    grid-size: 1 2;
    grid-rows: 1fr auto;
}

#history-list {
    background: #2d2b3a;
    border: none;
}

ListView > ListItem {
    layout: horizontal;
    background: #2d2b3a;
    margin: 1 0;
    height: auto;
    padding: 1;
    border-bottom: solid #3d3b4a;
}

ListView > ListItem:hover {
    background: #3d3b4a;
}

ListView > ListItem > Static {
    width: 80%;
    padding: 0 1;
}

.delete-btn {
    width: 20%;
    background: #e53935;
    color: white;
    margin-left: 1;
    min-width: 3;
    border: none;
}

.delete-btn:hover {
    background: #f44336;
}

#chat-container {
    padding: 1 2;
    background: #1f1d2e;
    overflow-y: auto;
    height: 100%;
}

#input-container {
    background: #1f1d2e;
    height: auto;
    padding: 1 2 2 2;
}

#user-input {
    border: solid #3d3b4a;
    background: #2d2b3a;
    color: #ffffff;
}

Markdown {
    margin: 1 0;
}
"""