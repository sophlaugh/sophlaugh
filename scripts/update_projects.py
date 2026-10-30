#!/usr/bin/env python3
"""Update only the public repository list between README markers."""
import json
import os
from pathlib import Path
from urllib.request import Request, urlopen

USER = "sophlaugh"
README = Path(__file__).resolve().parents[1] / "README.md"
START = "<!-- PUBLIC_PROJECTS_START -->"
END = "<!-- PUBLIC_PROJECTS_END -->"
EXCLUDED = {"sophlaugh", "youtube-dl", "rea"}

def get_public_repos():
    req = Request(
        f"https://api.github.com/users/{USER}/repos?type=owner&per_page=100&sort=updated",
        headers={"Accept": "application/vnd.github+json", "User-Agent": "profile-project-index",
                 **({"Authorization": f"Bearer {os.environ['GH_TOKEN']}"} if os.getenv("GH_TOKEN") else {})},
    )
    with urlopen(req, timeout=20) as response:
        repos = json.load(response)
    return [r for r in repos if not r.get("private") and not r.get("fork") and not r.get("archived")
            and r["name"] not in EXCLUDED]

def main():
    original = README.read_text(encoding="utf-8")
    if original.count(START) != 1 or original.count(END) != 1:
        raise ValueError("Expected exactly one pair of project markers")
    entries = []
    for repo in get_public_repos()[:8]:
        name = repo["name"].replace("|", "\\|")
        description = (repo.get("description") or "Public software and research repository").replace("\n", " ").replace("|", "\\|")
        entries.append(f"- **[{name}]({repo['html_url']})** — {description[:160]}")
    replacement = "\n".join(entries) or "_No public projects to display._"
    before, remaining = original.split(START, 1)
    _, after = remaining.split(END, 1)
    updated = before + START + "\n" + replacement + "\n" + END + after
    if updated != original:
        README.write_text(updated, encoding="utf-8")
        print("Updated public projects")
    else:
        print("No changes")

if __name__ == "__main__":
    main()
