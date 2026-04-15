import sys
import copy
import os

# --- Global Metric Trackers ---
backtrack_calls = 0
backtrack_failures = 0

# --- CSP Setup ---
digits = "123456789"
rows = "ABCDEFGHI"

def cross(A, B):
    """Cross product of elements in A and elements in B."""
    return [a + b for a in A for b in B]

squares = cross(rows, digits) # 81 variables: A1...I9

# Build units and peers
unitlist = ([cross(rows, c) for c in digits] +
            [cross(r, digits) for r in rows] +
            [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')])

units = dict((s, [u for u in unitlist if s in u]) for s in squares)
peers = dict((s, set(sum(units[s],[])) - {s}) for s in squares)

# --- AC-3 Algorithm ---
def revise(domains, xi, xj):
    """Make variable xi arc consistent with variable xj."""
    revised = False
    for x in domains[xi][:]:
        # If the only available value in xj is x, then xi cannot be x
        if len(domains[xj]) == 1 and x == domains[xj][0]:
            domains[xi].remove(x)
            revised = True
    return revised

def ac3(domains, arcs=None):
    """Enforce arc consistency using the AC-3 algorithm."""
    if arcs is None:
        arcs = [(s, p) for s in squares for p in peers[s]]
    
    queue = list(arcs)
    while queue:
        (xi, xj) = queue.pop(0)
        if revise(domains, xi, xj):
            if len(domains[xi]) == 0:
                return False # Domain wiped out, impossible state
            for xk in peers[xi] - {xj}:
                queue.append((xk, xi))
    return True

# --- Backtracking Search ---
def select_unassigned_variable(assignment, domains):
    """Minimum Remaining Values (MRV) heuristic."""
    unassigned = [v for v in squares if v not in assignment]
    return min(unassigned, key=lambda v: len(domains[v]))

def backtrack(assignment, domains):
    """Recursive backtracking search with Forward Checking."""
    global backtrack_calls, backtrack_failures
    backtrack_calls += 1 # Strict requirement: incremented at the very beginning

    if len(assignment) == len(squares):
        return assignment

    var = select_unassigned_variable(assignment, domains)

    for value in domains[var]:
        # Check if the value is consistent with the current assignment
        if all(assignment.get(peer) != value for peer in peers[var]):
            assignment[var] = value
            
            # Forward Checking: Create a deep copy of domains for this branch
            new_domains = copy.deepcopy(domains)
            new_domains[var] = [value]
            
            fc_failed = False
            # Forward Checking: Immediately prune the assigned value from unassigned peers
            for peer in peers[var]:
                if peer not in assignment:
                    if value in new_domains[peer]:
                        new_domains[peer].remove(value)
                        if len(new_domains[peer]) == 0:
                            fc_failed = True # Pruning resulted in an empty domain
                            break
            
            if not fc_failed:
                result = backtrack(assignment, new_domains)
                if result is not None:
                    return result
            
            # Backtrack step: undo assignment
            del assignment[var]

    backtrack_failures += 1 # Strict requirement: incremented before returning None
    return None

# --- I/O and Utility Functions ---
def parse_board(grid_str):
    """Convert grid string into a dict of {cell: [domains]}."""
    domains = dict((s, list(digits)) for s in squares)
    grid_chars = [c for c in grid_str if c in digits or c == '0']
    
    for s, d in zip(squares, grid_chars):
        if d != '0' and d in digits:
            domains[s] = [d]
    return domains

def print_board(board_dict):
    """Display the board in a 9x9 grid layout."""
    if not board_dict:
        print("Unsolvable Board")
        return
    for r in rows:
        row_str = ""
        for c in digits:
            val = board_dict[r+c]
            # Print value if assigned/single domain, else '.'
            row_str += (val[0] if isinstance(val, list) and len(val) == 1 
                        else val if isinstance(val, str) else '.') + " "
            if c in '36':
                row_str += "| "
        print(row_str)
        if r in 'CF':
            print("-" * 21)

def solve_sudoku(filename):
    """Main pipeline for reading, parsing, AC-3, and solving a Sudoku board."""
    global backtrack_calls, backtrack_failures
    # Reset counters for each board
    backtrack_calls = 0
    backtrack_failures = 0

    if not os.path.exists(filename):
        print(f"File not found: {filename}")
        return

    with open(filename, 'r') as f:
        grid_str = f.read()

    print(f"\n{'='*30}\nSolving: {filename}\n{'='*30}")
    domains = parse_board(grid_str)
    
    print("Initial Board State:")
    print_board(domains)
    print("")

    # Initial Constraint Propagation
    if not ac3(domains):
        print("Inconsistent initial board (failed AC-3).")
        return
        
    # Extract assignments made purely by AC-3
    assignment = {s: domains[s][0] for s in squares if len(domains[s]) == 1}

    # Run Backtracking search
    result = backtrack(assignment, domains)

    print("Solved Board State:")
    print_board(result)
    print(f"\nBacktrack Calls: {backtrack_calls}")
    print(f"Backtrack Failures: {backtrack_failures}")


def main():
    files = ['easy.txt', 'medium.txt', 'hard.txt', 'veryhard.txt']
    for file in files:
        solve_sudoku(file)

if __name__ == '__main__':
    main()