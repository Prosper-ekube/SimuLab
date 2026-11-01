import tkinter as tk
from database.db import get_all_exercises_with_status, get_student_overall_progress

BG_MAIN = "#060b13"
BG_PANEL = "#091324"
BORDER_COLOR = "#1c3150"
TEXT_PRIMARY = "#ffffff"
TEXT_MUTED = "#94a3b8"

class ProgressFrame(tk.Frame):
    """Progress tracking section displaying completed exercises and overall performance scores[cite: 1, 2]."""
    def __init__(self, parent, student_data):
        super().__init__(parent, bg=BG_MAIN)
        self.student_data = student_data
        self.build_ui()

    def build_ui(self):
        header = tk.Frame(self, bg=BG_MAIN)
        header.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        tk.Label(header, text="STUDENT LEARNING PROGRESS", font=("Arial", 12, "bold"), fg=TEXT_PRIMARY, bg=BG_MAIN).pack(anchor="w")
        tk.Label(header, text=f"Performance summary and exercise completion history for {self.student_data['full_name']}[cite: 1].", font=("Arial", 9), fg=TEXT_MUTED, bg=BG_MAIN).pack(anchor="w")

        # Performance Summary Card
        stats = get_student_overall_progress(self.student_data['student_id'])
        
        summary = tk.Frame(self, bg=BG_PANEL, highlightbackground=BORDER_COLOR, highlightthickness=1)
        summary.pack(fill=tk.X, padx=20, pady=10)
        
        inner = tk.Frame(summary, bg=BG_PANEL)
        inner.pack(fill=tk.X, padx=15, pady=12)
        
        tk.Label(inner, text=f"Overall Completion: {stats['completed']} of {stats['total']} Exercises", font=("Arial", 10, "bold"), fg=TEXT_PRIMARY, bg=BG_PANEL).pack(anchor="w")
        
        # Progress Bar Representation
        progress_pct = (stats['completed'] / stats['total']) if stats['total'] > 0 else 0
        bar_bg = tk.Frame(inner, bg="#030914", height=12, highlightbackground=BORDER_COLOR, highlightthickness=1)
        bar_bg.pack(fill=tk.X, pady=8)
        
        fill_width = int(progress_pct * 400)
        fill_bar = tk.Frame(bar_bg, bg="#10b981", height=12, width=fill_width)
        fill_bar.pack(side=tk.LEFT)

        # History List
        history_label = tk.Label(self, text="EXERCISE BREAKDOWN", font=("Arial", 10, "bold"), fg=TEXT_PRIMARY, bg=BG_MAIN)
        history_label.pack(anchor="w", padx=20, pady=(10, 5))

        list_panel = tk.Frame(self, bg=BG_PANEL, highlightbackground=BORDER_COLOR, highlightthickness=1)
        list_panel.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        exercises = get_all_exercises_with_status(self.student_data['student_id'])
        for ex in exercises:
            ex_id, title, _, difficulty, status, score = ex
            
            row = tk.Frame(list_panel, bg=BG_PANEL)
            row.pack(fill=tk.X, padx=15, pady=6)
            
            tk.Label(row, text=f"#{ex_id} {title}", font=("Arial", 9), fg=TEXT_PRIMARY, bg=BG_PANEL, width=25, anchor="w").pack(side=tk.LEFT)
            tk.Label(row, text=f"[{difficulty}]", font=("Arial", 8, "italic"), fg=TEXT_MUTED, bg=BG_PANEL, width=15, anchor="w").pack(side=tk.LEFT)
            
            status_color = "#10b981" if status == "Completed" else ("#f59e0b" if status == "In Progress" else TEXT_MUTED)
            tk.Label(row, text=status, font=("Courier", 9, "bold"), fg=status_color, bg=BG_PANEL, width=15, anchor="w").pack(side=tk.LEFT)
            tk.Label(row, text=f"Score: {score}%", font=("Courier", 9), fg=TEXT_PRIMARY, bg=BG_PANEL).pack(side=tk.RIGHT)