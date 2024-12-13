import numpy as np

from src.drone_environment import DroneEnvironment
from src.drone_agent import DroneAgent
from src.filters import ParticleFilter
from src.path_searching import DynamicAStar
from src.utils import Utils

from tqdm import tqdm

np.random.seed(42)

def main(visualize: bool = True, drone_initial_position: tuple = None, goal_position: tuple = None, grid_size: int = None) -> bool:
    grid_size = grid_size if grid_size is not None else np.random.randint(low=10, high=30)
    sensing_range = np.random.randint(low=2, high=5)

    if drone_initial_position is not None and goal_position is not None:
        drone_object = DroneAgent(grid_size=grid_size,sensing_range=sensing_range)
    else:
        drone_object = DroneAgent(drone_initial_position=drone_initial_position, goal_position=goal_position,
                                  grid_size=grid_size,sensing_range=sensing_range)

    environment = DroneEnvironment(grid_size=grid_size, drone_initial_position=drone_object.get_initial_position(),
                                   goal_position=drone_object.get_goal_position())

    particle_filter = ParticleFilter(sensing_range=sensing_range)
    searching_algorithm = DynamicAStar(
        drone_agent=drone_object, environment=environment, particle_filter=particle_filter,
        heuristic_function=Utils.manhattan_heuristic)

    drone_path = searching_algorithm.compute_drone_path()

    if drone_path is not None:
        print(f"Path Found: {list(map(lambda x: (int(x[0]), int(x[1])), drone_path))}")

        if visualize:
            environment.create_environment(drone_path=drone_path)

        return True

    else:
        print(f"Path Not Found!")
        return False

def run_simulations() -> None:
    positive_results = 0
    negative_results = 0

    for _ in tqdm(range(100)):
        if main(visualize=False):
            positive_results += 1
        else:
            negative_results += 1

    print(f"Number of Positive Results: {positive_results}")


if __name__ == "__main__":
    NUM_SIMULATIONS = 100

    drone_initial_position = (1, 5)
    goal_position = (28, 27)
    grid_size = 30

    # main(drone_initial_position=drone_initial_position, goal_position=goal_position, grid_size=grid_size)

    # run_simulations()
