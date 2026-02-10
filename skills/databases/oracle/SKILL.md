---
name: oracle
description: Oracle Database with PL/SQL, RAC, and enterprise features. Use for enterprise systems.
---

# Oracle Database

Oracle Database is a multi-model database management system. It is the de-facto standard for Fortune 500 mission-critical systems due to its reliability, scalability (RAC), and PL/SQL power.

## When to Use

- **Mission Critical**: Banking, Airlines, Telecoms where 99.999% uptime is required.
- **PL/SQL**: When you have massive business logic that needs to run close to the data.
- **Complex Workloads**: OLTP and OLAP in the same DB.

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

### PL/SQL

Procedural Language/SQL. Extremely mature and powerful language stored within the DB.

### RAC (Real Application Clusters)

Allows multiple servers to access the same database storage simultaneously. If one server fails, the others keep running (High Availability).

### Multi-Tenant (CDB/PDB)

One Container Database (CDB) hosts multiple Pluggable Databases (PDBs). Efficient resource sharing.

## Best Practices (2025)

**Do**:

- **Use Oracle 23ai**: Leverage "JSON Relational Duality" to view the same data as both Tables and JSON Documents simultaneously.
- **Use Tuning Advisor**: Oracle's automated tuning tools are excellent.
- **Use Flashback**: Query data "as of" a timestamp in the past to recover from accidental logical errors.

**Don't**:

- **Don't commit in loops**: It kills IO. Commit once at the end.
- **Don't treat it like MySQL**: Oracle's architecture (Redo, Undo, Shared Pool) is heavier and requires specific tuning.

## References

- [Oracle Database 23ai Documentation](https://docs.oracle.com/en/database/oracle/oracle-database/)
