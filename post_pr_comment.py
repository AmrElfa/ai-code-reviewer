#!/usr/bin/env python3
import os, json, requests

def main():
    if not os.path.exists("review_comments.json"):
        print("review_comments.json not found.")
        return
    with open("review_comments.json", "r") as f:
        review_comments = json.load(f)
    comment_body = "## AI Code Review Suggestions\n\n"
    for filename, suggestions in review_comments.items():
        comment_body += f"### File: `{filename}`\n{suggestions}\n\n"
    event_path = os.getenv("GITHUB_EVENT_PATH")
    if not event_path:
        print("GITHUB_EVENT_PATH not set.")
        return
    with open(event_path, "r") as f:
        event_data = json.load(f)
    pr_number = event_data.get("number") or event_data.get("pull_request", {}).get("number")
    if not pr_number:
        print("PR number not found.")
        return
    repo_full_name = os.getenv("GITHUB_REPOSITORY")
    if not repo_full_name:
        print("GITHUB_REPOSITORY not set.")
        return
    api_url = f"https://api.github.com/repos/{repo_full_name}/issues/{pr_number}/comments"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {os.getenv('GITHUB_TOKEN')}"
    }
    data = {"body": comment_body}
    response = requests.post(api_url, headers=headers, json=data)
    if response.status_code == 201:
        print("Comment posted.")
    else:
        print(f"Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    main()

