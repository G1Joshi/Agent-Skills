# Agent Skills

### A comprehensive **skill catalog** for AI agents.

![Agents](https://img.shields.io/badge/Agents-40+-10B981)
![Categories](https://img.shields.io/badge/Categories-10+-F59E0B)
![Skills](https://img.shields.io/badge/Skills-350+-8B5CF6)

## Installation

```bash
npx skills add g1joshi/agent-skills/skills
```

Or install specific skills:

```bash
npx skills add g1joshi/agent-skills/skills --skill dart
npx skills add g1joshi/agent-skills/skills --skill flutter
```

## Compatible Agents

![Adal](https://img.shields.io/badge/Adal-6366F1?style=for-the-badge&logoColor=white)
![Amp](https://img.shields.io/badge/Amp-0066FF?style=for-the-badge&logoColor=white)
![Antigravity](https://img.shields.io/badge/Antigravity-4285F4?style=for-the-badge&logo=google&logoColor=white)
![Augment](https://img.shields.io/badge/Augment-7C3AED?style=for-the-badge&logoColor=white)
![Claude Code](https://img.shields.io/badge/Claude_Code-D4A27F?style=for-the-badge&logo=anthropic&logoColor=white)
![Cline](https://img.shields.io/badge/Cline-5A67D8?style=for-the-badge&logoColor=white)
![CodeBuddy](https://img.shields.io/badge/CodeBuddy-10B981?style=for-the-badge&logoColor=white)
![Codex](https://img.shields.io/badge/Codex-412991?style=for-the-badge&logo=openai&logoColor=white)
![Command Code](https://img.shields.io/badge/Command_Code-1E3A8A?style=for-the-badge&logoColor=white)
![Continue](https://img.shields.io/badge/Continue-000000?style=for-the-badge&logoColor=white)
![Crush](https://img.shields.io/badge/Crush-EC4899?style=for-the-badge&logoColor=white)
![Cursor](https://img.shields.io/badge/Cursor-000000?style=for-the-badge&logo=cursor&logoColor=white)
![Droid](https://img.shields.io/badge/Droid-3DDC84?style=for-the-badge&logo=android&logoColor=white)
![Gemini CLI](https://img.shields.io/badge/Gemini_CLI-8E75B2?style=for-the-badge&logo=googlegemini&logoColor=white)
![GitHub Copilot](https://img.shields.io/badge/GitHub_Copilot-000000?style=for-the-badge&logo=githubcopilot&logoColor=white)
![Goose](https://img.shields.io/badge/Goose-FF9900?style=for-the-badge&logoColor=white)
![iFlow CLI](https://img.shields.io/badge/iFlow_CLI-3B82F6?style=for-the-badge&logoColor=white)
![Junie](https://img.shields.io/badge/Junie-000000?style=for-the-badge&logo=jetbrains&logoColor=white)
![Kilo](https://img.shields.io/badge/Kilo-00D4AA?style=for-the-badge&logoColor=white)
![Kimi CLI](https://img.shields.io/badge/Kimi_CLI-000000?style=for-the-badge&logoColor=white)
![Kiro CLI](https://img.shields.io/badge/Kiro_CLI-FF9900?style=for-the-badge&logo=amazon&logoColor=white)
![Kode](https://img.shields.io/badge/Kode-6366F1?style=for-the-badge&logoColor=white)
![MCPJam](https://img.shields.io/badge/MCPJam-F59E0B?style=for-the-badge&logoColor=white)
![Mistral Vibe](https://img.shields.io/badge/Mistral_Vibe-FF7000?style=for-the-badge&logoColor=white)
![Mux](https://img.shields.io/badge/Mux-FA4616?style=for-the-badge&logoColor=white)
![Neovate](https://img.shields.io/badge/Neovate-57A143?style=for-the-badge&logo=neovim&logoColor=white)
![OpenClaw](https://img.shields.io/badge/OpenClaw-6366F1?style=for-the-badge&logoColor=white)
![OpenCode](https://img.shields.io/badge/OpenCode-3B82F6?style=for-the-badge&logoColor=white)
![OpenHands](https://img.shields.io/badge/OpenHands-10B981?style=for-the-badge&logoColor=white)
![Pi](https://img.shields.io/badge/Pi-FF6B6B?style=for-the-badge&logoColor=white)
![Pochi](https://img.shields.io/badge/Pochi-F472B6?style=for-the-badge&logoColor=white)
![Qoder](https://img.shields.io/badge/Qoder-8B5CF6?style=for-the-badge&logoColor=white)
![Qwen Code](https://img.shields.io/badge/Qwen_Code-6366F1?style=for-the-badge&logoColor=white)
![Replit](https://img.shields.io/badge/Replit-F26207?style=for-the-badge&logo=replit&logoColor=white)
![Roo](https://img.shields.io/badge/Roo-E11D48?style=for-the-badge&logoColor=white)
![Trae](https://img.shields.io/badge/Trae-00D6C6?style=for-the-badge&logoColor=white)
![Trae CN](https://img.shields.io/badge/Trae_CN-00D6C6?style=for-the-badge&logoColor=white)
![Windsurf](https://img.shields.io/badge/Windsurf-09B6A2?style=for-the-badge&logo=codeium&logoColor=white)
![Zencoder](https://img.shields.io/badge/Zencoder-14B8A6?style=for-the-badge&logoColor=white)

## Directory Structure

```
agent-skills/
├── skills/                    # All skill definitions
│   ├── ai-ml/                 # ML frameworks, LLMs, data science
│   ├── architecture/          # Design patterns, API design
│   ├── databases/             # SQL, NoSQL, ORMs
│   ├── devops/                # CI/CD, containers, cloud
│   ├── frameworks/            # Frontend, backend frameworks
│   ├── languages/             # Programming languages
│   ├── mobile/                # iOS, Android, cross-platform
│   ├── security/              # Auth, encryption, secure coding
│   ├── testing/               # Unit, E2E, integration testing
│   └── tools/                 # Developer tools, IDEs
├── template/                  # Skill template
│   └── SKILL.md
├── .gitignore                 # Git ignore patterns
├── LICENSE                    # MIT License
└── README.md                  # This file
```

## Skill Format

Each skill is a directory containing a `SKILL.md` file with YAML frontmatter:

```
skill-name/
└── SKILL.md          # Required: instructions + metadata
```

### SKILL.md Structure

```yaml
---
name: skill-name
description: What this skill does and when to use it. Use of X for Y.
---
```

See [template/SKILL.md](template/SKILL.md) for details.

## Learn More

- [agentskills.io](https://agentskills.io/) - Agent Skills specification
- [skills.sh](https://skills.sh/) - Browse and install skills
