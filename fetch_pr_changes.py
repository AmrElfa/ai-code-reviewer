#!/usr/bin/env python3
import os, json, requests

def main():
    event_path = os.getenv("GITHUB_EVENT_PATH")
    if not event_path:
        print("GITHUB_EVENT_PATH not found.")
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
    api_url = f"https://api.github.com/repos/{repo_full_name}/pulls/{pr_number}/files"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {os.getenv('GITHUB_TOKEN')}"
    }
    response = requests.get(api_url, headers=headers)
    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
        return
    with open("pr_changes.json", "w") as out_file:
        json.dump(response.json(), out_file, indent=2)
    print("PR changes saved to pr_changes.json.")

if __name__ == "__main__":
    main()

