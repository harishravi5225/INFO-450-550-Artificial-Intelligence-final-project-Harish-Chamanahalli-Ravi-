# Adversarial Search Comparison Project

This project compares the performance of three adversarial search algorithms:

- Minimax with alpha-beta pruning
- Monte Carlo Tree Search (MCTS)
- Random agent

across three classic board games:

- Tic-Tac-Toe
- Reversi
- Checkers

##  Repository Structure

```
.
├── problems.py          # Game environments: Tic-Tac-Toe, Reversi, Checkers
├── algorithms.py        # Agents: RandomAgent, MinimaxAgent, MCTSAgent
├── demo.py              # Play a single game interactively in the console
├── comparisons.py       # Run automated experiments
├── README.md            # This file
```

## Requirements

- Python 3.x
- NumPy

Install dependencies:

```
pip install numpy
```

No other external libraries are required.

---

##  Running the Demo

To run a single game between Minimax and Random agent, use:

```
python demo.py
```

By default, this will play Tic-Tac-Toe.

**To run a different game:**

```
python demo.py checkers
```
or
```
python demo.py reversi
```

---

##  Running Experiments

The `comparisons.py` script automates running multiple games between agents and logs the results.

### Basic Usage

```
python comparisons.py [game] [opponent] [num_games]
```

- `game`: `tictactoe`, `reversi`, or `checkers` (default: `tictactoe`)
- `opponent`: `random` or `mcts` (default: `mcts`)
- `num_games`: Number of games to run (default: `20`)

### Example Commands

**Run 100 games of Tic-Tac-Toe, Minimax vs Random:**

```
python comparisons.py tictactoe random 100
```

**Run 100 games of Reversi, Minimax vs MCTS:**

```
python comparisons.py reversi mcts 100
```

**Run 100 games of Checkers, Minimax vs MCTS:**

```
python comparisons.py checkers mcts 100
```

---

## Results

Each run prints a summary table showing:

- Wins, losses, and draws
- Average moves per game
- Average time per move per agent

You can redirect output to a text file for your report:

```
python comparisons.py tictactoe mcts 100 > tictactoe_mcts_results.txt
```

---

## Notes

- MCTS is computationally intensive, especially in Reversi and Checkers.
- You can reduce `num_simulations` in `MCTSAgent` to make it faster.
- Reversi and Checkers often result in long games or draws if evaluation functions are shallow.

---

##  Project Objectives

This project demonstrates:

- How algorithm choice impacts performance across different problem domains.
- The trade-offs between deterministic search (Minimax) and stochastic search (MCTS).
- The importance of adapting search depth and evaluation heuristics to problem complexity.

---



