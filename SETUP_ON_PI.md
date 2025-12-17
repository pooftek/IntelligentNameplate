# Quick Setup on Raspberry Pi - Copy & Paste Instructions

Follow these simple steps to get the Classroom App running on your Pi in minutes!

## Method 1: Automated Setup (Easiest!)

### Step 1: Open Terminal on Your Pi
Press `Ctrl+Alt+T` or click the terminal icon.

### Step 2: Run the Setup Script
Copy and paste this entire command:

```bash
cd ~ && curl -sSL https://raw.githubusercontent.com/pooftek/IntelligentNameplate/main/setup_pi.sh | bash
```

**OR** if you prefer to download first:

```bash
cd ~
wget https://raw.githubusercontent.com/pooftek/IntelligentNameplate/main/setup_pi.sh
chmod +x setup_pi.sh
./setup_pi.sh
```

The script will:
- ✅ Update your system
- ✅ Install Python and dependencies
- ✅ Download the project from GitHub
- ✅ Install all required packages
- ✅ Show you your IP address
- ✅ Create a quick start script

### Step 3: Start the App
After setup completes, run:

```bash
~/start_classroom.sh
```

Or manually:
```bash
cd ~/IntelligentNameplate
python3 app.py
```

---

## Method 2: Manual Setup (If Method 1 Doesn't Work)

### Step 1: Open Terminal
Press `Ctrl+Alt+T`

### Step 2: Install Required Packages
```bash
sudo apt update
sudo apt install -y python3 python3-pip git
```

### Step 3: Download the Project
```bash
cd ~
git clone https://github.com/pooftek/IntelligentNameplate.git
cd IntelligentNameplate
```

### Step 4: Install Python Dependencies
```bash
pip3 install --user -r requirements.txt
```

### Step 5: Find Your IP Address
```bash
hostname -I
```
(Write down the IP address - you'll need it!)

### Step 6: Start the App
```bash
python3 app.py
```

### Step 7: Access the App
- **On Pi:** Open browser → http://localhost:5000
- **From Windows:** Open browser → http://YOUR_PI_IP:5000

**Default Login:**
- Username: `professor`
- Password: `password`

---

## Troubleshooting

### "curl: command not found"
Install curl first:
```bash
sudo apt install curl -y
```

### "Permission denied"
Make the script executable:
```bash
chmod +x setup_pi.sh
```

### "Module not found" errors
Install system dependencies:
```bash
sudo apt install python3-dev libffi-dev -y
pip3 install --user -r requirements.txt
```

### Can't access from Windows
1. Make sure both devices are on the same Wi-Fi network
2. Check the Pi's IP: `hostname -I`
3. Try accessing from the Pi first: http://localhost:5000
4. Check Windows Firewall settings

---

## After Setup

The app will run as long as the terminal is open. To stop it, press `Ctrl+C`.

To make it start automatically on boot, see **RASPBERRY_PI_SETUP.md** for systemd service setup.

---

**That's it! You're ready to go!** 🎓

