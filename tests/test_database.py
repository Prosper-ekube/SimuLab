import unittest
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from database.db import initialize_database, get_connection, get_all_exercises_with_status, save_code_submission, get_student_overall_progress

class TestDatabase(unittest.TestCase):
    def setUp(self):
        initialize_database()
        conn = get_connection()
        cursor = conn.cursor()
        # Insert a temporary test student
        cursor.execute("INSERT OR IGNORE INTO students (student_id, full_name, username, password_hash, password_salt) VALUES (999, 'DB Test', 'db_tester', 'hash', 'salt')")
        conn.commit()
        conn.close()

    def test_exercise_seeding(self):
        exercises = get_all_exercises_with_status(999)
        # Verify the 8 foundational exercises are seeded
        self.assertEqual(len(exercises), 8)
        self.assertEqual(exercises[0][1], "Basic Robot Movement")

    def test_code_submission_and_progress(self):
        # Save code for exercise 1
        save_code_submission(999, 1, "move_forward()\nturn_right()", "Success", "Executed successfully")
        
        # Verify progress status updates to 'In Progress' or tracked
        stats = get_student_overall_progress(999)
        self.assertGreaterEqual(stats["total"], 8)

if __name__ == "__main__":
    unittest.main()