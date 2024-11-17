from collections import deque

def bfs(maze): 
    q = deque()
    q.append((1, 1))
    visited = []
    visited.append((1, 1))
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
                    visited.append(next_pos)
                    parent[next_pos] = cur

def reconstruct_path(parent, start, end):
    path = []
    current = end
    while current != start:
        path.append(current)
        current = parent[current]
    path.append(start)
    return path[::-1]
