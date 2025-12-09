# Classroom Management Web App

A comprehensive web application for managing classroom participation, attendance, polls, and student interactions using intelligent nameplate devices.

## Features

### Professor Side
- **Login System**: Secure professor authentication
- **Class Management**: Create and manage multiple classes
- **Classroom Page** with 4 main options:
  1. **Gradebook**: View attendance grades, peer participation, instructor participation, and poll grades
  2. **Class Details**: View all enrolled students and their student numbers
  3. **Settings & Preferences**: Configure display preferences (first name only, quiet mode, etc.)
  4. **Start Class**: Activate class session for student participation
- **Faculty Dashboard**: Real-time monitoring with:
  - Live statistics (attendance, hand raises, thumbs up/down)
  - Poll/Quiz creation and management
  - Live preference adjustments

### Student Side (Nameplate Device)
- **Dual Screen Interface**: 
  - Front screen (facing professor): Shows student name
  - Back screen (facing student): Shows class ID, controls, and time
- **Wake/Sleep Mode**: Tap screen or RFID card to activate
- **RFID Login**: Automatic login via RFID card tap
- **Manual Login/Register**: Fallback for students without cards
- **Auto Attendance**: Automatically marked present when joining active class
- **Interactive Controls**:
  - Raise Hand
  - Thumbs Up
  - Thumbs Down
  - Sign Out
- **Poll/Quiz Participation**: 
  - Kahoot-style multiple choice interface
  - Color feedback (green for correct, red for incorrect)
  - Anonymous mode support
- **Real-time Updates**: All interactions logged and displayed on faculty dashboard

## Quick Start

### Download the Project

1. **Download from GitHub:**
   - Visit: https://github.com/pooftek/IntelligentNameplate
   - Click "Code" → "Download ZIP"
   - Extract to a folder on your computer

   OR

2. **Clone with Git:**
   ```bash
   git clone https://github.com/pooftek/IntelligentNameplate.git
   cd IntelligentNameplate
   ```

### Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python app.py
   ```

3. **Access the application:**
   - Professor interface: http://localhost:5000
   - Student interface: http://localhost:5000/student

📖 **For detailed setup instructions, see [SETUP.md](SETUP.md)**

## Default Login

- **Username**: professor
- **Password**: password

*Note: Change these credentials in production!*

## Usage

### For Professors:

1. Login with your credentials
2. Create classes at the beginning of the school year
3. Select a class to enter the classroom page
4. Use "Start Class" button to activate the class session
5. Monitor live statistics in the Faculty Dashboard
6. Create polls/quizzes during class
7. View gradebook and class details as needed
8. Adjust settings and preferences in real-time

### For Students:

1. Tap the screen or RFID card to wake the nameplate
2. Login using RFID card or manually enter student number
3. Register if you're a new student
4. Select an active class to join
5. Use interactive buttons (Raise Hand, Thumbs Up/Down)
6. Participate in polls/quizzes when they're started
7. Sign out when done

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: SQLite (SQLAlchemy ORM)
- **Real-time Communication**: Flask-SocketIO (WebSockets)
- **Frontend**: Bootstrap 5, HTML5, JavaScript
- **Authentication**: Flask-Login

## Database Models

- Professor: User accounts for instructors
- Student: Student information and RFID card IDs
- Class: Class information and active status
- Enrollment: Student-class relationships
- Attendance: Daily attendance records
- Participation: Interaction tracking (hand raises, thumbs up/down)
- Poll: Poll/quiz questions and options
- PollResponse: Student poll responses
- ClassSettings: Per-class preferences

## RFID Integration

The app supports RFID card integration. In a production environment, you would connect an RFID reader to send card IDs to the `/api/student/login` endpoint. For testing, you can simulate RFID taps by entering card IDs manually.

## Future Enhancements

- Real RFID hardware integration
- Export gradebook to CSV/Excel
- Advanced analytics and reporting
- Mobile app versions
- Multi-language support
- Cloud deployment options

## License

This project is provided as-is for educational and development purposes.

