#!/bin/bash

# Simple EC2 deployment script for Invoice Analyzer
# Uses a pre-configured EC2 instance with Docker

set -e

# Configuration
PROFILE="alfabet"
REGION="sa-east-1"
EC2_HOST="ec2-invoice-analyzer.alfaentretenimento.com.br"  # Replace with your EC2 IP or domain
EC2_USER="ubuntu"
KEY_PATH="~/.ssh/alfa-key.pem"  # Replace with your SSH key path
APP_NAME="invoice-analyzer"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}=> Starting EC2 deployment for Invoice Analyzer...${NC}"
echo ""

# Step 1: Build Docker image locally
echo -e "${YELLOW}[DOCKER] Building Docker image...${NC}"
docker build -t ${APP_NAME}:latest .

# Step 2: Save Docker image
echo -e "${YELLOW}[DOCKER] Saving Docker image...${NC}"
docker save ${APP_NAME}:latest | gzip > ${APP_NAME}.tar.gz

# Step 3: Upload to EC2
echo -e "${YELLOW}[UPLOAD] Uploading to EC2 instance...${NC}"
scp -i ${KEY_PATH} ${APP_NAME}.tar.gz ${EC2_USER}@${EC2_HOST}:/tmp/

# Step 4: Deploy on EC2
echo -e "${YELLOW}[DEPLOY] Deploying on EC2...${NC}"
ssh -i ${KEY_PATH} ${EC2_USER}@${EC2_HOST} << 'ENDSSH'
    # Load the Docker image
    docker load < /tmp/invoice-analyzer.tar.gz
    
    # Stop existing container if running
    docker stop invoice-analyzer 2>/dev/null || true
    docker rm invoice-analyzer 2>/dev/null || true
    
    # Run new container
    docker run -d \
        --name invoice-analyzer \
        --restart unless-stopped \
        -p 80:8000 \
        invoice-analyzer:latest
    
    # Clean up
    rm /tmp/invoice-analyzer.tar.gz
    
    echo "Deployment completed!"
ENDSSH

# Clean up local file
rm -f ${APP_NAME}.tar.gz

echo ""
echo -e "${GREEN}[SUCCESS] Deployment completed successfully!${NC}"
echo -e "${BLUE}[URL] Application available at: http://${EC2_HOST}${NC}"
echo ""