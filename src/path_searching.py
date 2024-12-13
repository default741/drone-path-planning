from queue import PriorityQueue

from src.drone_agent import DroneAgent
from src.drone_environment import DroneEnvironment
from src.filters import ParticleFilter


class DynamicAStar:

    def __init__(
        self, drone_agent: DroneAgent, environment: DroneEnvironment, particle_filter: ParticleFilter,
        heuristic_function: object) -> None:

        self.drone_agent = drone_agent
        self.environment = environment
        self.pfilter = particle_filter
        self.heuristic_function = heuristic_function

    def reconstruct_path(self, position_history, current_position):
        final_drone_path = list()

        while current_position in position_history:
            final_drone_path.append(current_position)
            current_position = position_history[current_position]

        final_drone_path.append(current_position)

        return final_drone_path[::-1]

    def compute_drone_path(self) -> list:
        drone_initial_position = tuple(self.drone_agent.get_initial_position())
        goal_position = tuple(self.drone_agent.get_goal_position())

        frontier_queue = PriorityQueue()
        frontier_queue.put((0, drone_initial_position))

        position_history = {}
        path_cost_score = {drone_initial_position: 0}
        total_cost_score = {drone_initial_position: self.heuristic_function(drone_initial_position, goal_position)}

        while not frontier_queue.empty():
            _, current_position = frontier_queue.get()

            if current_position == goal_position:
                return self.reconstruct_path(position_history=position_history, current_position=current_position)

            for neighbor in self.drone_agent.get_next_positions(current_position):
                if self.pfilter.detect_obstacle(neighbor, self.environment):
                    continue

                self.environment.update_particles_history(self.pfilter.particles)
                tentative_neighbour_path_cost = path_cost_score[current_position] + 1

                if neighbor not in path_cost_score or tentative_neighbour_path_cost < path_cost_score[neighbor]:
                    position_history[neighbor] = current_position
                    path_cost_score[neighbor] = tentative_neighbour_path_cost

                    total_cost_score[neighbor] = path_cost_score[neighbor] + self.heuristic_function(neighbor, goal_position)
                    frontier_queue.put((total_cost_score[neighbor], neighbor))

            self.environment.update_dynamic_obstacles()

        return None
