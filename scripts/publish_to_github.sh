#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Publish AI Developer Effectiveness Framework to GitHub using GitHub CLI.

Usage:
  scripts/publish_to_github.sh [repo-name] [--public|--private] [--owner OWNER]

Examples:
  scripts/publish_to_github.sh ai-developer-effectiveness-framework --public
  scripts/publish_to_github.sh ai-developer-effectiveness-framework --private --owner isantonyhere

Requirements:
  - git
  - GitHub CLI: gh
  - gh auth login must be completed before running this script
USAGE
}

REPO_NAME="ai-developer-effectiveness-framework"
VISIBILITY="--public"
OWNER=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --public)
      VISIBILITY="--public"
      shift
      ;;
    --private)
      VISIBILITY="--private"
      shift
      ;;
    --owner)
      OWNER="${2:-}"
      if [[ -z "$OWNER" ]]; then
        echo "Error: --owner requires a value" >&2
        exit 1
      fi
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      REPO_NAME="$1"
      shift
      ;;
  esac
done

command -v git >/dev/null 2>&1 || { echo "Error: git is not installed" >&2; exit 1; }
command -v gh >/dev/null 2>&1 || { echo "Error: GitHub CLI 'gh' is not installed" >&2; exit 1; }

gh auth status >/dev/null 2>&1 || {
  echo "Error: GitHub CLI is not authenticated. Run: gh auth login" >&2
  exit 1
}

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ ! -d .git ]]; then
  git init
fi

git branch -M main >/dev/null 2>&1 || true

git add .

if git diff --cached --quiet; then
  echo "No staged changes to commit. Continuing with existing commit history."
else
  git commit -m "Initial AI Developer Effectiveness Framework"
fi

if git remote get-url origin >/dev/null 2>&1; then
  echo "Remote 'origin' already exists: $(git remote get-url origin)"
  echo "Pushing current branch to origin/main..."
  git push -u origin main
  exit 0
fi

if [[ -n "$OWNER" ]]; then
  FULL_NAME="$OWNER/$REPO_NAME"
else
  FULL_NAME="$REPO_NAME"
fi

echo "Creating GitHub repository: $FULL_NAME ($VISIBILITY)"
gh repo create "$FULL_NAME" "$VISIBILITY" --source=. --remote=origin --push

echo "Done. Repository:"
gh repo view --web=false --json url --jq .url
