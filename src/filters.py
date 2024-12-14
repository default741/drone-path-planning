import numpy as np
from src.drone_environment import DroneEnvironment

class ParticleFilter:

    def __init__(self, sensing_range: int = 5, num_particles: int = 100) -> None:
        self.sensing_range = sensing_range
        self.num_particles = num_particles
        self.particles = np.empty((0, 2), dtype=int)

        # print(f"Particle Filter initialized with {self.num_particles} particles and sensing range {self.sensing_range}.")

    def __generate_particles(self, current_position: np.array, current_environment: DroneEnvironment) -> None:
        x_offsets = np.random.randint(-self.sensing_range, self.sensing_range + 1, size=self.num_particles)
        y_offsets = np.random.randint(-self.sensing_range, self.sensing_range + 1, size=self.num_particles)

        particles = np.column_stack((x_offsets, y_offsets)) + current_position

        particles = particles[(particles[:, 0] >= 0) & (particles[:, 1] >= 0) &
                              (particles[:, 0] < current_environment.grid_size) & (particles[:, 1] < current_environment.grid_size)]

        self.particles = particles

    def __compute_obstacle_probabilities(self, current_environment: DroneEnvironment) -> float:
        obstacle_probabilities = []
        all_obstacles_positions = (current_environment.houses_positions +
                                    current_environment.trees_position +
                                    current_environment.dynamic_obstacles)

        for particle in self.particles:
            if list(particle) in all_obstacles_positions:
                obstacle_probabilities.append(1.0)
            else:
                obstacle_probabilities.append(0.0)

        return np.mean(obstacle_probabilities) if obstacle_probabilities else 0.0

    def update_particles(self, current_position: np.array, movement: np.array, updated_environment: DroneEnvironment) -> None:
        if len(self.particles) == 0:
            self.__generate_particles(current_position, updated_environment)
            return

        self.particles += movement
        self.particles = self.particles[(self.particles[:, 0] >= 0) & (self.particles[:, 1] >= 0) &
                                        (self.particles[:, 0] < updated_environment.grid_size) &
                                        (self.particles[:, 1] < updated_environment.grid_size)]

        if len(self.particles) < self.num_particles // 2:
            self.__generate_particles(current_position, updated_environment)

    def detect_obstacle(self, current_position: np.array, updated_environment: DroneEnvironment) -> bool:
        obstacle_probability = self.__compute_obstacle_probabilities(updated_environment)
        # print(f"Obstacle probability at {current_position}: {obstacle_probability}")

        return obstacle_probability > 0.5