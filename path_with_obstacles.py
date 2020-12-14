import pygame, sys, random, math
from collections import deque
from tkinter import messagebox, Tk
import pygame.freetype

size = (width, height) = 640, 480
pygame.init()
win = pygame.display.set_mode((640,600))
pygame.display.set_caption("Dijkstra's Path Finding")
clock = pygame.time.Clock()
cols, rows = 64, 48
w = width // cols
h = height // rows
grid = []
queue, visited = deque(), []
path = []
GAME_FONT = pygame.freetype.Font("fonts\\MyUnderwood.ttf",24)
INFO_FONT = pygame.freetype.Font("fonts\\MyUnderwood.ttf",15)

class Spot:
    def __init__(self, i, j):
        self.x, self.y = i, j
        self.f, self.g, self.h = 0, 0, 0
        self.neighbors = []
        self.prev = None
        self.wall = False
        self.visited = False
        #### Comment below two lines for 30% wall nodes ####
        if random.randint(0, 100) < 30:
            self.wall = True

    def show(self, win, col, shape=1):
        if self.wall == True:
            col = (0, 0, 0)
        if shape == 1:
            pygame.draw.rect(win, col, (self.x * w, self.y * h, w - 1, h - 1))
        else:
            pygame.draw.circle(win, col, (self.x * w + w // 2, self.y * h + h // 2), w // 3)

    def add_neighbors(self, grid):
        if self.x < cols - 1:
            self.neighbors.append(grid[self.x + 1][self.y])
        if self.x > 0:
            self.neighbors.append(grid[self.x - 1][self.y])
        if self.y < rows - 1:
            self.neighbors.append(grid[self.x][self.y + 1])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y - 1])

for i in range(cols):
    arr = []
    for j in range(rows):
        arr.append(Spot(i, j))
    grid.append(arr)

for i in range(cols):
    for j in range(rows):
        # if random.randint(1,10) == 1:
        #     continue
        grid[i][j].add_neighbors(grid)

start = grid[cols // 2][rows // 2]
#end = grid[cols - 50][rows - cols // 2]
end = grid[cols//2][rows - cols // 2]
start.wall = False
end.wall = False

def main():
    global start
    global end
    global queue
    global visited
    flag = False
    noflag = True
    startflag = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    screen_pos = pygame.mouse.get_pos()
                    start = grid[int(screen_pos[0]/10)][int(screen_pos[1]/10)]
                    queue, visited = deque(), []
                    queue.append(start)
                    start.visited = True
                if event.button == 3:
                    screen_pos = pygame.mouse.get_pos()
                    end = grid[int(screen_pos[0]/10)][int(screen_pos[1]/10)]

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    startflag = True

        if startflag:
            if len(queue) > 0:
                current = queue.popleft()
                if current == end:
                    temp = current
                    while temp.prev:
                        path.append(temp.prev)
                        temp = temp.prev
                    if not flag:
                        flag = True
                        print("Done")
                    elif flag:
                        continue
                if flag == False:
                    for i in current.neighbors:
                        if not i.visited and not i.wall:
                            i.visited = True
                            i.prev = current
                            queue.append(i)
            else:
                if noflag and not flag:
                    Tk().wm_withdraw()
                    messagebox.showinfo("No Solution", "There was no solution")
                    noflag = False
                else:
                    continue

        win.fill((0, 20, 20))
        pygame.draw.rect(win,(208, 208, 208),(0,481,640,120))
        pygame.draw.rect(win,(39, 174, 96),(100,500,24,24)) #visited
        pygame.draw.rect(win,(192, 57, 43),(100,530,24,24)) #final path
        pygame.draw.rect(win,(44, 62, 80),(375,500,24,24))  #not visited
        pygame.draw.rect(win,(0, 0, 0),(375,530,24,24))     #path blocked
        
        #rendering text
        GAME_FONT.render_to(win, (134, 500), "Node Visited", (39, 174, 96))
        GAME_FONT.render_to(win, (134, 530), "Final Path", (192, 57, 43))
        GAME_FONT.render_to(win, (374+34, 500), "Node Not Visited", (44, 62, 80))
        GAME_FONT.render_to(win, (375+34, 530), "Node Blocked", (0, 0, 0))
        INFO_FONT.render_to(win, (20, 560), "Left Click: Select starting node ", (39, 174, 96))
        INFO_FONT.render_to(win, (350, 560), "Right Click: Select ending node ", (0, 120, 255))
        INFO_FONT.render_to(win, (200, 580), "Enter: Start Pathfinding", (0, 0, 0))

        for i in range(cols):
            for j in range(rows):
                spot = grid[i][j]
                spot.show(win, (44, 62, 80))
                if spot in path:
                    spot.show(win, (192, 57, 43))
                elif spot.visited:
                    spot.show(win, (39, 174, 96))
                if spot in queue:
                    spot.show(win, (44, 62, 80))
                    spot.show(win, (39, 174, 96), 0)
                if spot == start:
                    spot.show(win, (0, 255, 200))
                if spot == end:
                    spot.show(win, (0, 120, 255))

        pygame.display.flip()

if __name__ == "__main__":
    main()
