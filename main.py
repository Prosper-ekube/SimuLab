from authentication.register import RegisterFrame
from authentication.login import LoginFrame
from database.db import initialize_database
import sys
import os
import tkinter as tk

sys.path.append(os.path.dirname(__file__))

class SimuLabApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SimuLab - Authentication")
        self.root.geometry("450x550")
        self.root.configure(bg="#060b13")
        self.root.resizable(False, False)

        self.current_frame = None
        self.show_login()

    def show_login(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = LoginFrame(
            self.root, self.show_register, self.on_login_success)
        self.current_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    def show_register(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = RegisterFrame(self.root, self.show_login)
        self.current_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    def on_login_success(self, student_data):
        print(
            f"Logged in successfully as: {student_data['full_name']} ({student_data['username']})")    
        self.root.destroy()


def main():
    initialize_database()
    root = tk.Tk()
    app = SimuLabApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()