import numpy as np

class DroneAgent:

    def __init__(
        self, drone_initial_position: tuple[int] = None, goal_position: tuple[int] = None, grid_size: int = 0,
        sensing_range: int = 0) -> None:

        self.grid_size = grid_size
        self.sensing_range = sensing_range

        print(f"Grid Shape: ({self.grid_size} x {self.grid_size})")

        # Initializing Drone
        if drone_initial_position is not None:
            self.drone_initial_position = np.array(drone_initial_position)
        else:
            self.drone_initial_position = np.random.randint(
                low=0, high=self.grid_size, size=2, dtype=np.int32)

        print(f"Drone's Initial Position: {tuple(self.drone_initial_position.tolist())}")

        # Initializing Goal
        if goal_position is not None:
            self.goal_position = np.array(goal_position)
        else:
            self.goal_position = np.random.randint(
                low=0, high=self.grid_size, size=2, dtype=np.int32)

        print(f"Destination Coordinates: {tuple(self.goal_position.tolist())}")

    def __get_possible_directions(self) -> list[tuple]:
        return [(0, 0), (0, 1), (0, -1), (1, 0), (-1, 0),
                (1, 1), (1, -1), (-1, 1), (-1, -1)]

    def get_initial_position(self) -> np.array:
        return self.drone_initial_position

    def get_goal_position(self) -> np.array:
        return self.goal_position

    def get_next_positions(self, current_position: list) -> list[tuple[int]]:
        neighbors = list()

        for dx, dy in self.__get_possible_directions():
            new_position_x, new_position_y = current_position[0] + dx, current_position[1] + dy

            if 0 < new_position_x < self.grid_size and 0 < new_position_y < self.grid_size:
                neighbors.append((new_position_x, new_position_y))

        return neighbors