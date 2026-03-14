class Path():
    def __init__(self):
        self.pose = [True, True, True, True]

    def update_pose(self, matrix):
        for row in matrix:
            if self in row:
                x = row.index(self)
                y = matrix.index(row)
                break

        rows, cols = len(matrix), len(matrix[0])

        # pose: [top, right, bottom, left]
        self.pose[0] = y > 0 and type(matrix[y - 1][x]) is Path           # top
        self.pose[1] = x < cols - 1 and type(matrix[y][x + 1]) is Path    # right
        self.pose[2] = y < rows - 1 and type(matrix[y + 1][x]) is Path    # bottom
        self.pose[3] = x > 0 and type(matrix[y][x - 1]) is Path           # left

    def get_element(self):
        # pose: [top, right, bottom, left]
        t, r, b, l = self.pose[0], self.pose[1], self.pose[2], self.pose[3]
        # Map (top, right, bottom, left) -> box-drawing character
        chars = {
            (1, 1, 1, 1): '┼',   # all four
            (1, 1, 1, 0): '┤',   # top, right, bottom
            (1, 1, 0, 1): '┬',   # top, right, left
            (1, 0, 1, 1): '├',   # top, bottom, left
            (0, 1, 1, 1): '┴',   # right, bottom, left
            (1, 1, 0, 0): '┐',   # top, right
            (1, 0, 1, 0): '│',   # top, bottom
            (1, 0, 0, 1): '┌',   # top, left
            (0, 1, 1, 0): '┘',   # right, bottom
            (0, 1, 0, 1): '─',   # right, left
            (0, 0, 1, 1): '└',   # bottom, left
            (1, 0, 0, 0): '╵',   # top only
            (0, 1, 0, 0): '╴',   # right only
            (0, 0, 1, 0): '╷',   # bottom only
            (0, 0, 0, 1): '╶',   # left only
            (0, 0, 0, 0): '·',   # none
        }
        return chars.get((t, r, b, l), '·')

field = []
for i in range(11):
    row = []
    for i in range(11):
        path = Path()
        row.append(path)
    field.append(row)

for i in field:
    for i in field:
        print(i[0].get_element(), end=' ')
    print()

for i in field:
    for i in field:
        i[0].update_pose(field)
        print(i[0].get_element(), end=' ')
    print()