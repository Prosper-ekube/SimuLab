import pygame

class SimulationRenderer:
    """Handles Pygame 2D grid rendering for the robot simulation."""
    def __init__(self, width=500, height=500, grid_size=10):
        pygame.init()
        self.width = width
        self.height = height
        self.grid_size = grid_size
        self.cell_size = width // grid_size
        self.screen = pygame.Surface((width, height))

    def render(self, robot, env) -> pygame.Surface:
        # Background color matching Dark IDE palette
        self.screen.fill((6, 11, 19))
        
        # Draw Grid Lines
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, (28, 49, 80), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, (28, 49, 80), (0, y), (self.width, y))

        # Draw Obstacles
        for ox, oy in env.obstacles:
            rect = pygame.Rect(ox * self.cell_size, oy * self.cell_size, self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, (158, 18, 27), rect)

        # Draw Robot
        rx = robot.x * self.cell_size + self.cell_size // 2
        ry = robot.y * self.cell_size + self.cell_size // 2
        pygame.draw.circle(self.screen, (15, 91, 150), (rx, ry), self.cell_size // 3)

        # Draw Robot Direction Indicator
        dx, dy = 0, 0
        if robot.direction == "NORTH": dy = -1
        elif robot.direction == "SOUTH": dy = 1
        elif robot.direction == "EAST": dx = 1
        elif robot.direction == "WEST": dx = -1
        
        end_x = rx + dx * (self.cell_size // 3)
        end_y = ry + dy * (self.cell_size // 3)
        pygame.draw.line(self.screen, (255, 255, 255), (rx, ry), (end_x, end_y), 3)

        return self.screen