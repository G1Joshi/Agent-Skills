---
name: gatling
description: Gatling load testing for APIs. Use for load testing.
---

# Gatling

Gatling is a powerful load testing tool. It is designed for ease of use, maintainability, and high performance. It uses an asynchronous (Akka/Netty) architecture that allows generating huge load from a single machine.

## When to Use

- **High Throughput**: When you need to simulate 10k+ users from a single laptop.
- **Complex Scenarios**: The DSL (Domain Specific Language) allows describing very complex user journeys.
- **JVM Shops**: If your team uses Java/Scala/Kotlin.

## Quick Start (Java)

```java
import static io.gatling.javaapi.core.CoreDsl.*;
import static io.gatling.javaapi.http.HttpDsl.*;

public class BasicSimulation extends Simulation {

  HttpProtocolBuilder httpProtocol = http
    .baseUrl("http://computer-database.gatling.io")
    .acceptHeader("application/json");

  ScenarioBuilder scn = scenario("BasicSimulation")
    .exec(http("request_1").get("/computers"));

  {
    setUp(
      scn.injectOpen(atOnceUsers(10))
    ).protocols(httpProtocol);
  }
}
```

## Core Concepts

### Simulation

The definition of the load test. Contains the HTTP configuration, the _Scenario_ (steps users take), and the _Injection Profile_ (how users arrive).

### Feeders

Mechanisms to inject data (valid usernames, search terms) from CSV/JSON into the virtual users so they don't all look identical.

## Best Practices (2025)

**Do**:

- **Use the Java/Kotlin DSL**: Scala was the default, but Java/Kotlin SDKs are now first-class and easier for most teams.
- **Record User Journeys**: Use the Gatling Recorder (proxy) to capture browser interactions, then clean up the code.

**Don't**:

- **Don't ignore reports**: Gatling generates beautiful HTML reports at the end. Open `index.html` to see the response time distribution graphs.

## References

- [Gatling Documentation](https://gatling.io/docs/gatling/)
