---
name: mariadb
description: MariaDB MySQL-compatible database with Galera clustering. Use for MySQL-compatible database needs.
---

# MariaDB

MySQL-compatible database with enhanced features and Galera clustering.

## When to Use

- MySQL-compatible applications
- High-availability setups with Galera
- Drop-in MySQL replacement
- Open-source enterprise databases

## Quick Start

```sql
-- Create table (MySQL compatible)
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- MariaDB-specific features
CREATE TABLE events (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    data JSON NOT NULL,
    created_at TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP(6)
);
```

## Core Concepts

### JSON Support

```sql
-- Store JSON data
INSERT INTO products (data) VALUES (
    '{"name": "Laptop", "specs": {"ram": 16, "storage": 512}}'
);

-- Query JSON
SELECT
    JSON_VALUE(data, '$.name') as name,
    JSON_VALUE(data, '$.specs.ram') as ram
FROM products
WHERE JSON_VALUE(data, '$.specs.ram') > 8;

-- JSON table functions
SELECT * FROM products,
    JSON_TABLE(data, '$' COLUMNS(
        name VARCHAR(100) PATH '$.name',
        ram INT PATH '$.specs.ram'
    )) AS jt;
```

### Window Functions

```sql
SELECT
    customer_id,
    order_date,
    amount,
    SUM(amount) OVER (
        PARTITION BY customer_id
        ORDER BY order_date
        ROWS UNBOUNDED PRECEDING
    ) as running_total,
    ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date) as order_num
FROM orders;
```

## Common Patterns

### Galera Cluster Setup

```ini
# my.cnf for Galera
[galera]
wsrep_on=ON
wsrep_provider=/usr/lib/galera/libgalera_smm.so
wsrep_cluster_address="gcomm://node1,node2,node3"
wsrep_cluster_name="my_cluster"
wsrep_node_address="node1_ip"
wsrep_node_name="node1"
wsrep_sst_method=rsync
binlog_format=ROW
```

### Sequence Engine

```sql
-- Generate sequences
SELECT seq FROM seq_1_to_10;  -- 1,2,3...10
SELECT seq FROM seq_0_to_100_step_5;  -- 0,5,10...100

-- Use in joins for reporting
SELECT
    d.seq as day,
    COALESCE(COUNT(o.id), 0) as orders
FROM seq_1_to_31 d
LEFT JOIN orders o ON DAY(o.created_at) = d.seq
GROUP BY d.seq;
```

## Best Practices

**Do**:

- Use InnoDB engine by default
- Enable binary logging for replication
- Use utf8mb4 charset
- Monitor Galera cluster state

**Don't**:

- Mix storage engines in transactions
- Use MyISAM for new tables
- Ignore wsrep\_\* status variables
- Skip backup testing

## Troubleshooting

| Issue         | Cause                         | Solution                   |
| ------------- | ----------------------------- | -------------------------- |
| Cluster split | Network partition             | Check wsrep_cluster_status |
| SST slow      | Large dataset                 | Use xtrabackup SST         |
| Deadlock      | Galera certification conflict | Retry transaction          |

## References

- [MariaDB Documentation](https://mariadb.com/kb/)
- [Galera Cluster](https://galeracluster.com/library/)
