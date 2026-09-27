---
name: kubernetes
description: Expert Kubernetes (K8s) assistance covering Pods, Deployments, Services, Ingress, ConfigMaps, Secrets, RBAC, and HPA. Use when orchestrating, deploying, and scaling containerized workloads.
---

# Kubernetes (K8s)

Kubernetes is the standard for orchestrating containerized applications. In 2025, the **Gateway API** has replaced Ingress as the standard for traffic routing, and **Sidecars** are native.

## When to Use

- **Container Orchestration at Scale**: Automating deployment, scaling, networking, and lifecycle of containerized services.
- **Self-Healing Infrastructure**: Automated container restarts, rescheduling dead nodes, and rolling zero-downtime updates.
- **Dynamic Horizontal Pod Autoscaling (HPA)**: Scaling replica counts dynamically based on CPU, memory, or custom metrics.
- **Multi-Tenant Workload Isolation**: Dividing cluster resources safely using Namespaces, RBAC, and NetworkPolicies.

## Quick Start

```yaml
# Gateway (The Load Balancer)
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: my-gateway
spec:
  gatewayClassName: nginx
  listeners:
    - name: http
      protocol: HTTP
      port: 80

---
# HTTPRoute (The Routing Rule)
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: my-app
spec:
  parentRefs:
    - name: my-gateway
  rules:
    - matches:
        - path:
            type: PathPrefix
            value: /api
      backendRefs:
        - name: my-service
          port: 8080
```

## Core Concepts

#Production Deployment Manifest with Probes & Resource Limits

Deploying resilient stateless applications:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-service
  namespace: production
  labels:
    app.kubernetes.io/name: api-service
    app.kubernetes.io/part-of: core-platform
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: api-service
  template:
    metadata:
      labels:
        app: api-service
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 10001
        fsGroup: 10001
      containers:
        - name: server
          image: registry.example.com/api-service:v2.1.0
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 8080
          resources:
            requests:
              cpu: "250m"
              memory: "256Mi"
            limits:
              cpu: "1000m"
              memory: "512Mi"
          readinessProbe:
            httpGet:
              path: /healthz/ready
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 5
          livenessProbe:
            httpGet:
              path: /healthz/live
              port: 8080
            initialDelaySeconds: 15
            periodSeconds: 10
```

#Ingress & ClusterIP Service Routing

Routing external HTTPS traffic to backend pods:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: api-service
  namespace: production
spec:
  type: ClusterIP
  selector:
    app: api-service
  ports:
    - port: 80
      targetPort: 8080
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: api-ingress
  namespace: production
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - api.example.com
      secretName: api-tls-cert
  rules:
    - host: api.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: api-service
                port:
                  number: 80
```

#Horizontal Pod Autoscaler (HPA)

Autoscaling based on real-time CPU utilization:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-service-hpa
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api-service
  minReplicas: 3
  maxReplicas: 20
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
```

## Common Patterns

### Production Deployment with Rolling Updates and Health Probes

**Problem**: Rolling deployments dropping active connections or directing traffic to unready pods.

**Solution**:
Configure readiness, liveness, and startup probes with graceful termination:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-deployment
spec:
  replicas: 3
  strategy:
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: api
  template:
    metadata:
      labels:
        app: api
    spec:
      terminationGracePeriodSeconds: 30
      containers:
        - name: api
          image: myorg/api:v1.2.0
          ports:
            - containerPort: 8080
          readinessProbe:
            httpGet:
              path: /health/ready
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 5
          livenessProbe:
            httpGet:
              path: /health/live
              port: 8080
            initialDelaySeconds: 15
            periodSeconds: 10
```

## Best Practices (2026)

- **Do** always define both `requests` and `limits` for CPU and memory on all containers.
- **Do** configure separate `readinessProbe` (controls traffic routing) and `livenessProbe` (triggers pod restart).
- **Do** enforce non-root security contexts (`runAsNonRoot: true`) and drop unnecessary Linux capabilities.
- **Do** use `maxUnavailable: 0` in rolling updates to ensure zero-downtime deployments.
- **Don't** deploy pods directly; always wrap pods in high-level controllers (`Deployment`, `StatefulSet`, `DaemonSet`).
- **Don't** use `:latest` image tags in manifests; use immutable tags or SHA256 digests.
- **Don't** store unencrypted passwords in plain ConfigMaps; use Kubernetes Secrets or External Secrets Operator.

## Troubleshooting

| Error                             | Cause                                                                    | Solution                                                                     |
| :-------------------------------- | :----------------------------------------------------------------------- | :--------------------------------------------------------------------------- |
| `CrashLoopBackOff`                | Application inside container crashed or exited immediately after launch. | Inspect logs: `kubectl logs <pod-name> --previous` and check entrypoint.     |
| `ImagePullBackOff / ErrImagePull` | Image tag typo, non-existent repository, or missing imagePullSecret.     | Verify image name and check registry secrets: `kubectl describe pod <name>`. |
| `OOMKilled (Exit Code 137)`       | Container memory usage exceeded `resources.limits.memory`.               | Increase container memory limit in pod spec.                                 |

## References

- [Kubernetes Documentation](https://kubernetes.io/)
