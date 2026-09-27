---
name: vbnet
description: Expert Visual Basic .NET assistance covering LINQ, WinForms, WPF, ASP.NET, and enterprise .NET migration. Use when maintaining or modernizing enterprise VB.NET applications.
---

# VB.NET

VB.NET is a first-class citizen on .NET, sharing the same runtime/libraries as C#. While C# gets new syntax first, VB.NET remains supported in .NET 8+.

## When to Use

- **Enterprise .NET Business Applications**: Maintaining and modernizing established line-of-business applications on .NET 8 / 9.
- **Office Automation & Desktop Systems**: WPF, Windows Forms, and VSTO enterprise solutions.
- **Rapid Database Scripting & Reporting**: Utilizing LINQ to SQL, Entity Framework Core, and typed DataSets in enterprise IT environments.
- **Financial & Insurance Calculation Engines**: Leveraging clear English-like syntax for complex business rule implementation.

## Quick Start

```vb
Module Program
    Sub Main()
        Dim numbers = {1, 2, 3, 4, 5}
        Dim evens = From n In numbers Where n Mod 2 = 0 Select n

        For Each num In evens
            Console.WriteLine("Even number: " & num)
        Next
    End Sub
End Module
```

## Core Concepts

#Modern Asynchronous I/O with Async/Await

Non-blocking operations using .NET Task-based Asynchronous Pattern (TAP):

```vb
Imports System.IO
Imports System.Net.Http
Imports System.Threading.Tasks

Public Class ApiService
    Private Shared ReadOnly HttpClient As New HttpClient()

    Public Async Function DownloadAndSaveAsync(url As String, destinationPath As String) As Task(Of Integer)
        Using response As HttpResponseMessage = Await HttpClient.GetAsync(url, HttpCompletionOption.ResponseHeadersRead)
            response.EnsureSuccessStatusCode()

            Using contentStream As Stream = Await response.Content.ReadAsStreamAsync()
                Using fileStream As New FileStream(destinationPath, FileMode.Create, FileAccess.Write, FileShare.None, 8192, useAsync:=True)
                    Await contentStream.CopyToAsync(fileStream)
                End Using
            End Using
        End Using

        Return CInt(New FileInfo(destinationPath).Length)
    End Function
End Class
```

#Expressive LINQ Queries & In-Memory Transformations

Declarative data filtering, grouping, and projection:

```vb
Imports System
Imports System.Collections.Generic
Imports System.Linq

Public Class Order
    Public Property OrderId As Integer
    Public Property CustomerName As String
    Public Property TotalAmount As Decimal
    Public Property IsFulfilled As Boolean
End Class

Public Module OrderAnalytics
    Public Function SummarizeTopCustomers(orders As IEnumerable(Of Order)) As IEnumerable(Of Object)
        Dim query = From o In orders
                    Where o.IsFulfilled AndAlso o.TotalAmount > 500D
                    Group o By o.CustomerName Into CustomerOrders = Group, TotalSpent = Sum(o.TotalAmount)
                    Order By TotalSpent Descending
                    Select New With {
                        .Customer = CustomerName,
                        .OrderCount = CustomerOrders.Count(),
                        .TotalSpent = TotalSpent
                    }

        Return query.ToList()
    End Function
End Module
```

#Event Handling & Custom Delegates

Clean event publication and subscription using the .NET event model:

```vb
Imports System

Public Class StockTicker
    Public Event PriceChanged(sender As Object, e As PriceChangedEventArgs)

    Private _currentPrice As Decimal

    Public Sub UpdatePrice(newPrice As Decimal)
        If _currentPrice <> newPrice Then
            Dim old = _currentPrice
            _currentPrice = newPrice
            RaiseEvent PriceChanged(Me, New PriceChangedEventArgs(old, newPrice))
        End If
    End Sub
End Class

Public Class PriceChangedEventArgs
    Inherits EventArgs

    Public ReadOnly Property OldPrice As Decimal
    Public ReadOnly Property NewPrice As Decimal

    Public Sub New(oldPrice As Decimal, newPrice As Decimal)
        Me.OldPrice = oldPrice
        Me.NewPrice = newPrice
    End Sub
End Class
```

## Common Patterns

### Safe Null Checking and Null-Coalescing

**Problem**: `NullReferenceException` on optional database objects or missing configuration.

**Solution**:
Use null-conditional `?.` and null-coalescing `If`:

```vb
Public Class CustomerService
    Public Function GetCustomerCity(cust As Customer) As String
        ' Safe traversal and default fallback
        Dim city As String = If(cust?.Address?.City, "Unknown City")
        Return city
    End Function
End Class
```

## Best Practices (2026)

- **Do** set `Option Strict On` and `Option Explicit On` at the top of every file or project-wide to eliminate runtime type coercion bugs.
- **Do** target modern `.NET 8` or `.NET 9` LTS rather than legacy .NET Framework 4.x for performance, security, and cross-platform runtime execution.
- **Do** use `Using ... End Using` statements on all types implementing `IDisposable` to ensure deterministic resource cleanup.
- **Do** use `Async` and `Await` for I/O operations rather than synchronous `.Result` or `.Wait()`.
- **Don't** use legacy Microsoft.VisualBasic runtime helpers (e.g. `Len()`, `Left()`, `MsgBox()`); use standard .NET BCL equivalents.
- **Don't** use untyped `Object` variables; use strongly typed generic collections (`List(Of T)`, `Dictionary(Of TKey, TValue)`).
- **Don't** leave exception catch blocks empty; log errors or rethrow with `Throw` preserving the stack trace.

## Troubleshooting

| Error                                                      | Cause                                                            | Solution                                                                |
| :--------------------------------------------------------- | :--------------------------------------------------------------- | :---------------------------------------------------------------------- |
| `BC30456: '...' is not a member of '...'`                  | Method or property does not exist on target type or casing typo. | Verify property spelling and imported namespaces.                       |
| `System.NullReferenceException: Object reference not set`  | Accessing member on uninstantiated object reference.             | Guard access with `If obj IsNot Nothing Then` or null-conditional `?.`. |
| `BC30512: Option Strict On disallows implicit conversions` | Attempting implicit type conversion with `Option Strict On`.     | Cast explicitly using `CInt()`, `CStr()`, or `CType()`.                 |

## References

- [Microsoft VB.NET Guide](https://learn.microsoft.com/en-us/dotnet/visual-basic/)
