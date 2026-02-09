---
name: kubernetes
description: Kubernetes container orchestration with Helm, operators, and service mesh. Use for cluster management.
---

# Kubernetes

Container orchestration for deploying and managing applications at scale.

## When to Use

- Container orchestration
- Microservices deployment
- Auto-scaling applications
- High-availability setups

## Quick Start

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
        - name: myapp
          image: myapp:1.0.0
          ports:
            - containerPort: 3000
          resources:
            requests:
              memory: "128Mi"
              cpu: "250m"
            limits:
              memory: "256Mi"
              cpu: "500m"
```

## Core Concepts

### Service & Ingress

```yaml
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  selector:
    app: myapp
  ports:
    - port: 80
      targetPort: 3000
---
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
    - host: myapp.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: myapp
                port:
                  number: 80
```

### ConfigMap & Secrets

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: myapp-config
data:
  DATABASE_HOST: postgres.default.svc.cluster.local
  LOG_LEVEL: info
---
apiVersion: v1
kind: Secret
metadata:
  name: myapp-secrets
type: Opaque
stringData:
  DATABASE_PASSWORD: supersecret
  API_KEY: myapikey
```

## Common Patterns

### Horizontal Pod Autoscaler

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
```

### Common Commands

```bash
# Cluster info
kubectl cluster-info
kubectl get nodes

# Resources
kubectl get pods -A
kubectl get deployments
kubectl describe pod myapp-xxx

# Debugging
kubectl logs myapp-xxx -f
kubectl exec -it myapp-xxx -- sh

# Apply/Delete
kubectl apply -f deployment.yaml
kubectl delete -f deployment.yaml
```

## Best Practices

**Do**:

- Set resource requests/limits
- Use liveness/readiness probes
- Use namespaces for isolation
- Use Helm for templating

**Don't**:

- Run as root in containers
- Use `latest` tag
- Skip resource limits
- Store secrets in ConfigMaps

## Troubleshooting

| Issue            | Cause            | Solution                   |
| ---------------- | ---------------- | -------------------------- |
| Pod pending      | No resources     | Check node capacity        |
| CrashLoopBackOff | App crashing     | Check logs                 |
| ImagePullBackOff | Can't pull image | Check registry/credentials |

## References

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Helm Documentation](https://helm.sh/docs/)
