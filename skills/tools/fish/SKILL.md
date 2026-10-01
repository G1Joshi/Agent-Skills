---
name: fish
description: Expert Fish shell assistance covering completions, functions, syntax highlighting, universal variables, and prompt customization. Use when operating interactive modern command line environments.
---

# Fish (Friendly Interactive Shell)

Fish (Friendly Interactive Shell) is a smart, user-friendly command-line shell featuring autosuggestions, syntax highlighting, and clean scriptable syntax out of the box.

## When to Use

- **Interactive Developer Shell**: Out-of-the-box autosuggestions, syntax highlighting, and tab completions without plugins.
- **Clean Shell Scripting**: Intuitive scripting syntax without legacy POSIX quirks (no subshells for math, clear array handling).
- **Custom Universal Variables**: Persisting user variables (`set -U`) across all shell sessions without editing config files.
- **High-Speed Shell Startup**: Instant startup times (< 20ms) without heavy plugin manager overhead.

## Quick Start

```fish
# Define and persist a custom function in Fish
function mkcd --description "Create directory and cd into it"
    mkdir -p $argv[1]; and cd $argv[1]
end

# Save function permanently
funcsave mkcd
```

## Core Concepts

### Modern Shell Configuration (config.fish)

Configuring environment, completions, and aliases:

```fish
# ~/.config/fish/config.fish
if status is-interactive
    # Disable default greeting
    set -g fish_greeting ""

    # Modern path exports
    fish_add_path /opt/homebrew/bin $HOME/.cargo/bin $HOME/.local/bin

    # Environment variables
    set -gx EDITOR nvim
    set -gx KUBECONFIG $HOME/.kube/config

    # Fast shell abbreviations (expanded automatically on Space/Enter)
    abbr -a g git
    abbr -a gco git checkout
    abbr -a k kubectl
    abbr -a d docker
    abbr -a tf terraform

    # Initialize Starship prompt if installed
    if command -q starship
        starship init fish | source
    end
end
```

### Clean Fish Scripting Syntax

Writing readable, modular functions and loops:

```fish
# ~/.config/fish/functions/deploy_service.fish
function deploy_service --description "Build and deploy service container"
    set -l service_name $argv[1]

    if test -z "$service_name"
        echo "Error: Service name argument required"
        return 1
    end

    echo "Deploying $service_name to production cluster..."
    docker build -t "myregistry.com/$service_name:latest" .
    and docker push "myregistry.com/$service_name:latest"
    and kubectl rollout restart deployment/$service_name

    if test $status -eq 0
        echo "Deployment completed successfully!"
    else
        echo "Deployment failed with exit code $status"
    end
end
```

### Universal Variables (set -U)

Setting variables across all current and future shell sessions instantly:

```fish
# Persist variable globally across all fish sessions without writing to config.fish
set -U FZF_DEFAULT_OPTS "--height 40% --layout=reverse --border"
```

## Common Patterns

### Universal Environment Variables and Custom PATH

**Problem**: Exported environment variables lost when closing shell session in bash/zsh.

**Solution**:
Use Fish universal variables (`set -U`):

```fish
# Set once; persisted across all shell sessions and reboots permanently
set -U EDITOR nvim
set -U fish_user_paths /opt/homebrew/bin $HOME/.cargo/bin $fish_user_paths
```

## Best Practices

**Do**:

- Use `fish_add_path` to add directories to `$PATH` idempotently without duplicates.
- Use abbreviations (`abbr -a`) rather than aliases; abbreviations expand in place, maintaining transparent history.
- Wrap interactive configurations inside `if status is-interactive ... end` to keep non-interactive script startup instant.
- Store standalone functions in `~/.config/fish/functions/<name>.fish` for automatic lazy loading.

**Don't**:

- Write system administration shell scripts in Fish if POSIX `/bin/sh` or `/bin/bash` portability is required.
- Use legacy bash syntax (e.g. `export FOO=bar` or `$(command)`); use `set -gx FOO bar` and `(command)`.
- Overload `config.fish` with heavy external subshell calls; benchmark startup with `fish --profile`.

## Troubleshooting

| Error                                        | Cause                                             | Solution                                                                      |
| :------------------------------------------- | :------------------------------------------------ | :---------------------------------------------------------------------------- |
| `fish: Unknown command: source .../activate` | Sourcing bash virtualenv script into Fish shell.  | Source the fish-specific activation script: `source .venv/bin/activate.fish`. |
| `export: command not found`                  | Attempting POSIX `export VAR=val` syntax in Fish. | Use Fish syntax: `set -gx VAR val`.                                           |
| `&& operator syntax error in legacy Fish`    | Using `&&` in older Fish versions.                | Upgrade to Fish 3.0+ or use `; and` operator.                                 |

## References

- [Fish Shell Documentation](https://fishshell.com/docs/current/index.html)
