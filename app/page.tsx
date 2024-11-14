type CellType = '#' | 'S' | 'E' | ' ';
type DataGrid = CellType[][];

export default async function Home() {
  const response = await fetch("http://127.0.0.1:5000/new_maze" as string, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' }
  });
  const data = await response.json();

  return (
    <div className="overflow-x-auto max-w-screen-lg mx-auto">
      <div className="grid grid-cols-31 max-w-max">
        {data.map((row: CellType[], rowIndex: number) =>
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
