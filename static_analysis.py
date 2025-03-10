#!/usr/bin/env python3
import os, json, subprocess

def run_pylint(file_path):
    try:
        result = subprocess.run(["pylint", file_path, "--score", "n"], capture_output=True, text=True)
        return result.stdout + "\n" + result.stderr
    except Exception as e:
        return f"pylint error for {file_path}: {e}"

def run_eslint(file_path):
    try:
        result = subprocess.run(["eslint", file_path, "--format", "compact"], capture_output=True, text=True)
        return result.stdout + "\n" + result.stderr
    except Exception as e:
        return f"ESLint error for {file_path}: {e}"

def main():
    if not os.path.exists("pr_changes.json"):
        print("pr_changes.json not found.")
        return
    with open("pr_changes.json", "r") as f:
        pr_changes = json.load(f)
    analysis_results = {}
    for file_change in pr_changes:
        filename = file_change.get("filename")
        if file_change.get("status") not in ["modified", "added"]:
            continue
        if not os.path.exists(filename):
            print(f"File {filename} missing.")
            continue
        print(f"Analyzing {filename}...")
        if filename.endswith(".py"):
            result = run_pylint(filename)
        elif filename.endswith(".js"):
            result = run_eslint(filename)
        else:
            result = "No analysis available."
        analysis_results[filename] = result
    with open("static_analysis_results.json", "w") as out_file:
        json.dump(analysis_results, out_file, indent=2)
    print("Results saved to static_analysis_results.json.")

if __name__ == "__main__":
    main()

