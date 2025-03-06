# Kubernetes Commands Cheat Sheet

A quick reference guide for common kubectl commands used in this project.

## Context and Namespace Commands

```bash
# View current context and namespace
kubectl config current-context
kubectl config view --minify | grep namespace

# Switch namespace
kubectl config set-context --current --namespace=k8s-demo
```

## Resource Management

```bash
# View resources
kubectl get pods -n k8s-demo
kubectl get all -n k8s-demo
kubectl get pods -n k8s-demo -o wide

# Describe resources (detailed info)
kubectl describe pod <pod-name> -n k8s-demo
kubectl describe deployment k8s-master-app -n k8s-demo

# Delete resources
kubectl delete pod <pod-name> -n k8s-demo
```

## Logs and Debugging

```bash
# View logs
kubectl logs <pod-name> -n k8s-demo
kubectl logs -f <pod-name> -n k8s-demo  # Stream logs

# Execute commands in pod
kubectl exec -it <pod-name> -n k8s-demo -- /bin/bash
kubectl exec <pod-name> -n k8s-demo -- ls /data

# Port forwarding
kubectl port-forward service/k8s-master-app 8080:80 -n k8s-demo
```

## Working with Minikube

```bash
# Start/stop Minikube
minikube start
minikube stop

# Get Minikube IP
minikube ip

# Open service in browser
minikube service k8s-master-app -n k8s-demo

# Access dashboard
minikube dashboard

# Configure docker to use Minikube's daemon
eval $(minikube docker-env)
```

## Tips for WSL2 Users

1. **If Minikube won't start**: Try `minikube start --driver=docker`

2. **If mounting fails**: Avoid host path mounts, use EmptyDir volumes instead

3. **If addons won't enable**: They may not be critical - the app can run without them

4. **If WSL networking issues occur**: Use port forwarding instead of NodePort access
