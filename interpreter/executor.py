class CommandExecutor:
    """Executes parsed command tokens sequentially against the robot and simulation environment."""
    def __init__(self, robot, environment):
        self.robot = robot
        self.env = environment
        self.output_logs = []

    def execute(self, tokens: list) -> tuple[bool, list]:
        self.output_logs.clear()
        try:
            for token in tokens:
                success = self._process_token(token)
                if not success:
                    return False, self.output_logs
            return True, self.output_logs
        except Exception as e:
            self.output_logs.append(f"Execution Error: {str(e)}")
            return False, self.output_logs

    def _process_token(self, token: dict) -> bool:
        ttype = token["type"]
        
        if ttype == "command":
            res, msg = self._run_single_command(token["raw"])
            self.output_logs.append(msg)
            return res
            
        elif ttype == "repeat":
            for _ in range(token["count"]):
                for cmd_str in token["block"]:
                    res, msg = self._run_single_command(cmd_str)
                    self.output_logs.append(msg)
                    if not res:
                        return False
            return True
            
        elif ttype == "if_else":
            cond_value = self._evaluate_condition(token["condition"])
            target_block = token["if_block"] if cond_value else token["else_block"]
            self.output_logs.append(f"Evaluated condition '{token['condition']}' -> {cond_value}")
            for cmd_str in target_block:
                res, msg = self._run_single_command(cmd_str)
                self.output_logs.append(msg)
                if not res:
                    return False
            return True
            
        return True

    def _evaluate_condition(self, cond_str: str) -> bool:
        if "is_obstacle_detected()" in cond_str:
            return self.robot.is_obstacle_detected(self.env)
        elif "read_distance()" in cond_str:
            return self.robot.read_distance(self.env) > 0
        return False

    def _run_single_command(self, cmd_str: str) -> tuple[bool, str]:
        if cmd_str == "move_forward()":
            res = self.robot.move_forward(self.env)
            return res, f"move_forward() -> {'OK' if res else 'Blocked by wall/obstacle'}"
        elif cmd_str == "move_backward()":
            res = self.robot.move_backward(self.env)
            return res, f"move_backward() -> {'OK' if res else 'Blocked'}"
        elif cmd_str == "turn_left()":
            self.robot.turn_left()
            return True, "turn_left() -> Rotated 90° CCW"
        elif cmd_str == "turn_right()":
            self.robot.turn_right()
            return True, "turn_right() -> Rotated 90° CW"
        elif cmd_str == "stop()":
            self.robot.stop()
            return True, "stop() -> Robot stopped"
        elif "read_distance()" in cmd_str:
            dist = self.robot.read_distance(self.env)
            return True, f"read_distance() -> {dist} units"
        elif "is_obstacle_detected()" in cmd_str:
            detected = self.robot.is_obstacle_detected(self.env)
            return True, f"is_obstacle_detected() -> {detected}"
        else:
            return False, f"Unknown command: {cmd_str}"