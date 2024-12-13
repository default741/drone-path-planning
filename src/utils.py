import numpy as np


class Utils:

    @staticmethod
    def manhattan_heuristic(point_a: list, point_b: list) -> int:
        return np.sum(np.abs(np.array(point_a) - np.array(point_b)))

    @staticmethod
    def eucledian_distance(point_a: list, point_b: list) -> float | int:
        return np.sqrt(np.pow(np.array(point_a) - np.array(point_b), 2))