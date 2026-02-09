---
name: spring-boot
description: Spring Boot Java framework for microservices with auto-configuration. Use for enterprise Java.
---

# Spring Boot

Java framework for building production-ready microservices.

## When to Use

- Enterprise Java applications
- Microservices architecture
- REST APIs with Java/Kotlin
- Cloud-native applications

## Quick Start

```java
@RestController
@RequestMapping("/api/users")
public class UserController {
    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }

    @GetMapping("/{id}")
    public ResponseEntity<User> getUser(@PathVariable Long id) {
        return userService.findById(id)
            .map(ResponseEntity::ok)
            .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping
    public ResponseEntity<User> createUser(@Valid @RequestBody CreateUserRequest request) {
        User user = userService.create(request);
        return ResponseEntity.created(URI.create("/api/users/" + user.getId())).body(user);
    }
}
```

## Core Concepts

### Dependency Injection

```java
@Service
@Transactional(readOnly = true)
public class UserService {
    private final UserRepository repository;
    private final PasswordEncoder passwordEncoder;

    public UserService(UserRepository repository, PasswordEncoder passwordEncoder) {
        this.repository = repository;
        this.passwordEncoder = passwordEncoder;
    }

    @Transactional
    public User create(CreateUserRequest request) {
        User user = new User();
        user.setEmail(request.email());
        user.setPassword(passwordEncoder.encode(request.password()));
        return repository.save(user);
    }

    public Optional<User> findById(Long id) {
        return repository.findById(id);
    }
}
```

### Spring Data JPA

```java
@Entity
@Table(name = "users")
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String email;

    @OneToMany(mappedBy = "author", cascade = CascadeType.ALL)
    private List<Post> posts = new ArrayList<>();
}

public interface UserRepository extends JpaRepository<User, Long> {
    Optional<User> findByEmail(String email);

    @Query("SELECT u FROM User u WHERE u.active = true")
    List<User> findActiveUsers();
}
```

## Common Patterns

### Exception Handling

```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleNotFound(ResourceNotFoundException ex) {
        return ResponseEntity.status(404)
            .body(new ErrorResponse(ex.getMessage()));
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidation(MethodArgumentNotValidException ex) {
        Map<String, String> errors = ex.getBindingResult().getFieldErrors().stream()
            .collect(Collectors.toMap(
                FieldError::getField,
                FieldError::getDefaultMessage
            ));
        return ResponseEntity.badRequest().body(new ErrorResponse("Validation failed", errors));
    }
}
```

## Best Practices

**Do**:

- Use constructor injection
- Use Spring Data repositories
- Implement proper error handling
- Use profiles for environments

**Don't**:

- Use field injection (@Autowired on fields)
- Expose entities directly
- Skip validation annotations
- Hardcode configuration

## Troubleshooting

| Issue               | Cause                | Solution                       |
| ------------------- | -------------------- | ------------------------------ |
| Bean not found      | Missing @Component   | Add stereotype annotation      |
| Circular dependency | Constructor circular | Use setter or @Lazy            |
| N+1 queries         | Missing fetch join   | Use @EntityGraph or JOIN FETCH |

## References

- [Spring Boot Documentation](https://spring.io/projects/spring-boot)
- [Baeldung Spring](https://www.baeldung.com/spring-boot)
