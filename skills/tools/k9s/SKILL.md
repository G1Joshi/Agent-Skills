---
name: k9s
description: Expert K9s CLI assistance covering terminal Kubernetes cluster navigation, real-time log streaming, port forwarding, and pod debugging. Use when managing and troubleshooting Kubernetes clusters with speed.
---

# K9s

K9s is a terminal UI (TUI) for Kubernetes. It is faster than clicking in a web dashboard and morediscoverable than raw `kubectl`.

## When to Use

- **Terminal-Based Kubernetes Cluster Management**: Fast, interactive curses UI for navigating pods, services, and deployments.
- **Real-Time Log Streaming & Resource Monitoring**: Tailing multi-pod logs, sorting by CPU/memory, and port forwarding.
- **Custom K9s Plugins & Aliases**: Extending the CLI with custom shell commands (e.g. running stern, cert-manager status).
- **Read-Only Inspection & Troubleshooting**: Safely debugging production clusters with read-only modes.

## Quick Start

```bash
# Launch k9s with active kubeconfig
k9s

# Navigation shortcuts in k9s:
# :pods      - View all pods across namespaces
# :deploy    - View deployments
# :svc       - View services
# /<term>    - Filter items in active view
# l          - Stream logs for selected pod
# s          - Open shell (exec) inside selected container
```

## Core Concepts

### Custom Plugins Configuration (plugins.yaml)

Adding custom keyboard commands for rapid debugging:

```yaml
# ~/.config/k9s/plugins.yaml
plugin:
  # Press 'Shift-D' on a deployment to view detailed rollout history
  rollout-history:
    shortCut: Shift-D
    confirm: false
    description: "Rollout History"
    scopes:
      - deployments
    command: kubectl
    background: false
    args:
      - rollout
      - history
      - deployment/$NAME
      - -n
      - $NAMESPACE

  # Press 'Shift-F' on a pod to launch interactive debug container
  debug-pod:
    shortCut: Shift-F
    confirm: true
    description: "Debug Pod"
    scopes:
      - pods
    command: kubectl
    background: false
    args:
      - debug
      - -it
      - $NAME
      - --image=nicolaka/netshoot
      - -n
      - $NAMESPACE
```

### Essential Navigation & Keyboard Shortcuts

Accelerating cluster management:

- `:pod`: Jump to Pod view across namespaces.
- `:svc`, `:deploy`, `:ing`: Jump to Services, Deployments, and Ingresses.
- `/`: Search and filter resources by name or status.
- `l`: Tail logs for selected pod or container.
- `s`: Open an interactive shell (`sh` / `bash`) inside the selected container.
- `Shift-F`: Port-forward local port to selected pod service port.
- `y`: View full YAML manifest of selected resource.

### Launching K9s with Custom Options

Starting K9s in secure modes:

```bash
# Launch in read-only mode to prevent accidental pod deletion in production
k9s --readonly --namespace production

# Specify custom context and refresh rate
k9s --context prod-eks-cluster --refresh 2
```

## Common Patterns

### Custom K9s Shortcuts and Plugins

**Problem**: Frequently running custom kubectl commands across different namespaces.  
**Solution**: Define custom plugins in `~/.config/k9s/plugin.yaml`.

```yaml
# ~/.config/k9s/plugin.yaml
plugin:
  raw-logs:
    shortCut: Shift-L
    description: "Tail logs without truncation"
    scopes:
      - pods
    command: kubectl
    background: false
    args:
      - logs
      - -f
      - $NAME
      - -n
      - $NAMESPACE
      - --context
      - $CONTEXT
```

## Best Practices

**Do**:

- Use `k9s --readonly` when connecting to production environments to prevent accidental deletions.
- Configure custom plugins in `~/.config/k9s/plugins.yaml` for repetitive `kubectl` commands.
- Use the port-forward shortcut (`Shift-F`) instead of typing long `kubectl port-forward` commands.
- Filter views using `<all>` namespaces or specific namespaces to reduce API server query loads.

**Don't**:

- Leave dozens of active port forwards open; manage and terminate them in the `:portforwards` view.
- Run K9s against large enterprise clusters without setting appropriate `--refresh` intervals.
- Delete persistent volume claims (PVCs) through K9s without verifying backups.

## Troubleshooting

| Error                                    | Cause                                                              | Solution                                                                                        |
| :--------------------------------------- | :----------------------------------------------------------------- | :---------------------------------------------------------------------------------------------- |
| `Boom!! K9s cannot connect to cluster`   | Active kubeconfig context invalid or cluster endpoint unreachable. | Verify connection: `kubectl cluster-info` and switch context with `kubectl config use-context`. |
| `Pod logs failing to stream in k9s`      | Pod container crashed or user lacks RBAC `pods/log` permission.    | Check container status and verify cluster role permissions.                                     |
| `Terminal display corrupted / artifacts` | Incompatible terminal terminfo or small terminal window.           | Run `export TERM=xterm-256color` and maximize terminal window.                                  |

## References

- [K9s Documentation](https://k9scli.io/)
