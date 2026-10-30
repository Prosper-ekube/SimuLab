-- HRI System Database Schema

CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    password_salt TEXT NOT NULL,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS exercises (
    exercise_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    instructions TEXT NOT NULL,
    difficulty TEXT NOT NULL,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS student_progress (
    progress_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    exercise_id INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'Not Started', -- 'Not Started', 'In Progress', 'Completed'
    score INTEGER DEFAULT 0,
    completion_date TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (exercise_id) REFERENCES exercises(exercise_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS code_submissions (
    submission_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    exercise_id INTEGER NOT NULL,
    submitted_code TEXT NOT NULL,
    execution_status TEXT NOT NULL, -- 'Success', 'Error', 'Failed'
    execution_output TEXT,
    submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (exercise_id) REFERENCES exercises(exercise_id) ON DELETE CASCADE
);