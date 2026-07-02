# AGENTS.md

## Cursor Cloud specific instructions

This repository is **documentation / course materials only** — it is not a software
application. It contains:

- `README.md` — course title.
- `.firecrawl/week-01.md` — scraped Week 1 course content (Git, GitHub, and the command line).

There is intentionally **no application to build or run**, and there are:

- No package manifests (`package.json`, `requirements.txt`, `pyproject.toml`, etc.).
- No dependencies to install.
- No test suite, no lint configuration, and no build system.

Because of this, the update script has nothing to install. The only tools the course
content relies on are `git` and the GitHub CLI (`gh`), which are pre-installed on the VM.

### Working with this repo

- Edits are plain Markdown; there is nothing to compile. Preview changes with any
  Markdown viewer if desired.
- The repo's subject matter is the git/GitHub workflow itself. The closest thing to an
  end-to-end "run" is the course's own "Verify Everything Works" checklist in
  `.firecrawl/week-01.md` (Section 9): `git --version`, `gh --version`, `git status`,
  `git log --oneline`, `git remote -v`.
- If a future task adds real application code, add its install/build/test/run commands
  here and move dependency installation into the update script.
