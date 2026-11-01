from database.db import get_connection
import hashlib
import secrets
import sqlite3
import os
import sys
import tkinter as tk
from tkinter import messagebox

# Add root directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Dark IDE Styling Constants
BG_MAIN = "#060b13"
BG_PANEL = "#091324"
ACCENT_BLUE = "#0f5b96"
BORDER_COLOR = "#1c3150"
TEXT_PRIMARY = "#ffffff"
TEXT_MUTED = "#94a3b8"


def hash_password(password: str, salt: bytes = None) -> tuple[str, str]:
    """Hash password using PBKDF2 with SHA-256 and a unique random salt."""
    if salt is None:
        salt = secrets.token_bytes(32)
    pwd_hash = hashlib.pbkdf2_hmac(
        'sha256', password.encode('utf-8'), salt, 100000)
    return pwd_hash.hex(), salt.hex()


def register_student(full_name: str, username: str, password: str, confirm_password: str) -> tuple[bool, str]:
    """Validate student credentials and save user to SQLite."""
    if not full_name.strip() or not username.strip() or not password or not confirm_password:
        return False, "All required fields must be completed."

    if password != confirm_password:
        return False, "Passwords do not match."

    if len(password) < 6:
        return False, "Password must be at least 6 characters long."

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT student_id FROM students WHERE username = ?", (username.strip(),))
        if cursor.fetchone():
            return False, "Username already exists. Please choose a unique username[cite: 1]."

        pwd_hash, pwd_salt = hash_password(password)
        cursor.execute(
            """
            INSERT INTO students (full_name, username, password_hash, password_salt)
            VALUES (?, ?, ?, ?)
            """,
            (full_name.strip(), username.strip(), pwd_hash, pwd_salt)
        )
        conn.commit()
        return True, "Registration successful! You can now log in."
    except sqlite3.Error as e:
        return False, f"Database error: {e}"
    finally:
        conn.close()


class RegisterFrame(tk.Frame):
    """Tkinter frame for student registration UI adhering to the Dark IDE style."""

    def __init__(self, parent, switch_to_login_cb):
        super().__init__(parent, bg=BG_MAIN)
        self.switch_to_login_cb = switch_to_login_cb
        self.build_ui()

    def build_ui(self):
        title_label = tk.Label(self, text="SimuLab", font=(
            "Georgia", 22, "bold"), fg=TEXT_PRIMARY, bg=BG_MAIN)
        title_label.pack(pady=(5, 2))

        subtitle_label = tk.Label(self, text="Create Student Account", font=(
            "Arial", 9), fg=TEXT_MUTED, bg=BG_MAIN)
        subtitle_label.pack(pady=(0, 15))

        form_frame = tk.Frame(
            self, bg=BG_PANEL, highlightbackground=BORDER_COLOR, highlightthickness=1)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        inner = tk.Frame(form_frame, bg=BG_PANEL)
        inner.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        tk.Label(inner, text="Full Name", font=("Arial", 8),
                 fg=TEXT_MUTED, bg=BG_PANEL).pack(anchor="w")
        self.reg_name = tk.Entry(inner, bg="#030914", fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY,
                                 relief=tk.FLAT, highlightbackground=BORDER_COLOR, highlightthickness=1, font=("Courier", 9))
        self.reg_name.pack(fill=tk.X, pady=(2, 8), ipady=4)

        tk.Label(inner, text="Username", font=("Arial", 8),
                 fg=TEXT_MUTED, bg=BG_PANEL).pack(anchor="w")
        self.reg_user = tk.Entry(inner, bg="#030914", fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY,
                                 relief=tk.FLAT, highlightbackground=BORDER_COLOR, highlightthickness=1, font=("Courier", 9))
        self.reg_user.pack(fill=tk.X, pady=(2, 8), ipady=4)

        tk.Label(inner, text="Password", font=("Arial", 8),
                 fg=TEXT_MUTED, bg=BG_PANEL).pack(anchor="w")
        self.reg_pass = tk.Entry(inner, bg="#030914", fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY, show="*",
                                 relief=tk.FLAT, highlightbackground=BORDER_COLOR, highlightthickness=1, font=("Courier", 9))
        self.reg_pass.pack(fill=tk.X, pady=(2, 8), ipady=4)

        tk.Label(inner, text="Confirm Password", font=("Arial", 8),
                 fg=TEXT_MUTED, bg=BG_PANEL).pack(anchor="w")
        self.reg_cpass = tk.Entry(inner, bg="#030914", fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY, show="*",
                                  relief=tk.FLAT, highlightbackground=BORDER_COLOR, highlightthickness=1, font=("Courier", 9))
        self.reg_cpass.pack(fill=tk.X, pady=(2, 12), ipady=4)

        reg_btn = tk.Button(inner, text="REGISTER", bg=ACCENT_BLUE, fg=TEXT_PRIMARY, font=(
            "Arial", 9, "bold"), relief=tk.FLAT, cursor="hand2", command=self.handle_register)
        reg_btn.pack(fill=tk.X, ipady=6, pady=(0, 8))

        switch_frame = tk.Frame(inner, bg=BG_PANEL)
        switch_frame.pack()

        tk.Label(switch_frame, text="Already have an account?", font=(
            "Arial", 8), fg=TEXT_MUTED, bg=BG_PANEL).pack(side=tk.LEFT)
        login_link = tk.Label(switch_frame, text=" Login", font=(
            "Arial", 8, "bold"), fg=ACCENT_BLUE, bg=BG_PANEL, cursor="hand2")
        login_link.pack(side=tk.LEFT)
        login_link.bind("<Button-1>", lambda e: self.switch_to_login_cb())

    def handle_register(self):
        success, message = register_student(
            self.reg_name.get(),
            self.reg_user.get(),
            self.reg_pass.get(),
            self.reg_cpass.get()
        )
        if success:
            messagebox.showinfo("Success", message)
            self.switch_to_login_cb()
        else:
            messagebox.showerror("Registration Error", message)