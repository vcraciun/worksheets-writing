import random
from PIL import Image, ImageDraw
import numpy as np

class Cell:
    def __init__(self):
        self.north = True
        self.south = True
        self.east = True
        self.west = True
        self.visited = False

class Maze:
    def __init__(self, width=20, height=20, cell_width=50, index = 0):
        self.width = width
        self.height = height
        self.cell_width = cell_width
        self.cells = [[Cell() for _ in range(height)] for _ in range(width)]
        self.index = index

    def generate(self):
        x, y = random.choice(range(self.width)), random.choice(range(self.height))
        self.cells[x][y].visited = True
        path = [(x, y)]

        while not all(all(c.visited for c in cell) for cell in self.cells):
            x, y = path[len(path) - 1][0], path[len(path) - 1][1]

            good_adj_cells = []
            if self.exists(x, y - 1) and not self.cells[x][y - 1].visited:
                good_adj_cells.append('north')
            if self.exists(x, y + 1) and not self.cells[x][y + 1].visited:
                good_adj_cells.append('south')
            if self.exists(x + 1, y) and not self.cells[x + 1][y].visited:
                good_adj_cells.append('east')
            if self.exists(x - 1, y) and not self.cells[x - 1][y].visited:
                good_adj_cells.append('west')

            if good_adj_cells:
                go = random.choice(good_adj_cells)
                if go == 'north':
                    self.cells[x][y].north = False
                    self.cells[x][y - 1].south = False
                    self.cells[x][y - 1].visited = True
                    path.append((x, y - 1))
                if go == 'south':
                    self.cells[x][y].south = False
                    self.cells[x][y + 1].north = False
                    self.cells[x][y + 1].visited = True
                    path.append((x, y + 1))
                if go == 'east':
                    self.cells[x][y].east = False
                    self.cells[x + 1][y].west = False
                    self.cells[x + 1][y].visited = True
                    path.append((x + 1, y))
                if go == 'west':
                    self.cells[x][y].west = False
                    self.cells[x - 1][y].east = False
                    self.cells[x - 1][y].visited = True
                    path.append((x - 1, y))
            else:
                path.pop()

    def exists(self, x, y):
        if x < 0 or x > self.width - 1 or y < 0 or y > self.height - 1:
            return False
        return True

    def get_direction(self, direction, x, y):
        if direction == 'north':
            return x, y - 1
        if direction == 'south':
            return x, y + 1
        if direction == 'east':
            return x + 1, y
        if direction == 'west':
            return x - 1, y

    def draw(self):
        canvas_width, canvas_height = self.cell_width * self.width + 1, self.cell_width * self.height + 1
        a = np.full((canvas_height, canvas_width, 3), 255, dtype=np.uint8)
        im = Image.fromarray(a, 'RGB')
        #im = Image.new('RGB', (canvas_width, canvas_height))
        draw = ImageDraw.Draw(im)

        for x in range(self.width):            
            for y in range(self.height):
                if self.cells[x][y].north:
                    draw.line((x * self.cell_width, y * self.cell_width, (x + 1) * self.cell_width, y * self.cell_width), fill=0, width=3)
                if self.cells[x][y].south:
                    draw.line((x * self.cell_width, (y + 1) * self.cell_width, (x + 1) * self.cell_width,(y + 1) * self.cell_width), fill=0, width=3)
                if self.cells[x][y].east:
                    draw.line(((x + 1) * self.cell_width, y * self.cell_width, (x + 1) * self.cell_width,(y + 1) * self.cell_width), fill=0, width=3)
                if self.cells[x][y].west:
                    draw.line((x * self.cell_width, y * self.cell_width, x * self.cell_width, (y + 1) * self.cell_width), fill=0, width=3)
        shape1 = [(canvas_width - self.cell_width + 10, canvas_height - self.cell_width + 10), (canvas_width - 10, canvas_height - 10)]
        shape2 = [(10, 10), (self.cell_width - 10, self.cell_width - 10)]
        draw.rectangle(shape1, fill="#00FF00", outline='black')
        draw.rectangle(shape2, fill="#FF0000", outline='black')
        im.save(f"labirint_{self.width}x{self.height}_{self.index:>03}.png")

if __name__ == '__main__':
    for size in [7, 10, 12, 15, 17, 20, 22, 25, 27, 30]:
        for i in range(10):
            maze = Maze(size, size, 50, i)
            maze.generate()
            maze.draw()
          