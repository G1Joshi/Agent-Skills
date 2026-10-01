---
name: symfony
description: Expert Symfony assistance covering PHP HTTP kernel, Twig, Doctrine ORM, services, and MakerBundle. Use when building enterprise PHP applications and web services.
---

# Symfony

Symfony is a decoupled, reusable PHP framework and set of components, emphasizing strict typing, PHP Attributes, and enterprise application architecture.

## When to Use

- **Enterprise PHP Web Applications & APIs**: High-performance backend architectures adhering strictly to design patterns.
- **Modular Enterprise Microservices**: Decoupled Symfony Components (HTTP Kernel, Console, Messenger, Serializer).
- **Asynchronous Message Queue Processing**: Handling event-driven message architectures with Symfony Messenger.
- **REST & GraphQL with API Platform**: Auto-generating compliant JSON:API and OpenAPI backends.

## Quick Start

```php
// src/Controller/ApiController.php
namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\Routing\Attribute\Route;

class ApiController extends AbstractController
{
    #[Route('/api/status', name: 'api_status', methods: ['GET'])]
    public function status(): JsonResponse
    {
        return $this->json(['status' => 'operational', 'framework' => 'symfony']);
    }
}
```

## Core Concepts

### Modern Attribute Routing & Dependency Injection

Writing controllers with PHP 8.2+ native attributes:

```php
namespace App\Controller;

use App\Repository\CustomerRepository;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Attribute\Route;

#[Route('/api/v1/customers', name: 'api_customers_')]
class CustomerController extends AbstractController
{
    public function __construct(
        private readonly CustomerRepository $customerRepository
    ) {}

    #[Route('/{id}', name: 'show', methods: ['GET'])]
    public function show(int $id): JsonResponse
    {
        $customer = $this->customerRepository->find($id);

        if (!$customer) {
            return $this->json(['error' => 'Customer not found'], Response::HTTP_NOT_FOUND);
        }

        return $this->json($customer);
    }
}
```

### Doctrine ORM Entities & Attributes

Mapping database tables with native PHP attributes:

```php
namespace App\Entity;

use Doctrine\ORM\Mapping as ORM;
use Symfony\Component\Validator\Constraints as Assert;

#[ORM\Entity]
#[ORM\Table(name: 'orders')]
class Order
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column]
    private ?int $id = null;

    #[ORM\Column(length: 255)]
    #[Assert\NotBlank]
    private string $reference;

    #[ORM\Column(type: 'decimal', precision: 10, scale: 2)]
    #[Assert\Positive]
    private string $totalAmount;

    public function getId(): ?int { return $this->id; }
    public function getReference(): string { return $this->reference; }
    public function setReference(string $ref): self { $this->reference = $ref; return $this; }
    public function getTotalAmount(): string { return $this->totalAmount; }
    public function setTotalAmount(string $amount): self { $this->totalAmount = $amount; return $this; }
}
```

### Symfony Messenger for Async Processing

Decoupled message dispatching and handling:

```php
namespace App\Message;

class ProcessInvoiceMessage
{
    public function __construct(public readonly int $orderId) {}
}

// In Message Handler:
namespace App\MessageHandler;

use App\Message\ProcessInvoiceMessage;
use Symfony\Component\Messenger\Attribute\AsMessageHandler;

#[AsMessageHandler]
class ProcessInvoiceHandler
{
    public function __invoke(ProcessInvoiceMessage $message): void
    {
        // Handle background invoice generation
    }
}
```

## Common Patterns

### Doctrine Entity Repository with Custom DQL Query

**Problem**: Generic `find()` methods unable to execute efficient joined queries.

**Solution**:
Write custom repository query builders:

```php
namespace App\Repository;

use App\Entity\Product;
use Doctrine\Bundle\DoctrineBundle\Repository\ServiceEntityRepository;
use Doctrine\Persistence\ManagerRegistry;

class ProductRepository extends ServiceEntityRepository
{
    public function __construct(ManagerRegistry $registry)
    {
        parent::__construct($registry, Product::class);
    }

    public function findTopInStock(int $limit = 10): array
    {
        return $this->createQueryBuilder('p')
            ->andWhere('p.stock > 0')
            ->orderBy('p.createdAt', 'DESC')
            ->setMaxResults($limit)
            ->getQuery()
            ->getResult();
    }
}
```

## Best Practices

**Do**:

- Target Symfony 7+ using PHP 8.2+ native attributes for routing, entities, and validation.
- Utilize Symfony Messenger for all asynchronous and queue-based background processing.
- Run `bin/console lint:container` and `bin/console lint:yaml` in CI/CD pipelines.
- Configure Symfony Cache with Redis for high-traffic session and doctrine result caching.

**Don't**:

- Put business logic inside controllers; encapsulate workflows in domain services.
- Run `cache:clear` directly on active production traffic; warm up cache in a staging release directory.
- Disable CSRF protection on state-changing web form submissions.

## Troubleshooting

| Error                                                                 | Cause                                                       | Solution                                                              |
| :-------------------------------------------------------------------- | :---------------------------------------------------------- | :-------------------------------------------------------------------- |
| `ServiceNotFoundException: You have requested a non-existent service` | Service not autowired or missing in `config/services.yaml`. | Ensure class is in `src/` and check autowiring in `services.yaml`.    |
| `No route found for "GET /path"`                                      | Route attribute missing or cache stale.                     | Clear Symfony cache: `php bin/console cache:clear`.                   |
| `DriverException: An exception occurred in the driver: Access denied` | Database credentials incorrect in `.env` or `DATABASE_URL`. | Update `.env.local` with valid database host, username, and password. |

## References

- [Symfony Documentation](https://symfony.com/)
