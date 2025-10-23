import os
import tempfile
import requests
from git import Repo
from langchain_ollama import OllamaLLM

def clone_repo(github_url):
    """Clone the GitHub repository into a temporary folder."""
    temp_dir = tempfile.mkdtemp()
    print(f"📂 Cloning repository from {github_url} ...")
    Repo.clone_from(github_url, temp_dir)
    return temp_dir

def extract_repo_content(repo_path):
    """Extract readable content from repo files (including .ipynb)."""
    print("📄 Reading repository files...")
    summary = ""
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith((".py", ".js", ".ts", ".html", ".md", ".ipynb")):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                    summary += f"\n### File: {file}\n{content[:1500]}\n"
                except Exception as e:
                    print(f"⚠️ Error reading {file}: {e}")
            if len(summary) > 7000:  # Avoid overloading the model
                return summary
    return summary

def generate_readme(summary, github_url):
    """Use LLaMA 3 to generate README.md content."""
    print("🤖 Generating README content using LLaMA 3...")
    llm = OllamaLLM(model="llama3")
    prompt = f"""
You are an expert open-source developer.
Generate a professional README.md for this GitHub repository: {github_url}

Here is a summary of the repository's content:
{summary}

The README must include:
- Project Overview
- Features
- Installation
- Usage
- Tech Stack
- Example
- License

Format your response in Markdown.
"""
    return llm.invoke(prompt)

def create_readme_for_repo(github_url):
    """Complete pipeline: clone repo, extract, and generate README."""
    repo_path = clone_repo(github_url)
    summary = extract_repo_content(repo_path)
    readme_content = generate_readme(summary, github_url)
    return readme_content
