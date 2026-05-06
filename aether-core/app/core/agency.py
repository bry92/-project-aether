import os
from github import Github
from playwright.async_api import async_playwright
from typing import Optional

# GitHub Tooling
def get_github_client():
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        return None
    return Github(token)

async def create_github_repo(repo_name: str, description: str = ""):
    g = get_github_client()
    if not g: return "Error: No GITHUB_TOKEN set."
    user = g.get_user()
    repo = user.create_repo(repo_name, description=description, private=True)
    return f"Successfully created repo: {repo.html_url}"

async def create_pull_request(repo_full_name: str, title: str, head: str, base: str = "main"):
    g = get_github_client()
    if not g: return "Error: No GITHUB_TOKEN set."
    repo = g.get_repo(repo_full_name)
    pr = repo.create_pull(title=title, body="Autonomous PR from Aether.", head=head, base=base)
    return f"Successfully created PR: {pr.html_url}"

# Browser Tooling (Playwright)
async def browse_and_summarize(url: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new-page()
        await page.goto(url)
        # Simple text extraction for now
        content = await page.content()
        # In a real scenario, we'd pass this to an LLM to summarize
        await browser.close()
        return f"Captured content from {url}. Length: {len(content)} characters."

# Stripe Placeholder
async def create_stripe_product(name: str, price_cents: int):
    # This would use the stripe library
    return f"Successfully created Stripe product: {name} at ${price_cents/100}"
