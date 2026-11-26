# Setup

## `uv`
Within Visual Studio, copy the command for your system into the terminal and press Enter.

**macOS and Linux**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell)**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Then **close the terminal and open a new one** (important) and check it works:
```bash
uv --version
```
You should see something like `uv 0.9.x` (the number may differ). If you see *"command not found"* or *"not recognized"*, see [Troubleshooting](troubleshooting.md).

![uv installation page](img/02_installation/web_uv_install.jpg)
*The official page lists the same commands, with tabs for macOS/Linux and Windows. Other ways to install (Homebrew, WinGet…): [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/).*


## VS Code extensions
1. Open VS Code. Click the **Extensions** icon in the left bar (four squares) or press `Ctrl + Shift + X` (`Cmd + Shift + X` on macOS).
2. Search for each of these and click **Install**:

| Search for | Publisher | What it is for | Link |
|---|---|---|---|
| **Python** | Microsoft | Python support | [Marketplace](https://marketplace.visualstudio.com/items?itemName=ms-python.python) |
| **Jupyter** | Microsoft | Open and run notebooks | [Marketplace](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter) |
| **GitHub Copilot** | GitHub | AI assistant (autocomplete and chat) | [Marketplace](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot) · [VS Code docs](https://code.visualstudio.com/docs/copilot/overview) |
| **Claude Code for VS Code** | Anthropic | Second AI assistant | [Marketplace](https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code) · [Docs](https://code.claude.com/docs/en/vs-code) |

*Claude Code:* install it only; credentials come later.

*Extensions icon, search box, **Install** button. The exact list of results may differ a little.*


*Choose *Claude Code for VS Code* published by **Anthropic**.*

*Check: `@installed` in the search box lists what you have. Jupyter (2) and Python (3) must be there.*

### Sign in to GitHub from VS Code
Click the **Accounts** icon (person icon, bottom of the left bar), or *Sign In* at the top. This window appears. Choose **Continue with GitHub**: your browser opens, click **Authorize Visual Studio Code**, then **Open Visual Studio Code** when the browser asks. Use the GitHub account with the student benefit. You never type a password in VS Code. (The same sign-in is used later to push to GitHub.)

*Choose *Continue with GitHub* (not a password).*

Written by Copilot and Xavi Baró.

