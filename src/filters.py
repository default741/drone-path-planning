import numpy as np
from src.drone_environment import DroneEnvironment


class ParticleFilter:

    def __init__(self, sensing_range: int = 0, num_particles: int = 25) -> None:
        self.sensing_range = sensing_range
        self.num_particles = num_particles

        print(f"Number of Particles for Particle Filter: {self.num_particles}")

    def __generate_particles(self, current_position: np.array, current_environment: DroneEnvironment) -> None:
        x_offsets = np.arange(-self.sensing_range, self.sensing_range + 1)
        y_offsets = np.arange(-self.sensing_range, self.sensing_range + 1)

        grid = np.array(np.meshgrid(x_offsets, y_offsets)).T.reshape(-1, 2)
        particles = grid + current_position

        if len(particles) > self.num_particles:
            indices = np.linspace(0, len(particles) - 1, num=self.num_particles, dtype=int)
            particles = particles[indices]

        particles = particles[(particles[:, 0] >= 0) & (particles[:, 1] >= 0) &
                              (particles[:, 0] < current_environment.grid_size) & (particles[:, 1] < current_environment.grid_size)]

        self.particles = particles

    def __compute_obstacle_probabilities(self, current_environment: DroneEnvironment) -> float:
        obstacle_probabilities = list()
        all_obstacles_positions = (current_environment.houses_positions +
                                   current_environment.trees_position +
                                   current_environment.dynamic_obstacles)

        for particle in self.particles:
            x, y = particle

            if [x, y] in (all_obstacles_positions):
                obstacle_probabilities.append(1.0)
            else:
                obstacle_probabilities.append(0.1)

        return np.mean(obstacle_probabilities)

    def detect_obstacle(self, current_position, updated_environment):
        self.__generate_particles(current_position, updated_environment)

        return self.__compute_obstacle_probabilities(updated_environment) > 0.5
