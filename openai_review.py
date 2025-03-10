#!/usr/bin/env python3
import os, json, openai

def get_ai_review(file_name, file_content, analysis_output):
    prompt = f"Review the following file for improvements.\nFilename: {file_name}\n\nCode:\n{file_content}\n\nAnalysis:\n{analysis_output}\n"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful code reviewer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=300
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"OpenAI error: {e}"

def main():
    if not os.getenv("OPENAI_API_KEY"):
        print("OPENAI_API_KEY not set.")
        return
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not os.path.exists("pr_changes.json") or not os.path.exists("static_analysis_results.json"):
        print("Required files missing.")
        return
    with open("pr_changes.json", "r") as f:
        pr_changes = json.load(f)
    with open("static_analysis_results.json", "r") as f:
        analysis_results = json.load(f)
    review_comments = {}
    for file_change in pr_changes:
        filename = file_change.get("filename")
        if file_change.get("status") not in ["modified", "added"]:
            continue
        try:
            with open(filename, "r") as file_obj:
                file_content = file_obj.read()
        except Exception as e:
            file_content = f"Could not read: {e}"
        analysis_output = analysis_results.get(filename, "No analysis.")
        print(f"Reviewing {filename}...")
        review_comments[filename] = get_ai_review(filename, file_content, analysis_output)
    with open("review_comments.json", "w") as out_file:
        json.dump(review_comments, out_file, indent=2)
    print("Review suggestions saved to review_comments.json.")

if __name__ == "__main__":
    main()

