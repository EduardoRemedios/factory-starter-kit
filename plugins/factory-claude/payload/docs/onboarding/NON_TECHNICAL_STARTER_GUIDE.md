# Non-Technical Starter Guide

> Audience: a founder, product owner, operator, or domain expert who wants to use Factory with an AI coding agent without becoming a developer first.

## 1. What This Guide Helps You Do

This guide helps you create a local project folder, choose an AI coding tool, copy the Factory Starter Kit into the project, and start the first Factory planning run for a new application.

Factory is the planning and control layer. The AI coding tool is the worker. Your job is to give clear goals, approve scope, and review the Factory pack before implementation starts.

## 2. What You Need

You only need one AI coding tool to start.

Recommended beginner choices:

| Choice | Best For | Notes |
|--------|----------|-------|
| Cursor | People who prefer a code editor with chat built in | Install the desktop app, open your project folder, use the agent chat. |
| Claude Desktop | People who prefer a normal chat app | Useful for planning and review. For local file edits, pair it with Claude Code or another coding agent. |
| Claude Code CLI | People comfortable pasting one command into Terminal or PowerShell | Strong local coding agent. Runs inside the project folder. |
| Codex CLI or Codex app | People using OpenAI coding tools | Good for local repo work when opened in the project folder. |

You do not need all of these tools. Pick one primary tool and add another later only if you have a reason.

## 3. Install One AI Coding Tool

Use only official download pages.

Official links:
- Claude apps: https://claude.com/download
- Claude Code CLI: https://code.claude.com/docs/en/getting-started
- Cursor: https://cursor.com/download
- Codex CLI: https://developers.openai.com/codex/cli
- Git: https://git-scm.com/downloads

### Option A: Cursor

1. Go to https://cursor.com/download.
2. Download the version for your computer.
3. Install Cursor.
4. Open Cursor.
5. Choose `Open Folder` and select your project folder.
6. Use Cursor's agent chat with the setup prompt in section 7.

### Option B: Claude Desktop

1. Go to https://claude.com/download.
2. Download the macOS or Windows app.
3. Install and sign in.
4. Use Claude Desktop for planning prompts, brief writing, and reviewing Factory artifacts.
5. If you need Claude to edit local project files directly, also install Claude Code CLI or use Cursor/Codex for the local setup step.

### Option C: Claude Code CLI

macOS:

```bash
curl -fsSL https://claude.ai/install.sh | bash
claude --version
```

Windows PowerShell:

```powershell
irm https://claude.ai/install.ps1 | iex
claude --version
```

After installation, open Terminal or PowerShell inside your project folder and run:

```bash
claude
```

### Option D: Codex CLI

macOS or Linux:

```bash
curl -fsSL https://chatgpt.com/codex/install.sh | sh
codex
```

Windows users should follow the current Windows setup guide linked from https://developers.openai.com/codex/cli.

## 4. Create Your Project Folder

Use a short folder name with no spaces. Examples:
- `my-new-app`
- `customer-portal`
- `field-ops-tool`

### macOS, No Terminal

1. Open Finder.
2. Open your home folder.
3. Create a folder called `Projects`.
4. Inside `Projects`, create a folder for your app, for example `my-new-app`.
5. The project path will look like:

```text
/Users/YOUR_NAME/Projects/my-new-app
```

### macOS, Terminal

```bash
mkdir -p ~/Projects/my-new-app
cd ~/Projects/my-new-app
```

### Windows, No Terminal

1. Open File Explorer.
2. Open your user folder.
3. Create a folder called `Projects`.
4. Inside `Projects`, create a folder for your app, for example `my-new-app`.
5. The project path will look like:

```text
C:\Users\YOUR_NAME\Projects\my-new-app
```

### Windows, PowerShell

```powershell
mkdir $HOME\Projects\my-new-app
cd $HOME\Projects\my-new-app
```

If the setup agent later says `git` is missing, install Git from https://git-scm.com/downloads or ask the agent to use GitHub's ZIP download instead of `git clone`.

## 5. Open The Folder In Your AI Tool

Cursor:
- Open Cursor.
- Click `Open Folder`.
- Select your app folder.
- Paste the setup prompt from section 7 into the agent chat.

Claude Code CLI:
- Open Terminal or PowerShell.
- Go to your app folder.
- Run `claude`.
- Paste the setup prompt from section 7.

Codex CLI:
- Open Terminal or PowerShell.
- Go to your app folder.
- Run `codex`.
- Paste the setup prompt from section 7.

## 6. Decide What You Are Creating

Before asking the agent to start Factory, write three plain-language sentences:

```text
The app is for:

The main problem it solves:

The first useful version should let a user:
```

Example:

```text
The app is for small property managers.

The main problem it solves: they track maintenance requests in scattered texts, emails, and spreadsheets.

The first useful version should let a user create a maintenance request, assign it to a vendor, track status, and see overdue work.
```

This is enough for a first Factory planning conversation. The Factory run will harden it before implementation.

## 7. Setup Prompt To Paste Into An Agent

Paste this into Cursor, Claude Code, Codex, or another local coding agent after opening your project folder:

```text
You are working in my local application project folder.

Goal:
Set up the Factory Starter Kit in this project so we can use Factory to design and build a new application safely.

Factory Starter Kit source:
https://github.com/EduardoRemedios/factory-starter-kit.git

My app idea:
[PASTE YOUR THREE SENTENCES HERE]

Instructions:
1. Confirm the absolute path of the current project folder.
2. Clone or fetch the Factory Starter Kit into a temporary location. If git is not installed, download the starter kit ZIP from GitHub and unpack it into a temporary location instead.
3. Copy the Factory scaffolding into this project folder, preserving the starter kit structure, especially:
   - AGENTS.md
   - docs/Factory/
   - docs/onboarding/
   - docs/PROJECT_STATE.md
   - docs/ROADMAP.md
   - docs/CHANGELOG.md
   - scripts/
   - requirements.txt
   - tools/ if present
   - tests/fixtures used by Factory helper scripts if present
4. Do not delete existing app files.
5. Do not overwrite existing non-Factory files unless I explicitly approve it.
6. If a file conflict exists, stop and show me the conflict before changing it.
7. Install only the dependencies already declared by the starter kit.
8. Run these checks if the copied scripts are present. If `python3` is not available on Windows, try `py -m pip install -r requirements.txt` instead of the first command:
   - python3 -m pip install -r requirements.txt
   - bash scripts/knowledge_lint.sh
   - ./scripts/factoryctl context-index
9. Adapt only the minimum project context needed for a first Factory run:
   - docs/PROJECT_STATE.md
   - docs/ROADMAP.md
   - docs/CHANGELOG.md
   - AGENTS.md if it still describes the starter kit instead of this app
10. Keep unknown product details as explicit placeholders. Do not invent requirements.

After setup, summarize:
- files and folders copied
- files changed
- commands run
- checks that passed or failed
- conflicts or missing tools
- the exact next prompt I should paste to start the first Factory planning run

Guardrails:
- Keep changes small.
- Preserve Factory's fail-closed behavior.
- Do not start implementation yet.
- Do not create a product plan outside the Factory docs.
```

## 8. First Factory Planning Prompt

After the setup agent says the starter kit is installed and checks pass, paste this:

```text
Start a new Factory planning run for this app idea.

Execution Mode: PLANNING_ONLY

App idea:
[PASTE YOUR THREE SENTENCES HERE]

Use the repo's Factory process. Read the required context first, create the run root, write raw_brief.md, run knowledge lint, refresh the context index, generate the Stage A recall report, and proceed through the Factory planning stages until the final pack is ready for human review.

Do not implement code yet. The output I want is a reviewed Factory pack that tells me what should be built, what is out of scope, what risks exist, and how we will verify the first implementation sprint.
```

Use `PLANNING_ONLY` for the first run. Switch to `EXECUTION_ENABLED` only after you understand the pack and intentionally want the agent to build from it.

## 9. Human Review Checklist

Before approving any implementation, check:

- Does the pack describe the app you actually want?
- Is anything important listed as out of scope by mistake?
- Are risky assumptions called out instead of hidden?
- Are acceptance criteria written in plain language?
- Are there verification steps, not just feature descriptions?
- Did the agent avoid starting code before you approved implementation?

If any answer is unclear, ask the agent to revise the Factory pack before coding starts.

## 10. Simple Safety Rules

- Download tools only from official websites.
- Keep your project folder in a place you recognize.
- Do not paste passwords, private keys, banking data, or customer secrets into an agent chat.
- Ask the agent to stop before overwriting files you do not recognize.
- Use Factory planning first, implementation second.
- Keep the final Go or No-go decision human-owned.
