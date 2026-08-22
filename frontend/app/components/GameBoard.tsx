import styles from "./GameBoard.module.css";

type Position = {
  id: string;
  x: number;
  y: number;
};

const positions: Position[] = [
  { id: "a", x: 300, y: 42 },
  { id: "b", x: 540, y: 500 },
  { id: "c", x: 60, y: 500 },
  { id: "d", x: 466.351, y: 359.452 },
  { id: "e", x: 219.685, y: 500 },
  { id: "f", x: 228.743, y: 177.982 },
  { id: "g", x: 373.378, y: 327.618 },
  { id: "h", x: 290.885, y: 420.142 },
  { id: "i", x: 256.908, y: 287.737 },
];

const connections: [string, string][] = [
  ["a", "d"], ["a", "f"], ["a", "i"],
  ["b", "d"], ["b", "e"], ["b", "g"],
  ["c", "e"], ["c", "f"], ["c", "h"],
  ["d", "g"], ["d", "h"], ["e", "h"],
  ["e", "i"], ["f", "g"], ["f", "i"],
  ["g", "h"], ["g", "i"], ["h", "i"],
];

const byId = Object.fromEntries(positions.map((position) => [position.id, position]));

function BoardPosition({ id, x, y }: Position) {
  return (
    <g className={styles.position} aria-label={`${id}, open point`}>
      <circle className={styles.empty} cx={x} cy={y} r="23" />
      <text className={styles.label} x={x} y={y + 1}>
        {id.toUpperCase()}
      </text>
    </g>
  );
}

export function GameBoard() {
  return (
    <div className={styles.boardFrame}>
      <svg
        className={styles.board}
        viewBox="0 0 600 550"
        role="img"
        aria-labelledby="board-title board-description"
      >
        <title id="board-title">Triangle Tic-Tac-Toe board</title>
        <desc id="board-description">
          Nine empty labeled points connected by eighteen lines.
        </desc>

        <g className={styles.connections} aria-hidden="true">
          {connections.map(([from, to]) => (
            <line
              key={`${from}-${to}`}
              x1={byId[from].x}
              y1={byId[from].y}
              x2={byId[to].x}
              y2={byId[to].y}
            />
          ))}
        </g>

        {positions.map((position) => (
          <BoardPosition key={position.id} {...position} />
        ))}
      </svg>
    </div>
  );
}
