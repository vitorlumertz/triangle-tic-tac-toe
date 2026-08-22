import styles from "./page.module.css";
import { GameBoard } from "./components/GameBoard";

export default function Home() {
  return (
    <main className={styles.pageShell}>
      <h1>Triangle Tic-Tac-Toe</h1>
      <section className={styles.boardArea} aria-label="Game board">
        <GameBoard />
      </section>
    </main>
  );
}
