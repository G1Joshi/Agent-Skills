---
name: django
description: Expert Django assistance covering ORM, models, class-based views, admin interface, migrations, and Django REST Framework. Use when developing robust, scalable Python web applications and REST APIs.
---

# Django

Django is a high-level Python web framework encouraging rapid development, pragmatic clean design, built-in ORM security, robust migrations, and asynchronous view support.

## When to Use

- **Full-Featured Python Web Applications**: Batteries-included web development with built-in ORM, admin panel, auth, and migrations.
- **Content Management & Enterprise Backends**: Developing robust database-backed backends with automatic admin dashboards.
- **High-Throughput REST APIs**: Building secure APIs using Django REST Framework (DRF) or Django Ninja.
- **Async Python Web Services**: Utilizing ASGI, async views, and background tasks on Django 5.x.

## Quick Start

```python
# models.py
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    # New in 5.0: Database generated field
    slug = models.GeneratedField(
        expression=models.functions.Concat(models.F("title"), models.Value("-slug")),
        output_field=models.CharField(max_length=205),
        db_persist=True,
    )
```

## Core Concepts

### Django ORM Models & Migrations

Relational schema definition with indexing and query optimizations:

```python
from django.db import models
from django.utils import timezone

class Customer(models.Model):
    email = models.EmailField(unique=True, db_index=True)
    full_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} ({self.email})"

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_fulfilled = models.BooleanField(default=False)
    placed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['customer', 'is_fulfilled']),
        ]
```

### High-Performance Querying with select_related & prefetch_related

Eliminating N+1 database queries:

```python
from django.shortcuts import render
from .models import Order

def order_report_view(request):
    # select_related performs SQL JOIN for 1-to-1 and ForeignKey
    # prefetch_related performs separate batch query for ManyToMany
    orders = Order.objects.filter(is_fulfilled=True) \
                          .select_related('customer') \
                          .only('id', 'total_amount', 'customer__full_name')[:50]

    return render(request, 'orders/report.html', {'orders': orders})
```

### Fast Async APIs with Django Ninja

Type-safe REST API endpoints powered by Pydantic:

```python
from ninja import NinjaAPI, Schema
from typing import List

api = NinjaAPI(title="Inventory API", version="1.0.0")

class ProductOut(Schema):
    id: int
    name: str
    price: float
    in_stock: bool

@api.get("/products", response=List[ProductOut])
async def list_products(request):
    # Async view querying ASGI backend
    return [
        {"id": 1, "name": "Mechanical Keyboard", "price": 129.99, "in_stock": True}
    ]
```

## Common Patterns

### Prefetching Related Objects to Prevent N+1 Queries

**Problem**: Accessing foreign keys or many-to-many relationships in template/API loops generates hundreds of database queries.

**Solution**:
Use `select_related` for ForeignKeys and `prefetch_related` for M2M:

```python
# Fetches books and authors in a single optimized JOIN query
books = Book.objects.filter(is_published=True)    .select_related("publisher")    .prefetch_related("authors")    .order_by("-published_date")[:50]

for book in books:
    print(f"{book.title} published by {book.publisher.name}")
```

## Best Practices

**Do**:

- Always use `select_related` and `prefetch_related` to eliminate N+1 database query bottlenecks.
- Configure `django-environ` to keep secret keys, database credentials, and API tokens out of code.
- Run migrations in CI pipelines (`python manage.py check --deploy` and `makemigrations --check`).
- Use `Bulk` operations (`bulk_create`, `bulk_update`) when modifying more than 10 records.

**Don't**:

- Leave `DEBUG = True` in production environments; it leaks memory and sensitive stack traces.
- Put business logic inside templates or views; encapsulate domain rules in model methods or service layers.
- Use synchronous external HTTP calls in view handlers; use async views or Celery/Redis tasks.

## Troubleshooting

| Error                                                 | Cause                                                | Solution                                                                               |
| :---------------------------------------------------- | :--------------------------------------------------- | :------------------------------------------------------------------------------------- |
| `django.db.utils.OperationalError: no such table`     | Database migrations have not been applied.           | Run `python manage.py migrate`.                                                        |
| `CSRF verification failed. Request aborted (403)`     | POST form submitted without `{% csrf_token %}` tag.  | Include `{% csrf_token %}` in HTML form or verify CSRF cookie headers in API requests. |
| `FieldError: Cannot resolve keyword '...' into field` | Misspelled field name in `filter()` or `order_by()`. | Check model definition and ensure double underscores `__` for relationship lookups.    |

## References

- [Django Documentation](https://www.djangoproject.com/)
