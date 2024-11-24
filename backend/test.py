import numpy as np
import random


def initialize_grid(rows, cols):
    return [["#"] * cols for _ in range(rows)]

def generate_maze(grid, row, col):
    directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
    random.shuffle(directions)
    
    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < len(grid) and 0 <= new_col < len(grid[0]) and grid[new_row][new_col] == "#":
            grid[new_row - dr // 2][new_col - dc // 2] = " "
            grid[new_row][new_col] = " "
            generate_maze(grid, new_row, new_col)
            
rows = cols = 21
maze = initialize_grid(rows, cols)
generate_maze(maze, rows-2, cols-2)


maze[1][1] = "S"
maze[rows - 2][cols - 2] = "E"
for row in maze:
    print(" ".join(row))

alpha = 0.1  # Learning rate
gamma = 0.9  # Discount factor
epsilon = 0.1  # Exploration rate
episodes = 2000

# Actions: 0=Up, 1=Down, 2=Left, 3=Right
actions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
action_count = len(actions)


q_table = np.zeros((rows, cols, action_count))


def get_reward(state):
    r, c = state
    if maze[r][c] == "#":
        return -10
    elif (r, c) == (rows - 2, cols - 2):
        return 100
    return -1

def get_next_state(state, action):
    r, c = state
    dr, dc = actions[action]
    nr, nc = r + dr, c + dc
    if 0 <= nr < rows and 0 <= nc < cols:
        return (nr, nc)
    return state

for episode in range(episodes):
    state = (1, 1)
    while state != (rows - 2, cols - 2):
        if random.uniform(0, 1) < epsilon:
            action = random.randint(0, action_count - 1)
        else:
            action = np.argmax(q_table[state[0], state[1]])
        
        next_state = get_next_state(state, action)
        reward = get_reward(next_state)
        
        current_q = q_table[state[0], state[1], action]
        max_future_q = np.max(q_table[next_state[0], next_state[1]])
        new_q = current_q + alpha * (reward + gamma * max_future_q - current_q)
        q_table[state[0], state[1], action] = new_q
        
        state = next_state

# print("Trained Q-table:")
# print(q_table)

def run_path(q_table):
    state = (1, 1)
    path = [state]

    while state != (rows - 2, cols - 2):
        action = np.argmax(q_table[state[0], state[1]])
        next_state = get_next_state(state, action)

        if next_state == state:
            print("Stuck! No valid moves.")
            break

        path.append(next_state)
        state = next_state

    return path

optimal_path = run_path(q_table)
# print("Optimal Path:", optimal_path)

def display_path(path, maze):
    maze_copy = [row[:] for row in maze]
    for r, c in path:
        maze_copy[r][c] = "*"
    for row in maze_copy:
        print(" ".join(str(cell) if cell != "*" else "*" for cell in row))

# display_path(optimal_path, maze)
