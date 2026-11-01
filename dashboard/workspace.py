import tkinter as tk
from tkinter import scrolledtext, messagebox
from database.db import save_code_submission, get_latest_saved_code

BG_MAIN = "#060b13"
BG_PANEL = "#091324"
BORDER_COLOR = "#1c3150"
TEXT_PRIMARY = "#ffffff"
TEXT_MUTED = "#94a3b8"
ACCENT_BLUE = "#0f5b96"
BG_DARK_INPUT = "#030914"


class WorkspaceFrame(tk.Frame):
    """Split-pane programming workspace (Code Editor | Robot Simulation Window Placeholder)[cite: 1, 2]."""

    def __init__(self, parent, student_data):
        super().__init__(parent, bg=BG_MAIN)
        self.student_data = student_data
        self.active_exercise_id = 1
        self.active_exercise_title = "Basic Robot Movement"
        self.active_instructions = "Learn how to move the robot forward and backward across grid cells using basic movement commands."
        self.active_difficulty = "Beginner"

        self.build_ui()
        self.load_exercise(self.active_exercise_id, self.active_exercise_title,
                           self.active_instructions, self.active_difficulty)

    def set_active_exercise(self, ex_id, title, instructions, difficulty):
        self.active_exercise_id = ex_id
        self.active_exercise_title = title
        self.active_instructions = instructions
        self.active_difficulty = difficulty
        self.load_exercise(ex_id, title, instructions, difficulty)

    def load_exercise(self, ex_id, title, instructions, difficulty):
        self.ex_title_label.config(
            text=f"EXERCISE #{ex_id}: {title.upper()} ({difficulty})")
        self.instructions_label.config(text=instructions)

        saved_code = get_latest_saved_code(
            self.student_data['student_id'], ex_id)
        self.code_editor.delete("1.0", tk.END)
        if saved_code:
            self.code_editor.insert(tk.END, saved_code)
        else:
            default_template = f"# Exercise #{ex_id}: {title}\n# Write your robot commands below:\n\nmove_forward()\n"
            self.code_editor.insert(tk.END, default_template)

    def build_ui(self):
        # Header Info Banner
        header = tk.Frame(
            self, bg=BG_PANEL, highlightbackground=BORDER_COLOR, highlightthickness=1)
        header.pack(fill=tk.X, padx=10, pady=(10, 5))

        header_inner = tk.Frame(header, bg=BG_PANEL)
        header_inner.pack(fill=tk.X, padx=10, pady=8)

        self.ex_title_label = tk.Label(header_inner, text="", font=(
            "Arial", 10, "bold"), fg=TEXT_PRIMARY, bg=BG_PANEL)
        self.ex_title_label.pack(anchor="w")

        self.instructions_label = tk.Label(header_inner, text="", font=(
            "Arial", 8), fg=TEXT_MUTED, bg=BG_PANEL, justify=tk.LEFT)
        self.instructions_label.pack(anchor="w", pady=(2, 0))

        # Split Pane Grid Container (Left: Editor | Right: Simulation Window Placeholder)
        pane_container = tk.Frame(self, bg=BG_MAIN)
        pane_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        pane_container.columnconfigure(0, weight=1)
        pane_container.columnconfigure(1, weight=1)
        pane_container.rowconfigure(0, weight=1)

        # --- LEFT SECTION: Code Editor ---
        left_frame = tk.Frame(pane_container, bg=BG_PANEL,
                              highlightbackground=BORDER_COLOR, highlightthickness=1)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))

        editor_header = tk.Frame(left_frame, bg="#03060a")
        editor_header.pack(fill=tk.X)
        tk.Label(editor_header, text="CODE EDITOR (PYTHON COMMANDS)", font=(
            "Courier", 9, "bold"), fg=TEXT_MUTED, bg="#03060a").pack(side=tk.LEFT, padx=10, pady=6)

        self.code_editor = scrolledtext.ScrolledText(
            left_frame, bg=BG_DARK_INPUT, fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY,
            relief=tk.FLAT, font=("Courier", 10), wrap=tk.NONE
        )
        self.code_editor.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Editor Control Buttons
        btn_bar = tk.Frame(left_frame, bg=BG_PANEL)
        btn_bar.pack(fill=tk.X, padx=5, pady=5)

        tk.Button(btn_bar, text="RUN CODE", bg="#10b981", fg=TEXT_PRIMARY, font=("Arial", 8, "bold"), relief=tk.FLAT,
                  cursor="hand2", command=self.handle_run).pack(side=tk.LEFT, padx=(0, 5), ipady=4, ipadx=10)
        tk.Button(btn_bar, text="SAVE CODE", bg=ACCENT_BLUE, fg=TEXT_PRIMARY, font=("Arial", 8, "bold"),
                  relief=tk.FLAT, cursor="hand2", command=self.handle_save).pack(side=tk.LEFT, padx=5, ipady=4, ipadx=10)
        tk.Button(btn_bar, text="CLEAR", bg="#9e121b", fg=TEXT_PRIMARY, font=("Arial", 8, "bold"),
                  relief=tk.FLAT, cursor="hand2", command=self.handle_clear).pack(side=tk.RIGHT, ipady=4, ipadx=10)

        # --- RIGHT SECTION: Robot Simulation Window ---
        right_frame = tk.Frame(pane_container, bg=BG_PANEL,
                               highlightbackground=BORDER_COLOR, highlightthickness=1)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))

        sim_header = tk.Frame(right_frame, bg="#03060a")
        sim_header.pack(fill=tk.X)
        tk.Label(sim_header, text="ROBOT SIMULATION WINDOW (2D GRID)", font=(
            "Courier", 9, "bold"), fg=TEXT_MUTED, bg="#03060a").pack(side=tk.LEFT, padx=10, pady=6)

        sim_placeholder = tk.Frame(
            right_frame, bg="#03060a", highlightbackground=BORDER_COLOR, highlightthickness=1)
        sim_placeholder.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(
            sim_placeholder,
            text="[ 2D PYGAME SIMULATION CANVAS PLACEHOLDER ]\n\nExecution engine and Pygame rendering window\nwill connect in Phase 3.",
            font=("Courier", 9), fg=TEXT_MUTED, bg="#03060a", justify=tk.CENTER
        ).pack(expand=True)

        # Execution Feedback Output Console
        console_frame = tk.Frame(
            right_frame, bg="#03060a", highlightbackground=BORDER_COLOR, highlightthickness=1)
        console_frame.pack(fill=tk.X, padx=10, pady=(0, 10), ipady=5)

        tk.Label(console_frame, text="TERMINAL / FEEDBACK LOG", font=("Courier", 8,
                 "bold"), fg=TEXT_MUTED, bg="#03060a").pack(anchor="w", padx=8, pady=(4, 2))
        self.terminal_log = tk.Label(console_frame, text="System Ready. Editor linked to SQLite DB.", font=(
            "Courier", 8), fg="#10b981", bg="#03060a", anchor="w")
        self.terminal_log.pack(fill=tk.X, padx=8, pady=(0, 4))

    def handle_save(self):
        code = self.code_editor.get("1.0", tk.END).strip()
        save_code_submission(
            self.student_data['student_id'], self.active_exercise_id, code, "Saved", "Code saved to database.")
        self.terminal_log.config(
            text=f"Code for Exercise #{self.active_exercise_id} saved successfully.", fg="#10b981")
        messagebox.showinfo(
            "Saved", "Your code submission has been saved to the database.")

    def handle_clear(self):
        self.code_editor.delete("1.0", tk.END)
        self.terminal_log.config(text="Editor cleared.", fg=TEXT_MUTED)

    def handle_run(self):
        self.terminal_log.config(
            text="Simulation execution triggers in Phase 3. Code saved automatically.", fg="#f59e0b")
        self.handle_save()