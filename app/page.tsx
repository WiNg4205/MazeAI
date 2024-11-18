"use client";

import { useState, useEffect, useCallback } from "react";
import { Difficulty, GridData } from "@/app/types/maze";
import Maze from "@/app/components/Maze";

export default function Home() {
  const [difficulty, setDifficulty] = useState<Difficulty>("MEDIUM");
  const [grid, setGrid] = useState<GridData | null>(null);
  const [solved, setSolved] = useState<boolean>(false);
  const [algorithm, setAlgorithm] = useState<string>("bfs");

  const changeDifficulty = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const value = event.target.value as Difficulty;
    setDifficulty(value);
  };

  const changeAlgorithm = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setAlgorithm(event.target.value);
  };

  const fetchMaze = useCallback(async () => {
    setSolved(false);
    const response = await fetch(`${process.env.NEXT_PUBLIC_MAZE}?difficulty=${difficulty}`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    });

    const data = await response.json();
    setGrid(data["maze"]);
  }, [difficulty]);

  useEffect(() => {
    fetchMaze();
  }, [fetchMaze]);

  const fetchSolution = async () => {
    if (solved) return;

    const response = await fetch(`${process.env.NEXT_PUBLIC_SOLVE}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ maze: grid, algorithm }),
    });

    const data = await response.json();
    const visited = data["visited"];
    const path = data["path"];
    setSolved(true);

    for (const [row, col] of visited.slice(1)) {
      setGrid((prevGrid) => {
        const grid = prevGrid || [];
        const newGrid = grid.map((r, i) =>
          i === row ? r.map((c, j) => (j === col ? "V" : c)) : r
        );
        return newGrid;
      });
      await new Promise((resolve) => setTimeout(resolve, 10));
    }

    for (const [row, col] of path.slice(1, -1)) {
      setGrid((prevGrid) => {
        const grid = prevGrid || [];
        const newGrid = grid.map((r, i) =>
          i === row ? r.map((c, j) => (j === col ? "P" : c)) : r
        );
        return newGrid;
      });
      await new Promise((resolve) => setTimeout(resolve, 10));
    }
  };

  const resetMaze = async () => {
    setSolved(false);
    setGrid(null);
    fetchMaze();
  };

  return (
    <div className="flex flex-col justify-center">
      <div className="flex justify-center flex-col mx-auto">
        <div className="flex justify-around my-2">
          <select className="text-black font-semibold rounded-sm" value={difficulty} onChange={changeDifficulty}>
            <option value="EASY">Easy</option>
            <option value="MEDIUM">Medium</option>
            <option value="HARD">Hard</option>
          </select>
        </div>
        {grid ? (
          <>
            <div className="flex justify-between w-full my-4">
              <select
                className="text-black font-semibold rounded-sm px-2"
                value={algorithm}
                onChange={changeAlgorithm}
              >
                <option value="bfs">Breadth-First Search (BFS)</option>
                <option value="dfs">Depth-First Search (DFS)</option>
                <option value="a_star">A* Search</option>
              </select>
              <button
                className="bg-blue-500 text-white px-4 py-2 rounded"
                onClick={() => fetchSolution()}
              >
                Solve with {algorithm.toUpperCase()}
              </button>
              <button
                className="bg-gray-500 text-white px-4 py-2 rounded"
                onClick={() => resetMaze()}
              >
                Reset
              </button>
            </div>
            <Maze grid={grid} difficulty={difficulty} />
          </>
        ) : (
          <div>Loading grid...</div>
        )}
      </div>
    </div>
  );
}
