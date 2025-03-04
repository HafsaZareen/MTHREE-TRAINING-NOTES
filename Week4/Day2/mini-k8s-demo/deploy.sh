#!/bin/bash
# Simple script to deploy the application to Kubernetes

# Start with color definitions for better output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}===== KUBERNETES MINI DEMO DEPLOYMENT =====${NC}"

# Step 1: Ensure Minikube is running
echo -e "${GREEN}Checking if Minikube is running...${NC}"
if ! minikube status | grep -q "host: Running"; then #checking minikube status if its working or not and then in output checking if host is running
    echo "Starting Minikube..."
    minikube start
else
    echo "Minikube is already running"
fi

# Step 2: Configure Docker to use Minikube's Docker daemon
# This allows us to build images directly into Minikube's Docker registry
echo -e "${GREEN}Configuring Docker to use Minikube's Docker daemon...${NC}"
eval $(minikube docker-env)

# Step 3: Build the Docker image
echo -e "${GREEN}Building Docker image...${NC}"
cd ~/mini-k8s-demo/app
docker build -t mini-k8s-demo:latest .

# Step 4: Apply Kubernetes manifests in order
echo -e "${GREEN}Applying Kubernetes manifests...${NC}"
cd ~/mini-k8s-demo
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Step 5: Wait for deployment to be ready
echo -e "${GREEN}Waiting for deployment to be ready...${NC}"
kubectl -n mini-demo rollout status deployment/flask-app

# Step 6: Get the URL to access the application
echo -e "${GREEN}Getting application URL...${NC}"
minikube service flask-app -n mini-demo --url

echo -e "${BLUE}===== DEPLOYMENT COMPLETE =====${NC}"
echo "To view Kubernetes dashboard, run: minikube dashboard"
echo "To view application logs, run: kubectl -n mini-demo logs -l app=flask-app"
echo "To clean up resources, run: kubectl delete namespace mini-demo"