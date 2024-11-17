import random
from flask import Flask, json, jsonify, request
from flask_cors import CORS
from algorithms import bfs


app = Flask(__name__)
CORS(app)

sizeMap = {
    "EASY": 21,
    "MEDIUM": 31,
    "HARD": 51
}

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

@app.route('/new_maze', methods=['GET'])
def new_maze():
    difficulty = request.args.get('difficulty')
    rows = cols = sizeMap[difficulty]
    maze = initialize_grid(rows, cols)
    generate_maze(maze, rows-2, cols-2)

    maze[1][1] = "S"
    maze[rows - 2][cols - 2] = "E"
    
    return jsonify(maze=maze)

@app.route('/solve_maze', methods=['GET'])
def solve_maze():
    maze = request.args.get('maze')
    maze = json.loads(maze)
    algorithm = request.args.get('algorithm')
    path = []

    if algorithm == "bfs":
        path, visited = bfs(maze)
        path.reverse()

    return jsonify(path=path, visited=visited)

if __name__ == '__main__':
    app.run(debug=True)