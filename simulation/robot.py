class Robot:
    def __init__(self, x=1, y=1, direction="NORTH"):
        self.x = x
        self.y = y
        self.direction = direction  # NORTH, EAST, SOUTH, WEST
        self.directions = ["NORTH", "EAST", "SOUTH", "WEST"]

    def turn_right(self):
        curr_idx = self.directions.index(self.direction)
        self.direction = self.directions[(curr_idx + 1) % 4]

    def turn_left(self):
        curr_idx = self.directions.index(self.direction)
        self.direction = self.directions[(curr_idx - 1) % 4]

    def move_forward(self, env) -> bool:
        dx, dy = 0, 0
        if self.direction == "NORTH": dy = -1
        elif self.direction == "SOUTH": dy = 1
        elif self.direction == "EAST": dx = 1
        elif self.direction == "WEST": dx = -1

        new_x, new_y = self.x + dx, self.y + dy
        if env.is_valid_position(new_x, new_y):
            self.x, self.y = new_x, new_y
            return True
        return False

    def move_backward(self, env) -> bool:
        dx, dy = 0, 0
        if self.direction == "NORTH": dy = 1
        elif self.direction == "SOUTH": dy = -1
        elif self.direction == "EAST": dx = -1
        elif self.direction == "WEST": dx = 1

        new_x, new_y = self.x + dx, self.y + dy
        if env.is_valid_position(new_x, new_y):
            self.x, self.y = new_x, new_y
            return True
        return False

    def stop(self):
        pass

    def read_distance(self, env) -> int:
        """Calculates distance to nearest obstacle or boundary in current direction."""
        dist = 0
        curr_x, curr_y = self.x, self.y
        dx, dy = 0, 0
        if self.direction == "NORTH": dy = -1
        elif self.direction == "SOUTH": dy = 1
        elif self.direction == "EAST": dx = 1
        elif self.direction == "WEST": dx = -1

        while True:
            curr_x += dx
            curr_y += dy
            if not env.is_within_bounds(curr_x, curr_y) or env.has_obstacle(curr_x, curr_y):
                break
            dist += 1
        return dist

    def is_obstacle_detected(self, env) -> bool:
        return self.read_distance(env) <= 1