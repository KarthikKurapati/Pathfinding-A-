import pygame
import math
from queue import PriorityQueue

WIDTH = 1600
WIN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("A* Pathfinding Algorithm -- Karthik Kurapati")


RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)
PALEGREEN = (137,172,118)
MAP = [[0]] #put map here
CLASSROOMMAP = [2217,2218,2219,2216,3200,2215,3000,2213,2214,2221,2220,2212,2223,2222,2211,3201,3202,2211.01,2210,3001,2210.06,3002,3003,2201,2208,2209,2210.5,2327,2207,2206,2205,2204,2203,3203,2202,3204,2118,2117,6000,6001,6002,6003,6004]
CLASSROOMMAPCopy = CLASSROOMMAP.copy()
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 12)
class Node :
    def __init__(self, row, col, width, total_rows,color):
        self.row=row
        self.col=col
        self.x=row*width
        self.y=col*width
        self.color= color
        self.neighbors=[]
        self.width=width
        self.total_rows=total_rows
    def get_x(self):
         return self.x
    def get_y(self):
         return self.y
    def get_color(self):
        return self.color
    def get_pos(self):
        return self.row,self.col
    def is_closed(self):
        return self.color == RED
    def is_open(self):
        return self.color == GREEN
    def is_barrier(self):
        return self.color == BLACK
    def is_start(self):
        return self.color == ORANGE
    def is_end(self):
        return self.color == TURQUOISE
    def reset(self):
        self.color = WHITE
    def make_start(self):
        self.color = ORANGE
    def make_closed(self):
        self.color = RED
    def make_open(self):
        self.color = GREEN
    def make_barrier(self):
        self.color= BLACK
    def make_end(self):
        self.color = TURQUOISE
    def make_path(self):
        self.color = PURPLE
    def make_classroom(self):
        self.color = PALEGREEN
    def draw(self,win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
    def get_roomNumber(self):
        return 0
    def isClassroom(self):
        return False
    def update_neighbors(self,grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])
    def __lt__(self, other):
        return False
class Classroom(Node):
    def __init__(self, row, col, width, total_rows,color,roomNumber):
        self.row=row
        self.col=col
        self.x=row*width
        self.y=col*width
        self.color= PALEGREEN
        self.neighbors=[]
        self.width=width
        self.total_rows=total_rows
        self.roomNumber = roomNumber
        self.isClassroom = True
    def get_roomNumber(self):
        return self.roomNumber
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
        text_surface = font.render(str(self.roomNumber), False,BLACK)
        WIN.blit(text_surface,(self.x,self.y))
    def is_barrier(self):
        return self.color == PALEGREEN
    def isClassroom(self):
        return True


    
def h(p1,p2):
    x1,y1 = p1
    x2,y2 = p2
    return abs(x1-x2) + abs(y1 - y2)

def algorithm(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	came_from = {}
	g_score = {spot: float("inf") for row in grid for spot in row}
	g_score[start] = 0
	f_score = {spot: float("inf") for row in grid for spot in row}
	f_score[start] = h(start.get_pos(), end.get_pos())

	open_set_hash = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2]
		open_set_hash.remove(current)

		if current == end:
			reconstruct_path(came_from, end, draw)
			end.make_end()
			return True

		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + 1

			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()

		draw()

		if current != start:
			current.make_closed()

	return False
def reconstruct_path(came_from, current, draw):
     while current in came_from:
          current = came_from[current]
          current.make_path()
          draw()
def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i , j,gap,rows,WHITE)
            grid[i].append(node)

    return grid
def make_definedGrid(rows,width):
    CLASSROOMMAP =CLASSROOMMAPCopy.copy()
    grid = []
    gap = width // rows
    start = None
    end = None
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            if (MAP[j][i] == 1):
                node = Node(i , j,gap,rows,BLACK)
                grid[i].append(node)
            if (MAP[j][i] == 0):
                node = Node(i , j,gap,rows, WHITE)
                grid[i].append(node)
            if (MAP[j][i] == 2):
                node = Node(i , j,gap,rows,ORANGE)
                grid[i].append(node)
                end = grid[i][j]
            if (MAP[j][i] == 3):
                node = Node(i , j,gap,rows,TURQUOISE)
                grid[i].append(node)
                start= grid[i][j]
            if (MAP[j][i] == 4):
                node = Classroom(i , j,gap,rows,PALEGREEN,CLASSROOMMAP[0])
                CLASSROOMMAP.pop(0)
                grid[i].append(node)
    return start,end,grid
def draw_grid(win,rows,width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win,GREY,(0, i * gap),(width, i * gap))
        for j in range(rows):
            pygame.draw.line(win,GREY,(j * gap, 0),(j * gap,width))

def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(win)
    draw_grid(win,rows,width)
    pygame.display.update()
def get_clicked_pos(pos,rows,width):
    gap = width // rows
    y , x = pos

    row = y // gap
    col = x // gap

    return row, col
def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS , width)

    start = None
    end = None

    run = True
    started = False

    while run:
        draw(win,grid,ROWS,width)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if started:
                continue
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row,col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.make_start()
                elif not end and node != start:
                    end = node
                    end.make_end()
                elif node != end and node != start:
                    node.make_barrier()
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row,col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    
                    algorithm(lambda: draw(win,grid,ROWS,width), grid,start, end)
                if event.key == pygame.K_c:
                     start = None
                     end = None
                     grid = make_grid(ROWS, width)
                if event.key == pygame.K_1:
                     for row in grid:
                          for node in row:
                               print(node.get_color(), end = ',')
                if event.key == pygame.K_2:
                    for i in range(len(grid[0])):
                        for row in grid:
                            node = row[i]
                            if node.get_color() == WHITE:
                                print("0", end=',')
                            elif node.get_color() == BLACK:
                                print("1", end=',')
                            elif node.get_color() == ORANGE:
                                print("2", end=',')
                            elif node.get_color() == TURQUOISE:
                                print("3", end=',')
                            elif node.get_color() == PALEGREEN:
                                print("4", end=',')
                        print(";",end='')
                if event.key == pygame.K_3:
                    end,start,grid = make_definedGrid(ROWS, width)
                if event.key == pygame.K_g:
                    pos = pygame.mouse.get_pos()
                    row,col = get_clicked_pos(pos, ROWS, width)
                    node = grid[row][col]
                    node.make_classroom()
                if event.key == pygame.K_f:
                    pos = pygame.mouse.get_pos()
                    row,col = get_clicked_pos(pos, ROWS, width)
                    node = grid[row][col]
                    if (node.isClassroom == True):
                        print(node.get_roomNumber())
                if event.key == pygame.K_4:
                    start,end,grid = make_definedGrid(ROWS,width)
                    pygame.display.update()
                    start1 = int(input("What is your starting location?"))
                    end1 = int(input("What is your ending location?"))
                    for i in range (ROWS):
                         for j in range (ROWS):
                            if(MAP[j][i] == 4):
                                if(grid[i][j].get_roomNumber() == start1):
                                    grid[i][j].make_start()
                                    start = grid[i][j]
                                if(grid[i][j].get_roomNumber() == end1):
                                    grid[i][j].make_end()
                                    end = grid[i][j]
    pygame.quit()
     
main(WIN,WIDTH)