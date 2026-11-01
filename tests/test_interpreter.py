from simulation.environment import Environment
from simulation.robot import Robot
from interpreter.executor import CommandExecutor
from interpreter.parser import CommandParser
from interpreter.validator import validate_code
import unittest
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


class TestInterpreter(unittest.TestCase):
    def test_code_validator(self):
        valid_code = "move_forward()\nturn_right()\nread_distance()"
        is_val, _ = validate_code(valid_code)
        self.assertTrue(is_val)

        # Forbidden keyword security check
        malicious_code = "import os\nos.system('dir')"
        is_val_mal, _ = validate_code(malicious_code)
        self.assertFalse(is_val_mal)

    def test_parser_and_executor(self):
        code = "move_forward()\nturn_right()\nrepeat(2):\n    move_forward()"
        parser = CommandParser(code)
        tokens = parser.parse()
        self.assertGreater(len(tokens), 0)

        env = Environment(10, 10)
        robot = Robot(1, 1, "EAST")
        executor = CommandExecutor(robot, env)
        success, logs = executor.execute(tokens)

        self.assertTrue(success)
        self.assertGreater(len(logs), 0)


if __name__ == "__main__":
    unittest.main()