#!/bin/bash
# Test script for Kubernetes Zero to Hero application
# This script tests basic functionality of the application

# Color definitions
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${BLUE}======================================================================${NC}"
echo -e "${BLUE}             KUBERNETES ZERO TO HERO - APPLICATION TEST               ${NC}"
echo -e "${BLUE}======================================================================${NC}"

# Check if the application is running
echo -e "${CYAN}Checking if the application is running...${NC}"
kubectl -n k8s-demo get deployment k8s-master-app &> /dev/null
if [ $? -ne 0 ]; then
    echo -e "${RED}Application is not running. Please deploy it first.${NC}"
    exit 1
fi

# Get current pod count
CURRENT_PODS=$(kubectl -n k8s-demo get pods -l app=k8s-master | grep Running | wc -l)
echo -e "${GREEN}Current pod count: $CURRENT_PODS${NC}"

# Check if curl is installed
if ! command -v curl &> /dev/null; then
    echo -e "${RED}curl is not installed. Please install it and try again.${NC}"
    exit 1
fi

# Get the service URL
# Try port-forward first, then NodePort
if netstat -tulpn 2>/dev/null | grep -q ':8080'; then
    APP_URL="http://localhost:8080"
    echo -e "${GREEN}Found port-forwarded URL: $APP_URL${NC}"
else
    # Try to get Minikube IP
    MINIKUBE_IP=$(minikube ip 2>/dev/null)
    if [ $? -eq 0 ] && [ ! -z "$MINIKUBE_IP" ]; then
        APP_URL="http://$MINIKUBE_IP:30080"
        echo -e "${GREEN}Using NodePort URL: $APP_URL${NC}"
    else
        echo -e "${RED}Could not determine application URL. Starting port forwarding...${NC}"
        kubectl -n k8s-demo port-forward svc/k8s-master-app 8080:80 &
        PORT_FORWARD_PID=$!
        sleep 2
        APP_URL="http://localhost:8080"
    fi
fi

# Function to run a test request
run_test_request() {
    local path=$1
    local description=$2
    
    echo -e "${YELLOW}Testing $description...${NC}"
    
    # Run curl with a timeout
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "$APP_URL$path")
    
    if [ $HTTP_CODE -eq 200 ]; then
        echo -e "${GREEN}✓ $description test passed (HTTP 200)${NC}"
        return 0
    else
        echo -e "${RED}✗ $description test failed (HTTP $HTTP_CODE)${NC}"
        return 1
    fi
}

# Function to test the application's API
test_api() {
    echo -e "${CYAN}Running API tests...${NC}"
    
    # Test homepage
    run_test_request "/" "Homepage"
    
    # Test health check endpoint
    run_test_request "/api/health" "Health check endpoint"
    
    # Test info endpoint
    run_test_request "/api/info" "Info endpoint"
    
    # Test metrics endpoint
    run_test_request "/api/metrics" "Metrics endpoint"
    
    echo -e "${CYAN}API tests completed${NC}"
}

# Function to get pod information
get_pod_info() {
    echo -e "${CYAN}Getting pod information...${NC}"
    
    # Get pod details
    kubectl -n k8s-demo get pods -l app=k8s-master
    
    # Get detailed info for the first pod
    POD_NAME=$(kubectl -n k8s-demo get pods -l app=k8s-master -o name | head -1)
    if [ ! -z "$POD_NAME" ]; then
        echo -e "${YELLOW}Detailed info for $POD_NAME:${NC}"
        kubectl -n k8s-demo describe $POD_NAME
    fi
}

# Run the tests
test_api
get_pod_info

echo -e "${BLUE}======================================================================${NC}"
echo -e "${GREEN}TESTS COMPLETE!${NC}"
echo -e "${BLUE}======================================================================${NC}"
echo -e "${YELLOW}Your Kubernetes application is up and running.${NC}"
