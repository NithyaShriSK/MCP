import gradio as gr
from mcp import create_readme_for_repo

def generate_readme_from_github(github_url):
    if not github_url.strip():
        return "⚠️ Please provide a valid GitHub link."
    try:
        readme_content = create_readme_for_repo(github_url)
        return readme_content
    except Exception as e:
        return f"❌ Error: {e}"

with gr.Blocks(title="📘 GitHub README Generator") as demo:
    gr.Markdown("## 🤖 LLaMA 3 - GitHub README Generator")
    gr.Markdown("Enter your GitHub repository URL below and get a professional README.md file generated automatically.")

    github_input = gr.Textbox(label="🔗 GitHub Repository URL", placeholder="https://github.com/username/repo-name")
    generate_button = gr.Button("🚀 Generate README")
    output_box = gr.Textbox(label="📝 Generated README.md", lines=25)

    generate_button.click(fn=generate_readme_from_github, inputs=github_input, outputs=output_box)

demo.launch()
