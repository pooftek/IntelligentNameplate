#!/bin/bash
# Quick start script for Raspberry Pi
# Makes it easy to start the classroom app

echo "🎓 Starting Classroom Management App..."
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    echo "Install it with: sudo apt install python3 python3-pip"
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ app.py not found!"
    echo "Please run this script from the project directory."
    exit 1
fi

# Get IP address
IP=$(hostname -I | awk '{print $1}')

echo "📍 Your Raspberry Pi IP: $IP"
echo "🌐 Access the app at: http://$IP:5000"
echo "📱 Student interface: http://$IP:5000/student"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the app
python3 app.py

