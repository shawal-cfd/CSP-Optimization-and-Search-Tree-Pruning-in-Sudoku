# Sudoku Solver: Constraint Satisfaction Problem (CSP)

## Overview
This repository contains a highly optimized Python-based Sudoku solver utilizing Constraint Satisfaction Problem (CSP) techniques. The solver is capable of resolving Sudoku puzzles of varying difficulties (Easy to Very Hard) efficiently by avoiding combinatorial explosion.

## Architecture & Algorithms
This script implements a synergistic approach to CSP, utilizing:
* **AC-3 Algorithm:** Acts as a global pre-processor to enforce arc consistency and drastically shrink the initial domains of the variables before the search begins.
* **Backtracking Search:** A recursive depth-first search to navigate the state space.
* **Forward Checking:** A dynamic local pruning mechanism integrated into the backtracking search to immediately eliminate invalid domains.
* **Minimum Remaining Values (MRV) Heuristic:** Dynamically selects the most constrained unassigned variable to force failures early, effectively pruning redundant branches of the search tree.

## Files Included
* `p1.py`: The main Python script containing the CSP logic, AC-3, and backtracking algorithms.
* `easy.txt`: Test board (Easy difficulty).
* `medium.txt`: Test board (Medium difficulty).
* `hard.txt`: Test board (Hard difficulty).
* `veryhard.txt`: Test board (Very Hard difficulty).
* `README.md`: An analytical commentary detailing the metric scaling and the pruning power of the chosen algorithms.

## How to Run
Ensure you have Python 3.x installed. The script requires no external libraries. 

1. Clone this repository.
2. Ensure the four text files (`easy.txt`, `medium.txt`, `hard.txt`, `veryhard.txt`) are in the same directory as the Python script.
3. Execute the script from your terminal:
   ```bash
   python p1.py
