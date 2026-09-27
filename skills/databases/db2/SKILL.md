---
name: db2
description: Expert IBM Db2 assistance covering relational SQL, pureScale, BLU acceleration, and enterprise database administration. Use when managing mainframe systems, running hybrid cloud Db2, or tuning enterprise OLTP/OLAP.
---

# IBM Db2

Db2 is a family of data management products, including the relational database. It is famous for running on Mainframes (z/OS) but also runs on Linux/Unix/Windows (LUW).

## When to Use

- **Mission-Critical Enterprise Systems**: Running core banking, financial transaction processing, and mainframe legacy enterprise workloads.
- **PureXML & Hybrid Relational Workloads**: Storing and indexing hierarchical XML and JSON documents alongside relational SQL tables.
- **IBM z/OS Mainframe & Linux/Power Integration**: Interfacing with enterprise IBM infrastructure with absolute data durability.
- **High Availability Disaster Recovery (HADR)**: Mission-critical zero-data-loss failover architectures across physical datacenters.

## Quick Start

```sql
-- Minimal Db2 Table Creation with Index
CREATE TABLE HR.EMPLOYEES (
    EMP_ID INT NOT NULL GENERATED ALWAYS AS IDENTITY (START WITH 1000 INCREMENT BY 1),
    FIRST_NAME VARCHAR(50) NOT NULL,
    LAST_NAME VARCHAR(50) NOT NULL,
    DEPARTMENT VARCHAR(50),
    HIRE_DATE DATE DEFAULT CURRENT DATE,
    SALARY DECIMAL(10,2),
    PRIMARY KEY (EMP_ID)
);

CREATE INDEX HR.IDX_EMP_DEPT ON HR.EMPLOYEES (DEPARTMENT, SALARY DESC);
```

## Core Concepts

#Table Spaces & Storage Groups Architecture

Fine-grained control over physical storage containers, buffer pools, and disk layouts:

```sql
-- Create Enterprise Storage Space
CREATE TABLESPACE TS_ORDERS
  PAGESIZE 32K
  MANAGED BY AUTOMATIC STORAGE
  BUFFERPOOL BP32K;

CREATE TABLE ENTERPRISE.ORDERS (
  ORDER_ID BIGINT NOT NULL GENERATED ALWAYS AS IDENTITY (START WITH 1000, INCREMENT BY 1),
  CUSTOMER_ID VARCHAR(32) NOT NULL,
  ORDER_DATE TIMESTAMP NOT NULL DEFAULT CURRENT TIMESTAMP,
  TOTAL_AMOUNT DECIMAL(15,2) NOT NULL,
  CONSTRAINT PK_ORDERS PRIMARY KEY (ORDER_ID)
) IN TS_ORDERS;
```

#pureQuery & Static SQL Execution

Pre-compiles and optimizes SQL queries into static execution plans for maximum mainframe execution efficiency:

```sql
-- Optimized Stored Procedure
CREATE OR REPLACE PROCEDURE GET_CUSTOMER_SUMMARY (
    IN p_customer_id VARCHAR(32),
    OUT p_total_orders INT,
    OUT p_total_spend DECIMAL(15,2)
)
LANGUAGE SQL
BEGIN
    SELECT COUNT(*), COALESCE(SUM(TOTAL_AMOUNT), 0.0)
    INTO p_total_orders, p_total_spend
    FROM ENTERPRISE.ORDERS
    WHERE CUSTOMER_ID = p_customer_id;
END@
```

#High Availability Disaster Recovery (HADR)

Replicates transaction log buffers synchronously from primary to standby instances:

```
[ Primary DB2 Server ] ──Synchronous Log Shipping (HADR)──→ [ Standby DB2 Server ]
```

## Common Patterns

### Runstats and Optimizer Plan Refresh

**Problem**: The Db2 cost-based optimizer selects inefficient table-scan access plans after bulk inserts.

**Solution**:
Update catalog statistics and rebind packages:

```sql
-- Collect detailed distribution statistics for indexes and data pages
RUNSTATS ON TABLE HR.EMPLOYEES WITH DISTRIBUTION AND DETAILED INDEXES ALL;

-- Flush package cache to force plan recompilation
FLUSH PACKAGE CACHE DYNAMIC;
```

## Best Practices (2026)

**Do**:

- **Run `RUNSTATS` Regularly**: Ensure optimizer statistics are current (`RUNSTATS ON TABLE schema.table WITH DISTRIBUTION AND DETAILED INDEXES ALL`).
- **Tune Buffer Pools**: Allocate adequate physical memory to buffer pools to minimize disk I/O wait times.
- **Use Lock Avoidance Techniques**: Set `DB2_EVALUNCOMMITTED=YES` to skip rows that do not satisfy search predicates during scans.
- **Implement Reorg Checks**: Monitor table and index fragmentation and schedule automated reorganizations (`REORG TABLE`).

**Don't**:

- **Don't use unindexed foreign keys**: Unindexed child foreign keys cause table-level locks during parent row deletions.
- **Don't run long-running analytical queries against the OLTP primary**: Direct analytical queries to HADR read-on-standby replicas.
- **Don't omit isolation levels**: Explicitly declare isolation levels (`WITH CS`, `WITH UR`) to prevent unnecessary row locking.

## Troubleshooting

| Error                                           | Cause                                                                | Solution                                                                     |
| :---------------------------------------------- | :------------------------------------------------------------------- | :--------------------------------------------------------------------------- |
| `SQL0911N Deadlock or timeout (Reason code 68)` | Lock escalation or concurrent transactions contending on same pages. | Commit transactions frequently; check `LOCKLIST` and `MAXLOCKS` settings.    |
| `SQL0204N Undefined name`                       | Table or schema does not exist or user lacks schema qualification.   | Qualify tables explicitly (e.g. `SCHEMA.TABLENAME`) or set `CURRENT SCHEMA`. |
| `SQL0286N Default table space cannot be found`  | Table row size exceeds maximum page size of default tablespace.      | Create a tablespace with a larger page size (16K or 32K) for wide tables.    |

## References

- [IBM Db2 Documentation](https://www.ibm.com/docs/en/db2)
