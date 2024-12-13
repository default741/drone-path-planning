import numpy as np
import matplotlib.pyplot as plt


class DroneEnvironment:

    def __init__(self, grid_size: int = None, drone_initial_position: tuple[int] = None, goal_position: tuple[int] = None) -> None:
        self.BOUNDING_BOX_THRESHOLD = 1
        self.dynamic_obstacles_history = list()

        # Creating Grid Layout
        self.grid_size = grid_size
        self.grid_layout = np.zeros((self.grid_size, self.grid_size), dtype=np.int32)

        # Creating Roads, Buildings and Static Obstacles
        self.__get_roads_positions()
        self.__get_houses_positions()
        self.__get_tree_positions()
        self.__get_dynamic_obstacles()

        self.__update_grid_layout()

        self.dynamic_obstacles_history.append(self.dynamic_obstacles)

        # Get Image Assets
        self.__get_assets()

        # Initializing Drone and Goal Positions
        self.drone_position = np.array(drone_initial_position)
        self.goal_position = np.array(goal_position)

        # Particles History
        self.particles_history = list()

    def __get_roads_positions(self) -> None:
        roads_positions = set()

        vertical_roads = np.random.rand(self.grid_size) < 0.2
        horizontal_roads = np.random.rand(self.grid_size) < 0.2

        for i in range(self.grid_size):
            if vertical_roads[i]:
                roads_positions.update((i, j) for j in range(self.grid_size))
            if horizontal_roads[i]:
                roads_positions.update((j, i) for j in range(self.grid_size))

        self.roads_positions = list(map(lambda x: list(x), list(roads_positions)))

    def __get_houses_positions(self) -> None:
        NUM_HOUSES = np.random.randint(low=8, high=15)
        houses_positions = list()

        for _ in range(NUM_HOUSES):
            start_x, start_y = np.random.randint(0, self.grid_size), np.random.randint(0, self.grid_size)
            width, height = np.random.randint(2, 5), np.random.randint(2, 5)

            house = [(start_x + x, start_y + y) for x in range(height) for y in range(width)
                if (0 <= start_x + x < self.grid_size and 0 <= start_y + y < self.grid_size)
                and (start_x + x, start_y + y) not in self.roads_positions]

            if not any(coord in pos for pos in houses_positions for coord in house):
                houses_positions.extend(house)

        self.houses_positions = list(map(lambda x: list(x), list(houses_positions)))

    def __get_tree_positions(self):
        NUM_TREES = np.random.randint(low=10, high=15)
        trees_position = list()

        while len(trees_position) <= NUM_TREES:
            tree = list(np.random.randint(0, self.grid_size, size=2))

            if tree not in self.roads_positions and tree not in trees_position and tree not in self.houses_positions:
                trees_position.append(tree)

        self.trees_position = trees_position

    def __get_dynamic_obstacles(self) -> None:
        NUM_BIRDS = np.random.randint(low=5, high=10)
        dynamic_obstacles = list()

        while len(dynamic_obstacles) <= NUM_BIRDS:
            dynamic_object = list(np.random.randint(0, self.grid_size, size=2))

            if dynamic_object not in dynamic_obstacles:
                dynamic_obstacles.append(dynamic_object)

        self.dynamic_obstacles = dynamic_obstacles

    def __get_assets(self) -> None:
        self.image_assets = {'roads': plt.imread("./assets/road.png"),
                             'drone': plt.imread("./assets/drone.png"),
                             'goal': plt.imread("./assets/goal.png"),
                             'house': plt.imread("./assets/house.png"),
                             'tree': plt.imread("./assets/tree.png"),
                             'bird': plt.imread("./assets/bird.png")}

    def __update_grid_layout(self) -> None:
        all_obstacles_positions = self.houses_positions + self.trees_position + self.dynamic_obstacles

        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if [x, y] in all_obstacles_positions:
                    self.grid_layout[x, y] = 1

    def update_dynamic_obstacles(self) -> None:
        new_positions = list()

        for dynamic_object in self.dynamic_obstacles:
            new_position = np.array(dynamic_object) + np.random.choice([-1, 0, 1], size=2)
            new_position = list(np.clip(a=new_position, a_min=0, a_max=self.grid_size - 1))

            new_positions.append(new_position)

        self.dynamic_obstacles = new_positions
        self.dynamic_obstacles_history.append(self.dynamic_obstacles)

        self.__update_grid_layout()

    def update_particles_history(self, particles: list) -> None:
        self.particles_history.append(particles)

    def create_environment(self, drone_path: list) -> None:
        _, ax = plt.subplots(figsize=(8, 8))

        for time_step, new_position in enumerate(drone_path):
            ax.clear()
            ax.set_xlim(-1, self.grid_size + 1)
            ax.set_ylim(-1, self.grid_size + 1)

            for x in range(self.grid_size):
                for y in range(self.grid_size):
                    if [x, y] in self.roads_positions:
                        ax.imshow(self.image_assets['roads'], extent=(y, y + self.BOUNDING_BOX_THRESHOLD, x, x + self.BOUNDING_BOX_THRESHOLD))

                    elif [x, y] in self.houses_positions:
                        ax.imshow(self.image_assets['house'], extent=(y, y + self.BOUNDING_BOX_THRESHOLD, x, x + self.BOUNDING_BOX_THRESHOLD))

                    elif [x, y] in self.trees_position:
                        ax.imshow(self.image_assets['tree'], extent=(y, y + self.BOUNDING_BOX_THRESHOLD, x, x + self.BOUNDING_BOX_THRESHOLD))

                    if [x, y] in self.dynamic_obstacles_history[time_step]:
                        ax.imshow(self.image_assets['bird'], extent=(y, y + self.BOUNDING_BOX_THRESHOLD, x, x + self.BOUNDING_BOX_THRESHOLD))

            dx, dy = new_position
            gx, gy = self.goal_position.tolist()

            ax.imshow(self.image_assets['drone'], extent=(dy, dy + self.BOUNDING_BOX_THRESHOLD, dx, dx + self.BOUNDING_BOX_THRESHOLD))
            ax.imshow(self.image_assets['goal'], extent=(gy, gy + self.BOUNDING_BOX_THRESHOLD, gx, gx + self.BOUNDING_BOX_THRESHOLD))

            if len(self.particles_history) > 0:
                for (px, py) in self.particles_history[time_step]:
                    ax.scatter(py, px, color="red", s=5, alpha=0.7)

            plt.pause(0.5)

        plt.show()