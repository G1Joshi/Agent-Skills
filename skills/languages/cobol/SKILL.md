---
name: cobol
description: Expert COBOL programming assistance covering enterprise batch processing, divisions, copybooks, and data formatting. Use when maintaining legacy banking, government, or mainframe systems.
---

# COBOL

COBOL runs 70% of the world's business transactions. Modern COBOL (GnuCOBOL 3.2 / IBM Enterprise COBOL) supports **JSON**, XML, and Object-Oriented features.

## When to Use

- **Mainframe Core Banking & Insurance Systems**: Maintaining and extending mission-critical legacy financial ledger engines.
- **High-Volume Fixed-Point Financial Calculations**: Executing exact decimal math without floating-point rounding errors.
- **Batch Processing on IBM z/OS**: Processing millions of nightly accounting records, payroll statements, and clearinghouse transactions.
- **Modernizing Legacy Mainframes via APIs**: Wrapping legacy COBOL subprograms with REST/gRPC interfaces via IBM z/OS Connect.

## Quick Start

```cobol
       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLO-WORLD.
       PROCEDURE DIVISION.
           DISPLAY 'Hello, Enterprise COBOL'.
           STOP RUN.
```

## Core Concepts

#Four Classical Divisions Architecture

Every COBOL program is structured strictly across four standard functional divisions:

```cobol
IDENTIFICATION DIVISION.
PROGRAM-ID. HELLO-BANKING.

ENVIRONMENT DIVISION.
CONFIGURATION SECTION.

DATA DIVISION.
WORKING-STORAGE SECTION.
01 WS-TRANSACTION-AMOUNT  PIC 9(7)V99 VALUE 1500.50.
01 WS-FORMATTED-OUTPUT    PIC $$,$$$,$$9.99.

PROCEDURE DIVISION.
    MOVE WS-TRANSACTION-AMOUNT TO WS-FORMATTED-OUTPUT
    DISPLAY "Processed Amount: " WS-FORMATTED-OUTPUT
    GOBACK.
```

#Picture Clauses (`PIC`) for Fixed-Point Arithmetic

Eliminates floating-point rounding discrepancies by defining exact digit layouts and implied decimals (`V`):

```cobol
01 WS-ACCOUNT-BALANCE   PIC S9(9)V99 COMP-3.
*> S: Signed, 9 digits before decimal, V: implied decimal, 2 fractional digits
*> COMP-3: Packed Decimal (2 digits per byte) optimized for mainframe ALU
```

#Structured Paragraphs & PERFORM Loops

Modern COBOL (COBOL 2002/2014) utilizes structured control statements:

```cobol
PERFORM VARYING WS-IDX FROM 1 BY 1 UNTIL WS-IDX > 10
    ADD WS-ITEM-PRICE(WS-IDX) TO WS-ORDER-TOTAL
END-PERFORM.
```

## Common Patterns

### Sequential File Processing Loop

**Problem**: Processing large fixed-width batch files without loading entire file into memory.

**Solution**:
Use structured `READ` loop with `AT END` flag:

```cobol
       DATA DIVISION.
       FILE SECTION.
       FD  CUSTOMER-FILE.
       01  CUSTOMER-RECORD.
           05  CUST-ID        PIC 9(5).
           05  CUST-NAME      PIC X(20).
       WORKING-STORAGE SECTION.
       01  WS-EOF             PIC X VALUE 'N'.
           88  END-OF-FILE          VALUE 'Y'.

       PROCEDURE DIVISION.
       100-MAIN-PROCESS.
           OPEN INPUT CUSTOMER-FILE
           PERFORM UNTIL END-OF-FILE
               READ CUSTOMER-FILE
                   AT END
                       SET END-OF-FILE TO TRUE
                   NOT AT END
                       DISPLAY 'Customer: ' CUST-NAME
               END-READ
           END-PERFORM
           CLOSE CUSTOMER-FILE
           STOP RUN.
```

## Best Practices (2026)

**Do**:

- **Use `COMP-3` (Packed Decimal) for Financial Numbers**: Maximize mathematical computation performance on IBM Z enterprise hardware.
- **Adopt Modern Free-Format COBOL**: Eliminate column 7-72 restrictions when supported by modern compilers (GnuCOBOL, IBM Enterprise COBOL).
- **Use Explicit Scope Terminators**: Always close control blocks with `END-IF`, `END-PERFORM`, and `END-READ` rather than terminal periods.
- **Validate Input Data with `NUMERIC` Tests**: Run `IF WS-INPUT-VAL IS NUMERIC` to prevent data exception abends (`0C7`).

**Don't**:

- **Don't use `GO TO` statements**: Eliminate unstructured `GO TO` jumps; use modern structured `PERFORM` paragraphs.
- **Don't rely on terminal periods for logic flow**: Stray periods terminate all nested `IF` conditions prematurely.
- **Don't neglect binary fields initialization**: Always initialize working-storage variables with `VALUE` clauses to prevent garbage data.

## Troubleshooting

| Error                                      | Cause                                                                | Solution                                                              |
| :----------------------------------------- | :------------------------------------------------------------------- | :-------------------------------------------------------------------- |
| `FILE STATUS 35: File not found`           | Physical file path not mapped in JCL or environment.                 | Verify `ASSIGN TO` clause and dataset DD statement.                   |
| `DATA DIVISION syntax error in Area A`     | Division, Section, or 01 level headers not starting in columns 8-11. | Align level-01 and division headers in Area A (columns 8-11).         |
| `FILE STATUS 39: File attributes mismatch` | Record length in program differs from cataloged physical file.       | Ensure `RECORD CONTAINS` clause matches the actual file block length. |

## References

- [GnuCOBOL FAQ](https://gnucobol.sourceforge.io/faq/)
