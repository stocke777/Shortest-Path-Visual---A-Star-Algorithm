from queue import PriorityQueue
from collections import defaultdict
import pygame, math
from random import randint

pygame.init()

WHITE = (255, 255, 255)
WIN = pygame.display.set_mode((800, 800))
pygame.display.set_caption("A Star Algo")

class spot:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        self.d = {
            "unused" : (0, 0, 0),
            "start" : (255, 0, 0),
            "end" : (0, 255, 0),
            "path" : (0, 0, 255),
            "pq" : (255, 255, 0),
            "used" : (255, 0, 255),
            "ans" : (0, 255, 255)
        }
    def draw(self):
        pygame.draw.rect(WIN,self.d[self.type],(self.x*16,self.y*16,16,16))
        
grid = [[spot(i, j, "unused") for j in  range(50)] for i in range(50)]

def game():
    ck = pygame.time.Clock()
    run = True
    start = False
    end = False
    path = False


    def find_path(sx, sy, ex, ey):

        def h(point1, point2):
            x, y = point1
            a, b = point2
            return abs(x-a)+abs(y-b)
        
        def drawstep():
            WIN.fill((0, 0, 0))

            for row in grid:
                for spot in row:
                    spot.draw()

            for i in range(50):
                pygame.draw.line(WIN, WHITE, (i*16, 0), (i*16, 800), 1)
            for i in range(50):
                pygame.draw.line(WIN, WHITE, (0, i*16), (800, i*16), 1)

            pygame.display.update()


        print(sx, sy, ex, ey)
        start = (sx, sy)
        end = (ex, ey)
        pq = PriorityQueue()

        g_score = defaultdict(lambda: float("inf"))
        g_score[start] = 0

        f_score = defaultdict(lambda: float("inf"))
        f_score[start] = g_score[start] + h(start, end)

        pq.put((f_score[start], start, g_score[start], h(start, end)))

        pq_hash = set()
        pq_hash.add(start)
        grid[start[0]][start[1]].type = "pq"

        came_from = dict()

        f = 0
        
        # print(pq, f_score, g_score)

        while not pq.empty():
            
            # print(pq_hash)
            current = pq.get()
            print(current)
            grid[current[1][0]][current[1][1]].type = "used"
            grid[start[0]][start[1]].type = "start"

            if (grid[current[1][0]][current[1][1]].x, grid[current[1][0]][current[1][1]].y)==end:
                print("last reached\n")
                grid[end[0]][end[1]].type = "end"
                f = 1
                break
            
            x = [0, 0, 1, -1]
            y = [1, -1, 0, 0]

            pq_hash.remove(current[1])

            for r, c in zip(x, y):

                if 0<=current[1][0]+r<=49 and 0<=current[1][1]+c<=49:

                    temp_g_score = current[2] + 1
                    if temp_g_score < g_score[(r+current[1][0], c+current[1][1])]:
                        came_from[(r+current[1][0], c+current[1][1])] = current[1]
                        g_score[(r+current[1][0], c+current[1][1])] = temp_g_score

                        f_score[(r+current[1][0], c+current[1][1])] = g_score[(r+current[1][0], c+current[1][1])] + h((r+current[1][0], c+current[1][1]), end)

                        if ((r+current[1][0], c+current[1][1]) not in pq_hash) and grid[r+current[1][0]][c+current[1][1]].type!="path":
                            pq.put((f_score[(r+current[1][0], c+current[1][1])], (r+current[1][0], c+current[1][1]), temp_g_score,h((r+current[1][0], c+current[1][1]), end)))
                            pq_hash.add((r+current[1][0], c+current[1][1]))
                            grid[r+current[1][0]][c+current[1][1]].type = "pq"
            drawstep()

        if not f:
            print("failed")		
        else:
            print("passed")
            print(came_from)
            while True:
                x, y = came_from[end]
                if (x, y) == start:
                    break
                grid[x][y].type = "ans"
                end = (x, y)
            drawstep()

    def redraw():
        WIN.fill((0, 0, 0))

        for row in grid:
            for spot in row:
                spot.draw()

        for i in range(50):
            pygame.draw.line(WIN, WHITE, (i*16, 0), (i*16, 800), 1)
        for i in range(50):
            pygame.draw.line(WIN, WHITE, (0, i*16), (800, i*16), 1)

        pygame.display.update()

    while run:
        
        ck.tick(200)

        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                x, y = x//16, y//16
                if not start:
                    start = True
                    grid[x][y].type = "start"
                    start_x, start_y = x, y
                if not end:
                    if grid[x][y].type != "start":
                        grid[x][y].type = "end"
                        end_x, end_y = x, y
                        end = True
                print("Mouse pressed", x, y)

        path_list = set()
        if keys[pygame.K_SPACE] and path==False:
            print("loop1")
            if start and end:
                print("loop2")
                x, y = pygame.mouse.get_pos()
                x, y = x//16, y//16
                print(x, y)
                if (x, y) not in path_list:
                    path_list.add((x, y))
                    print(path_list)
                    for (x, y) in path_list:
                        grid[x][y].type = "path"
        
        if keys[pygame.K_RETURN]:
            path = True
            print("Enter")
            find_path(start_x, start_y, end_x, end_y)
            
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        print("Ending the Program")
                        exit()

        redraw()

game()

