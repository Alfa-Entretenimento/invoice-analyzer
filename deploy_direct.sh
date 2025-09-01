#!/bin/bash

# Direct deployment to EC2 - Upload project directly
set -e

# Configuration
PROFILE="alfabet"
REGION="sa-east-1"
KEY_PATH="$HOME/.ssh/alfa-key.pem"
INSTANCE_IP="56.125.206.138"
PROJECT_NAME="invoice-analyzer"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}=> Starting direct deployment to EC2...${NC}"

# Step 1: Create deployment package
echo -e "${YELLOW}[1/4] Creating deployment package...${NC}"
tar -czf ${PROJECT_NAME}.tar.gz \
    --exclude='*.pdf' \
    --exclude='notas' \
    --exclude='venv' \
    --exclude='__pycache__' \
    --exclude='.git' \
    --exclude='*.pyc' \
    --exclude='backup' \
    --exclude='.DS_Store' \
    app.py analisador_claude_api.py \
    requirements.txt templates static CLAUDE.md .env.example

echo -e "${GREEN}Package created: ${PROJECT_NAME}.tar.gz${NC}"

# Step 2: Upload to EC2
echo -e "${YELLOW}[2/4] Uploading to EC2 instance...${NC}"
USER="ubuntu"
scp -o StrictHostKeyChecking=no -i ${KEY_PATH} ${PROJECT_NAME}.tar.gz ${USER}@${INSTANCE_IP}:/tmp/

# Upload .env file if exists
if [ -f ".env" ]; then
    echo -e "${YELLOW}Uploading .env file with API keys...${NC}"
    scp -o StrictHostKeyChecking=no -i ${KEY_PATH} .env ${USER}@${INSTANCE_IP}:/tmp/.env
fi

# Step 3: Setup application on EC2
echo -e "${YELLOW}[3/4] Setting up application on EC2...${NC}"
ssh -o StrictHostKeyChecking=no -i ${KEY_PATH} ${USER}@${INSTANCE_IP} << 'ENDSSH'
# Update system
sudo yum update -y 2>/dev/null || sudo apt-get update -y

# Install Python and dependencies
if command -v yum &> /dev/null; then
    # Amazon Linux
    sudo yum install -y python3 python3-pip tesseract
    sudo amazon-linux-extras install nginx1 -y 2>/dev/null || sudo yum install -y nginx
else
    # Ubuntu
    sudo apt-get install -y python3-pip python3-venv nginx tesseract-ocr tesseract-ocr-por
fi

# Extract project
cd /home/${USER}
tar -xzf /tmp/invoice-analyzer.tar.gz
cd /home/${USER}

# Copy .env file if uploaded
if [ -f "/tmp/.env" ]; then
    cp /tmp/.env /home/${USER}/.env
    echo "API keys configured from .env file"
fi

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements with specific versions for compatibility
pip install --upgrade pip

# Install httpx first with compatible version to avoid proxies error
pip install httpx==0.24.1 httpcore==0.17.3

# Then install other requirements
pip install -r requirements.txt
pip install gunicorn

# Ensure anthropic is at correct version
pip install --upgrade anthropic==0.39.0

# Create systemd service
sudo tee /etc/systemd/system/invoice-analyzer.service > /dev/null << 'EOF'
[Unit]
Description=Invoice Analyzer
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu
Environment="PATH=/home/ubuntu/venv/bin"
ExecStart=/home/ubuntu/venv/bin/gunicorn --workers 2 --bind 0.0.0.0:8000 --timeout 120 app:app
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Adjust service file for correct user
sudo sed -i "s/ec2-user/${USER}/g" /etc/systemd/system/invoice-analyzer.service

# Configure nginx
sudo tee /etc/nginx/conf.d/invoice-analyzer.conf > /dev/null << 'EOF'
server {
    listen 80;
    server_name _;
    
    client_max_body_size 20M;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_read_timeout 120s;
        proxy_connect_timeout 120s;
    }
}
EOF

# Remove default nginx config if exists
sudo rm -f /etc/nginx/sites-enabled/default 2>/dev/null || true
sudo rm -f /etc/nginx/conf.d/default.conf 2>/dev/null || true

# Start services
sudo systemctl daemon-reload
sudo systemctl restart invoice-analyzer
sudo systemctl enable invoice-analyzer
sudo nginx -t && sudo systemctl restart nginx
sudo systemctl enable nginx

echo "Deployment complete!"
ENDSSH

# Step 4: Verify deployment
echo -e "${YELLOW}[4/4] Verifying deployment...${NC}"
sleep 5

# Test the application
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://${INSTANCE_IP})

if [ "$HTTP_CODE" == "200" ]; then
    echo -e "${GREEN}✅ Application is running successfully!${NC}"
else
    echo -e "${YELLOW}⏳ Application is starting... (HTTP code: $HTTP_CODE)${NC}"
    echo -e "${YELLOW}   Please wait 30 seconds and try again.${NC}"
fi

# Clean up local package
rm -f ${PROJECT_NAME}.tar.gz

echo ""
echo -e "${GREEN}[SUCCESS] Deployment completed!${NC}"
echo ""
echo -e "${BLUE}📱 Application URL: http://${INSTANCE_IP}${NC}"
echo ""
echo -e "${YELLOW}Share this link with your finance team: http://${INSTANCE_IP}${NC}"