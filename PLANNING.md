# Triangle Tic-Tac-Toe Web Development Plan

## 1. Purpose

This document is the shared reference for evolving the existing Python Triangle Tic-Tac-Toe game into a web application.

The project has two equally important goals:

1. Build a complete browser-based game in which a person can play against the computer.
2. Learn modern web development incrementally, keeping every phase small, understandable, and playable.

This file should be consulted at the beginning of every implementation task. It can be updated when the architecture or priorities change.

## 2. Current Project

The repository currently contains:

- `TriangleTicTacToe.py`: game rules, players, AI logic, and terminal game modes.
- `Statistics.py`: generation of precomputed best moves.
- `BestMoves.json`: precomputed moves used by the fast advanced AI.
- `board.png`: reference image for the board and its position labels.
- `Analysis.txt`: output and notes from previous game analysis.

The existing Python game supports:

- Human versus computer.
- Computer versus computer.
- Random, minimax-based, and precomputed-move AI strategies.
- A placement phase followed by a movement phase.

The original implementation should remain working while the web version is developed.

## 3. Product Vision

The first complete version should allow a player to:

- Open the game in a browser.
- Understand the board without reading terminal instructions.
- Place three pieces by clicking board positions.
- Move pieces between connected positions after the placement phase.
- Play against a computer opponent.
- See whose turn it is and which phase is active.
- Receive clear feedback for invalid moves, wins, and losses.
- Restart the game.
- Select at least an easy and a hard difficulty.

Features such as accounts, online multiplayer, rankings, and permanent match history are intentionally outside the initial scope.

## 4. Proposed Architecture

The application will eventually contain two services:

```text
Browser
  |
  v
Next.js frontend
  |
  | HTTP + JSON
  v
FastAPI backend
  |-- Game rules
  |-- State validation
  |-- Computer strategies
  `-- BestMoves.json
```

### Frontend responsibilities

The Next.js application will:

- Render the board and pieces.
- Handle clicks, selection, and visual feedback.
- Display the current turn, phase, result, and errors.
- Send player actions to the API.
- Render the authoritative game state returned by the API.

### Backend responsibilities

The FastAPI application will:

- Own the authoritative game rules.
- Validate all player actions.
- Store active game state initially in memory.
- Choose and apply computer moves.
- Expose game operations through JSON endpoints.
- Reuse the existing Python logic after it has been separated from terminal input/output.

### Why use an API

An API is appropriate because the existing rules and AI are written in Python. It also creates a useful learning boundary between frontend and backend development.

The API will not be introduced in the first visual phase. Starting with the interface keeps the early feedback loop short and makes each new concept easier to understand.

## 5. Intended Repository Structure

The exact structure can evolve, but the intended direction is:

```text
triangle-tic-tac-toe/
|-- frontend/                  # Next.js and TypeScript
|-- backend/                   # FastAPI and Python
|   |-- app/
|   |   |-- main.py            # Application and routes
|   |   |-- game.py            # Game state and rules
|   |   |-- ai.py              # Computer strategies
|   |   `-- models.py          # Request and response models
|   |-- data/
|   |   `-- BestMoves.json
|   `-- tests/
|-- legacy/                    # Optional home for preserved terminal code
|-- PLANNING.md
`-- README.md
```

Moving existing files into `legacy/` is optional and should only happen when it makes the repository clearer. No historical code should be deleted merely to match this proposed structure.

## 6. Domain Model

The board has nine positions, identified by the letters `a` through `i`.

Each game should represent at least:

- Human piece positions.
- Computer piece positions.
- Current player.
- Current phase: `placing`, `moving`, or `finished`.
- Winner, if any.
- Difficulty.
- Optional move history.

A move has two possible forms:

- Placement: a destination position only.
- Movement: an origin and a connected destination.

For API consistency, both can eventually use the same shape:

```json
{
  "from": null,
  "to": "d"
}
```

During movement:

```json
{
  "from": "d",
  "to": "g"
}
```

Position names, connection rules, and winning combinations must have one authoritative definition in the backend once the API is introduced.

## 7. Development Principles

Every phase should follow these principles:

- Keep the application runnable at the end of the phase.
- Introduce as few new concepts as practical at one time.
- Explain important implementation choices in plain language.
- Prefer small components and functions with clear responsibilities.
- Avoid premature databases, authentication, state libraries, and deployment complexity.
- Add tests where rules or behavior could regress.
- Preserve existing user work and avoid unrelated refactors.
- Update this document when a decision changes the overall direction.

## 8. Implementation Roadmap

### Phase 0 — Establish the baseline

Goal: understand and protect the current behavior before adding the web application.

Tasks:

- Document the game rules represented by the Python code.
- Identify board connections and winning combinations.
- Run the existing terminal game.
- Add focused tests around the existing rules if refactoring is about to begin.
- Decide which currently generated or analysis files remain part of the maintained project.

Completion criteria:

- The existing terminal game still runs.
- The placement phase, movement phase, and win conditions are understood.
- Future refactoring can be checked against known behavior.

### Phase 1 — Build a static board in Next.js

Goal: create the visual foundation without game state or backend communication.

Tasks:

- Create a Next.js application using TypeScript.
- Create the main game page.
- Draw all nine board positions and their connections.
- Add visual styles for empty positions and both players' pieces.
- Make the board usable on desktop and small screens.
- Add a small legend or instructional area.

Suggested learning topics:

- Next.js project structure.
- React components.
- JSX and component properties.
- CSS layout and responsive design.
- TypeScript basics.

Completion criteria:

- All nine positions are displayed in the correct geometry.
- Connections match the existing game rules.
- Sample pieces can be displayed for visual testing.
- The page remains readable at common desktop and mobile widths.

### Phase 2 — Add local browser interaction

Goal: make the board playable by two local players before introducing the API.

Tasks:

- Model the board state in TypeScript.
- Allow players to place pieces by clicking empty positions.
- Alternate turns.
- Detect wins.
- Display turn, phase, and result messages.
- Add a restart button.
- Add selection and destination highlighting for the movement phase.
- Prevent obviously invalid local actions.

Suggested learning topics:

- React state.
- Event handlers.
- Derived state.
- Conditional rendering.
- Immutable updates.

Completion criteria:

- Two people can complete a match in one browser.
- Placement and movement phases work.
- Invalid actions do not corrupt the state.
- A finished game can be restarted.

This frontend rule implementation is a learning step. It does not replace authoritative backend validation later.

### Phase 3 — Create the FastAPI foundation

Goal: expose the Python game through a small, understandable HTTP API.

Tasks:

- Create the FastAPI project.
- Separate game rules from terminal input/output.
- Define request and response models with Pydantic.
- Configure development CORS for the Next.js origin.
- Add a health endpoint.
- Add endpoints to create, inspect, play, and restart a game.
- Store active games in memory.
- Add backend rule tests.

Initial endpoint proposal:

```text
GET  /health
POST /games
GET  /games/{game_id}
POST /games/{game_id}/moves
POST /games/{game_id}/reset
```

Example create-game request:

```json
{
  "difficulty": "random",
  "humanStarts": true
}
```

Example game response:

```json
{
  "gameId": "abc123",
  "phase": "placing",
  "turn": "human",
  "humanPositions": [],
  "computerPositions": [],
  "winner": null,
  "lastMove": null
}
```

Suggested learning topics:

- HTTP methods and status codes.
- JSON requests and responses.
- FastAPI routes.
- Pydantic validation.
- CORS.
- Automated API tests.

Completion criteria:

- A game can be created and retrieved through HTTP.
- Legal human moves are accepted.
- Illegal moves return a clear error without changing the game.
- The rules are covered by focused tests.

### Phase 4 — Connect the frontend to a random computer

Goal: deliver the first end-to-end human-versus-computer game.

Tasks:

- Add an API client layer to the Next.js application.
- Create a new game from the interface.
- Send human moves to FastAPI.
- Apply a random legal computer move in the backend.
- Return the updated state after both actions.
- Show loading and error states.
- Disable interaction while waiting for the computer.

Suggested learning topics:

- Asynchronous JavaScript.
- `fetch` and HTTP errors.
- Client/server state boundaries.
- Loading and retry experiences.

Completion criteria:

- A person can finish a match against the random AI.
- The backend rejects invalid or out-of-turn moves.
- Network errors are visible and recoverable.
- The frontend renders the state returned by the server.

### Phase 5 — Complete and polish the movement phase

Goal: make the less obvious second phase intuitive to play.

Tasks:

- Select one of the human player's pieces.
- Highlight only valid connected destinations.
- Allow selection to be cancelled or changed.
- Clearly distinguish selected, available, occupied, and unavailable positions.
- Provide short contextual instructions.
- Verify all movement rules against backend tests.

Completion criteria:

- A new player can understand how to move pieces without terminal instructions.
- The interface never presents an illegal destination as legal.
- Backend validation remains authoritative.

### Phase 6 — Add the advanced computer

Goal: reuse the precomputed move database for a stronger opponent.

Tasks:

- Extract the current `FastAdvanced` behavior into the backend AI module.
- Load `BestMoves.json` safely and efficiently.
- Support at least `random` and `advanced` difficulties.
- Add a difficulty selector before starting a match.
- Define safe fallback behavior if a board state is absent from the file.
- Remove diagnostic printing from request-handling code.

Suggested learning topics:

- Strategy patterns or interchangeable functions.
- Loading application data.
- Error handling and fallbacks.
- Performance considerations.

Completion criteria:

- The player can select easy or hard difficulty.
- Advanced moves are returned quickly.
- Missing or malformed move data produces a controlled error or legal fallback.

Real-time minimax is not required for this phase. It may be explored later after the precomputed strategy is reliable.

### Phase 7 — Testing and user experience

Goal: make the complete game dependable and pleasant to use.

Tasks:

- Expand backend tests for legal moves, illegal moves, and wins.
- Add frontend tests for critical interactions.
- Add win, loss, and restart experiences.
- Add an optional session score.
- Improve keyboard and screen-reader accessibility.
- Review responsive layout and visual contrast.
- Improve development setup documentation.

Completion criteria:

- Core rules have automated coverage.
- The main user journey works on desktop and mobile layouts.
- Important controls are usable without a mouse.
- Setup instructions work from a fresh checkout.

### Phase 8 — Deployment

Goal: make the application available outside the local development environment.

Tasks:

- Choose hosting for the Next.js frontend and FastAPI backend.
- Configure production environment variables.
- Restrict CORS to the deployed frontend.
- Add production start commands and health checks.
- Document the deployment process.

Completion criteria:

- The public frontend communicates with the public API.
- A complete match can be played in the deployed application.
- No development-only URLs or permissions are required.

## 9. Deferred Ideas

These ideas are valuable but should wait until the initial game is complete:

- Persistent database storage.
- User accounts and authentication.
- Match history and replays.
- Online human-versus-human play.
- WebSocket-based live matches.
- Rankings and leaderboards.
- AI-versus-AI visualization.
- Real-time minimax with configurable depth.
- Containers and more advanced infrastructure.

Each deferred idea should become its own planning task before implementation.

## 10. Early Technical Decisions

### State storage

Active games will initially be stored in backend memory. Restarting the FastAPI process will remove them. This is acceptable for learning and local play and avoids introducing a database too early.

### Source of truth

After API integration, the backend is authoritative. The frontend may calculate highlights and previews for responsiveness, but the server must validate every submitted move.

### AI progression

The computer will be introduced in this order:

1. Random legal moves.
2. Precomputed advanced moves from `BestMoves.json`.
3. Optional real-time minimax exploration.

### Styling

The first version should prefer standard CSS or CSS Modules. A component library or utility CSS framework should only be added if it solves a concrete need and creates a useful learning opportunity.

### Frontend state management

Built-in React state should be sufficient initially. A third-party state library should not be added unless the application becomes complex enough to justify it.

## 11. Open Questions

These decisions can be made when their corresponding phase begins:

- Should the human always play first, or should this be configurable?
- Should the frontend use an SVG board, HTML elements with CSS, or another rendering technique?
- Should one API request apply both the human and computer moves, or should they be separate operations?
- How should repeated positions or indefinitely long matches be handled?
- Should the original terminal application remain at the repository root or move into `legacy/`?
- Which hosting services will be used?

Decisions should be recorded in the Decision Log below.

## 12. Decision Log

| Date | Decision | Reason |
| --- | --- | --- |
| 2026-08-19 | Use Next.js with TypeScript for the frontend. | The project is intended to teach modern web and React development. |
| 2026-08-19 | Use FastAPI for the backend. | The existing game rules and AI are implemented in Python. |
| 2026-08-19 | Introduce the API after the first frontend phases. | This keeps the learning progression simple and provides visible results early. |
| 2026-08-19 | Store games in memory initially. | Persistence is not needed for the first playable version. |
| 2026-08-19 | Introduce random AI before advanced AI. | It validates the full client/server flow with less complexity. |

## 13. Progress Tracker

| Phase | Status | Notes |
| --- | --- | --- |
| Phase 0 — Establish the baseline | Not started | |
| Phase 1 — Static Next.js board | Not started | |
| Phase 2 — Local browser interaction | Not started | |
| Phase 3 — FastAPI foundation | Not started | |
| Phase 4 — Random computer integration | Not started | |
| Phase 5 — Movement phase polish | Not started | |
| Phase 6 — Advanced computer | Not started | |
| Phase 7 — Testing and user experience | Not started | |
| Phase 8 — Deployment | Not started | |

Allowed status values are `Not started`, `In progress`, `Blocked`, and `Complete`.

## 14. Starting a New Implementation Task

Use a separate conversation for each phase or focused piece of work. A useful opening request is:

> We are implementing Phase N of the Triangle Tic-Tac-Toe web project. Read `PLANNING.md` and inspect the current repository before making changes. Keep the work within this phase, explain the important web development concepts as we go, verify the result, and update the progress tracker and decision log when appropriate.

At the end of each implementation task:

- Verify the relevant behavior.
- Summarize what changed and what was learned.
- Update the phase status in this file.
- Record any project-wide architectural decision.
- Identify the smallest sensible next task without implementing it automatically.
