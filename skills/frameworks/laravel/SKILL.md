---
name: laravel
description: Laravel PHP framework with Eloquent ORM and Blade templates. Use for PHP applications.
---

# Laravel

Laravel is a web application framework with expressive, elegant syntax. Laravel 11 (2025) introduces a streamlined skeleton and native WebSocket server (Reverb).

## When to Use

- **Solo Developers / Small Teams**: The ecosystem (Forge, Vapor, Nova) solves devops and admin needs.
- **PHP Shops**: The gold standard for modern PHP.
- **Real-time Apps**: The new Reverb server makes WebSockets a first-class citizen without external Node dependencies.

## Quick Start

```php
// routes/web.php
Route::get('/', function () {
    return view('welcome');
});

// app/Models/User.php
// Elegant Active Record
$users = User::where('active', 1)->get();
```

## Core Concepts

### Slim Skeleton (v11)

Laravel 11 removed `Kernel.php` and Middleware classes. Configuration fits in `bootstrap/app.php`. Example:

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->validateCsrfTokens(except: ['stripe/*']);
})
```

### Laravel Reverb

First-party WebSocket server written in PHP. Scalable and fast.

### Ecosystem

- **Livewire**: Build dynamic UIs with PHP (similar to Hotwire/Blazor).
- **Filament**: Amazing Admin/Dashboard builder built on Livewire.

## Best Practices (2025)

**Do**:

- **Use Filament**: For admin panels, it is vastly superior to Nova in 2025 for customizability.
- **Use `Pest`**: The new default testing framework. It's beautiful and minimal.
- **Use `cast()` attributes**: Define model casts using the method syntax for clear type conversions.

**Don't**:

- **Don't over-abstract**: Laravel Facades (`Route::`, `DB::`) are fine. Don't create Repository patterns unless you actually need to swap implementations.

## References

- [Laravel Documentation](https://laravel.com/)
