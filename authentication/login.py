from database.db import get_connection
import hashlib
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


def verify_password(stored_hash: str, stored_salt_hex: str, provided_password: str) -> bool:
    #Verify password hash against stored salt
    salt = bytes.fromhex(stored_salt_hex)
    pwd_hash = hashlib.pbkdf2_hmac(
        'sha256', provided_password.encode('utf-8'), salt, 100000)
    return pwd_hash.hex() == stored_hash


def authenticate_student(username: str, password: str) -> tuple[bool, str, dict | None]:
    #Authenticate student against SQLite records
    if not username.strip() or not password:
        return False, "Username and password are required.", None

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT student_id, full_name, username, password_hash, password_salt FROM students WHERE username = ?",
            (username.strip(),)
        )
        row = cursor.fetchone()

        if not row:
            return False, "Invalid username or password.", None

        student_id, full_name, db_username, stored_hash, stored_salt = row

        if verify_password(stored_hash, stored_salt, password):
            student_data = {
                "student_id": student_id,
                "full_name": full_name,
                "username": db_username
            }
            return True, "Login successful.", student_data
        else:
            return False, "Invalid username or password.", None

    except sqlite3.Error as e:
        return False, f"Database error: {e}", None
    finally:
        conn.close()


class LoginFrame(tk.Frame):
    #Tkinter frame for student login UI adhering to the Dark IDE style
    def __init__(self, parent, switch_to_register_cb, on_login_success_cb):
        super().__init__(parent, bg=BG_MAIN)
        self.switch_to_register_cb = switch_to_register_cb
        self.on_login_success_cb = on_login_success_cb
        self.build_ui()

    def build_ui(self):
        title_label = tk.Label(self, text="SimuLab", font=(
            "Georgia", 24, "bold"), fg=TEXT_PRIMARY, bg=BG_MAIN)
        title_label.pack(pady=(10, 5))

        subtitle_label = tk.Label(self, text="Human–Robot Interaction System", font=(
            "Arial", 10), fg=TEXT_MUTED, bg=BG_MAIN)
        subtitle_label.pack(pady=(0, 30))

        form_frame = tk.Frame(
            self, bg=BG_PANEL, highlightbackground=BORDER_COLOR, highlightthickness=1)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        inner = tk.Frame(form_frame, bg=BG_PANEL)
        inner.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        tk.Label(inner, text="STUDENT LOGIN", font=("Arial", 10, "bold"),
                 fg=TEXT_PRIMARY, bg=BG_PANEL).pack(anchor="w", pady=(0, 15))

        tk.Label(inner, text="Username", font=("Arial", 9),
                 fg=TEXT_MUTED, bg=BG_PANEL).pack(anchor="w")
        self.username_entry = tk.Entry(inner, bg="#030914", fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY, relief=tk.FLAT,
                                       highlightbackground=BORDER_COLOR, highlightcolor=ACCENT_BLUE, highlightthickness=1, font=("Courier", 10))
        self.username_entry.pack(fill=tk.X, pady=(5, 15), ipady=6)

        tk.Label(inner, text="Password", font=("Arial", 9),
                 fg=TEXT_MUTED, bg=BG_PANEL).pack(anchor="w")
        self.password_entry = tk.Entry(inner, bg="#030914", fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY, show="*", relief=tk.FLAT,
                                       highlightbackground=BORDER_COLOR, highlightcolor=ACCENT_BLUE, highlightthickness=1, font=("Courier", 10))
        self.password_entry.pack(fill=tk.X, pady=(5, 20), ipady=6)

        login_btn = tk.Button(inner, text="LOGIN", bg=ACCENT_BLUE, fg=TEXT_PRIMARY, font=(
            "Arial", 9, "bold"), relief=tk.FLAT, cursor="hand2", command=self.handle_login)
        login_btn.pack(fill=tk.X, ipady=8, pady=(0, 10))

        switch_frame = tk.Frame(inner, bg=BG_PANEL)
        switch_frame.pack(pady=10)

        tk.Label(switch_frame, text="Don't have an account?", font=(
            "Arial", 9), fg=TEXT_MUTED, bg=BG_PANEL).pack(side=tk.LEFT)
        reg_link = tk.Label(switch_frame, text=" Register", font=(
            "Arial", 9, "bold"), fg=ACCENT_BLUE, bg=BG_PANEL, cursor="hand2")
        reg_link.pack(side=tk.LEFT)
        reg_link.bind("<Button-1>", lambda e: self.switch_to_register_cb())

    def handle_login(self):
        success, message, student_data = authenticate_student(
            self.username_entry.get(),
            self.password_entry.get()
        )
        if success:
            messagebox.showinfo("Success", message)
            self.on_login_success_cb(student_data)
        else:
            messagebox.showerror("Login Error", message)