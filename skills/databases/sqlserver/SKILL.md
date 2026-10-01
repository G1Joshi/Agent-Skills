---
name: sqlserver
description: Expert Microsoft SQL Server assistance covering T-SQL, execution plans, index tuning, Always On availability groups, and DMV profiling. Use when developing enterprise .NET applications, administering SQL Server, or optimizing T-SQL.
---

# SQL Server (MSSQL)

Microsoft SQL Server is an enterprise-grade RDBMS. It uses T-SQL (Transact-SQL), an extension of SQL that adds procedural programming, local variables, and data processing.

## When to Use

- **Enterprise Microsoft Ecosystems**: The primary relational database for .NET, C#, Azure SQL, and Windows Server infrastructure.
- **Complex Financial & ERP Transaction Processing**: Running mission-critical workloads with Advanced Data Security and Always On Availability Groups.
- **In-Memory OLTP & Temporal Tables**: High-throughput memory-optimized tables and automated system-versioned temporal audit tracking.
- **Automated Performance Tuning**: Utilizing Query Store to analyze execution plan regressions and force optimal query plans.

## Quick Start

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

### System-Versioned Temporal Tables

Automatically captures complete historical audit trails for every row mutation:

```sql
CREATE TABLE dbo.Employee (
    EmployeeID INT IDENTITY(1,1) PRIMARY KEY,
    FullName NVARCHAR(100) NOT NULL,
    Department NVARCHAR(50) NOT NULL,
    Salary DECIMAL(10,2) NOT NULL,
    SysStartTime DATETIME2 GENERATED ALWAYS AS ROW START HIDDEN,
    SysEndTime DATETIME2 GENERATED ALWAYS AS ROW END HIDDEN,
    PERIOD FOR SYSTEM_TIME (SysStartTime, SysEndTime)
) WITH (SYSTEM_VERSIONING = ON (HISTORY_TABLE = dbo.EmployeeHistory));

-- Query row state as of specific point in time
SELECT * FROM dbo.Employee
FOR SYSTEM_TIME AS OF '2026-01-15 12:00:00'
WHERE EmployeeID = 101;
```

### Always On Availability Groups

Synchronous and asynchronous multi-database replication across high-availability failover nodes:

```text
[ Primary Replica (Read/Write) ] ──Synchronous Commit──→ [ Secondary Replica (Readable) ]
                                          │
                                          ▼
                               [ Disaster Recovery Replica (Async) ]
```

### Query Store & Plan Forcing

Captures query performance history, runtime statistics, and forces stable execution plans:

```sql
-- Enable Query Store
ALTER DATABASE EnterpriseDB SET QUERY_STORE = ON;

-- Force specific compiled execution plan to stop regression
EXEC sp_query_store_force_plan @query_id = 42, @plan_id = 108;
```

## Common Patterns

### Index with Included Columns for Covering Queries

**Problem**: Wide indexes waste storage and index page space, while narrow indexes trigger expensive Key Lookups.

**Solution**:
Create index with search columns in key and projection columns in `INCLUDE`:

```sql
CREATE NONCLUSTERED INDEX IX_Orders_CustomerId_Status
ON Sales.Orders (CustomerId, OrderStatus)
INCLUDE (OrderDate, TotalAmount);

-- Covering query executes purely from index pages without Key Lookup
SELECT OrderDate, TotalAmount
FROM Sales.Orders
WHERE CustomerId = 1205 AND OrderStatus = 'Shipped';
```

## Best Practices

**Do**:

- Enable Query Store on All Production Databases: Track execution plan regressions and runtime latency metrics automatically.
- Use Parameterized Queries: Prevent parameter sniffing regressions and eliminate SQL injection vulnerabilities.
- Index Foreign Keys: Manually index foreign key columns to prevent table locks during cascades and deletions.
- Use Read-Intent Routing: Direct reporting queries to readable secondary replicas (`ApplicationIntent=ReadOnly`).

**Don't**:

- Use `NOLOCK` indiscriminately: `WITH (NOLOCK)` causes dirty reads, phantom records, and duplicate row scans.
- Use generic `VARCHAR(MAX)` everywhere: Oversized LOB types bypass memory optimization and degrade performance.
- Perform row-by-row cursor processing: Replace procedural cursors with set-based SQL queries.

## Troubleshooting

| Error                                                                 | Cause                                                           | Solution                                                                          |
| :-------------------------------------------------------------------- | :-------------------------------------------------------------- | :-------------------------------------------------------------------------------- |
| `Transaction (Process ID ...) was deadlocked on lock resources`       | Two transactions competing for locks in reverse sequence.       | Implement try-catch retry logic; ensure consistent object access order.           |
| `Could not allocate space for object in database ... tablespace full` | Datafile or transaction log disk storage exhausted.             | Check autogrowth settings, backup transaction log (`BACKUP LOG`), or expand disk. |
| `Implicit conversion causing index scan`                              | Data type mismatch (e.g. VARCHAR comparing to NVARCHAR column). | Align parameter types with column definitions in application queries.             |

## References

- [Microsoft SQL Docs](https://learn.microsoft.com/en-us/sql/sql-server/)
