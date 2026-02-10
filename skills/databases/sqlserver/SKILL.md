---
name: sqlserver
description: Microsoft SQL Server with T-SQL, SSMS, and enterprise features. Use for Windows/Azure.
---

# SQL Server (MSSQL)

Microsoft SQL Server is an enterprise-grade RDBMS. It uses T-SQL (Transact-SQL), an extension of SQL that adds procedural programming, local variables, and data processing.

## When to Use

- **Enterprise .NET Stack**: Deep integration with C#, Azure, and Visual Studio.
- **Complex Analytics**: Built-in Analysis Services (SSAS) and Reporting (SSRS).
- **Corporate Environments**: Active Directory integration for security.

## Quick Start (T-SQL)

```sql
-- CTE and Window Function
WITH Sales_CTE AS (
    SELECT SalesPersonID, SUM(TotalDue) AS TotalSales
    FROM Sales.SalesOrderHeader
    GROUP BY SalesPersonID
)
SELECT SalesPersonID, TotalSales,
       RANK() OVER (ORDER BY TotalSales DESC) AS SalesRank
FROM Sales_CTE;
```

## Core Concepts

### T-SQL

Powerful procedural extensions.

```sql
DECLARE @Counter INT = 1;
WHILE @Counter <= 10
BEGIN
   PRINT @Counter;
   SET @Counter = @Counter + 1;
END
```

### SQL Agent

Built-in job scheduler for backups, maintenance, and scripts.

### Clustered Index

Organizes the data in the table physically. Usually the Primary Key. A table can likely have only one.

## Best Practices (2025)

**Do**:

- **Use AI Integration (2025)**: Call `sp_invoke_external_rest_endpoint` to integrate Azure OpenAI directly into queries.
- **Use `APPLY` operator**: `CROSS APPLY` is powerful for joining a table to a table-valued function.
- **Query Store**: Enable Query Store to track performance regressions over time automatically.

**Don't**:

- **Don't use cursors**: T-SQL set-based operations are almost always faster.
- **Don't use `NOLOCK` blindly**: It causes dirty reads. Use `READ COMMITTED SNAPSHOT` isolation instead.

## References

- [Microsoft SQL Docs](https://learn.microsoft.com/en-us/sql/sql-server/)
