"use client";

import { useState, useEffect, useCallback } from "react";
import { Difficulty, GridData } from "@/app/types/maze";
import Maze from "@/app/components/Maze";

export default function Home() {
  const [difficulty, setDifficulty] = useState<Difficulty>("MEDIUM");
  const [grid, setGrid] = useState<GridData | null>(null);
  const [solved, setSolved] = useState<boolean>(false);

  const fetchMaze = useCallback(async () => {
    setSolved(false);
    const response = await fetch(`${process.env.NEXT_PUBLIC_MAZE}?difficulty=${difficulty}`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' }
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
      body: JSON.stringify({ maze: grid, algorithm: "bfs" })
    });

    const data = await response.json();
    const visited = data["visited"];
    const path = data["path"];
    setSolved(true);
    for (const [row, col] of visited.slice(1)) {
      setGrid(prevGrid => {
        const grid = prevGrid || [];

        const newGrid = grid.map((r, i) =>
          i === row ? r.map((c, j) => (j === col ? "V" : c)) : r
        );
        return newGrid;
      });

      await new Promise(resolve => setTimeout(resolve, 10));
    }

    for (const [row, col] of path.slice(1, -1)) {
      setGrid(prevGrid => {
        const grid = prevGrid || [];

        const newGrid = grid.map((r, i) =>
          i === row ? r.map((c, j) => (j === col ? "P" : c)) : r
        );
        return newGrid;
      });

      await new Promise(resolve => setTimeout(resolve, 10));
    }

    
  };

  const resetMaze = async () => {
    setSolved(false);
    setGrid(null);
    fetchMaze();
  };

  return (
    <div className="flex flex-col justify-center">
      <div className="flex justify-center gap-4">
        <button
          className={`text-xl px-4 py-2 ${difficulty === "EASY" ? "bg-neutral-500" : ""}`}
          onClick={() => setDifficulty("EASY")}
        >
          Easy
        </button>
        <button
          className={`text-xl px-4 py-2 ${difficulty === "MEDIUM" ? "bg-neutral-500" : ""}`}
          onClick={() => setDifficulty("MEDIUM")}
        >
          Medium
        </button>
        <button
          className={`text-xl px-4 py-2 ${difficulty === "HARD" ? "bg-neutral-500" : ""}`}
          onClick={() => setDifficulty("HARD")}
        >
          Hard
        </button>
      </div>
      <div className="flex justify-center flex-col mx-auto">
        {grid ? <Maze grid={grid} difficulty={difficulty} /> : <div>Loading grid...</div>}
        {grid && <div className="flex justify-between w-full">
          <button onClick={() => fetchSolution()}>SOLVE</button>
          <button onClick={() => resetMaze()}>RESET</button>        
        </div>}
      </div>
    </div>
  );
}
