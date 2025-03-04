# Kubernetes Concepts Explained

## Why Kubernetes?

Docker provides containerization, but Kubernetes provides **orchestration** of containers. This means:

1. **Automated Deployment**: Deploy containers across multiple hosts
2. **Scaling**: Scale containers up or down based on demand
3. **Self-healing**: Restart or replace failed containers automatically
4. **Service Discovery**: Find and communicate with services dynamically
5. **Load Balancing**: Distribute traffic across container instances
6. **Rolling Updates**: Update applications without downtime

## Core Kubernetes Components

### Pod
- Smallest deployable unit in Kubernetes
- Contains one or more containers that share storage and network
- Usually one main application container per pod
- Think of it as a logical host for your container(s)

### Deployment
- Manages a set of identical pods (replicas)
- Ensures the specified number of pods are running
- Handles rolling updates and rollbacks
- Maintains pod health and replaces failed pods

### Service
- Provides stable network endpoint to access pods
- Pods are ephemeral (temporary) but services are persistent
- Types:
  - ClusterIP: Internal only
  - NodePort: Exposes on Node IP at static port
  - LoadBalancer: Exposes externally using cloud provider's load balancer

### ConfigMap & Secret
- ConfigMap: Stores non-sensitive configuration
- Secret: Stores sensitive data (passwords, tokens, keys)
- Both decouple configuration from container images

## Kubernetes Architecture

### Control Plane Components
- **API Server**: Front-end to the control plane, all communication goes through it
- **etcd**: Key-value store that holds all cluster data
- **Scheduler**: Assigns pods to nodes
- **Controller Manager**: Runs controller processes (e.g., deployment controller)

### Node Components
- **kubelet**: Agent that ensures containers are running in a pod
- **kube-proxy**: Maintains network rules on nodes
- **Container Runtime**: Software responsible for running containers (e.g., Docker)

## Kubernetes vs Docker

| Feature | Docker | Kubernetes |
|---------|--------|------------|
| Focus | Creating and running containers | Orchestrating containers at scale |
| Scale | Single host or small-scale | Multi-host clusters |
| Self-healing | Limited | Automatic pod replacement |
| Load Balancing | Basic | Advanced internal and external |
| Scaling | Manual | Automatic horizontal scaling |
| Updates | Manual | Automated rolling updates |
