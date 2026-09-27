---
name: phpstorm
description: Expert PhpStorm assistance covering PHP language tooling, Laravel/Symfony integrations, Xdebug setup, Composer dependency inspection, and database tooling. Use when configuring Xdebug remote debugging, setting up PHPStan/Psalm inspections, optimizing IDE performance, or debugging PHP applications.
---

# PhpStorm

PhpStorm is essential for modern PHP. It understands **Laravel** Facades, **Symfony** Dependency Injection, and **Doctrine** queries.

## When to Use

- **Enterprise PHP & Laravel/Symfony Development**: Deep static analysis, auto-completion, and framework-aware refactoring.
- **Interactive Step Debugging with Xdebug**: Profiling execution paths, variable inspections, and setting conditional breakpoints.
- **PHPStan & Psalm Static Analysis Integration**: Real-time IDE diagnostics and automated type inference repairs.
- **Database Tooling & Remote Server Deployment**: Managing MariaDB/PostgreSQL instances and SFTP/SSH deployment pipelines.

## Quick Start

### 1. Docker Xdebug Configuration for PhpStorm

```ini
; php.ini / 99-xdebug.ini
[xdebug]
zend_extension=xdebug.so
xdebug.mode=debug,develop
xdebug.start_with_request=yes
xdebug.client_host=host.docker.internal
xdebug.client_port=9003
xdebug.idekey=PHPSTORM
```

### 2. Configure PHP CLI Interpreter

- Go to **Settings/Preferences > PHP**.
- Set **PHP Executable** or configure **Docker / Docker Compose** remote interpreter.
- Click **Validate Debugger** to confirm port `9003` handshake.
- Turn on the telephone icon (**Start Listening for PHP Debug Connections**).

## Core Concepts

### Advanced Xdebug 3 Configuration

Setting up `php.ini` and configuring PhpStorm for zero-config Xdebug step debugging:

```ini
; php.ini (PHP 8.3 / 8.4)
[xdebug]
zend_extension = xdebug.so
xdebug.mode = debug,develop
xdebug.start_with_request = yes
xdebug.client_host = host.docker.internal
xdebug.client_port = 9003
xdebug.idekey = PHPSTORM
xdebug.log = /tmp/xdebug.log
```

Connecting PhpStorm to Docker Container mapping in `.idea/php.xml`:

```xml
<project version="4">
  <component name="PhpDebugGeneral" listening_started="true" />
  <component name="PhpServers">
    <servers>
      <server host="localhost" id="docker_server" name="docker_server" port="8080" use_path_mappings="true">
        <path_mappings>
          <mapping local-root="$PROJECT_DIR$" remote-root="/var/www/html" />
        </path_mappings>
      </server>
    </servers>
  </component>
</project>
```

### Framework Metadata Enhancement (`.phpstorm.meta.php`)

Providing PhpStorm with container return types and factory inference:

```php
<?php
// .phpstorm.meta.php
namespace PHPSTORM_META {
    override(\Illuminate\Contracts\Container\Container::make(0), map([
        '' => '@',
    ]));
    override(\app(0), map([
        '' => '@',
    ]));
}
```

### Static Analysis Automation (PHPStan & Pint)

Configuring Composer scripts and real-time inspections:

```json
{
  "scripts": {
    "lint": "pint --test",
    "lint:fix": "pint",
    "analyse": "phpstan analyse --level=9 --memory-limit=1G"
  }
}
```

## Common Patterns

### Path Mapping for Dockerized Projects

**Problem**: Breakpoints inside Docker containers are not hit because local and container filesystem paths differ.  
**Solution**: Define path mappings in **PHP > Servers**.

- Host: `localhost` (Port: `8080`)
- Check **Use path mappings**
- Map project root `/Users/username/Code/my-project` to `/var/www/html`.

### Static Analysis (PHPStan / Psalm) Integration

**Problem**: Enforce strict type checks inside editor inspection gutters before code commit.  
**Solution**: Enable PHPStan in PhpStorm settings.

- Navigate to **PHP > Quality Tools > PHPStan**.
- Select Configuration file: `./phpstan.neon`.
- Set inspection level (e.g. Level 8). Highlighted errors appear live in the editor.

```neon
# phpstan.neon
parameters:
    level: 8
    paths:
        - app
        - tests
    checkMissingIterableValueType: false
```

## Best Practices (2026)

- **Do** configure **PHPStan** or **Psalm** as a real-time inspection engine under **Settings -> Languages & Frameworks -> PHP -> Quality Tools**.
- **Do** generate `.phpstorm.meta.php` and `_ide_helper.php` using Laravel IDE Helper for full autocompletion of magic facades.
- **Do** use Docker Compose PHP Interpreters for consistent PHP runtime versions across engineering teams.
- **Do** configure path mappings accurately when debugging code executing inside Docker or remote VMs.
- **Don't** commit the user-specific workspace files inside `.idea/` (add `.idea/workspace.xml` and `.idea/shelf/` to `.gitignore`).
- **Don't** leave Xdebug enabled in production PHP environments; it carries significant performance overhead.
- **Don't** ignore PhpStorm inspections; utilize `Alt + Enter` for instant automated quick-fixes.

## Troubleshooting

| Error / Symptom                           | Cause                                                                   | Solution                                                                                                     |
| ----------------------------------------- | ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| Xdebug breakpoint ignored / not triggered | `xdebug.client_host` wrong or firewall blocking port 9003               | Use `host.docker.internal` on Docker for Mac/Windows, verify IDE listener is enabled (green telephone icon). |
| High memory usage or slow indexing        | Indexing large directories like `storage/`, `var/`, or generated caches | Right-click directory > **Mark Directory as > Excluded**.                                                    |
| Laravel facade autocompletion broken      | PhpStorm does not know dynamic magic methods on facades                 | Install and run `barryvdh/laravel-ide-helper`: `php artisan ide-helper:generate`.                            |

## References

- [PhpStorm Documentation](https://www.jetbrains.com/phpstorm/documentation/)
