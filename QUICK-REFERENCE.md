# Kubernetes 101 - Quick Reference Guide

**A cheat sheet for the Kubernetes 101 tutorial**

---

## Core Concepts

| Concept | What it is | Key Point |
|---------|-----------|-----------|
| **Container** | Packaged application + dependencies | Runs the same everywhere |
| **Pod** | Kubernetes wrapper for container(s) | Smallest deployable unit |
| **Deployment** | Manages multiple Pod replicas | Self-healing, scaling, updates |
| **Service** | Stable network endpoint for Pods | Load balancing, constant IP/DNS |

---

## Essential kubectl Commands

### Viewing Resources

```bash
# Get all resources
kubectl get all

# Get specific resource types
kubectl get pods
kubectl get deployments
kubectl get services
kubectl get nodes

# Watch resources update in real-time
kubectl get pods --watch

# Get detailed information
kubectl describe pod <POD_NAME>
kubectl describe deployment <DEPLOYMENT_NAME>
kubectl describe service <SERVICE_NAME>
```

### Creating Resources

```bash
# Apply YAML configuration
kubectl apply -f <FILE.yaml>
kubectl apply -f k8s/pod.yaml
kubectl apply -f k8s/deployment.yaml

# Create from command line (quick and dirty)
kubectl run nginx --image=nginx --port=80
kubectl create deployment nginx --image=nginx
```

### Deleting Resources

```bash
# Delete using YAML file
kubectl delete -f <FILE.yaml>

# Delete by resource type and name
kubectl delete pod <POD_NAME>
kubectl delete deployment <DEPLOYMENT_NAME>
kubectl delete service <SERVICE_NAME>

# Delete all resources of a type
kubectl delete pods --all
```

### Logs and Debugging

```bash
# View logs
kubectl logs <POD_NAME>

# Follow logs (like tail -f)
kubectl logs -f <POD_NAME>

# Logs from all pods with a label
kubectl logs -l app=hello

# Execute command in a pod
kubectl exec -it <POD_NAME> -- /bin/bash
kubectl exec <POD_NAME> -- curl localhost:8080
```

### Scaling

```bash
# Scale a deployment
kubectl scale deployment <NAME> --replicas=3
kubectl scale deployment hello-deployment --replicas=5

# View scaling in action
kubectl get pods --watch
```

### Accessing Applications

```bash
# Port forward from a Pod
kubectl port-forward pod/<POD_NAME> 8080:8080

# Port forward from a Service (preferred)
kubectl port-forward service/<SERVICE_NAME> 8080:80

# Then access at http://localhost:8080
```

---

## Docker Commands

### Basic Operations

```bash
# Pull an image
docker pull nginx:latest

# Build an image
docker build -t <IMAGE_NAME>:latest .
docker build -t hello-python:latest .

# List images
docker images

# Run a container
docker run --name <NAME> -d -p 8080:8080 <IMAGE>
docker run --rm -p 8080:8080 hello-python:latest

# List running containers
docker ps

# View logs
docker logs <CONTAINER_NAME>

# Execute command in container
docker exec -it <CONTAINER_NAME> /bin/bash

# Stop and remove container
docker stop <CONTAINER_NAME>
docker rm <CONTAINER_NAME>

# Force remove
docker rm -f <CONTAINER_NAME>
```

---

## YAML File Templates

### Pod (pod.yaml)

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  containers:
    - name: app
      image: hello-python:latest
      imagePullPolicy: Never
      ports:
      - containerPort: 8080
```

### Deployment (deployment.yaml)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-deployment
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
      - name: app
        image: hello-python:latest
        imagePullPolicy: Never
        ports:
        - containerPort: 8080
```

### Service (service.yaml)

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  selector:
    app: myapp
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  type: ClusterIP  # or LoadBalancer, NodePort
```

---

## Common Workflows

### Deploy a New Application

```bash
# 1. Build the image
cd app
docker build -t myapp:latest .
cd ..

# 2. Create deployment
kubectl apply -f k8s/deployment.yaml

# 3. Expose with service
kubectl apply -f k8s/service.yaml

# 4. Check status
kubectl get all
```

### Update an Application

```bash
# Rebuild image
docker build -t myapp:v2 .

# Update deployment
kubectl set image deployment/myapp app=myapp:v2

# Or restart with same image
kubectl rollout restart deployment/myapp
```

### Debug a Failing Pod

```bash
# 1. Check pod status
kubectl get pods

# 2. Describe the pod (look for events)
kubectl describe pod <POD_NAME>

# 3. Check logs
kubectl logs <POD_NAME>

# 4. Execute into the pod (if running)
kubectl exec -it <POD_NAME> -- /bin/bash
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| **Container name already in use** | `docker rm -f <NAME>` |
| **Pod stuck in Pending** | `kubectl describe pod <NAME>` - check events |
| **Pod in CrashLoopBackOff** | `kubectl logs <NAME>` - check application logs |
| **Can't access service** | Check if pods are running; use port-forward |
| **ImagePullBackOff** | Use `imagePullPolicy: Never` for local images |
| **Wrong context** | `kubectl config current-context` |

---

## Port Mapping

Understanding ports:

```
Browser:8080 → Service:80 → Pod:8080 → Flask App
```

- **Container Port**: Where app listens (8080)
- **Service Port**: External access point (80)
- **Target Port**: Routes to container port (8080)
- **Host Port**: Docker port mapping (8080:8080)

---

## Labels and Selectors

Labels connect resources. **Selectors must match labels!**

```yaml
# Deployment selector
selector:
  matchLabels:
    app: myapp

# Pod labels (must match!)
template:
  metadata:
    labels:
      app: myapp

# Service selector (must match pod labels!)
selector:
  app: myapp
```

---

## Helpful Tips

### Use --dry-run for testing

```bash
# Generate YAML without creating resource
kubectl create deployment test --image=nginx --dry-run=client -o yaml

# Test if YAML is valid
kubectl apply -f myfile.yaml --dry-run=client
```

### Get help anytime

```bash
kubectl explain pod
kubectl explain deployment.spec
kubectl explain service.spec.type
```

### Auto-cleanup containers

```bash
# Use --rm flag to auto-remove when stopped
docker run --rm -p 8080:8080 myapp:latest
```

### Watch logs from multiple pods

```bash
# All pods with label
kubectl logs -l app=myapp --follow
```

---

## Tutorial File Structure

```
kubernetes101/
├── app/                # Flask application
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── k8s/                # Kubernetes manifests
│   ├── pod.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   └── custom-deployment.yaml
│
└── README.md           # Main tutorial
```

---

## Next Steps

After mastering the basics:

1. **ConfigMaps & Secrets** - External configuration
2. **Namespaces** - Resource isolation
3. **Persistent Volumes** - Data storage
4. **Ingress** - HTTP routing
5. **Health Checks** - Liveness & readiness probes
6. **Helm** - Package manager
7. **RBAC** - Security & permissions

---

## Resources

- Official docs: https://kubernetes.io/docs/
- kubectl cheat sheet: https://kubernetes.io/docs/reference/kubectl/cheatsheet/
- Colima: https://github.com/abiosoft/colima

---

**Remember:**
- Kubernetes is declarative - describe what you want, K8s makes it happen
- Start simple, iterate
- Use `kubectl describe` and `kubectl logs` for debugging
- Labels must match between Deployments, Pods, and Services

---

© Kubernetes 101 Tutorial | https://github.com/your-repo/kubernetes101
