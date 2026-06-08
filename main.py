from playfield import Puzzle
from gui import PuzzleGUI


def build_demo_puzzle():
    puzzle = Puzzle()
    puzzle.generate_field(11, 11)
    puzzle.generate_bounds()
    puzzle.populate_matrix()
    puzzle.fill_bounds()
    puzzle.generate_internal_paths(spacing=2)
    puzzle.place_random_parameter(required=2)
    puzzle.generate_start_and_end()

    return puzzle


if __name__ == "__main__":
    puzzle = build_demo_puzzle()

    # TEMPORARY DEBUG - remove after verifying start/end/movement
    print("START:", puzzle.start)
    print("END:", puzzle.end)
    print("CURRENT:", puzzle.current_path)
    print("STATUS:", puzzle.game_status)

    gui = PuzzleGUI(puzzle)
    gui.run()