import tkinter as tk
from tkinter import ttk
from database.db import get_all_exercises_with_status

BG_MAIN = "#060b13"
BG_PANEL = "#091324"
BORDER_COLOR = "#1c3150"
TEXT_PRIMARY = "#ffffff"
TEXT_MUTED = "#94a3b8"
ACCENT_BLUE = "#0f5b96"


class ExercisesFrame(tk.Frame):
    """Exercise list view allowing students to browse tasks and open them in Workspace."""

    def __init__(self, parent, student_data, open_exercise_cb):
        super().__init__(parent, bg=BG_MAIN)
        self.student_data = student_data
        self.open_exercise_cb = open_exercise_cb
        self.build_ui()

    def build_ui(self):
        header = tk.Frame(self, bg=BG_MAIN)
        header.pack(fill=tk.X, padx=20, pady=(20, 10))

        tk.Label(header, text="ROBOTICS PROGRAMMING EXERCISES", font=(
            "Arial", 12, "bold"), fg=TEXT_PRIMARY, bg=BG_MAIN).pack(anchor="w")
        tk.Label(header, text="Select a task to review instructions and start coding in the workspace[cite: 1].", font=(
            "Arial", 9), fg=TEXT_MUTED, bg=BG_MAIN).pack(anchor="w")

        # Scrollable Frame Container
        container = tk.Frame(self, bg=BG_MAIN)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        canvas = tk.Canvas(container, bg=BG_MAIN, highlightthickness=0)
        scrollbar = tk.Scrollbar(
            container, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=BG_MAIN)

        scroll_frame.bind("<Configure>", lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        exercises = get_all_exercises_with_status(
            self.student_data['student_id'])

        for ex in exercises:
            ex_id, title, instructions, difficulty, status, score = ex

            card = tk.Frame(scroll_frame, bg=BG_PANEL,
                            highlightbackground=BORDER_COLOR, highlightthickness=1)
            card.pack(fill=tk.X, pady=6, ipadx=10, ipady=5)

            # Card Top Row
            top_row = tk.Frame(card, bg=BG_PANEL)
            top_row.pack(fill=tk.X, padx=10, pady=(8, 2))

            tk.Label(top_row, text=f"EXERCISE #{ex_id}: {title.upper()}", font=(
                "Arial", 10, "bold"), fg=TEXT_PRIMARY, bg=BG_PANEL).pack(side=tk.LEFT)

            status_color = "#10b981" if status == "Completed" else (
                "#f59e0b" if status == "In Progress" else TEXT_MUTED)
            tk.Label(top_row, text=f"[{status.upper()}]", font=(
                "Courier", 9, "bold"), fg=status_color, bg=BG_PANEL).pack(side=tk.RIGHT)

            # Instructions Body
            tk.Label(card, text=instructions, font=("Arial", 9), fg=TEXT_MUTED, bg=BG_PANEL,
                     justify=tk.LEFT, wraplength=600).pack(anchor="w", padx=10, pady=(2, 8))

            # Bottom Action Bar
            bottom_row = tk.Frame(card, bg=BG_PANEL)
            bottom_row.pack(fill=tk.X, padx=10, pady=(0, 8))

            tk.Label(bottom_row, text=f"Difficulty: {difficulty}", font=(
                "Arial", 8, "italic"), fg=TEXT_MUTED, bg=BG_PANEL).pack(side=tk.LEFT)

            btn = tk.Button(
                bottom_row, text="OPEN IN WORKSPACE", bg=ACCENT_BLUE, fg=TEXT_PRIMARY,
                font=("Arial", 8, "bold"), relief=tk.FLAT, cursor="hand2",
                command=lambda e_id=ex_id, t=title, inst=instructions, diff=difficulty: self.open_exercise_cb(
                    e_id, t, inst, diff)
            )
            btn.pack(side=tk.RIGHT, ipady=3, ipadx=10)