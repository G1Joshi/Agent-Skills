---
name: django
description: Django Python full-stack framework with ORM, admin, and auth. Use for Python web apps.
---

# Django

Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. Django 5.0 (2025) introduces database-computed default values and expanded async support.

## When to Use

- **Perfectionists with deadlines**: The "batteries-included" philosophy means Auth, Admin, and ORM are ready day one.
- **Data-Driven Apps**: The Django Admin is still the best auto-generated admin interface in the industry.
- **Enterprise**: Security features (CSRF, SQL Injection protection) are best-in-class.

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

### MTV Architecture

Model (Data), Template (Presentation), View (Business Logic).

### The ORM

Powerful abstraction over SQL. `Post.objects.filter(pub_date__year=2025)`.

### Async Django

Django 5 supports async views, ORM calls (`aget_object_or_404`), and Auth methods (`alogin`).

## Best Practices (2025)

**Do**:

- **Use `GeneratedField`**: Let the database handle computed columns instead of Python properties for better performance.
- **Use Async Views**: For I/O bound tasks (calling external APIs), use `async def view(request):`.
- **Use `django-ninja`**: For building APIs, it's faster and cleaner than DRF (Django Rest Framework) and uses Pydantic.

**Don't**:

- **Don't put logic in templates**: Keep templates dumb. Put logic in Models or Services.

## References

- [Django Documentation](https://www.djangoproject.com/)
