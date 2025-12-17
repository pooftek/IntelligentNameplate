# Setup Guide - Download and Run Instructions

This guide will help you download and run the Classroom Management Web App on your computer.

## Prerequisites

Before you begin, make sure you have:

- **Python 3.7 or higher** installed ([Download Python](https://www.python.org/downloads/))
- **Git** installed ([Download Git](https://git-scm.com/downloads)) - Optional, for cloning the repository
- A web browser (Chrome, Firefox, Edge, etc.)

## Step 1: Download the Project

### Option A: Download from GitHub (Recommended)

1. Go to the GitHub repository: https://github.com/pooftek/IntelligentNameplate
2. Click the green **"Code"** button
3. Select **"Download ZIP"**
4. Extract the ZIP file to a folder on your computer (e.g., `C:\Users\YourName\classroom_app`)

### Option B: Clone with Git

```bash
git clone https://github.com/pooftek/IntelligentNameplate.git
cd IntelligentNameplate
```

## Step 2: Install Python Dependencies

1. Open a terminal/command prompt in the project folder
2. Install the required packages:

```bash
pip install -r requirements.txt
```

**Note for Windows users:** If `pip` doesn't work, try `python -m pip install -r requirements.txt`

**Note for Mac/Linux users:** You may need to use `pip3` instead of `pip`

## Step 3: Run the Application

1. In the same terminal, run:

```bash
python app.py
```

**Note for Windows:** If `python` doesn't work, try `py app.py` or `python3 app.py`

2. You should see output like:
```
 * Running on http://0.0.0.0:5000
```

## Step 4: Access the Application

1. Open your web browser
2. Go to: **http://localhost:5000**

### Default Login Credentials

- **Username:** `professor`
- **Password:** `password`

⚠️ **Important:** Change these credentials in production!

## Step 5: First Time Setup

### For Professors:

1. Login with the default credentials
2. Create your first class:
   - Click "Add New Class"
   - Enter a class name and class code
   - Click "Add Class"
3. Click on the class card to enter the classroom
4. Click "Start Class" to activate the class session

### For Students:

1. Open a new browser tab/window
2. Go to: **http://localhost:5000/student**
3. Tap the screen to wake the nameplate
4. Register as a new student or login with your student number

## Troubleshooting

### Port Already in Use

If you see an error about port 5000 being in use:

1. Close any other applications using port 5000
2. Or modify `app.py` line 763 to use a different port:
   ```python
   socketio.run(app, debug=True, host='0.0.0.0', port=5001)
   ```

### Module Not Found Errors

If you get errors about missing modules:

```bash
pip install --upgrade -r requirements.txt
```

### Database Issues

The database is automatically created when you first run the app. If you need to reset it:

1. Delete the `instance/classroom_app.db` file
2. Restart the application

### Windows: Python Not Recognized

1. Make sure Python is installed and added to PATH
2. Try using `py` instead of `python`
3. Or use the full path: `C:\Python39\python.exe app.py`

## Project Structure

```
classroom_app/
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── SETUP.md              # This file
├── templates/            # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   ├── classroom.html
│   ├── faculty_dashboard.html
│   └── student_interface.html
└── instance/             # Database (created automatically)
    └── classroom_app.db
```

## Next Steps

- Read the [README.md](README.md) for detailed feature documentation
- Check [QUICKSTART.md](QUICKSTART.md) for a quick reference guide
- Review [VERIFICATION_TUTORIAL.md](VERIFICATION_TUTORIAL.md) for verification procedures

## Getting Help

If you encounter issues:

1. Check that all prerequisites are installed
2. Verify you're using Python 3.7+
3. Make sure all dependencies are installed
4. Check the terminal output for error messages

## Security Notes

⚠️ **Before deploying to production:**

1. Change the default professor password
2. Update the `SECRET_KEY` in `app.py` (line 11)
3. Use a production-grade database (PostgreSQL, MySQL)
4. Enable HTTPS
5. Set up proper authentication and authorization

---

**Enjoy using the Classroom Management Web App!** 🎓



