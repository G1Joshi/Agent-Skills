---
name: goland
description: Expert JetBrains GoLand IDE assistance covering Go tools, live profiling, delve debugger, refactoring, and test runners. Use when developing, profiling, and debugging Go applications.
---

# GoLand

GoLand provides deep understanding of Go code. It excels at **Interface implementation** navigation and **Goroutine** debugging.

## When to Use

- **Professional Go Application Development**: JetBrains IDE with deep static analysis, refactoring, and Delve debugging.
- **Go Microservices & Concurrency Debugging**: Inspecting active goroutines, stack frames, channel states, and deadlocks.
- **Profiling Benchmarks with pprof**: Visualizing CPU profiles, memory allocations, and block profiles directly in the IDE.
- **Database & Docker Tooling Integration**: Exploring database schemas and container logs alongside Go code.

## Quick Start

```go
// Set breakpoint in GoLand and press Shift+F9 to debug with Delve:
package main

import "fmt"

func main() {
    message := "Debugging with GoLand"
    fmt.Println(message) // Set breakpoint here to inspect variables
}
```

## Core Concepts

### Delve Debugger & Goroutine Inspection

Configuring launch settings and inspecting runtime state:

```json
// .vscode/launch.json or GoLand Run Configuration
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Debug API Microservice",
      "type": "go",
      "request": "launch",
      "mode": "auto",
      "program": "${workspaceFolder}/cmd/server/main.go",
      "env": {
        "PORT": "8080",
        "ENV": "local_dev"
      },
      "args": ["--verbose"]
    }
  ]
}
```

During a breakpoint pause:

- Open **Goroutines View** to inspect all paused and running goroutines.
- Inspect channel buffer capacities and blocked channel readers/writers.

### Built-in Profiling with pprof & Flame Graphs

Running benchmarks with integrated memory and CPU profiling:

```go
// Benchmarking function in user_test.go
func BenchmarkUserSerialization(b *testing.B) {
    user := NewTestUser()
    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        _ = user.SerializeToJSON()
    }
}
```

- Right click benchmark -> **Run 'BenchmarkUserSerialization' with Profile** -> Select **CPU** or **Memory Allocation**.
- GoLand opens interactive **Flame Graphs** and **Method Call Trees** directly in the IDE.

### Build Tags & Cross-Compilation Run Configurations

Switching between build environments:

```go
// +build integration

package tests

import "testing"

func TestRemoteDatabaseIntegration(t *testing.T) {
    // Only compiled when build tag 'integration' is passed
}
```

## Common Patterns

### Headless Remote Delve Debugging

**Problem**: Debug Go services running inside Kubernetes or Docker containers.  
**Solution**: Connect GoLand to remote Delve debugger.

```bash
# Start Delve server in container
dlv exec ./my-binary --headless --listen=:2345 --api-version=2 --accept-multiclient
```

```xml
<!-- .run/Remote Debug.run.xml -->
<component name="ProjectRunConfigurationManager">
  <configuration default="false" name="Remote Debug" type="GoRemoteDebugConfigurationType">
    <port>2345</port>
    <host>localhost</host>
  </configuration>
</component>
```

## Best Practices

**Do**:

- Use GoLand's visual pprof flame graphs to profile memory allocations before optimizing code.
- Leverage GoLand inspections for detecting unchecked errors, unhandled goroutine leaks, and shadowed variables.
- Configure **Go Modules** integration with proper GOPROXY and GOPRIVATE settings for corporate repositories.
- Use structural search and replace for large-scale type and signature refactorings.

**Don't**:

- Ignore GoLand lint and staticcheck warnings; resolve warnings before committing.
- Commit `.idea/` workspace files containing local absolute paths or SDK bindings to Git.
- Run heavy tests without `-race` flag enabled to detect concurrent data races.

## Troubleshooting

| Error                                                    | Cause                                                                   | Solution                                                               |
| :------------------------------------------------------- | :---------------------------------------------------------------------- | :--------------------------------------------------------------------- |
| `Unresolved reference in GoLand but 'go build' succeeds` | IDE Go SDK or module cache out of sync with filesystem.                 | Go to **File > Invalidate Caches / Restart** and verify GOPATH/GOROOT. |
| `Debugger failed: could not launch process with Delve`   | Delve binary permission issue or macOS security signing.                | Grant Developer Tools permission in macOS System Settings > Security.  |
| `Go modules disabled in project`                         | GoLand project settings have "Enable Go modules integration" unchecked. | Check Settings > Go > Go Modules > **Enable Go modules integration**.  |

## References

- [GoLand Documentation](https://www.jetbrains.com/help/go/)
