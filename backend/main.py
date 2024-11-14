import random
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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
def new_grid():
    rows, cols = 31, 31
    maze = initialize_grid(rows, cols)
    maze[1][1] = " "
    generate_maze(maze, 1, 1)

    maze[1][1] = "S"
    maze[rows - 2][cols - 2] = "E"
    
    return jsonify(maze)

if __name__ == '__main__':
    app.run(debug=True)