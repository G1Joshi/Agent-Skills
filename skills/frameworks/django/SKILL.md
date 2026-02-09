---
name: django
description: Django Python full-stack framework with ORM, admin, and auth. Use for Python web apps.
---

# Django

Python full-stack web framework with batteries included.

## When to Use

- Full-stack Python web applications
- Content management systems
- Admin interfaces
- Rapid prototyping with ORM

## Quick Start

```python
# views.py
from django.http import JsonResponse
from .models import User

def user_list(request):
    users = User.objects.filter(is_active=True).values('id', 'name', 'email')
    return JsonResponse(list(users), safe=False)

# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('api/users/', views.user_list),
]
```

## Core Concepts

### Models

```python
from django.db import models

class User(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    content = models.TextField()
    published = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['author', 'published']),
        ]
```

### QuerySets

```python
# Efficient queries
users = User.objects.filter(
    is_active=True,
    posts__published=True
).select_related('profile').prefetch_related('posts').distinct()

# Aggregation
from django.db.models import Count, Avg

stats = User.objects.annotate(
    post_count=Count('posts'),
    avg_views=Avg('posts__views')
).filter(post_count__gt=5)

# F expressions for DB-level operations
from django.db.models import F

Post.objects.filter(id=post_id).update(views=F('views') + 1)
```

## Common Patterns

### Class-Based Views

```python
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

class PostListView(ListView):
    model = Post
    template_name = 'posts/list.html'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(published=True).select_related('author')

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    success_url = '/posts/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
```

## Best Practices

**Do**:

- Use select_related/prefetch_related
- Use F() and Q() for complex queries
- Implement proper permissions
- Use Django REST Framework for APIs

**Don't**:

- Query in templates (N+1)
- Store secrets in settings.py
- Skip migrations in production
- Use raw SQL without parameterization

## Troubleshooting

| Issue              | Cause            | Solution                    |
| ------------------ | ---------------- | --------------------------- |
| N+1 queries        | Missing prefetch | Add select/prefetch_related |
| Migration conflict | Parallel changes | Merge migrations            |
| CSRF error         | Missing token    | Add {% csrf_token %}        |

## References

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
