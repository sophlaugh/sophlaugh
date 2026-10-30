# Developer hub: architecture and maintenance

This repository provides the public-facing GitHub profile for Dr. Sophy M. Laughing. It does **not** house Alden, Ava, Digital Soph or Cobeal private source code.

## Project boundaries

- Alden and Ava are distinct private engineering workstreams.
- Cobeal tooling is maintained separately.
- Never paste proprietary infrastructure information, unpublished research, customer records, prompts, model weights, passwords, or secrets into public documentation.
- Public repository descriptions are summaries of workstreams, not representations of shipped capabilities.

## Dynamic profile index

The scheduled `profile-projects.yml` workflow executes `scripts/update_projects.py`, which queries the GitHub public REST API for public repositories owned by `sophlaugh`. It replaces only the text between `PUBLIC_PROJECTS_START` and `PUBLIC_PROJECTS_END` in `README.md`. The script is idempotent: it produces no write if content has not changed. It never searches private repositories.

The workflow runs daily or manually and commits changes using `GITHUB_TOKEN` with `contents: write`. **Important:** If branch protection requires pull requests, the automated push to `main` will be blocked. Configure an approved PR-based update mechanism before enabling scheduled writes; do not remove the rule. The script can also be run locally to propose changes through a normal PR.

## Optional Discord integration

The `discord-notify.yml` workflow sends a brief notification when the profile's main branch is updated or when manually dispatched. It is inert unless the repository secret `DISCORD_WEBHOOK_URL` exists. Obtain a webhook from a Discord channel controlled by you; enter it at Repository → Settings → Secrets and variables → Actions → New repository secret. Never commit webhook URLs. Notifications contain only the profile repository name, commit summary, and GitHub URL.

To publish an invite, verify the Discord server's invitation URL and then add a public Markdown link to the profile README. A webhook alone is not a public invite.

## Recommended public repo standards

Each code repository should have an accurate README, screenshots or diagrams where useful, a LICENSE when sharing rights are intended, CONTRIBUTING and SECURITY guidance, issue and PR templates, unit tests, CI, release notes and real setup instructions. Do not claim tests are passing until GitHub Actions shows success. Avoid public badges for private build statuses.

## Development rules

Use short-lived feature branches and reviewable PRs. Keep workstreams isolated, preserve branch protection, avoid posting credentials in issues, and prefer a completed usable feature over perpetual refactoring. Verify links, assets and workflows before calling an integration operational.
