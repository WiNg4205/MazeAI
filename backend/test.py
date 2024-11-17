import random
from collections import deque


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

def print_maze(maze):
    for row in maze:
        print("".join(row))
        
def bfs(maze):   
    q = deque()
    q.append((1, 1))
    visited = set()
    visited.add((1, 1))
    parent = {}
    
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    while q:
        cur = q.popleft()
        row, col = cur[0], cur[1]

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            next_pos = (new_row, new_col)

            if 0 <= new_row < len(maze) and 0 <= new_col < len(maze[0]):
                if maze[new_row][new_col] == "E":
                    parent[next_pos] = cur
                    return reconstruct_path(parent, (1, 1), next_pos), visited

                if maze[new_row][new_col] == " " and next_pos not in visited:
                    q.append(next_pos)
                    visited.add(next_pos)
                    parent[next_pos] = cur

def reconstruct_path(parent, start, end):
    path = []
    current = end
    while current != start:
        path.append(current)
        current = parent[current]
    path.append(start)
    return path[::-1]



rows = cols = 21
maze = initialize_grid(rows, cols)
generate_maze(maze, rows-2, cols-2)

maze[1][1] = "S"
maze[rows - 2][cols - 2] = "E"



print_maze(maze)
print(bfs(maze)[0])
print(bfs(maze)[1])