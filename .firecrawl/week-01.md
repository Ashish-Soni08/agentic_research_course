[Skip to content](https://courses.osc.earth/agentic-research/week-01/#week-1-git-github-and-the-command-line)

[Edit this page](https://github.com/OpenScience-Collective/edit/master/docs/agentic-research/week-01.md "Edit this page") [View source of this page](https://github.com/OpenScience-Collective/raw/master/docs/agentic-research/week-01.md "View source of this page")

# Week 1: Git, GitHub, and the Command Line [¶](https://courses.osc.earth/agentic-research/week-01/\#week-1-git-github-and-the-command-line "Permanent link")

## Overview [¶](https://courses.osc.earth/agentic-research/week-01/\#overview "Permanent link")

This session does double duty: it teaches the foundational tools (git, terminal, GitHub) and sets the stage for the entire course. The core argument is simple: AI coding agents like Claude Code are extraordinarily powerful, and that power is exactly why you need version control, quality assurance (QA), and structured workflows.

Learning Objectives

- Describe the current landscape of AI coding agents and how they fit into research workflows
- Explain why AI-powered productivity demands stronger quality assurance, not weaker
- Navigate the filesystem using `cd`, `ls`, `pwd`, `mkdir`
- Initialize a git repository, stage files, commit, push to GitHub
- Understand the difference between `git` (version control) and `gh` (GitHub CLI)
- Create branches, pull requests, and issues on GitHub

Agentic Research Course - Week 1: Version Control, Git and GitHub - YouTube

Tap to unmute

[Agentic Research Course - Week 1: Version Control, Git and GitHub](https://www.youtube.com/watch?v=t7x8dU8_V3U) [Neuromechanist](https://www.youtube.com/channel/UCDJrOhQfKvdEYXX7L_kSIKA)

![thumbnail-image](https://yt3.ggpht.com/zDL-FLmF_JsGjqIhdxGcsatjaOq-WrbWAl6w9E1wuppBS1F-H9JCdkLl1rBcXfRMZMtezC8Z=s68-c-k-c0x00ffffff-no-rj)

Neuromechanist63 subscribers

[Watch on](https://www.youtube.com/watch?v=t7x8dU8_V3U)

## Slides [¶](https://courses.osc.earth/agentic-research/week-01/\#slides "Permanent link")

Agentic Research Course

Loading presentation...

# Agentic Research Course

Week 1: Git, GitHub, and the Command Line

**Seyed Yahya Shirazi, Ph.D.**

Assistant Project Scientist, Swartz Center for Computational Neuroscience

UC San Diego

[Open Science Collective](https://osc.earth/)

Resume presentation

Agentic Research Course Week 1: Git, GitHub, and the Command Line Seyed Yahya Shirazi, Ph.D. Assistant Project Scientist, Swartz Center for Computational Neuroscience UC San Diego Open Science Collective Welcome everyone to the first session of Agentic Research Course. I'm Yahya Shirazi, and over the next 10 weeks we're going to transform how you do research.

### Keyboard Shortcuts

`S`Speaker notes (popup)

`O`Slide overview

`F`Fullscreen

`Esc`Exit overview / pause

`← →`Navigate slides

`Home`First slide

`End`Last slide

`B / .`Blackout screen

`?`Toggle this help

Press `?` or `Esc` to close

?

Use arrow keys to navigate. Press `F` for fullscreen, `?` for shortcuts.

* * *

## Setup Guide [¶](https://courses.osc.earth/agentic-research/week-01/\#setup-guide "Permanent link")

A step-by-step walkthrough for getting your research computing environment ready. No prior coding experience is assumed.

### 1\. Open Your Terminal [¶](https://courses.osc.earth/agentic-research/week-01/\#1-open-your-terminal "Permanent link")

Every operating system has a built-in terminal. This is where you type commands instead of clicking buttons.

[macOS](https://courses.osc.earth/agentic-research/week-01/#__tabbed_1_1)[Linux](https://courses.osc.earth/agentic-research/week-01/#__tabbed_1_2)[Windows](https://courses.osc.earth/agentic-research/week-01/#__tabbed_1_3)

- Open Spotlight (`Cmd` + `Space`), type `Terminal`, press Enter
- Or find it in Applications > Utilities > Terminal

- Press `Ctrl` + `Alt` + `T` (most distributions)
- Or search for "Terminal" in your application launcher

Install [Windows Subsystem for Linux (WSL)](https://learn.microsoft.com/en-us/windows/wsl/install). Open PowerShell as Administrator and run:

```
wsl --install
```

Restart your computer, then open "Ubuntu" from the Start menu. WSL gives you a full Linux terminal inside Windows.

Once your terminal is open, verify it works:

```
pwd    # Where am I?
ls     # What files are here?
ls -la # List with details
```

### 2\. Install a Package Manager [¶](https://courses.osc.earth/agentic-research/week-01/\#2-install-a-package-manager "Permanent link")

Package managers let you install software from the command line. Think of them as an app store for developer tools.

[macOS](https://courses.osc.earth/agentic-research/week-01/#__tabbed_2_1)[Linux](https://courses.osc.earth/agentic-research/week-01/#__tabbed_2_2)[Windows](https://courses.osc.earth/agentic-research/week-01/#__tabbed_2_3)

Install [Homebrew](https://brew.sh/), the standard macOS package manager:

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Follow the on-screen instructions, then verify:

```
brew --version
```

You already have `apt`. Update it:

```
sudo apt update
```

Your WSL Ubuntu terminal already has `apt` (see Step 1). Update it:

```
sudo apt update
```

### 3\. Install Git and the GitHub CLI [¶](https://courses.osc.earth/agentic-research/week-01/\#3-install-git-and-the-github-cli "Permanent link")

You need two command-line tools: `git` for version control and `gh` (the GitHub CLI) for interacting with GitHub.

[macOS](https://courses.osc.earth/agentic-research/week-01/#__tabbed_3_1)[Linux](https://courses.osc.earth/agentic-research/week-01/#__tabbed_3_2)[Windows](https://courses.osc.earth/agentic-research/week-01/#__tabbed_3_3)

```
brew install git gh
```

```
sudo apt install git gh
```

In your WSL Ubuntu terminal:

```
sudo apt install git gh
```

Verify both:

```
git --version
gh --version
```

Configure your git identity (use the same email you will use for GitHub):

```
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 4\. Understanding `git` vs `gh` [¶](https://courses.osc.earth/agentic-research/week-01/\#4-understanding-git-vs-gh "Permanent link")

These two tools work together but handle different things:

|  | `git` | `gh` |
| --- | --- | --- |
| **What it is** | Version control system | GitHub CLI |
| **What it does** | Tracks file changes, manages history | Manages GitHub features (issues, PRs, repos) |
| **Works without GitHub?** | Yes | No |
| **Installed by default?** | Sometimes (macOS ships a version) | No |

**`git` commands you will use daily:**

```
git init           # Start tracking a folder
git add file.md    # Stage a file
git commit -m ""   # Save a snapshot
git push           # Send to remote
git pull           # Get updates
git log --oneline  # View history
git diff           # See what changed
git clone <url>    # Copy a remote repo locally
```

**`gh` commands for GitHub operations:**

```
gh repo create     # Create a new GitHub repo
gh repo clone      # Clone a GitHub repo (shorthand)
gh issue create    # Open an issue
gh issue develop   # Create a branch from an issue
gh pr create       # Open a pull request
gh pr view         # View PR details
```

Where they overlap

Both can clone a repository (`git clone <url>` vs `gh repo clone user/repo`). That is essentially the only overlap. In practice, you use `git` for all version control and `gh` for all GitHub operations.

### 5\. Create a GitHub Account [¶](https://courses.osc.earth/agentic-research/week-01/\#5-create-a-github-account "Permanent link")

If you do not already have one:

1. Go to [github.com](https://github.com/)
2. Click **Sign up**
3. Choose a username, enter your email, create a password
4. Verify your email address

#### GitHub Education (free upgrades for researchers) [¶](https://courses.osc.earth/agentic-research/week-01/\#github-education-free-upgrades-for-researchers "Permanent link")

GitHub offers free benefits for students, faculty, and research labs. These are worth setting up before you go further.

[Students](https://courses.osc.earth/agentic-research/week-01/#__tabbed_4_1)[Faculty and researchers](https://courses.osc.earth/agentic-research/week-01/#__tabbed_4_2)[Research labs (organizations)](https://courses.osc.earth/agentic-research/week-01/#__tabbed_4_3)

Apply for the [GitHub Student Developer Pack](https://education.github.com/pack):

1. Go to [education.github.com/students](https://education.github.com/students)
2. Click **Join Global Campus**
3. Verify your academic status (use your `.edu` email or upload proof of enrollment)
4. Once approved, you get GitHub Pro for free, plus access to dozens of developer tools

Benefits include unlimited private repos, GitHub Copilot access, and free domain names.

Apply for the [GitHub Teacher Toolbox](https://education.github.com/teachers):

1. Go to [education.github.com/teachers](https://education.github.com/teachers)
2. Click **Join Global Campus**
3. Verify your academic status with your institutional email
4. Once approved, you get GitHub Pro and can create free GitHub Classroom organizations

If your lab or research group has a GitHub organization, you can upgrade it to GitHub Team for free:

1. Visit [education.github.com/globalcampus/teacher](https://education.github.com/globalcampus/teacher) (you must be verified as faculty first)
2. Find the **Upgrade your academic organizations** section
3. Click **Upgrade to GitHub Team**
4. Select your organization and click **Upgrade**

This gives your entire lab access to GitHub Team features for free: protected branches, required reviews, code owners, advanced audit logs, and more. Highly recommended for any research group managing shared code.

#### Set up SSH keys (recommended) [¶](https://courses.osc.earth/agentic-research/week-01/\#set-up-ssh-keys-recommended "Permanent link")

SSH keys let you push to GitHub without typing your password every time.

```
# Generate a new SSH key
ssh-keygen -t ed25519 -C "your.email@example.com"
```

Press Enter to accept the default file location. You can set a passphrase or press Enter for none.

```
# Start the SSH agent
eval "$(ssh-agent -s)"

# Add your key
ssh-add ~/.ssh/id_ed25519
```

[macOS](https://courses.osc.earth/agentic-research/week-01/#__tabbed_5_1)[Linux](https://courses.osc.earth/agentic-research/week-01/#__tabbed_5_2)[Windows](https://courses.osc.earth/agentic-research/week-01/#__tabbed_5_3)

```
cat ~/.ssh/id_ed25519.pub | pbcopy
```

```
cat ~/.ssh/id_ed25519.pub
# Select and copy the output manually
```

In your WSL Ubuntu terminal:

```
cat ~/.ssh/id_ed25519.pub
# Select and copy the output manually
```

Or in PowerShell:

```
Get-Content ~\.ssh\id_ed25519.pub | Set-Clipboard
```

Then add it to GitHub:

1. Go to [github.com/settings/keys](https://github.com/settings/keys)
2. Click **New SSH key**
3. Paste your key and give it a title (e.g., "My Laptop")
4. Click **Add SSH key**

Test the connection:

```
ssh -T git@github.com
```

You should see: `Hi username! You've successfully authenticated...`

#### Authenticate the GitHub CLI [¶](https://courses.osc.earth/agentic-research/week-01/\#authenticate-the-github-cli "Permanent link")

```
gh auth login
```

Follow the prompts: select GitHub.com, choose SSH, and authenticate through your browser.

### 6\. Terminal Navigation Basics [¶](https://courses.osc.earth/agentic-research/week-01/\#6-terminal-navigation-basics "Permanent link")

```
pwd              # Print working directory (where you are)
ls               # List files and folders
cd Documents     # Change directory
cd ..            # Go back up one level
mkdir my-project # Create a new folder
cd my-project    # Move into it
```

Key concepts

- **Absolute path**: starts from the root, e.g., `/Users/jane/Documents`
- **Relative path**: starts from where you are, e.g., `Documents/projects`
- `..` means "one directory up"
- `.` means "this directory"
- `~` means your home directory

### 7\. Create Your First Repository [¶](https://courses.osc.earth/agentic-research/week-01/\#7-create-your-first-repository "Permanent link")

```
# Create a project folder and move into it
mkdir my-research-project
cd my-research-project

# Initialize git tracking
git init
```

Create a file and make your first commit:

```
# Create a README
echo "# My Research Project" > README.md
echo "" >> README.md
echo "This is my first git repository." >> README.md

# Stage and commit
git add README.md
git commit -m "Add README with project description"
```

Make a few more commits to practice:

```
# Add a notes file
echo "## Research Notes" > notes.md
echo "" >> notes.md
echo "- Started project setup" >> notes.md
git add notes.md
git commit -m "Add initial research notes"

# Update the README
echo "" >> README.md
echo "## Goals" >> README.md
echo "- Learn git and GitHub" >> README.md
echo "- Set up a reproducible workflow" >> README.md
git add README.md
git commit -m "Add project goals to README"
```

View your history:

```
git log --oneline
```

### 8\. Push to GitHub [¶](https://courses.osc.earth/agentic-research/week-01/\#8-push-to-github "Permanent link")

Create a remote repository:

1. Go to [github.com/new](https://github.com/new)
2. Name it `my-research-project`
3. Leave it **public** (or private, your choice)
4. Do **not** check "Add a README" (you already have one)
5. Click **Create repository**

Connect and push:

```
git remote add origin git@github.com:YOUR-USERNAME/my-research-project.git
git branch -M main
git push -u origin main
```

Refresh the GitHub page. Your files and commits are now online.

### 9\. Verify Everything Works [¶](https://courses.osc.earth/agentic-research/week-01/\#9-verify-everything-works "Permanent link")

```
git --version       # Git is installed
gh --version        # GitHub CLI is installed
pwd                 # You are in your project
git status          # Git is tracking the project
git log --oneline   # You have commits
git remote -v       # Your remote is set
```

If all of these work, you are ready for Week 2.

* * *

## Before Next Session [¶](https://courses.osc.earth/agentic-research/week-01/\#before-next-session "Permanent link")

Install Claude Code

Before Week 2, install [Claude Code](https://claude.ai/claude-code):

[macOS](https://courses.osc.earth/agentic-research/week-01/#__tabbed_6_1)[Linux](https://courses.osc.earth/agentic-research/week-01/#__tabbed_6_2)[Windows](https://courses.osc.earth/agentic-research/week-01/#__tabbed_6_3)

```
brew install claude-code
```

```
curl -fsSL https://claude.ai/install-cli | sh
```

In your WSL Ubuntu terminal:

```
curl -fsSL https://claude.ai/install-cli | sh
```

Verify:

```
claude --version
```

We will walk through the full setup together in Week 2.

* * *

## Quick Reference [¶](https://courses.osc.earth/agentic-research/week-01/\#quick-reference "Permanent link")

### Terminal [¶](https://courses.osc.earth/agentic-research/week-01/\#terminal "Permanent link")

| Command | What it does |
| --- | --- |
| `pwd` | Print current directory |
| `ls` | List files |
| `cd <dir>` | Change directory |
| `mkdir <name>` | Create a directory |

### Git (version control) [¶](https://courses.osc.earth/agentic-research/week-01/\#git-version-control "Permanent link")

| Command | What it does |
| --- | --- |
| `git init` | Start tracking a folder |
| `git status` | See what changed |
| `git add <file>` | Stage a file for commit |
| `git commit -m "msg"` | Save a snapshot |
| `git push` | Send commits to GitHub |
| `git pull` | Get updates from GitHub |
| `git log --oneline` | View commit history |
| `git diff` | Show uncommitted changes |
| `git clone <url>` | Copy a remote repo |

### GitHub CLI (`gh`) [¶](https://courses.osc.earth/agentic-research/week-01/\#github-cli-gh "Permanent link")

| Command | What it does |
| --- | --- |
| `gh auth login` | Authenticate with GitHub |
| `gh repo create` | Create a new repository |
| `gh repo clone user/repo` | Clone a GitHub repo |
| `gh issue create` | Open a new issue |
| `gh issue develop <num>` | Create a branch from an issue |
| `gh pr create` | Open a pull request |
| `gh pr view` | View pull request details |

* * *

## Resources [¶](https://courses.osc.earth/agentic-research/week-01/\#resources "Permanent link")

- [Git documentation](https://git-scm.com/doc)
- [GitHub Skills](https://skills.github.com/) (free interactive courses)
- [Course repository](https://github.com/OpenScience-Collective/agentic-research-course)
- [Open Science Collective Discord](https://discord.gg/5dWJCUmUww)
- [research-skills plugin](https://github.com/neuromechanist/research-skills)

Back to top