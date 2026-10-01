---
name: warp
description: Expert Warp terminal assistance covering AI command search, block-based navigation, workflows, team sharing, and session customization. Use when using Warp terminal, authoring custom Warp workflows, configuring AI prompts, or optimizing terminal command management.
---

# Warp

Warp is a modern, GPU-accelerated terminal built in Rust, featuring block-based navigation, IDE-style text editing, and automated command workflows.

## When to Use

- **Modern AI-Powered Terminal Operations**: Executing CLI commands with block-based outputs, native autocomplete, and integrated AI error fixes.
- **Team Command Sharing via Warp Workflows**: Packaging complex multi-step devops commands into parameterized, searchable workflows.
- **Collaborative Terminal Sessions**: Sharing session outputs and command blocks securely via web permalinks.
- **Fast Rust-Based Terminal Performance**: Rendering high-throughput terminal logs with GPU-accelerated rendering.

## Quick Start

### 1. Essential Warp Controls

- `Cmd + P`: Open Command Palette
- `Ctrl + Space`: Activate Warp AI command prediction
- `Cmd + Up / Down`: Jump between command execution blocks
- `Cmd + Shift + C`: Copy block command output directly to clipboard

### 2. Custom Workflow Definition

Save under `~/.warp/workflows/docker_clean.yaml`:

```yaml
name: Docker Prune Dangling Images
description: Remove dangling Docker containers, volumes, and networks safely
command: docker system prune -a --volumes -f
tags:
  - docker
  - devops
```

## Core Concepts

### Authoring Parameterized Warp Workflows (`.warp/workflows/*.yaml`)

Defining reproducible, searchable engineering runbooks:

```yaml
# ~/.warp/workflows/k8s_debug_pod.yaml
name: Debug Failing Kubernetes Pod
description: Spin up an ephemeral debugging container attached to a failing pod.
command: kubectl debug -it {{pod_name}} --image=nicolaka/netshoot --namespace={{namespace}} --target={{container_name}}
tags:
  - kubernetes
  - devops
  - debugging
arguments:
  - name: pod_name
    description: The name of the target pod
    default_value: auth-service-784f4bf78d-9x2kz
  - name: namespace
    description: Kubernetes namespace
    default_value: default
  - name: container_name
    description: Target container inside pod
    default_value: app
```

Search and execute workflow:

- Open Warp -> Press `Ctrl + Shift + R` -> Type `k8s debug pod` -> Fill parameters -> Run.

### Warp Drive Team Synchronization

Sharing workflows, launch configurations, and documentation across teams:

- Navigate to **Warp Drive** in the left sidebar.
- Create a team workspace (e.g. `Platform-Engineering`).
- Save workflows directly into the shared folder; team members receive instant real-time synchronization.

### Native AI Command Generation & Diagnostics

- Press `Ctrl + Space` or click **Warp AI**:
  - Ask: _"Generate a command to find all Docker images older than 30 days and delete them."_
  - Warp generates the exact command line with safe preview before execution.
- If a command exits with code `1`, click **Ask AI** on the error block to diagnose stack traces automatically.

## Common Patterns

### Parameterized Warp Workflows

**Problem**: Team members frequently forget complex CLI syntax with multiple arguments.  
**Solution**: Define workflows with parameterized arguments.

```yaml
# ~/.warp/workflows/k8s_restart.yaml
name: Restart Kubernetes Deployment
description: Rollout restart a specific deployment in target namespace
command: kubectl rollout restart deployment {{deployment_name}} -n {{namespace}}
arguments:
  - name: deployment_name
    description: Target deployment name
    default_value: api-gateway
  - name: namespace
    description: Kubernetes namespace
    default_value: production
```

### Block Sharing & Collaboration

**Problem**: Sharing terminal command output and stack traces with team members without formatting loss or screenshotting.

**Solution**:

```bash
# Share individual command block and execution output directly:
warp share --block-id last-command --access restricted --team engineering
```

## Best Practices

**Do**:

- Parameterize repeated deployment and debugging commands as Warp Workflows (`.warp/workflows/`).
- Use **Block Sharing** (right-click block -> Share) to generate secure links to command outputs during incidents.
- Organize team operational runbooks inside **Warp Drive** for centralized onboarding.
- Inspect and review generated shell commands from Warp AI before pressing enter on production environments.

**Don't**:

- Share terminal output blocks containing unredacted API tokens, customer PII, or credentials.
- Hardcode static credentials or cluster names into shared team workflows; use variables (`{{argument}}`).
- Disable native shell integrations; Warp relies on them for command status tracking and block boundaries.

## Troubleshooting

| Error                                                 | Cause                                                    | Solution                                                                   |
| ----------------------------------------------------- | -------------------------------------------------------- | -------------------------------------------------------------------------- |
| Shell integration not loading custom `.zshrc` aliases | Warp subshell initialization sequence overriding aliases | Place custom aliases in `~/.zshrc` after the Warp shell integration block. |
| AI Assistant suggests outdated CLI commands           | Missing local context or outdated CLI version            | Provide specific target version in prompt or update CLI binary on host.    |
| Custom keybinding conflict with terminal multiplexer  | Warp intercepting keys assigned to tmux or nvim          | Customize shortcut mappings under **Settings > Keyboard Shortcuts**.       |

## References

- [Warp Documentation](https://docs.warp.dev/)
