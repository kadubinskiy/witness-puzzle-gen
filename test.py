class Path():
    def __init__(self, x, y):
        self.pose = [True, True, True, True]
        self.x = x
        self.y = y

    def update_pose(self, matrix):
        rows, cols = len(matrix), len(matrix[0])
        x = self.x
        y = self.y

        self.pose[0] = y > 0 and type(matrix[y - 1][x]) is Path
        self.pose[1] = x < cols - 1 and type(matrix[y][x + 1]) is Path
        self.pose[2] = y < rows - 1 and type(matrix[y + 1][x]) is Path
        self.pose[3] = x > 0 and type(matrix[y][x - 1]) is Path
        # n_row = 0
        # for row in matrix:
        #     n_item = 0
        #     for item in row:
        #         x = n_item
        #         y = n_row
        #         self.pose[0] = y > 0 and type(matrix[y - 1][x]) is Path
        #         self.pose[1] = x < cols - 1 and type(matrix[y][x + 1]) is Path
        #         self.pose[2] = y < rows - 1 and type(matrix[y + 1][x]) is Path
        #         self.pose[3] = x > 0 and type(matrix[y][x - 1]) is Path
        #         print(x, y, self.pose, self.get_element())
        #         n_item+=1
        #     n_row+=1

    def get_element(self):
        # pose: [top, right, bottom, left]
        t, r, b, l = self.pose[0], self.pose[1], self.pose[2], self.pose[3]
        # Map (top, right, bottom, left) -> box-drawing character
        chars = {
            (1, 1, 1, 1): '┼',   # all four
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
            (0, 1, 0, 0): '╴',   # right only
            (0, 0, 1, 0): '╷',   # bottom only
            (0, 0, 0, 1): '╶',   # left only
            (0, 0, 0, 0): '·',   # none
        }
        return chars.get((t, r, b, l))

field = []
for y in range(11):
    row = []
    for x in range(11):
        path = Path(x, y)
        row.append(path)
    field.append(row)

for i in field:
    for i in field:
        print(i[0].get_element(), end=' ')
    print()

print()

for row in field:
    for i in row:
        i.update_pose(field)
        # print(i.pose, end='')
        print(i.get_element(), end=' ')
    print()