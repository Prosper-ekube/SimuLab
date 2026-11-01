import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(
    os.path.dirname(__file__)), "data", "hri_system.db")
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")


def get_connection():
    """Establish and return a connection to the SQLite database with foreign keys enabled."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def seed_initial_exercises(cursor):
    """Populate the 8 foundational robotics exercises if the table is empty."""
    cursor.execute("SELECT COUNT(*) FROM exercises;")
    if cursor.fetchone()[0] == 0:
        initial_exercises = [
            ("Basic Robot Movement", "Learn how to move the robot forward and backward across grid cells using basic movement commands.", "Beginner"),
            ("Directional Control", "Practice rotating the robot using 90-degree turns to navigate specific orientations.", "Beginner"),
            ("Combined Movement", "Combine forward movements and directional turns to follow a defined path.", "Beginner"),
            ("Obstacle Detection", "Utilize sensor commands to check for obstacles within the detection range before moving.", "Intermediate"),
            ("Distance Detection", "Read precise distances to nearest obstacles using simulated distance sensors.", "Intermediate"),
            ("Target Navigation", "Guide the robot across the grid to reach a specific target destination.", "Intermediate"),
            ("Conditional Movement",
             "Implement decision-making using if/else conditional logic based on sensor readings.", "Advanced"),
            ("Repeated Movement", "Use repetition loops (repeat(n)) to automate repetitive grid traversal steps.", "Advanced")
        ]
        cursor.executemany(
            """
            INSERT INTO exercises (title, instructions, difficulty)
            VALUES (?, ?, ?)
            """,
            initial_exercises
        )


def initialize_database():
    """Automatically create the SQLite database, tables, and seed data on first run."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = get_connection()
    cursor = conn.cursor()

    if os.path.exists(SCHEMA_PATH):
        with open(SCHEMA_PATH, "r") as schema_file:
            cursor.executescript(schema_file.read())

        seed_initial_exercises(cursor)
        conn.commit()
        print("Database initialized and seeded successfully.")
    else:
        print(f"Error: Schema file not found at {SCHEMA_PATH}")

    conn.close()


def get_all_exercises_with_status(student_id: int):
    """Fetch all exercises along with the progress status for a specific student."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT e.exercise_id, e.title, e.instructions, e.difficulty,
               COALESCE(sp.status, 'Not Started') AS status,
               COALESCE(sp.score, 0) AS score
        FROM exercises e
        LEFT JOIN student_progress sp 
               ON e.exercise_id = sp.exercise_id AND sp.student_id = ?
        ORDER BY e.exercise_id ASC
        """,
        (student_id,)
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


def save_code_submission(student_id: int, exercise_id: int, code: str, execution_status: str = "Saved", execution_output: str = ""):
    """Save student code submission into the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO code_submissions (student_id, exercise_id, submitted_code, execution_status, execution_output)
        VALUES (?, ?, ?, ?, ?)
        """,
        (student_id, exercise_id, code, execution_status, execution_output)
    )

    # Update progress status to 'In Progress' if currently 'Not Started'
    cursor.execute(
        """
        SELECT progress_id, status FROM student_progress 
        WHERE student_id = ? AND exercise_id = ?
        """,
        (student_id, exercise_id)
    )
    row = cursor.fetchone()
    if not row:
        cursor.execute(
            """
            INSERT INTO student_progress (student_id, exercise_id, status, score)
            VALUES (?, ?, 'In Progress', 0)
            """,
            (student_id, exercise_id)
        )
    elif row[1] == 'Not Started':
        cursor.execute(
            """
            UPDATE student_progress SET status = 'In Progress'
            WHERE progress_id = ?
            """,
            (row[0],)
        )
    conn.commit()
    conn.close()


def get_latest_saved_code(student_id: int, exercise_id: int) -> str:
    """Retrieve the latest submitted code for a student and exercise."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT submitted_code FROM code_submissions
        WHERE student_id = ? AND exercise_id = ?
        ORDER BY submission_date DESC LIMIT 1
        """,
        (student_id, exercise_id)
    )
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else ""


def get_student_overall_progress(student_id: int):
    """Retrieve student completed exercise count and average score."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT 
            COUNT(CASE WHEN status = 'Completed' THEN 1 END) AS completed_count,
            COUNT(CASE WHEN status = 'In Progress' THEN 1 END) AS in_progress_count,
            COUNT(*) AS total_count,
            COALESCE(AVG(score), 0) AS avg_score
        FROM (
            SELECT e.exercise_id, COALESCE(sp.status, 'Not Started') AS status, COALESCE(sp.score, 0) AS score
            FROM exercises e
            LEFT JOIN student_progress sp ON e.exercise_id = sp.exercise_id AND sp.student_id = ?
        )
        """,
        (student_id,)
    )
    row = cursor.fetchone()
    conn.close()
    return {
        "completed": row[0],
        "in_progress": row[1],
        "total": row[2],
        "avg_score": round(row[3], 1)
    }


if __name__ == "__main__":
    initialize_database()
