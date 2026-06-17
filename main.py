from playfield import Puzzle
from gui import PuzzleGUI
from finder import PuzzleFinder

# Simple settings — replace with a menu screen later.
PUZZLE_SEED = None
MIN_SIZE = 7
MAX_SIZE = 15
RECTANGLE_CHANCE = 0.20
PARAMETER_COUNT = 1
SEARCH_ALGORITHM = "bfs"
MAX_SOLUTIONS = 500
MAX_DEAD_ENDS = 1000
MAX_BFS_STATES = 100000
MAX_PARAMETER_ATTEMPTS = 20


def solve_puzzle(puzzle, algorithm=SEARCH_ALGORITHM):
    finder = PuzzleFinder(puzzle, algorithm=algorithm)

    if algorithm == "dfs":
        found = finder.solve(
            algorithm="dfs",
            max_solutions=MAX_SOLUTIONS,
            max_dead_ends=MAX_DEAD_ENDS,
        )
    elif algorithm == "bfs":
        found = finder.solve(
            algorithm="bfs",
            max_dead_ends=MAX_DEAD_ENDS,
            max_states=MAX_BFS_STATES,
        )
    else:
        raise ValueError(f"Unknown search algorithm: {algorithm}")

    return finder, found


def add_valid_parameters(
    puzzle,
    target_count,
    algorithm=SEARCH_ALGORITHM,
    max_attempts_per_parameter=MAX_PARAMETER_ATTEMPTS,
):
    added = 0

    while added < target_count:
        accepted = False

        for _ in range(max_attempts_per_parameter):
            candidate = puzzle.place_random_parameter()

            if not puzzle.is_parameter_locally_feasible(
                candidate.x,
                candidate.y,
                candidate.required,
                candidate.parameter_type,
            ):
                puzzle.remove_parameter(candidate)
                continue

            finder, solvable = solve_puzzle(puzzle, algorithm=algorithm)

            if solvable:
                accepted = True
                added += 1
                summary = finder.get_search_summary()
                print(
                    f"Accepted parameter {added}: "
                    f"type={candidate.parameter_type} "
                    f"value={candidate.get_element()} "
                    f"at ({candidate.x}, {candidate.y}) | "
                    f"explored={summary['explored_states']} "
                    f"dead_ends={summary['dead_ends']} "
                    f"solution_length={summary['solution_length']} "
                    f"solution_count={summary['solution_count']}",
                )
                break

            puzzle.remove_parameter(candidate)

        if not accepted:
            break

    return added


def build_demo_puzzle(seed=PUZZLE_SEED):
    puzzle = Puzzle()
    puzzle.set_seed(seed)
    cols, rows = puzzle.generate_dimensions(
        min_size=MIN_SIZE,
        max_size=MAX_SIZE,
        rectangle_chance=RECTANGLE_CHANCE,
    )
    puzzle.generate_field(cols, rows)
    puzzle.generate_bounds()
    puzzle.populate_matrix()
    puzzle.fill_bounds()
    puzzle.generate_internal_paths(spacing=2)
    puzzle.generate_start_and_end()

    print("Puzzle seed:", puzzle.seed)
    print("Dimensions:", puzzle.cols, "x", puzzle.rows)

    added = add_valid_parameters(puzzle, PARAMETER_COUNT, algorithm=SEARCH_ALGORITHM)
    print(f"Parameters added: {added}/{PARAMETER_COUNT}")

    return puzzle


if __name__ == "__main__":
    puzzle = build_demo_puzzle()
    print("START:", puzzle.start)
    print("END:", puzzle.end)

    finder, found = solve_puzzle(puzzle, algorithm=SEARCH_ALGORITHM)

    print("Search algorithm:", SEARCH_ALGORITHM)
    print("Solver found solution:", found)
    print(finder.get_search_summary())

    gui = PuzzleGUI(puzzle, finder=finder)
    gui.run()
