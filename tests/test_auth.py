import unittest
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from authentication.register import hash_password, register_student
from authentication.login import verify_password, authenticate_student
from database.db import initialize_database, get_connection

class TestAuthentication(unittest.TestCase):
    def setUp(self):
        initialize_database()
        # Clean test user if exists
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE username = 'test_student'")
        conn.commit()
        conn.close()

    def test_password_hashing(self):
        pwd = "securepassword123"
        h1, s1 = hash_password(pwd)
        h2, s2 = hash_password(pwd)
        
        # Salts should be unique
        self.assertNotEqual(s1, s2)
        # Hashes should be different due to unique salts
        self.assertNotEqual(h1, h2)
        # Verification should succeed with correct salt and hash
        self.assertTrue(verify_password(h1, s1, pwd))
        self.assertFalse(verify_password(h1, s1, "wrongpassword"))

    def test_student_registration_and_login(self):
        # Register new student
        success, msg = register_student("Test User", "test_student", "password123", "password123")
        self.assertTrue(success)
        
        # Duplicate username registration should fail
        success_dup, _ = register_student("Another User", "test_student", "password123", "password123")
        self.assertFalse(success_dup)

        # Authenticate student
        auth_success, auth_msg, student_data = authenticate_student("test_student", "password123")
        self.assertTrue(auth_success)
        self.assertEqual(student_data["username"], "test_student")
        self.assertEqual(student_data["full_name"], "Test User")

        # Invalid login
        bad_success, _, _ = authenticate_student("test_student", "wrongpass")
        self.assertFalse(bad_success)

if __name__ == "__main__":
    unittest.main()