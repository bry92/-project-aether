import os
from github import Github

class GithubWrapper:
    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
        self.client = Github(self.token) if self.token else None

    def create_repo(self, name: str, description: str = ""):
        if not self.client: return "Error: GITHUB_TOKEN not set."
        user = self.client.get_user()
        repo = user.create_repo(name, description=description, private=True)
        return {"name": repo.name, "url": repo.html_url}

    def commit_files(self, repo_name: str, branch: str, message: str, files: dict):
        if not self.client: return "Error: GITHUB_TOKEN not set."
        repo = self.client.get_repo(repo_name)
        # Simplified commit logic for prototype
        for path, content in files.items():
            repo.create_file(path, message, content, branch=branch)
        return f"Successfully committed {len(files)} files to {branch}."

github = GithubWrapper()
