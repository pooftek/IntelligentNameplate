#!/bin/bash
# Automated setup script for Raspberry Pi
# This script will download and set up the Classroom App on your Pi

set -e  # Exit on any error

echo "🎓 Classroom App - Raspberry Pi Setup"
echo "======================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if running on Raspberry Pi (optional check)
if [ -f /proc/device-tree/model ] && grep -q "Raspberry Pi" /proc/device-tree/model; then
    echo -e "${GREEN}✓ Raspberry Pi detected${NC}"
else
    echo -e "${YELLOW}⚠ Not running on a detected Raspberry Pi, but continuing anyway...${NC}"
fi

# Step 1: Update system
echo ""
echo "📦 Step 1: Updating system packages..."
sudo apt update
sudo apt upgrade -y

# Step 2: Install required system packages
echo ""
echo "📦 Step 2: Installing required system packages..."
sudo apt install -y python3 python3-pip git python3-dev libffi-dev

# Step 3: Check Python version
echo ""
echo "🐍 Checking Python version..."
python3 --version

# Step 4: Navigate to home directory
cd ~

# Step 5: Check if project already exists
if [ -d "IntelligentNameplate" ]; then
    echo ""
    echo -e "${YELLOW}⚠ IntelligentNameplate directory already exists${NC}"
    read -p "Do you want to remove it and start fresh? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Removing existing directory..."
        rm -rf IntelligentNameplate
    else
        echo "Using existing directory..."
        cd IntelligentNameplate
        git pull
    fi
fi

# Step 6: Clone or update repository
if [ ! -d "IntelligentNameplate" ]; then
    echo ""
    echo "📥 Step 3: Downloading project from GitHub..."
    git clone https://github.com/pooftek/IntelligentNameplate.git
    cd IntelligentNameplate
else
    cd IntelligentNameplate
fi

# Step 7: Install Python dependencies
echo ""
echo "📦 Step 4: Installing Python dependencies..."
pip3 install --user -r requirements.txt

# Step 8: Make scripts executable
echo ""
echo "🔧 Step 5: Setting up scripts..."
chmod +x start_pi.sh 2>/dev/null || true

# Step 9: Get IP address
echo ""
echo "🌐 Step 6: Network information..."
IP=$(hostname -I | awk '{print $1}')
echo -e "${GREEN}Your Raspberry Pi IP address: ${IP}${NC}"

# Step 10: Create a simple start script
echo ""
echo "📝 Creating start script..."
cat > ~/start_classroom.sh << 'EOF'
#!/bin/bash
cd ~/IntelligentNameplate
IP=$(hostname -I | awk '{print $1}')
echo "🎓 Starting Classroom App..."
echo "📍 Your Pi IP: $IP"
echo "🌐 Access at: http://$IP:5000"
echo "📱 Student interface: http://$IP:5000/student"
echo ""
echo "Press Ctrl+C to stop"
echo ""
python3 app.py
EOF

chmod +x ~/start_classroom.sh

# Step 11: Summary
echo ""
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 Summary:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📍 Project location: ~/IntelligentNameplate"
echo "🌐 Your Pi IP address: $IP"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 To start the app, run:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  cd ~/IntelligentNameplate"
echo "  python3 app.py"
echo ""
echo "  OR use the quick start script:"
echo "  ~/start_classroom.sh"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🌐 Access the app:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  On Pi:        http://localhost:5000"
echo "  From network: http://$IP:5000"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔐 Default Login:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  Username: professor"
echo "  Password: password"
echo ""
echo -e "${YELLOW}⚠ Remember to change these in production!${NC}"
echo ""

