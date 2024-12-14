# Drone Path Planning with Dynamic Obstacles

___Disclaimer - The whole code is written by us from scratch. We have only used the libraries like NumPy's and Matplotlib's documentation as a references for function's use cases. We did use ChatGPT for conceptual understanding of Particle Filters as we were stuck why is it not detecting obstacles.___

## Overview

The goal of this project is to create a navigation system for drones that allows them to travel safely and efficiently from their starting point to their destination, even in environments that are constantly changing. This involves designing an intelligent algorithm that enables the drone to autonomously find its path while avoiding obstacles that might move or appear suddenly.

---

## Software and Hardware Requirements

- **Python Version**: Python 3.11.10
- **Hardware**: A standard working laptop is sufficient.

No external data sources are needed, but the images provided in the `Assets` folder are essential for the code to run properly.

---

## Motivation for the Project

Drones are increasingly used for tasks like deliveries, surveillance, and rescue missions. However, real-world environments often include dynamic challenges, such as moving vehicles, people, or other drones. These conditions make it difficult for drones to plan a safe and efficient path.

Many existing algorithms, like the basic A* pathfinding algorithm, work well in static environments but fail in dynamic and uncertain situations. To overcome this limitation, we combined the **Dynamic A* (D*) algorithm** with a **particle filter**:

- **Dynamic A* (D*)**: Extends A* to dynamically update paths in response to changes in the environment.
- **Particle Filter**: Estimates the position and movement of obstacles, helping the drone adapt proactively to its surroundings.

This combination ensures adaptability, efficiency, and robustness in navigating complex and changing environments.

---

## Why This Approach Is Better

Our approach addresses the shortcomings of current methods in drone path planning:

1. **Handling Dynamic Environments**:
   D* allows the drone to update its path in real time as obstacles move or new ones appear.

2. **Efficiency**:
   Unlike computationally expensive approaches (e.g., reinforcement learning or deep learning), D* with particle filters balances real-time performance with computational efficiency.

3. **Robustness**:
   Combining D* with probabilistic estimates from particle filters ensures the drone handles unexpected changes more reliably than reactive or traditional algorithms.

4. **Real-Time Adaptation**:
   This approach recalculates paths dynamically, unlike pre-computed or slow-to-update methods, enabling safe and efficient navigation.

---

## Accomplishments

1. **D* Algorithm Implementation**: Enables real-time path recalculations.
2. **Particle Filter Integration**: Predicts nearby dynamic obstacles effectively.
3. **Visualization Tool**: Provides a GUI to visualize drone navigation in real time.

---

## Measure of Success

- The **D* algorithm** successfully recalculates paths when encountering dynamic obstacles.
- The **particle filter** accurately predicts nearby obstacles in most cases.
- After running the code 100 times:
  - The optimal path was found **52 times**, indicating a strong foundation but with room for improvement.

---

## Areas for Improvement

While the system works efficiently, the particle filter occasionally struggles to detect obstacles accurately. Improving its prediction accuracy would further enhance navigation reliability.

---

## How to Execute the Code

1. **Download the Repository**: Clone or download the repository to your local machine.
2. **Set Up a Python Environment**:
   Create a new Python environment with version 3.11.x.
3. **Install Dependencies**:
   Install the required packages using the `requirements.txt` file:
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the Code**:
   - Open the ```drone_path_planning.py``` file.
   - For a single simulation, uncomment the ```main()``` function. This will visually show how the drone finds its path.
   - To run multiple simulations, set the ```NUM_SIMULATIONS``` variable to the desired number and uncomment the ```run_simulation()``` function.
   - Execute the code by running:
        ```python
        python drone_path_planning.py
        ```

---

## Conclusion

This project demonstrates a practical solution for drone navigation in dynamic environments. By integrating D* and particle filters, we provide a system that adapts to uncertainties while maintaining efficiency. Future enhancements in obstacle prediction could make the approach even more robust and reliable.

---

## References
1. To Understand D* Algorithm - https://www.cs.cmu.edu/~motionplanning/lecture/AppH-astar-dstar_howie.pdf
2. To Understand Particle Filters -
   - https://medium.com/@mathiasmantelli/particle-filter-part-1-introduction-fb6954bc12ec
   - https://medium.com/@mathiasmantelli/particle-filter-part-2-intuitive-example-and-equations-0716223b862b
3. To Understand what drone path planning means - https://arxiv.org/pdf/2006.04103 (After reading this research paper we chucked everything and just did the whole project from our own intuition.)