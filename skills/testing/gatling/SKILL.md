---
name: gatling
description: Expert Gatling load testing assistance covering virtual users, scenarios, assertions, and throughput benchmarking. Use when designing performance tests, stress-testing HTTP APIs, or analyzing latency distributions.
---

# Gatling

Gatling is a powerful load testing tool. It is designed for ease of use, maintainability, and high performance. It uses an asynchronous (Akka/Netty) architecture that allows generating huge load from a single machine.

## When to Use

- **High-Concurrency Load Testing**: Simulating tens of thousands of concurrent virtual users with minimal CPU and memory footprints.
- **Performance Regression Gates in CI/CD**: Running automated performance assertions against staging environments on every release.
- **Scala / Java / Kotlin / TypeScript Load DSLs**: Writing programmatic, version-controlled load testing scenarios as code.
- **Protocol Benchmarking**: Stress testing HTTP, WebSockets, Server-Sent Events, and JMS message queues.

## Quick Start

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

### Non-Blocking Asynchronous Engine (Netty & Akka)

Unlike thread-per-user load tools, Gatling uses non-blocking actors to simulate thousands of users on a single OS thread:

```text
[ Gatling Scenario Engine ] ──(Netty Event Loop)──→ [ Thousands of Async Virtual Users ]
```

### Scenario DSL & Injection Profiles (Java / TypeScript)

Defines user journeys, think times, and virtual user ramp-up profiles:

```java
// Java / Scala Gatling Simulation
import io.gatling.javaapi.core.*;
import io.gatling.javaapi.http.*;
import static io.gatling.javaapi.core.CoreDsl.*;
import static io.gatling.javaapi.http.HttpDsl.*;

public class ApiLoadSimulation extends Simulation {
    HttpProtocolBuilder httpProtocol = http
        .baseUrl("https://api.staging.example.com")
        .acceptHeader("application/json");

    ScenarioBuilder scn = scenario("Browse and Checkout")
        .exec(http("Get Products").get("/products").check(status().is(200)))
        .pause(2)
        .exec(http("Add to Cart").post("/cart").body(StringBody("{"id": 101}")).asJson());

    {
        setUp(
            scn.injectOpen(
                rampUsers(500).during(60) // Ramp up to 500 users over 60 seconds
            )
        ).protocols(httpProtocol)
         .assertions(
             global().responseTime().percentile(95).lt(300), // 95th percentile under 300ms
             global().successfulRequests().percent().gt(99.0) // 99% success rate
         );
    }
}
```

### Feeders for Dynamic Parameterized Test Data

Injects dynamic user credentials and search queries from CSV or JSON files:

```java
FeederBuilder<String> csvFeeder = csv("users.csv").circular();

ScenarioBuilder scn = scenario("User Login")
    .feed(csvFeeder)
    .exec(http("Login")
        .post("/login")
        .formParam("user", "#{username}")
        .formParam("pass", "#{password}"));
```

## Common Patterns

### Ramp-up Virtual Users with Latency Assertions

**Problem**: Sudden spike tests cause immediate connection saturation that masks normal production bottlenecks.

**Solution**:
Use incremental user ramping with percentile assertions:

```scala
import io.gatling.core.Predef._
import io.gatling.http.Predef._
import scala.concurrent.duration._

class ApiLoadTest extends Simulation {
  val httpProtocol = http.baseUrl("https://api.example.com")
    .acceptHeader("application/json")

  val scn = scenario("Checkout Workflow")
    .exec(http("Get Products").get("/products"))
    .pause(1)
    .exec(http("Place Order").post("/orders").body(StringBody("{\"item\":\"widget\"}")) .asJson)

  setUp(
    scn.inject(rampUsers(500).during(60.seconds))
  ).protocols(httpProtocol)
   .assertions(
     global.responseTime.percentile3.lt(500),
     global.successfulRequests.percent.gt(99.0)
   )
}
```

## Best Practices

**Do**:

- Enforce Service Level Agreements (SLAs) with Assertions: Define explicit assertions on p95/p99 response times and error rates.
- Ramp Virtual Users Smoothly: Use `rampUsers` or `rampUsersPerSec` to allow connection pools and autoscalers to adapt realistically.
- Model Realistic Think Times: Use `pause(min, max)` to replicate human user behavior rather than firing continuous request loops.
- Generate Real-Time Reports with Graphite / InfluxDB: Stream Gatling metrics live into Grafana dashboards during tests.

**Don't**:

- Run load tests from the same machine hosting the application: CPU contention corrupts latency measurements.
- Ignore network bandwidth limits on test runners: Saturated runner network cards artificially degrade response percentiles.
- Hardcode fixed authentication tokens: Rotate users via feeders to test realistic database index and cache hit rates.

## Troubleshooting

| Error                                                        | Cause                                                       | Solution                                                                    |
| :----------------------------------------------------------- | :---------------------------------------------------------- | :-------------------------------------------------------------------------- |
| `java.net.ConnectException: Cannot assign requested address` | OS ephemeral socket exhaustion on Gatling runner.           | Increase ephemeral port range and enable TCP TIME_WAIT socket recycling.    |
| `i.g.h.c.i.Response: 504 Gateway Timeout`                    | Target server overwhelmed under simulated load.             | Inspect server metrics, connection pool limits, and database query latency. |
| `Gatling simulation compile error`                           | Gatling version API mismatch between Gatling 3.x and 3.10+. | Check imported packages against official Gatling SDK migration guide.       |

## References

- [Gatling Documentation](https://gatling.io/docs/gatling/)
