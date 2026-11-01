import re


class CommandParser:
    """Parses validated student code into structured instruction tokens, including loops and conditionals."""

    def __init__(self, code_text: str):
        self.code_text = code_text

    def parse(self) -> list:
        tokens = []
        lines = self.code_text.splitlines()

        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if not line or line.startswith("#"):
                i += 1
                continue

            # Handle repeat loops: repeat(n):
            if line.startswith("repeat("):
                match = re.match(r"repeat\((\d+)\):", line)
                if match:
                    count = int(match.group(1))
                    block_instructions = []
                    i += 1
                    while i < len(lines) and (lines[i].startswith("    ") or lines[i].startswith("\t")):
                        block_instructions.append(lines[i].strip())
                        i += 1
                    tokens.append(
                        {"type": "repeat", "count": count, "block": block_instructions})
                    continue

            # Handle if/else structures: if condition:
            if line.startswith("if "):
                match = re.match(r"if\s+(.+):", line)
                if match:
                    condition_expr = match.group(1).strip()
                    if_block = []
                    else_block = []
                    i += 1

                    # Collect IF block
                    while i < len(lines) and (lines[i].startswith("    ") or lines[i].startswith("\t")):
                        if_block.append(lines[i].strip())
                        i += 1

                    # Check for optional ELSE block
                    if i < len(lines) and lines[i].strip() in ("else:", "else :"):
                        i += 1
                        while i < len(lines) and (lines[i].startswith("    ") or lines[i].startswith("\t")):
                            else_block.append(lines[i].strip())
                            i += 1

                    tokens.append({
                        "type": "if_else",
                        "condition": condition_expr,
                        "if_block": if_block,
                        "else_block": else_block
                    })
                    continue

            tokens.append({"type": "command", "raw": line})
            i += 1

        return tokens