# SimuLab

## Human–Robot Interaction System for Basic Robotics Programming Task Execution

**SimuLab** is a desktop-based Human–Robot Interaction (HRI) learning environment designed for undergraduate students in Enugu State. It provides a structured, immersive platform for learning basic robotics programming concepts through a simulated 2D robot environment, a secure authentication system, and an integrated progress tracker.

---

### Project Aesthetic & Design ("Dark IDE")

The application mimics a professional desktop Integrated Development Environment (IDE) like VS Code. It features a serious, academic, and information-dense dark theme (`#060b13` background) with sharp corners, monospace code editors, and high-contrast telemetry panels. The brand name **SimuLab** utilizes _Playfair Display_ to establish an academic, premium feel.

---

### Core Technology Stack

The project is built entirely in **Python**, avoiding unnecessary web or external backend servers:

- **Language:** Python 3.13.14
- **GUI Framework:** Tkinter / ttk
- **Simulation Engine:** Pygame (2D grid environment)
- **Database:** SQLite (`sqlite3`)
- **Security:** Python `hashlib` & `secrets` (salted password hashing)
- **Distribution:** PyInstaller (Standalone Windows `.exe`)

---

### Project Directory Structure

```text
hri-system/
│
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── database/
│   ├── db.py
│   └── schema.sql
│
├── authentication/
│   ├── login.py
│   └── register.py
│
├── dashboard/
│   ├── home.py
│   ├── workspace.py
│   ├── exercises.py
│   └── progress.py
│
├── simulation/
│   ├── robot.py
│   ├── environment.py
│   └── sensors.py
│   └── renderer.py
│
├── interpreter/
│   ├── parser.py
│   ├── executor.py
│   └── validator.py
│
├── tests/
│   ├── test_auth.py
│   ├── test_database.py
│   ├── test_interpreter.py
│   └── test_simulation.py
│
├── assets/
│   ├── images/
│   └── icons/
│
└── data/
    └── hri_system.db
```
