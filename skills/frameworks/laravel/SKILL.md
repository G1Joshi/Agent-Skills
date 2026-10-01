---
name: laravel
description: Expert Laravel assistance covering Eloquent ORM, Blade templating, queues, service providers, and Artisan CLI. Use when developing enterprise PHP web applications and robust REST APIs.
---

# Laravel

Laravel is an expressive PHP web application framework providing an elegant developer experience with Eloquent ORM, robust queues, events, and native real-time broadcasting.

## When to Use

- **Enterprise Full-Stack PHP Web Applications**: Building robust web portals with Eloquent ORM, Blade, and queues.
- **Modern Monoliths with Inertia.js**: Pairing Laravel backend routes directly with React or Vue frontends without API boilerplate.
- **High-Velocity REST APIs**: Utilizing Laravel API Resources, Sanctum authentication, and Form Requests.
- **Real-Time Applications with Laravel Reverb**: First-party WebSocket broadcasting and real-time dashboard events.

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

### Eloquent ORM with Relationships & Scopes

Expressive database models with type hinting:

```php
namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Illuminate\Database\Eloquent\Builder;

class Customer extends Model
{
    protected $fillable = ['name', 'email', 'is_active'];

    public function orders(): HasMany
    {
        return $this->hasMany(Order::class);
    }

    // Local query scope
    public function scopeActive(Builder $query): void
    {
        $query->where('is_active', true);
    }
}
```

### Form Requests & Validated Controllers

Strict input validation separated from controller logic:

```php
namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class StoreOrderRequest extends FormRequest
{
    public function authorize(): bool
    {
        return $this->user() !== null;
    }

    public function rules(): array
    {
        return [
            'customer_id' => 'required|exists:customers,id',
            'amount' => 'required|numeric|min:0.01',
            'items' => 'required|array|min:1',
            'items.*.product_id' => 'required|integer',
            'items.*.qty' => 'required|integer|min:1',
        ];
    }
}

// In Controller:
namespace App\Http\Controllers;

use App\Http\Requests\StoreOrderRequest;
use App\Models\Order;
use Illuminate\Http\JsonResponse;

class OrderController extends Controller
{
    public function store(StoreOrderRequest $request): JsonResponse
    {
        $validated = $request->validated();
        $order = Order::create($validated);

        return response()->json($order, 201);
    }
}
```

### Asynchronous Queue Workers & Jobs

Offloading heavy processing to Redis or SQS workers:

```php
namespace App\Jobs;

use App\Models\Order;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;
use Illuminate\Support\Facades\Mail;

class ProcessInvoiceJob implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    public function __construct(public Order $order) {}

    public function handle(): void
    {
        // Generate PDF and send invoice email
    }
}
```

## Common Patterns

### Eloquent Scope and Queue Dispatch

**Problem**: Processing heavy invoice calculations synchronously blocks user HTTP requests.

**Solution**:
Dispatch queued jobs with Eloquent local scopes:

```php
namespace App\Http\Controllers;

use App\Models\Order;
use App\Jobs\ProcessInvoiceJob;
use Illuminate\Http\JsonResponse;

class OrderController extends Controller
{
    public function complete(int $id): JsonResponse
    {
        $order = Order::active()->findOrFail($id);
        $order->update(['status' => 'completed']);

        // Dispatch to background queue worker
        ProcessInvoiceJob::dispatch($order)->onQueue('invoices');

        return response()->json(['message' => 'Order completed, invoice queued']);
    }
}
```

## Best Practices

**Do**:

- Target Laravel 11/12 with streamlined application structure and minimal configuration files.
- Use Form Requests for input validation instead of validating inline inside controllers.
- Utilize Eloquent eager loading (`with(['customer', 'items'])`) to prevent N+1 queries.
- Run queue workers under supervisor with Redis for reliable background job execution.

**Don't**:

- Execute raw database queries in Blade views or controllers; use Eloquent or repository classes.
- Run migrations directly in production without a verified backup and dry run.
- Commit the `.env` file to source control.

## Troubleshooting

| Error                                                 | Cause                                                       | Solution                                                              |
| :---------------------------------------------------- | :---------------------------------------------------------- | :-------------------------------------------------------------------- |
| `No application encryption key has been specified`    | `APP_KEY` missing in `.env` configuration file.             | Run `php artisan key:generate`.                                       |
| `Class '...' not found / Target class does not exist` | Namespace mismatch or service provider not loaded.          | Run `composer dump-autoload` and check namespace in `config/app.php`. |
| `SQLSTATE[HY000] [2002] Connection refused`           | Database service down or `.env` DB host/port misconfigured. | Verify database credentials and host (`127.0.0.1` vs `localhost`).    |

## References

- [Laravel Documentation](https://laravel.com/)
