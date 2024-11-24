from collections import deque
import heapq
import random
import numpy as np

from test import get_next_state, get_reward

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def bfs(maze): 
    q = deque()
    q.append((1, 1))
    visited = []
    parent = {}

    while q:
        cur = q.popleft()
        visited.append(cur)
        row, col = cur[0], cur[1]

        for dr, dc in DIRECTIONS:
            new_row, new_col = row + dr, col + dc
            next_pos = (new_row, new_col)

            if 0 <= new_row < len(maze) and 0 <= new_col < len(maze[0]):
                if maze[new_row][new_col] == "E":
                    parent[next_pos] = cur
                    return reconstruct_path(parent, (1, 1), next_pos), visited

                if maze[new_row][new_col] == " " and next_pos not in visited:
                    q.append(next_pos)
                    visited.append(next_pos)
                    parent[next_pos] = cur

def dfs(maze): 
    q = deque()
    q.append((1, 1))
    visited = []
    parent = {}
    
    while q:
        cur = q.popleft()
        visited.append(cur)
        row, col = cur[0], cur[1]

        for dr, dc in DIRECTIONS:
            new_row, new_col = row + dr, col + dc
            next_pos = (new_row, new_col)

            if 0 <= new_row < len(maze) and 0 <= new_col < len(maze[0]):
                if maze[new_row][new_col] == "E":
                    parent[next_pos] = cur
                    return reconstruct_path(parent, (1, 1), next_pos), visited

                if maze[new_row][new_col] == " " and next_pos not in visited:
                    q.appendleft(next_pos)
                    
                    parent[next_pos] = cur

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(maze):
    start = (1,1)
    end = (len(maze)-2, len(maze)-2)
    open_list = []
    visited = []
    heapq.heappush(open_list, (0 + heuristic(start, end), 0, start))
    parent = {}
    g_score = {start: 0}
    
    while open_list:
        _, g, current = heapq.heappop(open_list)
        visited.append(current)

        for dr, dc in DIRECTIONS:
            neighbor = (current[0] + dr, current[1] + dc)
            if maze[neighbor[0]][neighbor[1]] == "E":
                parent[neighbor] = current
                return reconstruct_path(parent, start, end), visited
            if (0 <= neighbor[0] < len(maze)) and (0 <= neighbor[1] < len(maze[0])) and maze[neighbor[0]][neighbor[1]] == " ":
                tentative_g_score = g + 1
                
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + heuristic(neighbor, end)
                    heapq.heappush(open_list, (f_score, tentative_g_score, neighbor))
                    parent[neighbor] = current
                    
def q_learning(maze):
    alpha = 0.1  # Learning rate
    gamma = 0.9  # Discount factor
    epsilon = 0.1  # Exploration rate
    episodes = 500
    rows = cols = len(maze)
    
    action_count = len(DIRECTIONS)
    q_table = np.zeros((rows, cols, action_count))
    
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
        
    return path, []
    

def reconstruct_path(parent, start, end):
    path = []
    current = end
    while current != start:
        path.append(current)
        current = parent[current]
    path.append(start)
    return path[::-1]
