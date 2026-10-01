---
name: oracle
description: Expert Oracle Database assistance covering PL/SQL, cost-based optimizer, partitioning, RAC, and Data Guard. Use when writing enterprise SQL, managing Oracle schemas, or optimizing heavy OLTP workloads.
---

# Oracle Database

Oracle Database is a multi-model database management system. It is the de-facto standard for Fortune 500 mission-critical systems due to its reliability, scalability (RAC), and PL/SQL power.

## When to Use

- **Mission-Critical Global Enterprise OLTP**: Running Tier-1 core banking, telecommunications, ERP, and supply chain workloads.
- **Oracle Real Application Clusters (RAC)**: Achieving active-active shared-everything database clustering and transparent failover.
- **Advanced PL/SQL Procedural Logic**: Executing complex enterprise business rules, packages, and triggers directly inside the database.
- **Multitenant Pluggable Databases (PDB)**: Consolidating hundreds of isolated tenant databases under a single Container Database (CDB).

## Quick Start

```sql
-- Implicit cursor loop in PL/SQL
BEGIN
  FOR r IN (SELECT first_name, last_name FROM employees WHERE department_id = 10)
  LOOP
    DBMS_OUTPUT.PUT_LINE(r.first_name || ' ' || r.last_name);
  END LOOP;
END;
/
```

## Core Concepts

### Multitenant Architecture (CDB and PDBs)

One Container Database (CDB) manages system memory and background processes; Pluggable Databases (PDBs) run independently:

```text
[ Container Database (CDB$ROOT) ]
        ├── [ Pluggable DB: PDB_FINANCE ]
        ├── [ Pluggable DB: PDB_HR ]
        └── [ Pluggable DB: PDB_COMMERCE ]
```

### PL/SQL Stored Packages & Transaction Management

Encapsulates procedural business logic with compiled database performance:

```sql
CREATE OR REPLACE PACKAGE BODY FinancialOps AS
    PROCEDURE TransferFunds(
        p_from_acc IN NUMBER,
        p_to_acc   IN NUMBER,
        p_amount   IN NUMBER
    ) IS
    BEGIN
        UPDATE Accounts SET Balance = Balance - p_amount WHERE AccountId = p_from_acc;
        UPDATE Accounts SET Balance = Balance + p_amount WHERE AccountId = p_to_acc;
        COMMIT;
    EXCEPTION
        WHEN OTHERS THEN
            ROLLBACK;
            RAISE_APPLICATION_ERROR(-20001, 'Fund transfer failed: ' || SQLERRM);
    END TransferFunds;
END FinancialOps;
/
```

### Automatic Workload Repository (AWR) & ASH

Comprehensive database performance monitoring and execution profiling:

```sql
-- Generate AWR Performance Snapshot
EXEC DBMS_WORKLOAD_REPOSITORY.CREATE_SNAPSHOT();
```

## Common Patterns

### Bulk Data Processing with PL/SQL FORALL and BULK COLLECT

**Problem**: Processing thousands of rows row-by-row in PL/SQL creates massive context-switch overhead between SQL and PL/SQL engines.

**Solution**:
Use `BULK COLLECT` and `FORALL` for batch processing:

```sql
DECLARE
  TYPE t_emp_list IS TABLE OF employees%ROWTYPE;
  v_emps t_emp_list;
BEGIN
  -- Batch collect into memory
  SELECT * BULK COLLECT INTO v_emps FROM employees WHERE status = 'PENDING';

  -- Batch update in a single engine context switch
  FORALL i IN 1..v_emps.COUNT
    UPDATE employees
    SET status = 'PROCESSED', processed_date = SYSDATE
    WHERE employee_id = v_emps(i).employee_id;

  COMMIT;
END;
/
```

## Best Practices

**Do**:

- Use Bind Variables Everywhere: Bind variables (`:val`) prevent hard parsing, reduce latch contention, and stop SQL injection.
- Analyze AWR Reports Regularly: Inspect the "Top 5 Timed Events" in AWR to identify I/O bottlenecks and locking contention.
- Implement Partitioning for Massive Tables: Partition multi-terabyte tables by range or hash to enable partition pruning.
- Use Automatic Memory Management (AMM): Allow Oracle to balance PGA (work areas) and SGA (buffer cache/shared pool) dynamically.

**Don't**:

- Hardcode literals in production queries: Literal strings force Oracle to recompile and pollute the Shared Pool with distinct execution plans.
- Commit inside iterative row loops: Committing row-by-row causes `ORA-01555 Snapshot Too Old` errors and redo log thrashing.
- Ignore index monitoring: Drop unused indexes to reclaim storage and reduce write lock overhead.

## Troubleshooting

| Error                                                        | Cause                                                                | Solution                                                                             |
| :----------------------------------------------------------- | :------------------------------------------------------------------- | :----------------------------------------------------------------------------------- |
| `ORA-01555: snapshot too old`                                | Rollback segments/undo tablespace overwritten by long-running query. | Increase `UNDO_RETENTION` and resize undo tablespace.                                |
| `ORA-00054: resource busy and acquire with NOWAIT specified` | Table locked by another active uncommitted DDL or DML transaction.   | Wait for transaction to complete or identify blocking session via `V$LOCKED_OBJECT`. |
| `ORA-01653: unable to extend table ... in tablespace`        | Tablespace is full or max datafile size reached.                     | Add a new datafile or enable `AUTOEXTEND ON` for tablespace.                         |

## References

- [Oracle Database 23ai Documentation](https://docs.oracle.com/en/database/oracle/oracle-database/)
