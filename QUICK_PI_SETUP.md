# Quick Setup - Raspberry Pi (HDMI Connected)

Follow these steps to get the Classroom App running on your Raspberry Pi right now!

## Step 1: Open Terminal on Your Pi

1. On your Raspberry Pi desktop, click the terminal icon (or press `Ctrl+Alt+T`)
2. You should see a terminal window open

## Step 2: Navigate to Home Directory

```bash
cd ~
```

## Step 3: Download the Project

### Option A: Clone from GitHub (Easiest)

```bash
git clone https://github.com/pooftek/IntelligentNameplate.git
cd IntelligentNameplate
```

### Option B: If Git is Not Installed

First install git:
```bash
sudo apt update
sudo apt install git -y
```

Then clone:
```bash
git clone https://github.com/pooftek/IntelligentNameplate.git
cd IntelligentNameplate
```

## Step 4: Install Python Dependencies

```bash
pip3 install -r requirements.txt
```

**If you get permission errors**, use:
```bash
pip3 install --user -r requirements.txt
```

**If pip3 is not installed:**
```bash
sudo apt install python3-pip -y
pip3 install -r requirements.txt
```

## Step 5: Find Your Pi's IP Address

You'll need this to access the app from other devices:

```bash
hostname -I
```

Write down the IP address (it will look like `192.168.1.100`)

## Step 6: Start the Application

```bash
python3 app.py
```

You should see:
```
 * Running on http://0.0.0.0:5000
```

## Step 7: Access the App

### On the Pi itself:
- Open a web browser on the Pi
- Go to: **http://localhost:5000**

### From your Windows computer (on the same network):
- Open a web browser
- Go to: **http://YOUR_PI_IP:5000** (use the IP from Step 5)

### Default Login:
- **Username:** `professor`
- **Password:** `password`

## Troubleshooting

### "Command not found" errors:
- Make sure you're using `python3` not `python`
- Install missing packages: `sudo apt install python3 python3-pip git -y`

### Port already in use:
- Something else is using port 5000
- You can change it in `app.py` line 763 to port 5001

### Can't access from Windows computer:
1. Make sure both devices are on the same Wi-Fi network
2. Check the Pi's IP address again: `hostname -I`
3. Try accessing from the Pi first to make sure it's working
4. Check Windows Firewall settings

### Module installation fails:
```bash
sudo apt install python3-dev libffi-dev -y
pip3 install --upgrade pip
pip3 install -r requirements.txt
```

## Keep It Running

The app will run as long as the terminal is open. To keep it running after closing the terminal or rebooting, see the full **RASPBERRY_PI_SETUP.md** guide for setting up the systemd service.

## Quick Commands Reference

```bash
# Start the app
python3 app.py

# Stop the app
Press Ctrl+C in the terminal

# Check if it's running
ps aux | grep app.py

# Find IP address
hostname -I
```

---

**That's it! Your Classroom App should now be running!** 🎓

