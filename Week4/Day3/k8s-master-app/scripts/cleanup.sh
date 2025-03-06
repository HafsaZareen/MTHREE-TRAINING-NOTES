#!/bin/bash
# Cleanup script for Kubernetes Zero to Hero application
# This script removes all Kubernetes resources created for the application

# Color definitions
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${BLUE}======================================================================${NC}"
echo -e "${BLUE}             KUBERNETES ZERO TO HERO - CLEANUP                        ${NC}"
echo -e "${BLUE}======================================================================${NC}"

# Step 1: Stop any port forwarding
echo -e "${CYAN}Stopping any port forwarding processes...${NC}"
pkill -f "kubectl -n k8s-demo port-forward" || true
echo -e "${GREEN}✓ Port forwarding stopped${NC}"

# Step 2: Delete all Kubernetes resources
echo -e "${CYAN}Deleting all resources in k8s-demo namespace...${NC}"
kubectl delete namespace k8s-demo

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ All resources in k8s-demo namespace deleted${NC}"
else
    echo -e "${RED}Failed to delete namespace. Trying individual resources...${NC}"
    
    # Delete resources in reverse order of creation
    kubectl delete -f ~/k8s-master-app/k8s/monitoring/hpa.yaml || true
    kubectl delete -f ~/k8s-master-app/k8s/networking/service.yaml || true
    kubectl delete -f ~/k8s-master-app/k8s/base/deployment.yaml || true
    kubectl delete -f ~/k8s-master-app/k8s/config/secret.yaml || true
    kubectl delete -f ~/k8s-master-app/k8s/config/configmap.yaml || true
    kubectl delete -f ~/k8s-master-app/k8s/volumes/volumes.yaml || true
    kubectl delete -f ~/k8s-master-app/k8s/base/namespace.yaml || true
    
    echo -e "${YELLOW}Individual resource deletion complete${NC}"
fi

# Step 3: Optional - clean up Docker images
echo -e "${CYAN}Cleaning up Docker images in Minikube...${NC}"
eval $(minikube docker-env)
docker rmi k8s-master-app:latest || true
echo -e "${GREEN}✓ Docker images cleaned up${NC}"

echo -e "${BLUE}======================================================================${NC}"
echo -e "${GREEN}CLEANUP COMPLETE!${NC}"
echo -e "${BLUE}======================================================================${NC}"
echo -e "${YELLOW}You can restart the application by running ./scripts/deploy.sh${NC}"
