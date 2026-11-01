from dashboard.home_container import DashboardWindow
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
        self.student_data = None
        self.show_auth_window()

    def show_auth_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("SimuLab - Authentication")
        self.root.geometry("450x550")
        self.root.configure(bg="#060b13")
        self.root.resizable(False, False)

        self.current_frame = LoginFrame(
            self.root, self.show_register, self.on_login_success)
        self.current_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    def show_register(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.current_frame = RegisterFrame(self.root, self.show_auth_window)
        self.current_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    def on_login_success(self, student_data):
        self.student_data = student_data
        for widget in self.root.winfo_children():
            widget.destroy()

        # Launch Dashboard Window upon successful authentication[cite: 1]
        self.dashboard = DashboardWindow(
            self.root, self.student_data, self.show_auth_window)
        self.dashboard.pack(fill=tk.BOTH, expand=True)


def main():
    initialize_database()
    root = tk.Tk()
    app = SimuLabApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()