---
name: perl
description: Expert Perl assistance covering regular expressions, hashes, CPAN modules, and text processing. Use when maintaining legacy Perl scripts, performing complex regex manipulations, or writing sysadmin tools.
---

# Perl

Perl 5.40 (2024) introduced a **native `try/catch`** and the `__CLASS__` keyword. It remains unbeatable for text processing one-liners.

## When to Use

- **Text Processing & Regex Data Extraction**: Rapidly parsing unstructured log files, reports, and legacy data streams.
- **Legacy System Administration & DevOps**: Maintaining established Unix/Linux automation scripts and cron jobs.
- **Bioinformatics & Scientific Data Wrangling**: Processing genomic sequencing data and legacy scientific FASTA records.
- **Maintaining Classic CPAN Applications**: Supporting production enterprise backends built on Catalyst, Mojolicious, or Dancer.

## Quick Start

```perl
#!/usr/bin/env perl
use strict;
use warnings;
use feature 'say';

my %scores = ( Alice => 95, Bob => 88, Charlie => 92 );

for my $name (sort keys %scores) {
    say "$name scored $scores{$name}";
}
```

## Core Concepts

#Regular Expressions as First-Class Language Primitives

Perl regular expressions are deeply integrated into language syntax:

```perl
use strict;
use warnings;
use v5.36;

my $log_entry = '[2026-09-27 10:15:30] ERROR: Payment gateway timeout (code 504)';

if ($log_entry =~ /\[(.*?)\]\s+(\w+):\s+(.*)/) {
    my ($timestamp, $severity, $message) = ($1, $2, $3);
    say "Timestamp: $timestamp";
    say "Severity:  $severity";
    say "Message:   $message";
}
```

#Modern Perl (v5.36+ / v5.38+) Native Subroutine Signatures

Replaces manual `@_` unpacking with native typed signatures and experimental class features:

```perl
use v5.38;
use experimental 'class';

class Account {
    field $balance :param = 0;

    method deposit($amount) {
        $balance += $amount;
        return $balance;
    }

    method get_balance() { return $balance; }
}

my $acc = Account->new(balance => 100);
$acc->deposit(50);
say "Balance: ", $acc->get_balance(); # 150
```

#Context Awareness (Scalar vs List Context)

Functions dynamically change return values based on whether a scalar or list is expected:

```perl
my @items = ("apple", "banana", "cherry");
my $count = @items;     # Scalar context returns array count: 3
my ($first) = @items;   # List context returns first element: "apple"
```

## Common Patterns

### Robust File Parsing with Regular Expressions

**Problem**: Extracting structured fields from inconsistent log files.

**Solution**:
Use strict mode with named regex capture groups:

```perl
use strict;
use warnings;
use feature 'say';

while (my $line = <DATA>) {
    chomp $line;
    if ($line =~ /^\[(?<timestamp>[^\]]+)\]\s+(?<level>INFO|WARN|ERROR)\s+(?<msg>.*)$/) {
        say "Time: $+{timestamp} | Level: $+{level} | Message: $+{msg}";
    }
}

__DATA__
[2025-03-01 12:00:00] INFO Server started successfully
[2025-03-01 12:01:23] ERROR Database connection failed
```

## Best Practices (2026)

**Do**:

- **Always Declare `use strict; use warnings;`**: Eliminate dangerous silent global variables and undeclared lexical bugs.
- **Use `use v5.36;` or Higher**: Automatically enables strict, warnings, modern subroutine signatures, and say syntax.
- **Use Mojolicious for Web APIs**: Build modern non-blocking web backends and WebSockets with Mojolicious.
- **Manage Dependencies with `cpanm` and `Carton`**: Isolate project dependencies locally in `local/` rather than modifying system Perl.

**Don't**:

- **Don't use single-character global punctuation variables**: Replace `$@`, `$/`, and `$_` with readable `English` module aliases or modern signatures.
- **Don't use two-argument `open`**: Always use 3-argument open (`open(my $fh, "<", $filename)`) with lexical filehandles.
- **Don't write new OO code with bare blessed hashes**: Use modern `use v5.38; use experimental 'class';` or `Moo`/`Moose`.

## Troubleshooting

| Error                                                | Cause                                                                   | Solution                                                           |
| :--------------------------------------------------- | :---------------------------------------------------------------------- | :----------------------------------------------------------------- |
| `Global symbol "..." requires explicit package name` | Variable used without prior `my`, `our`, or `state` under `use strict`. | Declare variable with `my $var`.                                   |
| `Can't locate ... in @INC`                           | Required CPAN module not installed in Perl lib path.                    | Install module using `cpanm Module::Name`.                         |
| `Modification of a read-only value attempted`        | Attempting to modify constant or `$_` aliased to literal string.        | Assign to local mutable variable `my $copy = $_` before modifying. |

## References

- [Perl.org](https://www.perl.org/)
