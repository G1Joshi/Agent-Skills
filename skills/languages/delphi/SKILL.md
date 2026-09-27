---
name: delphi
description: Expert Delphi / Object Pascal assistance covering VCL, FireMonkey, RTL, and enterprise desktop software. Use when maintaining or modernizing Windows desktop and cross-platform native applications.
---

# Delphi / Object Pascal

Delphi (RAD Studio) and Free Pascal (Lazarus) keep Object Pascal alive. It is famous for **Single EXE** deployment and instant compilation.

## When to Use

- **Rapid Application Development (RAD) for Windows Desktop**: Building native Windows desktop applications with rich VCL graphical controls.
- **Legacy Enterprise Maintenance**: Modernizing and maintaining established corporate desktop software suites.
- **Single-Binary Zero-Dependency Native Compilation**: Producing fast, standalone native binaries that run without external runtime frameworks.
- **High-Performance Database Clients**: Interfacing with enterprise SQL databases via native FireDAC data access components.

## Quick Start

```pascal
program HelloWorld;
{$APPTYPE CONSOLE}
uses
  System.SysUtils;

begin
  try
    Writeln('Hello from Delphi Object Pascal!');
  except
    on E: Exception do
      Writeln(E.ClassName, ': ', E.Message);
  end;
end.
```

## Core Concepts

#Object Pascal Strong Typing & Class Architecture

Clean, readable object-oriented architecture with explicit interfaces:

```pascal
unit OrderProcessor;

interface

type
  IOrderService = interface
    ['{8F3D1E1C-3A62-47CF-A98B-7D12A9E32049}']
    function ProcessOrder(const OrderId: Integer; const Amount: Double): Boolean;
  end;

  TOrderService = class(TInterfacedObject, IOrderService)
  public
    function ProcessOrder(const OrderId: Integer; const Amount: Double): Boolean;
  end;

implementation

function TOrderService.ProcessOrder(const OrderId: Integer; const Amount: Double): Boolean;
begin
  // Business logic execution
  Result := Amount > 0.0;
end;

end.
```

#Visual Component Library (VCL) & FireMonkey (FMX)

- **VCL**: Native Windows-only components wrapping direct Win32/Win64 APIs.
- **FireMonkey (FMX)**: Cross-platform GPU-accelerated UI framework targeting Windows, macOS, iOS, and Android.

#FireDAC Unified Database Connectivity

High-performance data access layer:

```pascal
var
  Query: TFDQuery;
begin
  Query := TFDQuery.Create(nil);
  try
    Query.Connection := FDConnection1;
    Query.SQL.Text := 'SELECT * FROM Customers WHERE Balance > :MinBalance';
    Query.ParamByName('MinBalance').AsCurrency := 1000.0;
    Query.Open;
    // Process records
  finally
    Query.Free;
  end;
end;
```

## Common Patterns

### Safe Memory Management with Try..Finally

**Problem**: Object memory leaks in non-ARC desktop platforms when exceptions occur.

**Solution**:
Use explicit `try..finally` destruction blocks:

```pascal
procedure ProcessCustomerList;
var
  List: TStringList;
begin
  List := TStringList.Create;
  try
    List.Add('Customer 1');
    List.Add('Customer 2');
    List.SaveToFile('customers.txt');
  finally
    List.Free;
  end;
end;
```

## Best Practices (2026)

**Do**:

- **Always Wrap Object Allocations in `try...finally`**: Guarantee that `.Free` executes to prevent memory leaks in non-ARC Windows runtimes.
- **Use FireDAC for All Database Operations**: Standardize on FireDAC; deprecate legacy BDE and dbExpress components.
- **Target 64-Bit Windows (Win64)**: Ensure new applications compile for 64-bit to utilize modern memory spaces and system libraries.
- **Use Parameterized Queries**: Always use `ParamByName()` to prevent SQL injection vulnerabilities.

**Don't**:

- **Don't ignore compiler hints and warnings**: Treat Delphi compiler warnings with priority; they frequently identify uninitialized variables.
- **Don't use global variables in units**: Keep state encapsulated inside classes and records.
- **Don't block the UI thread with long database queries**: Execute heavy queries asynchronously using `TTask.Run` from the Parallel Programming Library.

## Troubleshooting

| Error                                                 | Cause                                                           | Solution                                                                        |
| :---------------------------------------------------- | :-------------------------------------------------------------- | :------------------------------------------------------------------------------ |
| `Access Violation at address ... (EAccessViolation)`  | Attempting to access an uninstantiated or freed object pointer. | Verify object was created with `.Create` before calling methods.                |
| `[dcc32 Fatal Error] F2084 Internal Error`            | Compiler cache corruption or circular unit dependency.          | Clean build directory and resolve circular references in `uses` clauses.        |
| `Memory Leak Detected in ReportMemoryLeaksOnShutdown` | Object created without matching `.Free` call.                   | Ensure every object creation is guarded with a `try..finally Free; end;` block. |

## References

- [Free Pascal](https://www.freepascal.org/)
