# repo-forge

Builds complete, runnable repositories from a project description and delivers them as a file tree, files and a zip.

- `SKILL.md`: the skill (open Agent Skills layout: YAML frontmatter + instructions). Use with any agent or tool that loads skills from a folder.
- `PORTABLE_PROMPT.md`: the same behavior as one pasteable prompt for chat apps that do not load skills.
- `references/`: stack playbooks and the plain-chat bundler template.
- `scripts/package_repo.py`: standard-library Python for scanning and zipping a generated project.

Install: copy this folder into your agent's skills directory (the location differs per tool; check its docs), or paste PORTABLE_PROMPT.md into a chat.
