# Quick Start Guide

## Initial Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**
   ```bash
   python app.py
   ```

3. **Access the Application**
   - Open your browser and go to: `http://localhost:5000`
   - Default login credentials:
     - Username: `professor`
     - Password: `password`

## First Steps

### As a Professor:

1. **Login** with the default credentials
2. **Create a Class**:
   - Click "Add New Class" on the dashboard
   - Enter class name and class code
   - Click "Add Class"

3. **Enter Classroom**:
   - Click on a class card to enter the classroom page

4. **Start a Class Session**:
   - Click the green "Start Class" button (bottom right)
   - This opens the Faculty Dashboard with live statistics

5. **Create a Poll/Quiz**:
   - In the Faculty Dashboard, click "Create Poll/Quiz"
   - Enter question and options (2-4 options)
   - Optionally set a correct answer for quizzes
   - Toggle "Anonymous Mode" if desired
   - Click "Start Poll"

6. **View Gradebook**:
   - In the classroom page, click "Gradebook"
   - View attendance, participation, and poll grades

### As a Student:

1. **Open Student Interface**:
   - Navigate to: `http://localhost:5000/student`
   - Or open in a separate browser/device

2. **Wake the Nameplate**:
   - Tap either screen to wake from sleep mode

3. **Login**:
   - **Option A**: Enter student number manually
   - **Option B**: Register as a new student first
   - **Option C**: Simulate RFID tap (for testing, enter any ID)

4. **Join a Class**:
   - Select an active class from the list
   - You'll be automatically marked as present

5. **Interact**:
   - Use "Raise Hand", "Thumbs Up", or "Thumbs Down" buttons
   - Participate in polls when they're started
   - View your name on the front screen (facing professor)

6. **Sign Out**:
   - Click the power button (bottom right) when done

## Testing the System

### Create Test Data:

1. **As Professor**:
   - Create a class (e.g., "Computer Science 101", Code: "CS101")

2. **As Student** (in separate browser/device):
   - Register a new student:
     - Student Number: "STU001"
     - First Name: "John"
     - Last Name: "Doe"
     - RFID Card ID: "RFID123" (optional)

3. **Start Class**:
   - As professor, click "Start Class"
   - As student, join the class

4. **Test Interactions**:
   - Student clicks "Raise Hand" - see it update in Faculty Dashboard
   - Professor creates a poll - student sees it on both screens
   - Student answers poll - see results in Faculty Dashboard

## Features to Explore

- **Settings**: Toggle "Show First Name Only" to see nameplate change
- **Live Stats**: Watch real-time updates in Faculty Dashboard
- **Poll Results**: View response counts and percentages
- **Gradebook**: See how attendance and participation are tracked
- **Multiple Students**: Open multiple student interfaces to simulate a full classroom

## Troubleshooting

- **Port already in use**: Change the port in `app.py` (last line)
- **Database errors**: Delete `classroom_app.db` and restart the app
- **Socket connection issues**: Make sure Flask-SocketIO is installed correctly
- **Student can't join**: Make sure professor has started the class first

## Next Steps

- Add more classes and students
- Customize settings for each class
- Run polls during class sessions
- Review gradebook after class ends
- Export data (future feature)

Enjoy using the Classroom Management App!

