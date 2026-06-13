from playfield import Puzzle
from gui import PuzzleGUI
from finder import PuzzleFinder


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

    finder = PuzzleFinder(puzzle)
    found = finder.find_solutions(max_solutions=50, max_dead_ends=100)
    print("Solver found solution:", found)
    print(finder.get_search_summary())

    gui = PuzzleGUI(puzzle, finder=finder)
    gui.run()