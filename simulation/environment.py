class Environment:
    def __init__(self, width=10, height=10):
        self.width = width
        self.height = height
        # Set obstacle coordinates (x, y)
        self.obstacles = {(4, 4), (4, 5), (7, 2)}

    def is_within_bounds(self, x, y) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def has_obstacle(self, x, y) -> bool:
        return (x, y) in self.obstacles

    def is_valid_position(self, x, y) -> bool:
        return self.is_within_bounds(x, y) and not self.has_obstacle(x, y)