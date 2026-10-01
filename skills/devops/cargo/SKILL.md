---
name: cargo
description: Expert Cargo Rust package manager assistance covering workspaces, dependencies, feature flags, cross-compilation, and release profiles. Use when building, testing, and packaging Rust projects.
---

# Cargo

Cargo is Rust's build system and package manager. It is famous for its reliability and developer experience.

## When to Use

- **Rust Dependency & Build Management**: Compiling, building, packaging, and publishing Rust packages and crates.
- **Workspace Multi-Crate Architectures**: Managing monorepos with shared dependencies and unified lockfiles.
- **Continuous Integration & Static Analysis**: Running `cargo test`, `cargo clippy`, `cargo fmt`, and `cargo audit`.
- **Release Optimization & Cross-Compilation**: Building stripped, LTO-optimized release binaries for production.

## Quick Start

```bash
cargo new my-project
cd my-project
cargo run
```

```toml
# Cargo.toml
[dependencies]
serde = "1.0"
```

## Core Concepts

### Cargo Workspace Configuration (Cargo.toml)

Managing multiple interdependent crates in a monorepo:

```toml
# /Cargo.toml (Workspace Root)
[workspace]
members = [
    "crates/api-server",
    "crates/core-domain",
    "crates/db-migrations",
]
resolver = "2"

[workspace.dependencies]
tokio = { version = "1.40", features = ["full"] }
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
tracing = "0.1"
thiserror = "1.0"

[profile.release]
opt-level = 3
lto = "fat"            # Link-time optimization
codegen-units = 1      # Maximize optimizations across units
panic = "abort"        # Eliminate unwinding code overhead
strip = true           # Automatically strip symbols from binary
```

### High-Speed Testing, Benchmarking & Lints

Automating quality checks in CI/CD pipelines:

```bash
# Format check
cargo fmt --all -- --check

# Clippy linter with strict warning enforcement
cargo clippy --all-targets --all-features -- -D warnings

# Execute all workspace unit and integration tests in parallel
cargo test --workspace --all-features

# Security audit against RustSec advisory database
cargo audit
```

### Adding and Managing Dependencies

Adding pinned crates with specific feature sets:

```bash
# Add dependency with targeted features
cargo add tokio --features full
cargo add serde --features derive
cargo add axum --features ws

# Update dependencies adhering to SemVer
cargo update
```

## Common Patterns

### Optimized Release Profile with LTO and Symbol Stripping

**Problem**: Default Rust release binaries are bloated and larger than necessary for container deployment.

**Solution**:
Configure release profile optimizations in `Cargo.toml`:

```toml
[profile.release]
opt-level = 3          # Maximum optimization
lto = "fat"            # Link-time optimization across all crates
codegen-units = 1      # Maximize LTO optimization (slower compile, faster binary)
panic = "abort"        # Strip unwind tables
strip = true           # Strip all debug symbols
```

## Best Practices

**Do**:

- Use `lto = "fat"`, `codegen-units = 1`, and `strip = true` in release profiles to minimize binary size.
- Commit `Cargo.lock` for all binary application crates to guarantee reproducible builds.
- Run `cargo clippy -- -D warnings` and `cargo audit` in all CI pipelines.
- Leverage workspace-level dependencies (`workspace.dependencies`) to synchronize versions across crates.

**Don't**:

- Ignore `Cargo.lock` in application repositories (only libraries should consider omitting it).
- Enable heavy, unneeded crate features; include only the specific feature flags your application uses.
- Deploy debug build artifacts (`target/debug`); always compile production releases with `cargo build --release`.

## Troubleshooting

| Error                                                   | Cause                                                           | Solution                                                             |
| :------------------------------------------------------ | :-------------------------------------------------------------- | :------------------------------------------------------------------- |
| `error: failed to select a version for the requirement` | Incompatible dependency version constraints in `Cargo.toml`.    | Run `cargo update` or inspect conflicts in `Cargo.lock`.             |
| `error: could not compile ... (exit status: 101)`       | Compile error in code or missing native C library dependencies. | Install missing system packages (e.g. `libssl-dev` or `pkg-config`). |
| `linking with cc failed: exit code: 1`                  | Missing linker or C toolchain on host system.                   | Install build essentials: `sudo apt-get install build-essential`.    |

## References

- [The Cargo Book](https://doc.rust-lang.org/cargo/)
