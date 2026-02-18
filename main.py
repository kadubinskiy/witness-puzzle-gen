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

    def generate_bounds(self, seed):
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
                        self.seed.append([randint(0, self.cols-1), randint(0, self.rows-1)])
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
            if corner == 0:
                for i in range(coordinates[0]):
                    self.field[i][coordinates[1]-1] = '*'
                for i in range(coordinates[1]):
                    self.field[coordinates[0]-1][i] = '*'
            if corner == 1:
                for i in range(coordinates[0]):
                    self.field[i][coordinates[1]-1] = '*'
                for i in range(self.rows-coordinates[1]+1):
                    self.field[coordinates[0]-1][coordinates[1]-1+i] = '*'
            if corner == 2:
                for i in range(self.cols-coordinates[0]+1):
                    self.field[coordinates[0]-1+i][coordinates[1]-1] = '*'
                for i in range(coordinates[1]):
                    self.field[coordinates[0]-1][i] = '*'
            if corner == 3:
                for i in range(self.cols-coordinates[0]+1):
                    self.field[coordinates[0]-1+i][coordinates[1]-1] = '*'
                for i in range(self.rows-coordinates[1]+1):
                    self.field[coordinates[0]-1][coordinates[1]-1+i] = '*'
    
    def fill_gaps(self):
        if self.broken_corner_list.index(0):
            if self.broken_corner_list.index(1):
                for i in range()
                self.field[0]
        else:
            if not self.broken_corner_list.index(1):
                for i in range(len(self.field[0])):
                    self.field[0][i] = '*'
        self.field[-1]

    def draw_raw(self):
        for i in range(len(self.field)):
            print(self.field[i])

    def draw_game(self):
        for i in range(len(self.field)):
            for n in self.field[i]:
                if n == [None]:
                    print(" ", end="")
                if n == '*':
                    print("*", end="")
            print("\n", end="")

    
puzzle = Puzzle()
puzzle.generate_field(7, 7)
puzzle.generate_bounds(seed=[8, 8, 4, 4, [3, 3], [3, 5]])
puzzle.populate_matrix()
puzzle.fill_gaps()
puzzle.draw_game()


# seed = [top-left, top-right, bottom-left, bottom-right, first_corner([y, x])...]