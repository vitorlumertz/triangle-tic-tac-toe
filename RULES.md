# Legacy Game Rules

This document records the behavior of the original Python game before the web
application is introduced. It is a baseline for later refactoring and API
tests, not a proposal for new rules.

## Players and turns

- Player 1 is the human in `HumanVsAi`; Player 2 is the computer.
- Player 1 takes the first turn, then turns alternate.
- A win is checked immediately after each move. The game ends as soon as the
  player who just moved occupies a winning combination.
- The legacy game has no draw, repetition, or maximum-turn rule in human play.

## Board

The board contains nine positions named `a` through `i`. A connection permits
movement in either direction.

| Position | Connected positions |
| --- | --- |
| `a` | `d`, `f`, `i` |
| `b` | `d`, `e`, `g` |
| `c` | `e`, `f`, `h` |
| `d` | `a`, `b`, `g`, `h` |
| `e` | `b`, `c`, `h`, `i` |
| `f` | `a`, `c`, `g`, `i` |
| `g` | `b`, `d`, `f`, `h`, `i` |
| `h` | `c`, `d`, `e`, `g`, `i` |
| `i` | `a`, `e`, `f`, `g`, `h` |

The labeled geometry is also shown in `board.png`.

## Placement phase

- Each player has three pieces.
- Until all three of a player's pieces are on the board, that player's legal
  moves are placements on any unoccupied position.
- A placement is represented internally as `('x', destination)`. The `x` is a
  sentinel meaning that the piece does not yet have an origin on the board.

## Movement phase

- Once all three of a player's pieces are placed, that player must move one of
  those pieces on each turn.
- A move must start at a position occupied by that player.
- Its destination must be directly connected to the origin and unoccupied.
- Jumping over positions is not allowed.

## Winning combinations

A player wins by occupying all three positions in any one of these sets:

```text
a b d    b c e    a c f
a e i    b f g    c d h
d g i    e g h    f h i
```

The order in which the three positions were acquired does not matter.

## Maintained legacy artifacts

- `legacy/TriangleTicTacToe.py` remains the runnable legacy game and the current
  rule reference until the backend extracts those rules.
- `BestMoves.json` remains runtime data for the `FastAdvanced` computer player.
- `board.png` remains the visual reference for labels and geometry.
- `legacy/Statistics.py` remains the utility that can regenerate best-move data;
  its output is not regenerated as part of normal development.
- `legacy/Analysis.txt` is retained as historical analysis, but is not
  maintained as application source or regenerated output.

## Known legacy limitation

`Player.Move` applies a `Random` move but does not return that move, unlike the
two advanced strategies. The default human game uses `FastAdvanced` and is not
affected. This should be addressed when AI strategies are extracted in a later
phase, rather than changing legacy behavior during baseline work.
