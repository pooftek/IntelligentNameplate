# Raspberry Pi Setup Guide

This guide will help you set up and run the Classroom Management Web App on your Raspberry Pi.

## Prerequisites

- Raspberry Pi (any model with Raspberry Pi OS)
- Internet connection
- SSH access (optional, for remote setup)

## Step 1: Update Your Raspberry Pi

```bash
sudo apt update
sudo apt upgrade -y
```

## Step 2: Install Python and pip

Raspberry Pi OS usually comes with Python 3, but verify and install pip if needed:

```bash
python3 --version  # Should show Python 3.7 or higher
sudo apt install python3-pip -y
```

## Step 3: Download the Project

### Option A: Clone from GitHub (Recommended)

```bash
cd ~
git clone https://github.com/pooftek/IntelligentNameplate.git
cd IntelligentNameplate
```

### Option B: Download ZIP

1. On your Pi, open a browser and go to: https://github.com/pooftek/IntelligentNameplate
2. Click "Code" → "Download ZIP"
3. Extract the ZIP file:
   ```bash
   cd ~/Downloads
   unzip IntelligentNameplate-main.zip
   mv IntelligentNameplate-main ~/IntelligentNameplate
   cd ~/IntelligentNameplate
   ```

## Step 4: Install Python Dependencies

```bash
pip3 install -r requirements.txt
```

**Note:** If you get permission errors, use:
```bash
pip3 install --user -r requirements.txt
```

Or install system-wide (requires sudo):
```bash
sudo pip3 install -r requirements.txt
```

## Step 5: Find Your Raspberry Pi's IP Address

You'll need this to access the app from other devices:

```bash
hostname -I
```

Or check your router's admin panel for the Pi's IP address.

**Example output:** `192.168.1.100`

## Step 6: Run the Application

### Manual Start

```bash
python3 app.py
```

You should see:
```
 * Running on http://0.0.0.0:5000
```

### Access from Other Devices

Once running, you can access the app from:
- **On the Pi itself:** http://localhost:5000
- **From other devices on the same network:** http://YOUR_PI_IP:5000
  - Example: http://192.168.1.100:5000

## Step 7: Run on Boot (Optional - Recommended)

Create a systemd service to automatically start the app when your Pi boots:

### Create the Service File

```bash
sudo nano /etc/systemd/system/classroom-app.service
```

Paste this content (adjust paths if needed):

```ini
[Unit]
Description=Classroom Management Web App
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/IntelligentNameplate
Environment="PATH=/usr/bin:/usr/local/bin"
ExecStart=/usr/bin/python3 /home/pi/IntelligentNameplate/app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Important:** Replace `/home/pi/IntelligentNameplate` with your actual project path if different!

Save and exit (Ctrl+X, then Y, then Enter).

### Enable and Start the Service

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service to start on boot
sudo systemctl enable classroom-app.service

# Start the service now
sudo systemctl start classroom-app.service

# Check status
sudo systemctl status classroom-app.service
```

### Useful Service Commands

```bash
# Stop the service
sudo systemctl stop classroom-app.service

# Restart the service
sudo systemctl restart classroom-app.service

# View logs
sudo journalctl -u classroom-app.service -f

# Disable auto-start on boot
sudo systemctl disable classroom-app.service
```

## Step 8: Configure Firewall (If Needed)

If you have a firewall enabled, allow port 5000:

```bash
sudo ufw allow 5000/tcp
```

## Troubleshooting

### Port Already in Use

If port 5000 is already in use:

1. Find what's using it:
   ```bash
   sudo lsof -i :5000
   ```

2. Or change the port in `app.py` (line 763):
   ```python
   socketio.run(app, debug=True, host='0.0.0.0', port=5001)
   ```

### Module Installation Issues

If `eventlet` fails to install:

```bash
sudo apt install python3-dev libffi-dev -y
pip3 install --upgrade pip
pip3 install -r requirements.txt
```

### Permission Errors

If you get permission errors with the database:

```bash
chmod 755 ~/IntelligentNameplate
chmod 644 ~/IntelligentNameplate/*.py
```

### Service Won't Start

Check the logs:
```bash
sudo journalctl -u classroom-app.service -n 50
```

Make sure:
- The path in the service file is correct
- Python3 is at `/usr/bin/python3` (check with `which python3`)
- The user has permission to access the directory

### Can't Access from Other Devices

1. Make sure the app is running: `sudo systemctl status classroom-app.service`
2. Check the Pi's IP: `hostname -I`
3. Make sure both devices are on the same network
4. Try accessing from the Pi first: `http://localhost:5000`
5. Check firewall: `sudo ufw status`

## Accessing from Student Devices

Once running on your Pi, students can access the student interface from any device on the same network:

- **Student Interface:** http://YOUR_PI_IP:5000/student
- **Professor Interface:** http://YOUR_PI_IP:5000

## Default Login

- **Username:** `professor`
- **Password:** `password`

⚠️ **Change these in production!**

## Performance Tips

1. **For better performance**, consider using a production WSGI server:
   ```bash
   pip3 install gunicorn
   gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:5000 app:app
   ```

2. **Monitor resource usage:**
   ```bash
   htop
   ```

3. **Check disk space:**
   ```bash
   df -h
   ```

## RFID Integration

If you're connecting an RFID reader to your Raspberry Pi:

1. Install required libraries for your RFID reader
2. Modify the `/api/student/login` endpoint to read from the hardware
3. See the main README.md for RFID integration details

## Next Steps

- Read [README.md](README.md) for feature documentation
- Check [QUICKSTART.md](QUICKSTART.md) for usage guide
- Review [SETUP.md](SETUP.md) for general setup info

---

**Your Classroom App is now running on Raspberry Pi!** 🎓

