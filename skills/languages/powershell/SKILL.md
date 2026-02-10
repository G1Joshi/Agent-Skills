---
name: powershell
description: PowerShell scripting for Windows automation, cmdlets, and administration. Use for .ps1 files.
---

# PowerShell

A task-based command-line shell and scripting language built on .NET.

## When to Use

- Windows system administration
- Azure management
- Object-oriented scripting
- Cross-platform automation (PowerShell Core)

## Quick Start

```powershell
$name = "World"
Write-Host "Hello, $name!"

$processes = Get-Process | Where-Object { $_.CPU -gt 10 }
foreach ($p in $processes) {
    Write-Output $p.Name
}
```

## Core Concepts

### Cmdlets

Lightweight commands used in the PowerShell environment (Verb-Noun structure).

- `Get-Process`
- `New-Item`
- `Set-Location`

### Objects

PowerShell pipes **Objects**, not text.

```powershell
Get-Service | Select-Object -Property Name, Status
```

### Pipeline

Passes objects from one cmdlet to the next.

## Best Practices

**Do**:

- Use the Verb-Noun naming convention for functions
- Use `Try/Catch` for error handling
- Use `[CmdletBinding()]` for advanced functions
- Output objects, not text (`Write-Output` over `Write-Host`)

**Don't**:

- Parse text output like in Bash (use object properties)
- Use aliases in scripts (readability)

## References

- [Microsoft PowerShell Docs](https://learn.microsoft.com/en-us/powershell/)
