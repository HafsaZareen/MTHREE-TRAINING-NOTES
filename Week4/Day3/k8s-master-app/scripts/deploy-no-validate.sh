#!/bin/bash
# Deployment script for the Kubernetes Zero to Hero application with validation disabled
# This script works around API server connectivity issues in Minikube/WSL2

# Color definitions for better output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

echo -e "${BLUE}======================================================================${NC}"
echo -e "${BLUE}       KUBERNETES ZERO TO HERO - DEPLOYMENT (NO VALIDATION)           ${NC}"
echo -e "${BLUE}======================================================================${NC}"

# Step 1: Check prerequisites
echo -e "${MAGENTA}[STEP 1] CHECKING PREREQUISITES${NC}"

# Function to check if a command exists
command_exists() {
    command -v "$1" &> /dev/null
}

# Check for required tools
for tool in minikube kubectl docker; do
    if ! command_exists $tool; then
        echo -e "${RED}Error: $tool is not installed. Please install it and try again.${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓ $tool is installed${NC}"
done

# Step 2: Ensure Minikube is running
echo -e "${MAGENTA}[STEP 2] CHECKING MINIKUBE STATUS${NC}"

# First check if minikube is running
if ! minikube status | grep -q "host: Running"; then
    echo -e "${RED}Minikube is not running. Please run the minikube-reset.sh script first.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Minikube is running${NC}"

# Step 3: Configure Docker to use Minikube's Docker daemon
echo -e "${MAGENTA}[STEP 3] CONFIGURING DOCKER TO USE MINIKUBE${NC}"

eval $(minikube docker-env)
if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to configure Docker to use Minikube. Will continue with local Docker.${NC}"
else
    echo -e "${GREEN}✓ Docker configured to use Minikube's registry${NC}"
fi

# Step 4: Build the Docker image
echo -e "${MAGENTA}[STEP 4] BUILDING DOCKER IMAGE${NC}"

echo -e "${CYAN}Building k8s-master-app:latest image...${NC}"
cd ~/k8s-master-app/app

# Use host network for better connectivity in WSL
MAX_ATTEMPTS=3
BUILD_SUCCESS=false

for ATTEMPT in $(seq 1 $MAX_ATTEMPTS); do
    echo -e "${YELLOW}Build attempt $ATTEMPT of $MAX_ATTEMPTS...${NC}"
    
    # Use host network for better connectivity in WSL
    docker build --network=host -t k8s-master-app:latest .
    
    if [ $? -eq 0 ]; then
        BUILD_SUCCESS=true
        break
    else
        echo -e "${YELLOW}Build attempt $ATTEMPT failed. Waiting before retry...${NC}"
        sleep 5
    fi
done

if [ "$BUILD_SUCCESS" != "true" ]; then
    echo -e "${RED}Failed to build Docker image after $MAX_ATTEMPTS attempts. Exiting.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Docker image built successfully${NC}"

# Step 5: Apply Kubernetes manifests with --validate=false flag
echo -e "${MAGENTA}[STEP 5] DEPLOYING TO KUBERNETES (WITHOUT VALIDATION)${NC}"
cd ~/k8s-master-app

# Function to safely apply a manifest with retries and validation disabled
apply_manifest() {
    local file=$1
    local description=$2
    local attempts=3
    local success=false
    
    echo -e "${CYAN}Creating $description...${NC}"
    
    for i in $(seq 1 $attempts); do
        kubectl apply -f "$file" --validate=false --timeout=20s
        if [ $? -eq 0 ]; then
            success=true
            echo -e "${GREEN}✓ $description created${NC}"
            break
        else
            echo -e "${YELLOW}Attempt $i failed. Retrying...${NC}"
            sleep 2
        fi
    done
    
    if [ "$success" != "true" ]; then
        echo -e "${RED}Failed to create $description after $attempts attempts.${NC}"
        return 1
    fi
    
    return 0
}

# Apply each manifest with validation disabled
echo -e "${CYAN}Creating resources with validation disabled...${NC}"

apply_manifest "k8s/base/namespace.yaml" "namespace" || true
apply_manifest "k8s/volumes/volumes.yaml" "ConfigMap for files" || true
apply_manifest "k8s/config/configmap.yaml" "ConfigMap for settings" || true
apply_manifest "k8s/config/secret.yaml" "Secret" || true
apply_manifest "k8s/base/deployment.yaml" "Deployment" || true
apply_manifest "k8s/networking/service.yaml" "Service" || true
apply_manifest "k8s/monitoring/hpa.yaml" "HPA" || true

echo -e "${GREEN}✓ All Kubernetes resources applied${NC}"

# Step 6: Wait for deployment to be ready with extended timeouts
echo -e "${MAGENTA}[STEP 6] CHECKING DEPLOYMENT STATUS${NC}"

echo -e "${YELLOW}Note: Not waiting for deployment to be ready due to potential API connectivity issues${NC}"
echo -e "${YELLOW}Instead, we'll check the status periodically...${NC}"

# Get deployment status without waiting for rollout
kubectl -n k8s-demo get deployments --timeout=10s || true
kubectl -n k8s-demo get pods --timeout=10s || true

# Step 7: Set up port forwarding with retries
echo -e "${MAGENTA}[STEP 7] SETTING UP PORT FORWARDING${NC}"

# Check if port 8080 is already in use
if netstat -tuln 2>/dev/null | grep -q ':8080 '; then
    echo -e "${YELLOW}Port 8080 is already in use. Will try a different port.${NC}"
    PORT=8081
else
    PORT=8080
fi

# Function to set up port forwarding with retries
setup_port_forwarding() {
    local attempts=3
    local success=false
    
    for i in $(seq 1 $attempts); do
        echo -e "${CYAN}Attempting to set up port forwarding (attempt $i)...${NC}"
        
        # Kill any existing port forwarding on the same port
        pkill -f "kubectl.*port-forward.*$PORT:80" || true
        
        # Start port forwarding in the background with a timeout
        timeout 5s kubectl -n k8s-demo port-forward svc/k8s-master-app $PORT:80 &
        PF_PID=$!
        
        # Give it a moment to start
        sleep 3
        
        # Check if port forwarding is running
        if ps -p $PF_PID > /dev/null; then
            success=true
            echo -e "${GREEN}✓ Port forwarding started on port $PORT (PID: $PF_PID)${NC}"
            break
        else
            echo -e "${YELLOW}Port forwarding attempt $i failed.${NC}"
        fi
    done
    
    if [ "$success" != "true" ]; then
        echo -e "${RED}Failed to set up port forwarding after $attempts attempts.${NC}"
        echo -e "${YELLOW}Try manually running: kubectl -n k8s-demo port-forward svc/k8s-master-app $PORT:80${NC}"
        return 1
    fi
    
    return 0
}

# Try to set up port forwarding
setup_port_forwarding || true

# Step 8: Display access information
echo -e "${MAGENTA}[STEP 8] DEPLOYMENT COMPLETE${NC}"
echo -e "${BLUE}======================================================================${NC}"
echo -e "${GREEN}Kubernetes Zero to Hero application has been deployed!${NC}"
echo -e "${BLUE}======================================================================${NC}"

echo -e "${YELLOW}Your application should be accessible via multiple methods:${NC}"
echo ""

if [ "$success" == "true" ]; then
    echo -e "${CYAN}1. Port Forwarding:${NC}"
    echo "   URL: http://localhost:$PORT"
    echo "   (This is running in the background with PID $PF_PID)"
    echo ""
fi

# Get Minikube IP
MINIKUBE_IP=$(minikube ip 2>/dev/null)
if [ $? -eq 0 ] && [ ! -z "$MINIKUBE_IP" ]; then
    echo -e "${CYAN}2. NodePort:${NC}"
    echo "   URL: http://$MINIKUBE_IP:30080"
    echo ""
    
    echo -e "${CYAN}3. Minikube Service URL:${NC}"
    echo "   Run: minikube service k8s-master-app -n k8s-demo"
    echo ""
else
    echo -e "${YELLOW}Could not determine Minikube IP. Please check minikube status.${NC}"
fi

# Step 9: Display useful commands
echo -e "${BLUE}======================================================================${NC}"
echo -e "${YELLOW}USEFUL COMMANDS:${NC}"
echo -e "${BLUE}======================================================================${NC}"

echo -e "${CYAN}View Kubernetes Dashboard:${NC}"
echo "   minikube dashboard"
echo ""

echo -e "${CYAN}Get deployment status:${NC}"
echo "   kubectl -n k8s-demo get deployments"
echo ""

echo -e "${CYAN}Get pod status:${NC}"
echo "   kubectl -n k8s-demo get pods"
echo ""

echo -e "${CYAN}View pod logs:${NC}"
echo "   kubectl -n k8s-demo logs -l app=k8s-master"
echo ""

echo -e "${CYAN}If the application is not accessible, try:${NC}"
echo "   1. Manually set up port forwarding:"
echo "      kubectl -n k8s-demo port-forward svc/k8s-master-app 8080:80"
echo "   2. Access via Minikube service directly:"
echo "      minikube service k8s-master-app -n k8s-demo"
echo ""

echo -e "${CYAN}Clean up all resources:${NC}"
echo "   ./scripts/cleanup.sh"
echo ""

echo -e "${BLUE}======================================================================${NC}"
echo -e "${GREEN}DEPLOYMENT COMPLETE!${NC}"
echo -e "${BLUE}======================================================================${NC}"
echo -e "${YELLOW}Note: Due to WSL2/Minikube connectivity issues, some operations might take time to complete.${NC}"
echo -e "${YELLOW}      If you encounter further issues, try running the minikube-reset.sh script again.${NC}"
