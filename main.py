from playfield import Puzzle
from gui import PuzzleGUI
from finder import PuzzleFinder

# Simple settings — replace with a menu screen later.
SEARCH_ALGORITHM = "bfs"
MAX_SOLUTIONS = 500
MAX_DEAD_ENDS = 1000
MAX_BFS_STATES = 100000


def build_demo_puzzle():
    puzzle = Puzzle()
    puzzle.generate_field(11, 11)
    puzzle.generate_bounds()
    puzzle.populate_matrix()
    puzzle.fill_bounds()
    puzzle.generate_internal_paths(spacing=2)
    puzzle.place_random_parameter()
    puzzle.generate_start_and_end()

    return puzzle


if __name__ == "__main__":
    puzzle = build_demo_puzzle()
    print("START:", puzzle.start)
    print("END:", puzzle.end)

    finder = PuzzleFinder(puzzle, algorithm=SEARCH_ALGORITHM)

    if SEARCH_ALGORITHM == "dfs":
        found = finder.solve(
            algorithm="dfs",
            max_solutions=MAX_SOLUTIONS,
            max_dead_ends=MAX_DEAD_ENDS,
        )
    elif SEARCH_ALGORITHM == "bfs":
        found = finder.solve(
            algorithm="bfs",
            max_dead_ends=MAX_DEAD_ENDS,
            max_states=MAX_BFS_STATES,
        )
    else:
        raise ValueError(f"Unknown search algorithm: {SEARCH_ALGORITHM}")

    print("Search algorithm:", SEARCH_ALGORITHM)
    print("Solver found solution:", found)
    print(finder.get_search_summary())

    gui = PuzzleGUI(puzzle, finder=finder)
    gui.run()
