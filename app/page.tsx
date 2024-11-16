"use client"

import { useState, useEffect } from "react";
import { Difficulty, GridData } from "@/app/types/maze";
import Maze from "@/app/components/Maze";

export default function Home() {
  const [difficulty, setDifficulty] = useState<Difficulty>("MEDIUM");
  const [grid, setGrid] = useState<GridData | null>(null);

  useEffect(() => {
    const fetchMaze = async () => {
      const response = await fetch(`http://127.0.0.1:5000/new_maze?difficulty=${difficulty}`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
      });

      const gridData: GridData = await response.json();
      setGrid(gridData);
    };

    fetchMaze();
  }, [difficulty]);

  return (
    <div className="flex flex-col justify-center">
      <div className="flex justify-center gap-4">
        <button className={`text-xl px-4 py-2 ${difficulty === "EASY" ? "bg-neutral-500" : ""}`} onClick={() => setDifficulty("EASY")}>Easy</button>
        <button className={`text-xl px-4 py-2 ${difficulty === "MEDIUM" ? "bg-neutral-500" : ""}`} onClick={() => setDifficulty("MEDIUM")}>Medium</button>
        <button className={`text-xl px-4 py-2 ${difficulty === "HARD" ? "bg-neutral-500" : ""}`} onClick={() => setDifficulty("HARD")}>Hard</button>
      </div>

      {grid ? (
        <Maze grid={grid} difficulty={difficulty} />
      ) : (
        <p>Loading maze...</p>
      )}
    </div>
  );
}
