import pygame
import math
from queue import PriorityQueue
from queue import Queue

WIDTH = 800
ROWS = 50
win = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.colour = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_cord(self):
        return self.row, self.col

    def is_closed(self):
        return self.colour == RED

    def is_open(self):
        return self.colour == PURPLE

    def is_barrier(self):
        return self.colour == BLACK

    def is_start(self):
        return self.colour == ORANGE

    def is_end(self):
        return self.colour == TURQUOISE

    def is_path(self):
        return self.colour == GREEN

    def reset(self):
        self.colour = WHITE

    def make_closed(self):
        self.colour = RED

    def make_open(self):
        self.colour = PURPLE

    def make_barrier(self):
        self.colour = BLACK

    def make_end(self):
        self.colour = TURQUOISE

    def make_start(self):
        self.colour = ORANGE

    def make_path(self):
        self.colour = GREEN

    def draw(self, win):
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # Down
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # Up
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():  # Right
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # Left
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def make_path(came_from, start, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        if current == start:
            current.make_start()
        draw()


def algorithmn(draw, grid, start, end):
    count = 0
    open_set = Queue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h(start.get_cord(), end.get_cord())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            current.make_end()
            make_path(came_from, start, end, draw)
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_cord(), end.get_cord())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()
        if current != start:
            current.make_closed()

    return False

def depth_first_search(draw, grid, start, end):
    visited = [[False for j in range(ROWS)] for i in range(ROWS)]
    distance = [[-1 for j in range(ROWS)] for i in range(ROWS)]
    discovered = [[(0, 0) for j in range(ROWS)] for i in range(ROWS)]
    count = 0
    open_set = Queue()

    col, row = start.get_cord
    visited[col][row] = True
    distance[col][row] = 0
    discovered[col][row] = (col, row)
    open_set.put(start)

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()
        open_set.remove(current)

        if current == end:
            current.make_end()
            make_path(came_from, start, end, draw)
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_cord(), end.get_cord())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()
        if current != start:
            current.make_closed()

    return False



def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)

    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
    for j in range(rows):
        pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()


def click_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap
    return row, col


def main(win, width):
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    started = False

    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = click_pos(pos, ROWS, width)
                node = grid[row][col]
                if not start:
                    start = node
                    start.make_start()
                    if node == end:
                        end = None

                elif not end:
                    end = node
                    end.make_end()
                    if node == start:
                        start = None

                elif node != end and node != start:
                    node.make_barrier()



            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = click_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    algorithmn(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
    pygame.quit()


main(win, WIDTH)
