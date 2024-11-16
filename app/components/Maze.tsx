"use client"

import { GridData, CellType, Difficulty } from "@/app/types/maze";

type Props = {
  grid: GridData;
  difficulty: Difficulty;
}

export default function Maze({ grid, difficulty }: Props) {
  const sizeMap = {
    EASY: 21,
    MEDIUM: 31,
    HARD: 51
  };

  if (!grid || grid.length !== sizeMap[difficulty]) {
    return <p>Loading maze...</p>;
  }

  return (
    <div className="max-w-screen-lg mx-auto">
      <div className={`grid grid-cols-${sizeMap[difficulty]} max-w-max`}>
        {grid.map((row: CellType[], rowIndex: number) =>
          row.map((cell: CellType, cellIndex: number) => (
            <div
              key={`${rowIndex}-${cellIndex}`}
              className={`size-6 flex items-center justify-center text-xs font-bold ${
                cell === '#' ? 'bg-gray-800 text-white' :
                cell === 'S' ? 'bg-green-500 text-white' :
                cell === 'E' ? 'bg-red-500 text-white' :
                'bg-white'
              }`}
            >
              {cell !== ' ' ? cell : ''}
            </div>
          ))
        )}
      </div>
    </div>
  );
}