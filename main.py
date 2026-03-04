from time import sleep
from random import randint

class Puzzle():
    def generate_field(self, cols, rows):
        self.field = []
        self.cols = cols
        self.rows = rows
        for i in range(rows):
            row = []
            for i in range(cols):
                row.append([None])
            self.field.append(row)
        return self.field

    def generate_coords(self, flag1 = False, flag2 = False):
        half_rows = int(self.rows/4)
        half_cols = int(self.cols/4)
        multiplier1, multiplier2 = 1, 1
        adjuster1, adjuster2 = 0, 0
        if flag1:
            multiplier1 = -1
            adjuster1 = 1
        if flag2:
            multiplier2 = -1
            adjuster2 = 1
        coordinate1 = (multiplier1*randint(2, half_cols)*2)-adjuster1
        coordinate2 = (multiplier2*randint(2, half_rows)*2)-adjuster2
        return [coordinate1, coordinate2]

    def generate_bounds(self, seed=None):
        if not seed:
            self.broken_corner_list = []
            self.seed = []
            for i in range(4):
                self.seed.append(randint(0, 9))
            temp = self.seed.copy()
            if self.field and self.cols and self.rows:
                counter = 0
                for corner in temp:
                    if corner > 7:
                        if counter == 0:
                            self.seed.append(self.generate_coords())
                        if counter == 1:
                            self.seed.append(self.generate_coords(True, False))
                        if counter == 2:
                            self.seed.append(self.generate_coords(False, True))
                        if counter == 3:
                            self.seed.append(self.generate_coords(True, True))
                        self.broken_corner_list.append(counter)
                    counter += 1
        elif seed:
            self.seed = seed
            self.broken_corner_list = []
            temp = self.seed[0:4]
            if self.field and self.cols and self.rows:
                counter = 0
                for corner in temp:
                    if corner > 7:
                        self.broken_corner_list.append(counter)
                    counter += 1
            
    def populate_matrix(self):
        for i in range(len(self.broken_corner_list)):
            corner = self.broken_corner_list[i]
            coordinates = [self.seed[i+4][0], self.seed[i+4][1]]
            print(corner, ':', coordinates)
            if corner == 0:
                for i in range(coordinates[0]):
                    self.field[i][coordinates[1]] = '*'
                for i in range(coordinates[1]):
                    self.field[coordinates[0]][i] = '*'
            if corner == 1:
                for i in range(coordinates[0]):
                    self.field[i][coordinates[1]] = '*'
                for i in range(self.rows-coordinates[1]):
                    self.field[coordinates[0]][coordinates[1]+i] = '*'
            if corner == 2:
                for i in range(self.cols-coordinates[0]):
                    self.field[coordinates[0]+i][coordinates[1]] = '*'
                for i in range(coordinates[1]):
                    self.field[coordinates[0]][i] = '*'
            if corner == 3:
                for i in range(self.cols-coordinates[0]):
                    self.field[coordinates[0]+i][coordinates[1]] = '*'
                for i in range(self.rows-coordinates[1]):
                    self.field[coordinates[0]][coordinates[1]+i] = '*'
        if 0 not in self.broken_corner_list:
            self.field[0][0] = '*'
        if 1 not in self.broken_corner_list:
            self.field[0][-1] = '*'
        if 2 not in self.broken_corner_list:
            self.field[-1][0] = '*'
        if 3 not in self.broken_corner_list:
            self.field[-1][-1] = '*'
    
    def unindex(self, list, value):
        for i in range(len(list)):
            if list[-1*(i+1)] == value:
                return -1*(i+1)

    def fill_row(self, row_n):
        left = self.field[row_n].index('*')
        right = self.unindex(self.field[row_n], '*')
        for index in range(left, len(self.field[row_n])+right):
            self.field[row_n][index] = '*'

    def fill_column(self, column_n):
        updown = []
        for i in range(self.rows):
            if self.field[i][column_n] == '*':
                updown.append(i)
        for index in range(updown[0], updown[-1]):
            self.field[index][column_n] = '*'

    def fill_bounds(self):
        self.fill_row(0)
        self.fill_row(-1)
        self.fill_column(0)
        self.fill_column(-1)

    def draw_raw(self):
        for i in range(len(self.field)):
            print(self.field[i])

    def draw_game(self):
        for i in range(len(self.field)):
            for n in self.field[i]:
                if n == [None]:
                    print("  ", end="")
                if n == '*':
                    print("* ", end="")
            print("\n", end="")

    
puzzle = Puzzle()
puzzle.generate_field(11, 11)
puzzle.generate_bounds()
puzzle.populate_matrix()
puzzle.fill_bounds()
puzzle.fill_row(2)
puzzle.fill_row(4)
puzzle.fill_row(6)
puzzle.fill_row(8)
puzzle.fill_column(2)
puzzle.fill_column(4)
puzzle.fill_column(6)
puzzle.fill_column(8)

puzzle.draw_game()


# seed = [top-left, top-right, bottom-left, bottom-right, first_corner([y, x])...]
# seed=[8, 8, 4, 4, [3, 3], [3, 5]]