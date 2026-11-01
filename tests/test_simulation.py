import unittest
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from simulation.robot import Robot
from simulation.environment import Environment

class TestSimulation(unittest.TestCase):
    def test_robot_turns(self):
        robot = Robot(1, 1, "NORTH")
        self.assertEqual(robot.direction, "NORTH")
        
        robot.turn_right()
        self.assertEqual(robot.direction, "EAST")
        
        robot.turn_right()
        self.assertEqual(robot.direction, "SOUTH")
        
        robot.turn_left()
        self.assertEqual(robot.direction, "EAST")

    def test_robot_movement_and_obstacles(self):
        env = Environment(10, 10)
        # Obstacle at (4, 4)
        robot = Robot(3, 4, "EAST") # Facing towards obstacle at (4, 4)
        
        # Should detect obstacle ahead
        self.assertTrue(robot.is_obstacle_detected(env))
        
        # Moving forward should be blocked by obstacle
        moved = robot.move_forward(env)
        self.assertFalse(moved)
        self.assertEqual(robot.x, 3)

        # Turn North where path is clear
        robot.direction = "NORTH"
        moved_north = robot.move_forward(env)
        self.assertTrue(moved_north)
        self.assertEqual(robot.y, 3)

if __name__ == "__main__":
    unittest.main()