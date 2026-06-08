from random import randint, choice


class Path:
    def __init__(self, x, y):
        self.pose = [True, True, True, True]  # top, right, bottom, left
        self.x = x
        self.y = y
        self.filled = False
        self.is_start = False
        self.is_end = False

    def toggle(self):
        self.filled = not self.filled

    def set_filled(self, value: bool):
        self.filled = value

    def update_pose(self, matrix):
        rows, cols = len(matrix), len(matrix[0])
        x = self.x
        y = self.y

        self.pose[0] = y > 0 and isinstance(matrix[y - 1][x], Path)
        self.pose[1] = x < cols - 1 and isinstance(matrix[y][x + 1], Path)
        self.pose[2] = y < rows - 1 and isinstance(matrix[y + 1][x], Path)
        self.pose[3] = x > 0 and isinstance(matrix[y][x - 1], Path)

    def get_element(self):
        t, r, b, l = self.pose

        chars = {
            (1, 1, 1, 1): '┼',   # top, right, bottom, left

            (1, 1, 1, 0): '├',   # top, right, bottom
            (1, 1, 0, 1): '┴',   # top, right, left
            (1, 0, 1, 1): '┤',   # top, bottom, left
            (0, 1, 1, 1): '┬',   # right, bottom, left

            (1, 1, 0, 0): '└',   # top, right
            (1, 0, 1, 0): '│',   # top, bottom
            (1, 0, 0, 1): '┘',   # top, left
            (0, 1, 1, 0): '┌',   # right, bottom
            (0, 1, 0, 1): '─',   # right, left
            (0, 0, 1, 1): '┐',   # bottom, left

            (1, 0, 0, 0): '╵',   # top only
            (0, 1, 0, 0): '╶',   # right only
            (0, 0, 1, 0): '╷',   # bottom only
            (0, 0, 0, 1): '╴',   # left only

            (0, 0, 0, 0): ' ',   # none
        }

        return chars.get((t, r, b, l), '?')

    def __repr__(self):
        return (
            f"Path({self.x}, {self.y}, "
            f"filled={self.filled}, "
            f"start={self.is_start}, end={self.is_end})"
        )


class Parameter:
    def __init__(self, x, y, required=1):
        self.x = x
        self.y = y
        self.required = required
        self.satisfied = False

    def validate(self, matrix):
        rows, cols = len(matrix), len(matrix[0])

        count = 0

        directions = [
            (0, -1),  # top
            (1, 0),   # right
            (0, 1),   # bottom
            (-1, 0),  # left
        ]

        for dx, dy in directions:
            nx = self.x + dx
            ny = self.y + dy

            if 0 <= nx < cols and 0 <= ny < rows:
                neighbour = matrix[ny][nx]

                if isinstance(neighbour, Path) and neighbour.filled:
                    count += 1

        self.satisfied = count == self.required
        return self.satisfied

    def get_element(self):
        return str(self.required)

    def __repr__(self):
        return (
            f"Parameter({self.x}, {self.y}, "
            f"required={self.required}, satisfied={self.satisfied})"
        )


class Puzzle:
    def generate_field(self, cols, rows):
        self.field = []
        self.cols = cols
        self.rows = rows
        self.parameters = []
        self.start = None
        self.end = None
        self.current_path = None
        self.filled_path_stack = []
        self.game_status = "playing"

        for y in range(rows):
            row = []

            for x in range(cols):
                row.append(None)

            self.field.append(row)

        return self.field

    def generate_coords(self, flag1=False, flag2=False):
        half_rows = int(self.rows / 4)
        half_cols = int(self.cols / 4)

        multiplier1, multiplier2 = 1, 1
        adjuster1, adjuster2 = 0, 0

        if flag1:
            multiplier1 = -1
            adjuster1 = 1

        if flag2:
            multiplier2 = -1
            adjuster2 = 1

        coordinate1 = (multiplier1 * randint(2, half_cols) * 2) - adjuster1
        coordinate2 = (multiplier2 * randint(2, half_rows) * 2) - adjuster2

        return [coordinate1, coordinate2]

    def generate_bounds(self, seed=None):
        self.broken_corner_list = []

        if seed is None:
            self.seed = []

            for _ in range(4):
                self.seed.append(randint(0, 9))

            temp = self.seed.copy()

            if self.field and self.cols and self.rows:
                counter = 0

                for corner in temp:
                    if corner > 7:
                        if counter == 0:
                            self.seed.append(self.generate_coords())
                        elif counter == 1:
                            self.seed.append(self.generate_coords(True, False))
                        elif counter == 2:
                            self.seed.append(self.generate_coords(False, True))
                        elif counter == 3:
                            self.seed.append(self.generate_coords(True, True))

                        self.broken_corner_list.append(counter)

                    counter += 1

        else:
            self.seed = seed
            temp = self.seed[0:4]

            if self.field and self.cols and self.rows:
                counter = 0

                for corner in temp:
                    if corner > 7:
                        self.broken_corner_list.append(counter)

                    counter += 1

    def populate_matrix(self):
        for i, corner in enumerate(self.broken_corner_list):
            raw_x, raw_y = self.seed[i + 4]

            x = raw_x if raw_x >= 0 else self.cols + raw_x
            y = raw_y if raw_y >= 0 else self.rows + raw_y

            if corner == 0:
                for row in range(0, y + 1):
                    self.field[row][x] = Path(x, row)

                for col in range(0, x + 1):
                    self.field[y][col] = Path(col, y)

            elif corner == 1:
                for row in range(0, y + 1):
                    self.field[row][x] = Path(x, row)

                for col in range(x, self.cols):
                    self.field[y][col] = Path(col, y)

            elif corner == 2:
                for row in range(y, self.rows):
                    self.field[row][x] = Path(x, row)

                for col in range(0, x + 1):
                    self.field[y][col] = Path(col, y)

            elif corner == 3:
                for row in range(y, self.rows):
                    self.field[row][x] = Path(x, row)

                for col in range(x, self.cols):
                    self.field[y][col] = Path(col, y)

        if 0 not in self.broken_corner_list:
            self.field[0][0] = Path(0, 0)

        if 1 not in self.broken_corner_list:
            self.field[0][self.cols - 1] = Path(self.cols - 1, 0)

        if 2 not in self.broken_corner_list:
            self.field[self.rows - 1][0] = Path(0, self.rows - 1)

        if 3 not in self.broken_corner_list:
            self.field[self.rows - 1][self.cols - 1] = Path(
                self.cols - 1,
                self.rows - 1,
            )

    def find_first_path_index(self, row):
        for i, cell in enumerate(row):
            if isinstance(cell, Path):
                return i

        return None

    def find_last_path_index(self, row):
        for i in range(len(row) - 1, -1, -1):
            if isinstance(row[i], Path):
                return i

        return None

    def fill_row(self, row_n):
        y = row_n if row_n >= 0 else self.rows + row_n
        row = self.field[y]

        left = self.find_first_path_index(row)
        right = self.find_last_path_index(row)

        if left is None or right is None:
            raise ValueError(f"No Path objects found in row {y}")

        for x in range(left, right + 1):
            self.field[y][x] = Path(x, y)

    def fill_column(self, column_n):
        x = column_n if column_n >= 0 else self.cols + column_n

        found = []

        for y in range(self.rows):
            if isinstance(self.field[y][x], Path):
                found.append(y)

        if not found:
            raise ValueError(f"No Path objects found in column {x}")

        for y in range(found[0], found[-1] + 1):
            self.field[y][x] = Path(x, y)

    def fill_bounds(self):
        self.fill_row(0)
        self.fill_row(self.rows - 1)
        self.fill_column(0)
        self.fill_column(self.cols - 1)

    def generate_internal_paths(self, spacing=2):
        for y in range(spacing, self.rows - 1, spacing):
            self.fill_row(y)

        for x in range(spacing, self.cols - 1, spacing):
            self.fill_column(x)

    def iter_paths(self):
        for row in self.field:
            for cell in row:
                if isinstance(cell, Path):
                    yield cell

    def get_border_paths(self):
        seen = set()
        border_paths = []

        for y in range(self.rows):
            for x in range(self.cols):
                on_border = (
                    y == 0
                    or y == self.rows - 1
                    or x == 0
                    or x == self.cols - 1
                )

                if not on_border:
                    continue

                cell = self.field[y][x]

                if isinstance(cell, Path) and (x, y) not in seen:
                    seen.add((x, y))
                    border_paths.append(cell)

        return border_paths

    def generate_start_and_end(self):
        if self.start:
            self.start.is_start = False

        if self.end:
            self.end.is_end = False

        border_paths = self.get_border_paths()

        if len(border_paths) < 2:
            raise ValueError("Need at least 2 border paths for start and end")

        self.start = choice(border_paths)
        remaining = [path for path in border_paths if path is not self.start]
        self.end = choice(remaining)

        self.start.is_start = True
        self.end.is_end = True
        self.current_path = self.start
        self.start.filled = True
        self.filled_path_stack = [self.start]
        self.game_status = "playing"

        return self.start, self.end

    def reset_filled_paths(self):
        for path in self.iter_paths():
            path.filled = False

        if self.start:
            self.start.filled = True
            self.current_path = self.start
            self.filled_path_stack = [self.start]
        else:
            self.current_path = None
            self.filled_path_stack = []

        self.game_status = "playing"
        self.validate_parameters()

    def move_player(self, dx, dy):
        if self.game_status != "playing":
            return False

        if self.current_path is None:
            return False

        nx = self.current_path.x + dx
        ny = self.current_path.y + dy

        if not self.is_in_bounds(nx, ny):
            return False

        target = self.get_path_at(nx, ny)

        if target is None:
            return False

        if len(self.filled_path_stack) >= 2:
            previous = self.filled_path_stack[-2]

            if target is previous:
                current = self.filled_path_stack.pop()

                if not current.is_start:
                    current.filled = False

                self.current_path = previous
                return True

        if not target.filled:
            target.filled = True
            self.filled_path_stack.append(target)
            self.current_path = target

            if target.is_end:
                self.finish_attempt()

            return True

        return False

    def finish_attempt(self):
        if self.validate_parameters():
            self.game_status = "win"
        else:
            self.game_status = "try_again"

        return self.game_status

    def is_in_bounds(self, x, y):
        return 0 <= x < self.cols and 0 <= y < self.rows

    def get_path_at(self, x, y):
        if not self.is_in_bounds(x, y):
            return None

        cell = self.field[y][x]

        if isinstance(cell, Path):
            return cell

        return None

    def toggle_path_at(self, x, y):
        path = self.get_path_at(x, y)

        if path is None:
            return False

        path.toggle()
        self.validate_parameters()

        return True

    def place_random_parameter(self, required=None):
        empty_cells = []

        for y in range(self.rows):
            for x in range(self.cols):
                if self.field[y][x] is None:
                    empty_cells.append((x, y))

        if not empty_cells:
            raise ValueError("No empty cells available for parameter placement")

        if required is None:
            required = randint(1, 4)

        x, y = choice(empty_cells)

        parameter = Parameter(x, y, required)
        self.field[y][x] = parameter
        self.parameters.append(parameter)

        return parameter

    def validate_parameters(self):
        return all(parameter.validate(self.field) for parameter in self.parameters)

    def draw_raw(self):
        for row in self.field:
            print(row)

    def draw_game(self):
        for row in self.field:
            for cell in row:
                if cell is None:
                    print("  ", end="")

                elif isinstance(cell, Path):
                    cell.update_pose(self.field)
                    print(cell.get_element() + " ", end="")

                elif isinstance(cell, Parameter):
                    print(cell.get_element() + " ", end="")

            print()


if __name__ == "__main__":
    puzzle = Puzzle()
    puzzle.generate_field(11, 11)
    puzzle.generate_bounds()
    puzzle.populate_matrix()

    puzzle.fill_bounds()
    puzzle.generate_internal_paths(spacing=2)
    puzzle.place_random_parameter(required=2)
    puzzle.generate_start_and_end()
    puzzle.draw_game()