import tkinter as tk
from database.db import get_student_overall_progress

BG_MAIN = "#060b13"
BG_PANEL = "#091324"
BORDER_COLOR = "#1c3150"
TEXT_PRIMARY = "#ffffff"
TEXT_MUTED = "#94a3b8"
ACCENT_BLUE = "#0f5b96"


class HomeFrame(tk.Frame):
    """Dashboard Welcome / Home view displaying student details and summary metrics."""

    def __init__(self, parent, student_data, switch_tab_cb):
        super().__init__(parent, bg=BG_MAIN)
        self.student_data = student_data
        self.switch_tab_cb = switch_tab_cb
        self.build_ui()

    def build_ui(self):
        # Header Greeting
        header = tk.Frame(self, bg=BG_MAIN)
        header.pack(fill=tk.X, padx=20, pady=(20, 10))

        tk.Label(
            header, text=f"WELCOME BACK, {self.student_data['full_name'].upper()}",
            font=("Arial", 14, "bold"), fg=TEXT_PRIMARY, bg=BG_MAIN
        ).pack(anchor="w")

        tk.Label(
            header, text=f"Username: {self.student_data['username']} | Account ID: #{self.student_data['student_id']}",
            font=("Courier", 10), fg=TEXT_MUTED, bg=BG_MAIN
        ).pack(anchor="w", pady=(2, 0))

        # Metrics Panel Row
        stats = get_student_overall_progress(self.student_data['student_id'])

        metrics_frame = tk.Frame(self, bg=BG_MAIN)
        metrics_frame.pack(fill=tk.X, padx=20, pady=10)

        self.create_card(metrics_frame, "COMPLETED EXERCISES", f"{stats['completed']} / {stats['total']}", "#10b981").pack(
            side=tk.LEFT, expand=True, fill=tk.BOTH, padx=(0, 5))
        self.create_card(metrics_frame, "IN PROGRESS", f"{stats['in_progress']}", "#f59e0b").pack(
            side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5)
        self.create_card(metrics_frame, "AVERAGE SCORE", f"{stats['avg_score']}%", ACCENT_BLUE).pack(
            side=tk.LEFT, expand=True, fill=tk.BOTH, padx=(5, 0))

        # System Guidance Panel
        info_panel = tk.Frame(
            self, bg=BG_PANEL, highlightbackground=BORDER_COLOR, highlightthickness=1)
        info_panel.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)

        inner = tk.Frame(info_panel, bg=BG_PANEL)
        inner.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        tk.Label(inner, text="QUICK START GUIDE", font=("Arial", 11, "bold"),
                 fg=TEXT_PRIMARY, bg=BG_PANEL).pack(anchor="w", pady=(0, 10))

        guide_text = (
            "1. Navigate to the 'Exercises' tab to browse available robotics tasks.\n"
            "2. Select an exercise to view instructions and load it into your Workspace.\n"
            "3. Use the Workspace Code Editor to draft robot command instructions.\n"
            "4. Save your programs regularly to preserve your work in the system database[cite: 1]."
        )
        tk.Label(inner, text=guide_text, font=("Arial", 10), fg=TEXT_MUTED,
                 bg=BG_PANEL, justify=tk.LEFT).pack(anchor="w", pady=(0, 20))

        btn = tk.Button(
            inner, text="BROWSE EXERCISES", bg=ACCENT_BLUE, fg=TEXT_PRIMARY,
            font=("Arial", 9, "bold"), relief=tk.FLAT, cursor="hand2",
            command=lambda: self.switch_tab_cb("Exercises")
        )
        btn.pack(anchor="w", ipady=6, ipadx=15)

    def create_card(self, parent, title, value, color):
        card = tk.Frame(parent, bg=BG_PANEL,
                        highlightbackground=BORDER_COLOR, highlightthickness=1)
        inner = tk.Frame(card, bg=BG_PANEL)
        inner.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        tk.Label(inner, text=title, font=("Arial", 8, "bold"),
                 fg=TEXT_MUTED, bg=BG_PANEL).pack(anchor="w")
        tk.Label(inner, text=value, font=("Arial", 20, "bold"),
                 fg=color, bg=BG_PANEL).pack(anchor="w", pady=(5, 0))
        return card