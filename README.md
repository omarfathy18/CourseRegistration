# Course Registration System

A web-based application for managing course registration, built using Flask and MySQL. The system allows users to log in, register for courses, add/drop courses, and view their registered courses. It includes user authentication and session management.

## Features

- **User Authentication**: Login and register with email and password.
- **Course Registration**:
  - View available courses.
  - Register for up to 5 courses.
  - Drop registered courses.
- **Session Management**: Tracks user activity and stores session-specific data.
- **Deadline Handling**: Enforces a registration deadline.

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: MySQL
- **Frontend**: HTML (via Flask templates)
- **Other Libraries**: 
  - `flask_mysqldb` for MySQL integration.
  - `flash` for messaging.

## Setup Instructions

1. Clone this repository:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
2. Install required Python packages:
   ```bash
    pip install -r requirements.txt

3. Set up the MySQL database:
  - Create a database named `CourseRegistration`.
  - Import the necessary tables (users, courses, registered) as per the application logic.

4. Configure database connection in `app.py`:
Replace `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_HOST`, and `MYSQL_DB` with your database credentials.

5. Run the application:
   ```bash
   python app.py

6. Access the application in your browser at http://127.0.0.1:5000.

## Project Structure

- `app.py`: Main application logic.
- `templates/`: Contains HTML templates for rendering pages.

## Usage

1. Navigate to the homepage (`/`) to log in.
2. Register a new account at `/register`.
3. Access the course registration portal at `/courses`.
4. Add or drop courses as needed before the deadline.
5. View the final list of registered courses at `/final`.

## Limitations

- Static deadline for course changes (`15-10-2022`); needs updating for dynamic deadlines.
- No email verification for user registration.
- Limited input validation and error handling.

## Future Improvements

- Add support for dynamic deadlines.
- Implement email verification and password recovery.
- Enhance UI/UX with modern frontend frameworks.
- Introduce admin panel for better management of users and courses.
