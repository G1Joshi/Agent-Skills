---
name: powershell
description: Expert PowerShell assistance covering cmdlet pipelines, object manipulation, modules, and cross-platform scripting. Use when automating Windows/Azure administration, creating scripts, or managing DevOps tasks.
---

# PowerShell

A task-based command-line shell and scripting language built on .NET.

## When to Use

- **Windows Enterprise & Active Directory Automation**: Managing Windows Server, Azure Active Directory, Hyper-V, and Exchange estates.
- **Cross-Platform DevOps Automation (PS 7+)**: Writing cross-platform administration scripts executing identically on Windows, Linux, and macOS.
- **Azure Infrastructure Orchestration (Az Module)**: Automating cloud resource deployment, subscriptions, and security compliance policies.
- **Object-Oriented Pipeline Scripting**: Passing structured .NET objects between commands rather than raw unstructured text streams.

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

#Object-Oriented Pipeline Architecture

Commands pass strongly-typed .NET objects rather than plain text; downstream commands access properties directly:

```powershell
# Passes rich Process objects through the pipeline
Get-Process |
  Where-Object WorkingSet64 -GT 500MB |
  Sort-Object WorkingSet64 -Descending |
  Select-Object -First 5 -Property Name, Id, @{Name="RAM_MB"; Expression={$_.WorkingSet64 / 1MB}}
```

#Advanced Parameter Validation & Cmdlet Binding

Enforces parameter types, mandatory attributes, and validation rules:

```powershell
function Invoke-Deployment {
    [CmdletBinding(SupportsShouldProcess)]
    param(
        [Parameter(Mandatory = $true)]
        [ValidateSet("Staging", "Production")]
        [string]$Environment,

        [Parameter(Mandatory = $true)]
        [ValidatePattern('^v\d+\.\d+\.\d+$')]
        [string]$Version
    )

    if ($PSCmdlet.ShouldProcess($Environment, "Deploying release $Version")) {
        Write-Host "Deploying $Version to $Environment..." -ForegroundColor Green
    }
}
```

#Error Action Preferences and Try/Catch

Handles terminating and non-terminating errors cleanly:

```powershell
$ErrorActionPreference = "Stop" # Treat all errors as terminating

try {
    Invoke-RestMethod -Uri "https://api.internal.corp/status" -Method GET -TimeoutSec 5
} catch [System.Net.WebException] {
    Write-Warning "Network connection failed: $($_.Exception.Message)"
} catch {
    Write-Error "Unexpected fatal error: $_"
}
```

## Common Patterns

### Advanced Pipeline Function with ShouldProcess Support

**Problem**: Automating destructive infrastructure changes without dry-run safety mechanisms.

**Solution**:
Build advanced functions supporting `-WhatIf` and pipeline input:

```powershell
function Remove-StaleLogs {
    [CmdletBinding(SupportsShouldProcess = $true)]
    param(
        [Parameter(Mandatory = $true, ValueFromPipelineByPropertyName = $true)]
        [string]$Path,
        [int]$DaysOld = 30
    )
    process {
        $cutoff = (Get-Date).AddDays(-$DaysOld)
        Get-ChildItem -Path $Path -Filter *.log | Where-Object { $_.LastWriteTime -lt $cutoff } | ForEach-Object {
            if ($PSCmdlet.ShouldProcess($_.FullName, "Delete stale log")) {
                Remove-Item $_.FullName -Force
            }
        }
    }
}
```

## Best Practices (2026)

**Do**:

- **Follow Standard Approved Verb-Noun Naming**: Use approved verbs (`Get-`, `Set-`, `New-`, `Remove-`, `Invoke-`).
- **Use PowerShell 7+ (pwsh)**: Standardize on cross-platform PowerShell 7+; avoid legacy Windows PowerShell 5.1.
- **Add `[CmdletBinding()]` to Custom Functions**: Gain automatic support for `-Verbose`, `-Debug`, and `-ErrorAction`.
- **Use PSScriptAnalyzer in CI**: Run automated static analysis to catch security flaws and code quality issues.

**Don't**:

- **Don't use command aliases in production scripts**: Avoid `ls`, `cat`, `curl`, and `select`; use full cmdlet names (`Get-ChildItem`).
- **Don't parse text output with regex when objects exist**: Access object properties directly (`$proc.Id`) rather than parsing text.
- **Don't store plaintext passwords**: Use `PSCredential` with SecretManagement or Azure Key Vault.

## Troubleshooting

| Error                                                      | Cause                                                                | Solution                                                                    |
| :--------------------------------------------------------- | :------------------------------------------------------------------- | :-------------------------------------------------------------------------- |
| `execution of scripts is disabled on this system`          | Execution policy restricts running unsigned PowerShell scripts.      | Run `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`. |
| `The term '...' is not recognized as the name of a cmdlet` | Module not installed, missing in `$env:PSModulePath`, or typo.       | Install module with `Install-Module -Name <Name>`.                          |
| `Cannot bind argument to parameter because it is null`     | Parameter defined with `[Parameter(Mandatory)]` received null input. | Verify pipeline output or provide default parameter value.                  |

## References

- [Microsoft PowerShell Docs](https://learn.microsoft.com/en-us/powershell/)
