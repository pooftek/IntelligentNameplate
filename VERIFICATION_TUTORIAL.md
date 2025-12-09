# Website Functionality Verification Tutorial

This tutorial provides a comprehensive guide to verify all functionality of the Classroom Management Web App.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Initial Setup Verification](#initial-setup-verification)
3. [Professor Interface Testing](#professor-interface-testing)
4. [Student Interface Testing](#student-interface-testing)
5. [Real-time Features Testing](#real-time-features-testing)
6. [Database Verification](#database-verification)
7. [Integration Testing](#integration-testing)
8. [Common Issues & Troubleshooting](#common-issues--troubleshooting)

---

## Prerequisites

Before starting verification, ensure you have:

1. **Python 3.7+** installed
   ```bash
   python --version
   ```

2. **All dependencies installed**
   ```bash
   pip install -r requirements.txt
   ```

3. **Application running**
   ```bash
   python app.py
   ```
   You should see output indicating the server is running on `http://0.0.0.0:5000`

4. **Two browser windows/tabs** ready (one for professor, one for student)

---

## Initial Setup Verification

### Step 1: Verify Server is Running

1. Open your browser and navigate to: `http://localhost:5000`
2. **Expected Result**: You should be redirected to the login page
3. **Check**: The page should display a login form with username and password fields

### Step 2: Verify Database Initialization

1. Check if `instance/classroom_app.db` file exists
2. **Expected Result**: Database file should be created automatically on first run
3. **Verify**: Default professor account should be created:
   - Username: `professor`
   - Password: `password`

---

## Professor Interface Testing

### Test 1: Login Functionality

**Steps:**
1. Navigate to `http://localhost:5000`
2. Enter username: `professor`
3. Enter password: `password`
4. Click "Login" button

**Expected Results:**
- ✅ Redirected to dashboard page
- ✅ Dashboard shows "Welcome" message
- ✅ No error messages displayed
- ✅ URL should be `http://localhost:5000/dashboard`

**Verification Checklist:**
- [ ] Login successful
- [ ] Redirected to dashboard
- [ ] No console errors (check browser DevTools F12)

---

### Test 2: Create a New Class

**Steps:**
1. On the dashboard, click "Add New Class" button
2. Fill in the form:
   - Class Name: `Computer Science 101`
   - Class Code: `CS101`
3. Click "Add Class" button

**Expected Results:**
- ✅ New class card appears on dashboard
- ✅ Class name and code are displayed correctly
- ✅ Success message appears (if implemented)
- ✅ Class is saved in database

**Verification Checklist:**
- [ ] Class appears on dashboard
- [ ] Class name displayed correctly
- [ ] Class code displayed correctly
- [ ] Can click on class card to enter classroom

---

### Test 3: Enter Classroom Page

**Steps:**
1. Click on a class card from the dashboard
2. Observe the classroom page

**Expected Results:**
- ✅ URL changes to `/classroom/<class_id>`
- ✅ Four main options visible:
  - Gradebook
  - Class Details
  - Settings & Preferences
  - Start Class
- ✅ Class name displayed at top
- ✅ Student list visible (may be empty initially)

**Verification Checklist:**
- [ ] All four options are visible
- [ ] Class name displayed correctly
- [ ] Page loads without errors

---

### Test 4: View Class Details

**Steps:**
1. In classroom page, click "Class Details" button
2. Observe the modal/popup

**Expected Results:**
- ✅ Modal opens showing enrolled students
- ✅ Student numbers displayed
- ✅ Student names displayed (if students are enrolled)
- ✅ List is scrollable if many students

**Verification Checklist:**
- [ ] Modal opens correctly
- [ ] Student information displayed (if any enrolled)
- [ ] Can close modal

---

### Test 5: View Gradebook

**Steps:**
1. In classroom page, click "Gradebook" button
2. Observe the gradebook data

**Expected Results:**
- ✅ Gradebook modal/table opens
- ✅ Shows columns: Student Number, Name, Attendance Grade, Peer Participation, Instructor Participation, Poll Grade
- ✅ Data loads (may show zeros if no activity yet)
- ✅ Grades are calculated correctly

**Verification Checklist:**
- [ ] Gradebook opens
- [ ] All columns visible
- [ ] Data loads without errors
- [ ] Grades are numeric (0-100 range)

---

### Test 6: Settings & Preferences

**Steps:**
1. In classroom page, click "Settings & Preferences" button
2. Toggle "Show First Name Only" checkbox
3. Toggle "Quiet Mode" checkbox
4. Save settings

**Expected Results:**
- ✅ Settings modal opens
- ✅ Checkboxes are toggleable
- ✅ Settings save successfully
- ✅ Changes persist after page refresh

**Verification Checklist:**
- [ ] Settings modal opens
- [ ] Can toggle checkboxes
- [ ] Settings save successfully
- [ ] Settings persist after refresh

---

### Test 7: Start Class Session

**Steps:**
1. In classroom page, click "Start Class" button (green button, bottom right)
2. Observe the Faculty Dashboard

**Expected Results:**
- ✅ Redirected to Faculty Dashboard
- ✅ URL: `/faculty_dashboard/<class_id>`
- ✅ Dashboard shows:
  - Live statistics section
  - Attendance count
  - Hand raises count
  - Thumbs up/down counts
  - Create Poll/Quiz button
- ✅ Class status changes to "Active"

**Verification Checklist:**
- [ ] Redirected to Faculty Dashboard
- [ ] Live stats section visible
- [ ] All counters start at 0
- [ ] Create Poll button visible
- [ ] Class is marked as active

---

### Test 8: Create a Poll/Quiz

**Steps:**
1. In Faculty Dashboard, click "Create Poll/Quiz" button
2. Fill in poll form:
   - Question: `What is 2 + 2?`
   - Option 1: `3`
   - Option 2: `4`
   - Option 3: `5`
   - Option 4: `6`
   - Correct Answer: Select `Option 2` (4)
   - Anonymous Mode: Leave unchecked
3. Click "Start Poll" button

**Expected Results:**
- ✅ Poll modal opens
- ✅ Form accepts input
- ✅ Poll is created and activated
- ✅ Poll appears on dashboard
- ✅ Real-time notification sent to students

**Verification Checklist:**
- [ ] Poll form opens
- [ ] Can enter question and options
- [ ] Can select correct answer
- [ ] Poll starts successfully
- [ ] Poll visible on dashboard

---

### Test 9: View Poll Results

**Steps:**
1. After creating a poll, wait for responses (from student interface)
2. Observe the poll results on Faculty Dashboard

**Expected Results:**
- ✅ Results update in real-time
- ✅ Shows response counts per option
- ✅ Shows percentages
- ✅ Shows total responses
- ✅ Correct answers highlighted (if quiz mode)

**Verification Checklist:**
- [ ] Results update automatically
- [ ] Counts are accurate
- [ ] Percentages calculated correctly
- [ ] Total responses shown

---

### Test 10: Stop Poll

**Steps:**
1. In Faculty Dashboard, find active poll
2. Click "Stop Poll" button

**Expected Results:**
- ✅ Poll stops successfully
- ✅ Poll no longer active
- ✅ Students can no longer respond
- ✅ Results remain visible

**Verification Checklist:**
- [ ] Poll stops successfully
- [ ] Status changes to inactive
- [ ] Results remain visible

---

### Test 11: Stop Class Session

**Steps:**
1. In Faculty Dashboard, click "Stop Class" or "End Session" button
2. Return to classroom page

**Expected Results:**
- ✅ Class session ends
- ✅ Class status changes to inactive
- ✅ Gradebook updated with participation data
- ✅ Redirected back to classroom page

**Verification Checklist:**
- [ ] Class stops successfully
- [ ] Status changes to inactive
- [ ] Gradebook updated
- [ ] Redirected correctly

---

## Student Interface Testing

### Test 12: Access Student Interface

**Steps:**
1. Open a new browser window/tab (or use incognito mode)
2. Navigate to: `http://localhost:5000/student`
3. Observe the student interface

**Expected Results:**
- ✅ Student interface loads
- ✅ Shows dual-screen layout:
  - Front screen (facing professor): Shows name display
  - Back screen (facing student): Shows controls
- ✅ Screen is in "sleep" mode initially
- ✅ Tap to wake functionality works

**Verification Checklist:**
- [ ] Page loads correctly
- [ ] Dual-screen layout visible
- [ ] Can tap screen to wake
- [ ] Login form appears when awake

---

### Test 13: Register New Student

**Steps:**
1. On student interface, click "Register" or "New Student" button
2. Fill in registration form:
   - Student Number: `STU001`
   - First Name: `John`
   - Last Name: `Doe`
   - RFID Card ID: `RFID123` (optional)
3. Click "Register" button

**Expected Results:**
- ✅ Registration form opens
- ✅ Form accepts all inputs
- ✅ Student is created successfully
- ✅ Auto-logged in after registration
- ✅ Student can see active classes

**Verification Checklist:**
- [ ] Registration form opens
- [ ] Can enter all fields
- [ ] Registration successful
- [ ] Auto-logged in
- [ ] Active classes list appears

---

### Test 14: Student Login

**Steps:**
1. If not registered, enter student number: `STU001`
2. Click "Login" button

**Expected Results:**
- ✅ Login successful
- ✅ Student information displayed
- ✅ Active classes list appears
- ✅ Can select a class to join

**Verification Checklist:**
- [ ] Login successful
- [ ] Student info displayed
- [ ] Active classes visible
- [ ] Can select class

---

### Test 15: Join Active Class

**Steps:**
1. After logging in, ensure a class is active (from professor side)
2. Select an active class from the list
3. Click "Join Class" button

**Expected Results:**
- ✅ Student joins class successfully
- ✅ Attendance automatically marked
- ✅ Student name appears on front screen
- ✅ Controls become active
- ✅ Real-time connection established

**Verification Checklist:**
- [ ] Can select active class
- [ ] Join successful
- [ ] Name displayed on front screen
- [ ] Controls enabled
- [ ] Attendance marked (check professor dashboard)

---

### Test 16: Raise Hand Interaction

**Steps:**
1. After joining a class, click "Raise Hand" button
2. Observe the front screen and professor dashboard

**Expected Results:**
- ✅ Hand raise registered
- ✅ Counter increments on professor dashboard
- ✅ Real-time update visible
- ✅ Can raise hand multiple times

**Verification Checklist:**
- [ ] Button click works
- [ ] Counter updates on professor side
- [ ] Real-time update works
- [ ] Multiple clicks increment counter

---

### Test 17: Thumbs Up/Down Interactions

**Steps:**
1. Click "Thumbs Up" button
2. Click "Thumbs Down" button
3. Observe professor dashboard

**Expected Results:**
- ✅ Both interactions registered
- ✅ Counters update on professor dashboard
- ✅ Real-time updates work
- ✅ Multiple clicks increment counters

**Verification Checklist:**
- [ ] Thumbs up works
- [ ] Thumbs down works
- [ ] Counters update correctly
- [ ] Real-time updates work

---

### Test 18: Participate in Poll

**Steps:**
1. Ensure a poll is active (created by professor)
2. Wait for poll to appear on student interface
3. Select an answer option
4. Click to submit answer

**Expected Results:**
- ✅ Poll appears on both screens (front and back)
- ✅ Can select an option
- ✅ Answer submits successfully
- ✅ Color feedback shown (green for correct, red for incorrect)
- ✅ Results update on professor dashboard

**Verification Checklist:**
- [ ] Poll appears automatically
- [ ] Can select option
- [ ] Answer submits
- [ ] Color feedback works
- [ ] Results update on professor side

---

### Test 19: Student Sign Out

**Steps:**
1. Click the power/sign out button (bottom right)
2. Observe the interface

**Expected Results:**
- ✅ Student signs out successfully
- ✅ Returns to login screen
- ✅ Session cleared
- ✅ Can log back in

**Verification Checklist:**
- [ ] Sign out works
- [ ] Returns to login
- [ ] Session cleared
- [ ] Can log back in

---

## Real-time Features Testing

### Test 20: Real-time Statistics Updates

**Steps:**
1. Open professor dashboard in one window
2. Open student interface in another window
3. Have student join class and perform interactions
4. Observe professor dashboard updates

**Expected Results:**
- ✅ Statistics update automatically without page refresh
- ✅ Attendance count updates
- ✅ Hand raises counter updates
- ✅ Thumbs up/down counters update
- ✅ Updates appear within 1-2 seconds

**Verification Checklist:**
- [ ] Updates happen automatically
- [ ] No page refresh needed
- [ ] Updates are timely (< 2 seconds)
- [ ] All counters update correctly

---

### Test 21: Real-time Poll Distribution

**Steps:**
1. Professor creates a poll
2. Student is already in class
3. Observe student interface

**Expected Results:**
- ✅ Poll appears on student interface automatically
- ✅ No page refresh needed
- ✅ Poll appears on both screens
- ✅ Student can immediately respond

**Verification Checklist:**
- [ ] Poll appears automatically
- [ ] No refresh needed
- [ ] Appears on both screens
- [ ] Can respond immediately

---

### Test 22: Real-time Poll Results

**Steps:**
1. Professor creates a poll
2. Multiple students respond (open multiple student windows)
3. Observe professor dashboard results

**Expected Results:**
- ✅ Results update in real-time as students respond
- ✅ Counts increment automatically
- ✅ Percentages recalculate automatically
- ✅ Total responses updates

**Verification Checklist:**
- [ ] Results update in real-time
- [ ] Counts increment automatically
- [ ] Percentages update
- [ ] Total responses accurate

---

### Test 23: Settings Update in Real-time

**Steps:**
1. Professor changes "Show First Name Only" setting
2. Student is in active class
3. Observe student nameplate

**Expected Results:**
- ✅ Nameplate updates automatically
- ✅ Shows only first name if setting enabled
- ✅ Updates without page refresh
- ✅ Changes persist

**Verification Checklist:**
- [ ] Nameplate updates automatically
- [ ] Setting applies correctly
- [ ] No refresh needed
- [ ] Changes persist

---

## Database Verification

### Test 24: Verify Data Persistence

**Steps:**
1. Create a class, add students, run a session
2. Stop the application
3. Restart the application
4. Login and check data

**Expected Results:**
- ✅ All classes still exist
- ✅ All students still exist
- ✅ Attendance records preserved
- ✅ Participation data preserved
- ✅ Poll data preserved

**Verification Checklist:**
- [ ] Classes persist
- [ ] Students persist
- [ ] Attendance records persist
- [ ] Participation data persists
- [ ] Poll data persists

---

### Test 25: Verify Database Relationships

**Steps:**
1. Check database using SQLite browser or command line
2. Verify foreign key relationships

**Expected Results:**
- ✅ Enrollments link students to classes correctly
- ✅ Attendance links to students and classes
- ✅ Participation links to students and classes
- ✅ Poll responses link to polls and students

**Verification Checklist:**
- [ ] Foreign keys work correctly
- [ ] Data integrity maintained
- [ ] Relationships correct

---

## Integration Testing

### Test 26: Full Class Session Flow

**Steps:**
1. **Professor Side:**
   - Login
   - Create a class
   - Start class session
   - Create a poll

2. **Student Side:**
   - Register/Login
   - Join class
   - Raise hand
   - Answer poll
   - Sign out

3. **Professor Side:**
   - View poll results
   - Stop poll
   - Stop class
   - View gradebook

**Expected Results:**
- ✅ Complete flow works end-to-end
- ✅ All features function together
- ✅ Data flows correctly between interfaces
- ✅ No errors occur

**Verification Checklist:**
- [ ] Complete flow works
- [ ] All features integrate
- [ ] Data flows correctly
- [ ] No errors

---

### Test 27: Multiple Students Scenario

**Steps:**
1. Open 3-5 student interface windows
2. Register different students in each
3. All join the same active class
4. Perform various interactions
5. Observe professor dashboard

**Expected Results:**
- ✅ All students can join simultaneously
- ✅ All interactions tracked separately
- ✅ Statistics aggregate correctly
- ✅ Poll results show all responses
- ✅ No conflicts or errors

**Verification Checklist:**
- [ ] Multiple students can join
- [ ] Interactions tracked separately
- [ ] Statistics aggregate correctly
- [ ] Poll results accurate
- [ ] No conflicts

---

### Test 28: Multiple Classes Scenario

**Steps:**
1. Create 2-3 different classes
2. Start multiple classes (if supported) or start one at a time
3. Have students join different classes
4. Verify data separation

**Expected Results:**
- ✅ Classes operate independently
- ✅ Students can only see active classes
- ✅ Data is separated by class
- ✅ No cross-class data leakage

**Verification Checklist:**
- [ ] Classes operate independently
- [ ] Students see correct classes
- [ ] Data separated correctly
- [ ] No data leakage

---

## Common Issues & Troubleshooting

### Issue 1: Server Won't Start

**Symptoms:**
- Error when running `python app.py`
- Port already in use error

**Solutions:**
1. Check if another instance is running: `netstat -ano | findstr :5000` (Windows)
2. Kill the process or change port in `app.py` (last line)
3. Check Python version: `python --version` (need 3.7+)
4. Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`

---

### Issue 2: Database Errors

**Symptoms:**
- Database locked errors
- Missing tables
- Data not persisting

**Solutions:**
1. Delete `instance/classroom_app.db` and restart app
2. Check file permissions on database file
3. Ensure only one instance of app is running
4. Check SQLite version compatibility

---

### Issue 3: Real-time Features Not Working

**Symptoms:**
- Statistics don't update
- Polls don't appear
- No WebSocket connection

**Solutions:**
1. Check browser console for errors (F12)
2. Verify Flask-SocketIO is installed: `pip show flask-socketio`
3. Check network tab for WebSocket connections
4. Try different browser
5. Check firewall/antivirus blocking WebSocket connections

---

### Issue 4: Student Can't Join Class

**Symptoms:**
- No active classes shown
- Join button doesn't work
- Error message appears

**Solutions:**
1. Verify professor has started the class
2. Check class is marked as active in database
3. Check student is logged in (session exists)
4. Verify WebSocket connection is established
5. Check browser console for errors

---

### Issue 5: Poll Not Appearing

**Symptoms:**
- Professor creates poll but student doesn't see it
- Poll doesn't start

**Solutions:**
1. Verify student is in the class
2. Check WebSocket connection
3. Verify poll is marked as active in database
4. Check browser console for errors
5. Try refreshing student page (shouldn't be needed but helps debug)

---

### Issue 6: Authentication Issues

**Symptoms:**
- Can't login
- Session expires unexpectedly
- Redirected to login repeatedly

**Solutions:**
1. Verify default credentials: `professor` / `password`
2. Check SECRET_KEY in app.py
3. Clear browser cookies
4. Check Flask-Login is installed correctly
5. Verify session storage is working

---

## Verification Checklist Summary

Use this checklist to ensure all major features are verified:

### Professor Features
- [ ] Login/Logout
- [ ] Create Class
- [ ] View Dashboard
- [ ] Enter Classroom
- [ ] View Class Details
- [ ] View Gradebook
- [ ] Update Settings
- [ ] Start/Stop Class
- [ ] Create Poll/Quiz
- [ ] View Poll Results
- [ ] Stop Poll

### Student Features
- [ ] Access Student Interface
- [ ] Register New Student
- [ ] Login
- [ ] Join Active Class
- [ ] Raise Hand
- [ ] Thumbs Up/Down
- [ ] Participate in Poll
- [ ] Sign Out

### Real-time Features
- [ ] Statistics Updates
- [ ] Poll Distribution
- [ ] Poll Results Updates
- [ ] Settings Updates

### Data & Integration
- [ ] Data Persistence
- [ ] Database Relationships
- [ ] Full Session Flow
- [ ] Multiple Students
- [ ] Multiple Classes

---

## Testing Tools & Tips

### Browser Developer Tools

1. **Open DevTools**: Press F12 or Right-click → Inspect
2. **Console Tab**: Check for JavaScript errors
3. **Network Tab**: Monitor API calls and WebSocket connections
4. **Application Tab**: Check cookies, session storage, local storage

### Useful Commands

```bash
# Check if server is running
netstat -ano | findstr :5000

# Check Python version
python --version

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Run with verbose output
python app.py --debug
```

### Testing Best Practices

1. **Test in Multiple Browsers**: Chrome, Firefox, Edge
2. **Test with Multiple Users**: Use incognito windows for different users
3. **Test Edge Cases**: Empty inputs, long strings, special characters
4. **Test Error Handling**: Invalid credentials, missing data, network issues
5. **Monitor Performance**: Check page load times, response times
6. **Document Issues**: Keep notes of any bugs or unexpected behavior

---

## Conclusion

This tutorial covers all major functionality of the Classroom Management Web App. Follow the tests in order for a systematic verification, or jump to specific features as needed.

**Remember:**
- Always test with multiple browser windows to simulate real-world usage
- Check browser console for errors
- Verify data persistence after restarts
- Test real-time features with multiple users
- Document any issues you find

Happy testing! 🎓

