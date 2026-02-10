---
name: cobol
description: COBOL for mainframe and legacy business systems. Use for .cob files.
---

# COBOL

COBOL runs 70% of the world's business transactions. Modern COBOL (GnuCOBOL 3.2 / IBM Enterprise COBOL) supports **JSON**, XML, and Object-Oriented features.

## When to Use

- **Mainframes**: The backbone of banking/insurance systems (CICS/IMS).
- **Legacy Migration**: Moving logic to Linux/Cloud using GnuCOBOL.
- **Decimal Arithmetic**: Native fixed-point math (`PICTURE 9V99`) is unmatched for currency.

## Core Concepts

### Divisions

`IDENTIFICATION`, `ENVIRONMENT`, `DATA`, `PROCEDURE`.

### Picture Clause

`01 SALARY PIC 9(5)V99`. Defines data layout precisely.

### PERFORM

The main control flow loop.

## Best Practices (2025)

**Do**:

- **Use GnuCOBOL**: For local development on Mac/Linux.
- **Use `VS Code`**: With the `bitlang.cobol` extension.
- **Unit Test**: Use `COBOL Check` or `ZUnit`.

**Don't**:

- **Don't use `GO TO`**: Use `PERFORM` and structured programming.

## References

- [GnuCOBOL FAQ](https://gnucobol.sourceforge.io/faq/)
