import re

ALLOWED_COMMANDS = {
    "move_forward",
    "move_backward",
    "turn_left",
    "turn_right",
    "stop",
    "read_distance",
    "is_obstacle_detected"
}


def validate_code(code_text: str) -> tuple[bool, str]:
    """
    Validates that student code only contains permitted robotics commands,
    control structures (repeat, if, else), and blocks dangerous built-ins.
    """
    lines = code_text.splitlines()

    # Check for forbidden keywords or modules
    forbidden_patterns = [
        r"\bimport\b", r"\bexec\b", r"\beval\b", r"\bos\b",
        r"\bsys\b", r"\bsubprocess\b", r"\bopen\b", r"__"
    ]

    for line_num, line in enumerate(lines, 1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        # Check forbidden patterns
        for pattern in forbidden_patterns:
            if re.search(pattern, stripped):
                return False, f"Line {line_num}: Security violation - unsupported or restricted keyword '{stripped}'."

        # Check if line is a control structure or a function call
        if stripped.startswith("repeat(") or stripped.startswith("if ") or stripped.startswith("else:") or stripped == "else:":
            continue

        # Match function calls like command()
        match = re.match(r"^([a-zA-Z_][a-zA-Z0-9_]*)\s*\(.*\)$", stripped)
        if not match:
            return False, f"Line {line_num}: Syntax error or unsupported statement '{stripped}'."

        func_name = match.group(1)
        if func_name not in ALLOWED_COMMANDS:
            return False, f"Line {line_num}: Unsupported command '{func_name}()'."

    return True, "Code validation successful."