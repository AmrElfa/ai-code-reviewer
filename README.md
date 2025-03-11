# AI-Powered Code Reviewer

This is an AI-powered code reviewer project built using GitHub Actions, Python, and the OpenAI API.

## Overview

The project automatically reviews pull requests in a GitHub repository. It:
- Triggers when a pull request is created or updated.
- Extracts changed files.
- Runs static analysis (using pylint for Python and ESLint for JavaScript).
- Sends code and analysis to the OpenAI API for review.
- Posts AI-generated suggestions as a comment on the pull request.

## How It Works

1. **GitHub Actions Workflow:**  
   The workflow (`.github/workflows/ai_code_reviewer.yml`) is triggered on pull requests. It runs several scripts to fetch changes, run static analysis, and get AI feedback.

2. **Scripts:**
   - `fetch_pr_changes.py` — Fetches the changed files.
   - `static_analysis.py` — Runs static analysis on the code.
   - `openai_review.py` — Sends the code to the OpenAI API and retrieves suggestions.
   - `post_pr_comment.py` — Posts the AI-generated suggestions as a comment on the pull request.

3. **API Integration:**  
   The OpenAI API is used to provide code review suggestions. You need to set your OpenAI API key as a GitHub secret (`OPENAI_API_KEY`) for the workflow to work.

## Setup

- Make sure to add your OpenAI API key as a secret in the repository settings under **Settings → Secrets and variables → Actions**.
- The repository is set to trigger the workflow on pull requests, so create a PR to see the AI review in action.

## Notes

- This project is fully automated using GitHub Actions.
- It’s designed to be modular, so you can extend it to support more languages or static analysis tools.
- For privacy, personal information has been kept out of this repository.

## How to Use

1. Fork or clone this repository.
2. Set up the GitHub secret for the OpenAI API key.
3. Open a pull request with some code changes.
4. Watch the workflow run and see the AI-generated code review suggestions in the pull request.

---
