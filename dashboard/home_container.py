import tkinter as tk
from dashboard.home import HomeFrame
from dashboard.workspace import WorkspaceFrame
from dashboard.exercises import ExercisesFrame
from dashboard.progress import ProgressFrame

BG_MAIN = "#060b13"
BG_PANEL = "#091324"
BORDER_COLOR = "#1c3150"
TEXT_PRIMARY = "#ffffff"
TEXT_MUTED = "#94a3b8"
ACCENT_BLUE = "#0f5b96"

class DashboardWindow(tk.Frame):
    """Main student dashboard navigation wrapper[cite: 1, 2]."""
    def __init__(self, parent, student_data, logout_cb):
        super().__init__(parent, bg=BG_MAIN)
        self.parent = parent
        self.student_data = student_data
        self.logout_cb = logout_cb
        
        self.parent.title(f"SimuLab - Dashboard [{self.student_data['full_name']}]")
        self.parent.geometry("1100x680")
        self.parent.configure(bg=BG_MAIN)
        
        self.build_ui()
        self.switch_tab("Home")

    def build_ui(self):
        # Top Navigation Bar
        nav_bar = tk.Frame(self, bg=BG_PANEL, highlightbackground=BORDER_COLOR, highlightthickness=1)
        nav_bar.pack(fill=tk.X)
        
        # Brand Tag
        brand_frame = tk.Frame(nav_bar, bg=BG_PANEL)
        brand_frame.pack(side=tk.LEFT, padx=15, pady=8)
        
        tk.Label(brand_frame, text="SimuLab", font=("Georgia", 14, "bold"), fg=TEXT_PRIMARY, bg=BG_PANEL).pack(side=tk.LEFT)
        tk.Label(brand_frame, text=" | IDE Workspace", font=("Arial", 9), fg=TEXT_MUTED, bg=BG_PANEL).pack(side=tk.LEFT)

        # Tab Navigation Buttons
        self.tabs = {}
        tab_names = ["Home", "Programming Workspace", "Exercises", "Progress"]
        
        tab_btn_frame = tk.Frame(nav_bar, bg=BG_PANEL)
        tab_btn_frame.pack(side=tk.LEFT, padx=20)
        
        for name in tab_names:
            btn = tk.Button(
                tab_btn_frame, text=name.upper(), font=("Arial", 8, "bold"),
                bg=BG_PANEL, fg=TEXT_MUTED, relief=tk.FLAT, cursor="hand2",
                command=lambda n=name: self.switch_tab(n)
            )
            btn.pack(side=tk.LEFT, padx=2, ipady=8, ipadx=10)
            self.tabs[name] = btn

        # Logout Button
        logout_btn = tk.Button(
            nav_bar, text="LOGOUT", bg="#9e121b", fg=TEXT_PRIMARY, 
            font=("Arial", 8, "bold"), relief=tk.FLAT, cursor="hand2", 
            command=self.logout_cb
        )
        logout_btn.pack(side=tk.RIGHT, padx=15, ipady=4, ipadx=10)

        # Dynamic Content View Area
        self.content_area = tk.Frame(self, bg=BG_MAIN)
        self.content_area.pack(fill=tk.BOTH, expand=True)

        # Initialize Workspace view instance so state persists across tab switches
        self.workspace_view = WorkspaceFrame(self.content_area, self.student_data)

    def switch_tab(self, tab_name):
        # Reset tab button highlights
        for name, btn in self.tabs.items():
            if name == tab_name:
                btn.config(bg=ACCENT_BLUE, fg=TEXT_PRIMARY)
            else:
                btn.config(bg=BG_PANEL, fg=TEXT_MUTED)

        # Clear active content area
        for widget in self.content_area.winfo_children():
            widget.pack_forget()

        # Render selected tab
        if tab_name == "Home":
            view = HomeFrame(self.content_area, self.student_data, self.switch_tab)
            view.pack(fill=tk.BOTH, expand=True)
        elif tab_name == "Programming Workspace":
            self.workspace_view.pack(fill=tk.BOTH, expand=True)
        elif tab_name == "Exercises":
            view = ExercisesFrame(self.content_area, self.student_data, self.open_exercise_in_workspace)
            view.pack(fill=tk.BOTH, expand=True)
        elif tab_name == "Progress":
            view = ProgressFrame(self.content_area, self.student_data)
            view.pack(fill=tk.BOTH, expand=True)

    def open_exercise_in_workspace(self, ex_id, title, instructions, difficulty):
        self.workspace_view.set_active_exercise(ex_id, title, instructions, difficulty)
        self.switch_tab("Programming Workspace")