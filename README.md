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

By default, the game starts in Human vs. AI mode. Enter `x` as the old position when placing a new piece, then enter a board position from `a` to `i`.

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
