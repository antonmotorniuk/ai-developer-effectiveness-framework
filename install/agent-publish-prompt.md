Publish this project to GitHub.

Goal:
Create a GitHub repository for this project and push the current files.

Repository name:
ai-developer-effectiveness-framework

Requirements:
- Use GitHub CLI if available.
- Do not modify project content except Git metadata if needed.
- If GitHub CLI is not authenticated, tell me to run `gh auth login`.
- If the repository already has a remote called `origin`, show it and ask me before replacing it.
- Use `main` as the default branch.
- Commit current files with message: `Initial AI Developer Effectiveness Framework`.
- Prefer public repository unless I explicitly ask for private.
- After publishing, show me the GitHub URL.

Suggested command:

```bash
scripts/publish_to_github.sh ai-developer-effectiveness-framework --public
```
