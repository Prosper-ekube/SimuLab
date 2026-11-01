import tkinter as tk
from tkinter import scrolledtext, messagebox
from PIL import Image, ImageTk
import pygame

from database.db import save_code_submission, get_latest_saved_code
from interpreter.validator import validate_code
from interpreter.parser import CommandParser
from interpreter.executor import CommandExecutor
from simulation.robot import Robot
from simulation.environment import Environment
from simulation.renderer import SimulationRenderer

BG_MAIN = "#060b13"
BG_PANEL = "#091324"
BORDER_COLOR = "#1c3150"
TEXT_PRIMARY = "#ffffff"
TEXT_MUTED = "#94a3b8"
ACCENT_BLUE = "#0f5b96"
BG_DARK_INPUT = "#030914"


class WorkspaceFrame(tk.Frame):
    """Integrated Workspace connecting code validation, execution, and 2D Pygame visual updates."""

    def __init__(self, parent, student_data):
        super().__init__(parent, bg=BG_MAIN)
        self.student_data = student_data
        self.active_exercise_id = 1
        self.active_exercise_title = "Basic Robot Movement"
        self.active_instructions = "Learn how to move the robot forward and backward across grid cells using basic movement commands."
        self.active_difficulty = "Beginner"

        # Initialize Simulation components
        self.env = Environment(width=10, height=10)
        self.robot = Robot(x=1, y=1, direction="EAST")
        self.renderer = SimulationRenderer(width=380, height=380, grid_size=10)

        self.build_ui()
        self.load_exercise(self.active_exercise_id, self.active_exercise_title,
                           self.active_instructions, self.active_difficulty)
        self.render_simulation()

    def set_active_exercise(self, ex_id, title, instructions, difficulty):
        self.active_exercise_id = ex_id
        self.active_exercise_title = title
        self.active_instructions = instructions
        self.active_difficulty = difficulty
        self.load_exercise(ex_id, title, instructions, difficulty)

    def reset_robot_state(self):
        """Reset robot position for exercise restart."""
        self.robot.x = 1
        self.robot.y = 1
        self.robot.direction = "EAST"
        self.render_simulation()

    def render_simulation(self):
        """Render Pygame surface into Tkinter image label."""
        surface = self.renderer.render(self.robot, self.env)
        raw_data = pygame.image.tostring(surface, "RGB")
        image = Image.frombytes("RGB", (380, 380), raw_data)
        photo = ImageTk.PhotoImage(image)
        self.sim_canvas_label.config(image=photo)
        self.sim_canvas_label.image = photo

    def load_exercise(self, ex_id, title, instructions, difficulty):
        self.ex_title_label.config(
            text=f"EXERCISE #{ex_id}: {title.upper()} ({difficulty})")
        self.instructions_label.config(text=instructions)
        self.reset_robot_state()

        saved_code = get_latest_saved_code(
            self.student_data['student_id'], ex_id)
        self.code_editor.delete("1.0", tk.END)
        if saved_code:
            self.code_editor.insert(tk.END, saved_code)
        else:
            default_template = f"# Exercise #{ex_id}: {title}\nmove_forward()\nturn_right()\nmove_forward()\n"
            self.code_editor.insert(tk.END, default_template)

    def build_ui(self):
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

        # Split Container
        pane_container = tk.Frame(self, bg=BG_MAIN)
        pane_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        pane_container.columnconfigure(0, weight=1)
        pane_container.columnconfigure(1, weight=1)
        pane_container.rowconfigure(0, weight=1)

        # --- LEFT PANEL: Editor ---
        left_frame = tk.Frame(pane_container, bg=BG_PANEL,
                              highlightbackground=BORDER_COLOR, highlightthickness=1)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))

        editor_header = tk.Frame(left_frame, bg="#03060a")
        editor_header.pack(fill=tk.X)
        tk.Label(editor_header, text="CODE EDITOR", font=("Courier", 9, "bold"),
                 fg=TEXT_MUTED, bg="#03060a").pack(side=tk.LEFT, padx=10, pady=6)

        self.code_editor = scrolledtext.ScrolledText(
            left_frame, bg=BG_DARK_INPUT, fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY,
            relief=tk.FLAT, font=("Courier", 10), wrap=tk.NONE
        )
        self.code_editor.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        btn_bar = tk.Frame(left_frame, bg=BG_PANEL)
        btn_bar.pack(fill=tk.X, padx=5, pady=5)

        tk.Button(btn_bar, text="RUN PROGRAM", bg="#10b981", fg=TEXT_PRIMARY, font=("Arial", 8, "bold"),
                  relief=tk.FLAT, cursor="hand2", command=self.handle_run).pack(side=tk.LEFT, padx=(0, 5), ipady=4, ipadx=10)
        tk.Button(btn_bar, text="SAVE CODE", bg=ACCENT_BLUE, fg=TEXT_PRIMARY, font=("Arial", 8, "bold"),
                  relief=tk.FLAT, cursor="hand2", command=self.handle_save).pack(side=tk.LEFT, padx=5, ipady=4, ipadx=10)
        tk.Button(btn_bar, text="RESET ROBOT", bg="#f59e0b", fg=TEXT_PRIMARY, font=("Arial", 8, "bold"),
                  relief=tk.FLAT, cursor="hand2", command=self.reset_robot_state).pack(side=tk.LEFT, padx=5, ipady=4, ipadx=8)
        tk.Button(btn_bar, text="CLEAR", bg="#9e121b", fg=TEXT_PRIMARY, font=("Arial", 8, "bold"),
                  relief=tk.FLAT, cursor="hand2", command=self.handle_clear).pack(side=tk.RIGHT, ipady=4, ipadx=10)

        # --- RIGHT PANEL: Pygame Grid Canvas & Feedback Log ---
        right_frame = tk.Frame(pane_container, bg=BG_PANEL,
                               highlightbackground=BORDER_COLOR, highlightthickness=1)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))

        sim_header = tk.Frame(right_frame, bg="#03060a")
        sim_header.pack(fill=tk.X)
        tk.Label(sim_header, text="2D ROBOT SIMULATION CANVAS", font=(
            "Courier", 9, "bold"), fg=TEXT_MUTED, bg="#03060a").pack(side=tk.LEFT, padx=10, pady=6)

        self.sim_canvas_label = tk.Label(right_frame, bg="#03060a")
        self.sim_canvas_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        console_frame = tk.Frame(
            right_frame, bg="#03060a", highlightbackground=BORDER_COLOR, highlightthickness=1)
        console_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        tk.Label(console_frame, text="EXECUTION LOG", font=("Courier", 8, "bold"),
                 fg=TEXT_MUTED, bg="#03060a").pack(anchor="w", padx=8, pady=(4, 2))

        self.log_box = scrolledtext.ScrolledText(
            console_frame, bg="#03060a", fg="#10b981", font=("Courier", 8), height=5, relief=tk.FLAT)
        self.log_box.pack(fill=tk.X, padx=5, pady=(0, 4))
        self.log_box.insert(
            tk.END, "System Ready. Interpreter and 2D Simulation linked.\n")

    def handle_save(self):
        code = self.code_editor.get("1.0", tk.END).strip()
        save_code_submission(
            self.student_data['student_id'], self.active_exercise_id, code, "Saved", "Code saved.")
        messagebox.showinfo(
            "Saved", "Your program has been saved to the database.")

    def handle_clear(self):
        self.code_editor.delete("1.0", tk.END)

    def handle_run(self):
        code = self.code_editor.get("1.0", tk.END).strip()
        if not code:
            return

        # 1. Validate Code
        is_valid, val_msg = validate_code(code)
        self.log_box.delete("1.0", tk.END)
        if not is_valid:
            self.log_box.insert(tk.END, f"[VALIDATION ERROR] {val_msg}\n")
            save_code_submission(
                self.student_data['student_id'], self.active_exercise_id, code, "Error", val_msg)
            return

        # 2. Parse Code
        parser = CommandParser(code)
        tokens = parser.parse()

        # 3. Execute Instructions
        executor = CommandExecutor(self.robot, self.env)
        success, logs = executor.execute(tokens)

        # 4. Update Simulation Canvas & Console
        self.render_simulation()
        for log in logs:
            self.log_box.insert(tk.END, f"> {log}\n")

        exec_status = "Success" if success else "Failed"
        save_code_submission(
            self.student_data['student_id'], self.active_exercise_id, code, exec_status, "\n".join(logs))
