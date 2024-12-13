from src.drone_environment import DroneEnvironment
from PIL import Image, ImageTk

import time

import tkinter as tk


class CreateEnvironment:

    def __init__(self, environment: DroneEnvironment) -> None:
        self.tk_images = dict()

    def __load_assets(self):
        asset_paths = {
            "road": "./assets/road.png",
            "drone": "./assets/drone.png",
            "goal": "./assets/goal.png",
            "house": "./assets/house.png",
            "tree": "./assets/tree.png",
            "bird": "./assets/bird.png",
        }

        cell_size = 30

        for key, path in asset_paths.items():
            image = Image.open(path).resize((cell_size, cell_size))
            self.tk_images[key] = ImageTk.PhotoImage(image)

    def run_environment(self) -> None:
        cell_size = 50  # Size of each grid cell in pixels
        canvas_size = self.grid_size * cell_size

        # Initialize Tkinter window
        root = tk.Tk()
        root.title("Drone Environment")
        canvas = tk.Canvas(root, width=canvas_size, height=canvas_size, bg="white")
        canvas.pack()

        self.__load_assets()


        # Draw the grid
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x1, y1 = j * cell_size, i * cell_size
                x2, y2 = x1 + cell_size, y1 + cell_size
                canvas.create_rectangle(x1, y1, x2, y2, outline="gray")

        # Draw assets
        def draw_assets():
            canvas.delete("asset")  # Clear all previous assets
            for x, y in self.roads_positions:
                draw_image(x, y, "road")

            for x, y in self.houses_positions:
                draw_image(x, y, "house")

            for x, y in self.trees_position:
                draw_image(x, y, "tree")

            for x, y in self.dynamic_obstacles:
                draw_image(x, y, "bird")

            dx, dy = self.drone_initial_position
            draw_image(dx, dy, "drone")

            gx, gy = self.goal_position
            draw_image(gx, gy, "goal")

            # Draw particles
            if self.particles and self.particle_weights:
                for (px, py), weight in zip(self.particles, self.particle_weights):
                    intensity = int(255 * weight)  # Scale weight to RGB intensity
                    color = f"#{intensity:02x}0000"  # Red shades
                    draw_circle(px, py, color, "particle")

        def draw_image(x, y, image_key):
            """
            Draw an image at the specified grid cell.
            """
            x1, y1 = y * cell_size, x * cell_size
            canvas.create_image(x1, y1, anchor=tk.NW, image=self.tk_images[image_key], tags=("asset", image_key))

        def draw_circle(x, y, color, tag):
            """
            Draw a circle representing a particle.
            """
            cx, cy = y * cell_size + cell_size // 2, x * cell_size + cell_size // 2
            radius = cell_size // 4
            canvas.create_oval(cx - radius, cy - radius, cx + radius, cy + radius, fill=color, tags=("asset", tag))

        # Update environment dynamically
        def update_environment():
            for _ in range(10):  # Simulate 10 timesteps
                self.update_dynamic_obstacles()
                draw_assets()
                root.update()  # Update the Tkinter window
                time.sleep(0.5)  # Pause for visualization

        # Start visualization
        draw_assets()
        root.after(100, update_environment)
        root.mainloop()
