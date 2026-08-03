# Triangle Tic-Tac-Toe

A Python implementation of triangle tic-tac-toe with random and minimax-based AI players.

## Features

- Human vs. AI mode
- AI vs. AI simulation
- Three AI levels: `Random`, `Advanced`, and `FastAdvanced`
- Precomputed moves in `BestMoves.json` for faster gameplay

## Requirements

- Python 3
- No external dependencies

## Run

```bash
python TriangleTicTacToe.py
```

Use the letters shown in the board image below as the position inputs:

<img src="board.png" alt="Triangle Tic-Tac-Toe board positions" width="500">

By default, the game starts in Human vs. AI mode. During the first three rounds, enter only the letter (`a` to `i`) corresponding to the position where you want to place a new piece. From the fourth round onward, enter the letters corresponding to the current and new positions to move one of your pieces.

To change the game mode, edit the calls at the bottom of `TriangleTicTacToe.py`:

```python
HumanVsAi('FastAdvanced')
# AIvsAI('FastAdvanced', 'FastAdvanced')
```

## Files

- `TriangleTicTacToe.py` - game rules, players, AI, and game modes
- `Statistics.py` - generates precomputed best moves
- `BestMoves.json` - precomputed move database
- `Analysis.txt` - project analysis notes
- `board.png` - board reference showing the letter assigned to each position
