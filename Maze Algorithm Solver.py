import pygame
import random

pygame.init()

gui = (650, 650)
screen = pygame.display.set_mode(gui)
pygame.display.set_caption("Maze Algorithm Solver")

YELLOW = (255, 255, 0) 
BLACK = (50, 50, 100)    
GREEN = (124, 252, 0)   
RED = (100, 149, 237) 
PEACH = (255, 223, 186) 

speed = 1
map_size = 60
size = gui[0] // map_size

class Cell:
    def __init__(self) -> None:
        self.neighbor: list = []
        self.generated: bool = False
        self.visited: bool = False

    def add_neig(self, neighbor: str) -> None:
        self.neighbor.append(neighbor)

    def add_gen(self) -> None:
        self.generated = True

    def add_vist(self) -> None:
        self.visited = True

    def get_neighbor(self) -> list:
        return self.neighbor

    def get_generated(self) -> bool:
        return self.generated

    def get_visited(self) -> bool:
        return self.visited

class Maze:
    def __init__(self, map_size, size) -> None:
        self.map_size: int = map_size
        self.size: int = size
        self.maze: list[Cell] = [Cell() for _ in range(self.map_size * self.map_size)]
        self.path: list[tuple[int, int]] = list()

    def at(self, x: int, y: int) -> Cell:
        return self.maze[y * self.map_size + x]

    def generate(self) -> None:
        visited: int = 0
        stack: list[tuple[int, int]] = list()

        x: int = random.randint(0, self.map_size - 1)
        y: int = random.randint(0, self.map_size - 1)
        stack.append((x, y))
        self.at(x, y).add_gen()
        visited += 1

        while visited < self.map_size * self.map_size:
            x = stack[-1][0]
            y = stack[-1][1]

            neighbor: list[str] = list()

            if x > 0 and self.at(x - 1, y).get_generated() is False:
                neighbor.append('left')
            if x < self.map_size - 1 and self.at(x + 1, y).get_generated() is False:
                neighbor.append('right')
            if y > 0 and self.at(x, y - 1).get_generated() is False:
                neighbor.append('up')
            if y < self.map_size - 1 and self.at(x, y + 1).get_generated() is False:
                neighbor.append('down')

            if len(neighbor) > 0:
                random_next: str = random.choice(neighbor)

                if random_next == 'left':
                    self.at(x, y).add_neig('left')
                    self.at(x - 1, y).add_neig('right')
                    self.at(x - 1, y).add_gen()
                    stack.append((x - 1, y))
                elif random_next == 'right':
                    self.at(x, y).add_neig('right')
                    self.at(x + 1, y).add_neig('left')
                    self.at(x + 1, y).add_gen()
                    stack.append((x + 1, y))
                elif random_next == 'up':
                    self.at(x, y).add_neig('up')
                    self.at(x, y - 1).add_neig('down')
                    self.at(x, y - 1).add_gen()
                    stack.append((x, y - 1))
                elif random_next == 'down':
                    self.at(x, y).add_neig('down')
                    self.at(x, y + 1).add_neig('up')
                    self.at(x, y + 1).add_gen()
                    stack.append((x, y + 1))
                visited += 1
            else:
                stack.pop()

    def solve(self, show: bool = True, speed: int = 10, vist_show: bool = True) -> list[tuple[int, int]]:
        stack: list[tuple[int, int]] = list()

        x: int = 0
        y: int = 0
        stack.append((x, y))
        self.at(x, y).add_vist()

        while x != self.map_size - 1 or y != self.map_size - 1:
            x = stack[-1][0]
            y = stack[-1][1]
            self.at(x, y).add_vist()

            backtrack: bool = True
            neighbor: list[str] = self.at(x, y).get_neighbor()

            for go_to in neighbor:
                if go_to == 'left' and self.at(x - 1, y).get_visited() is False:
                    stack.append((x - 1, y))
                    backtrack = False
                elif go_to == 'right' and self.at(x + 1, y).get_visited() is False:
                    stack.append((x + 1, y))
                    backtrack = False
                elif go_to == 'up' and self.at(x, y - 1).get_visited() is False:
                    stack.append((x, y - 1))
                    backtrack = False
                elif go_to == 'down' and self.at(x, y + 1).get_visited() is False:
                    stack.append((x, y + 1))
                    backtrack = False

            if backtrack is True:
                stack.pop()

            if show is True:
                self.show(vist_show=vist_show)
                pygame.draw.rect(screen, GREEN, (x * self.size, y * self.size, self.size, self.size))
                pygame.display.flip()
                pygame.time.delay(speed)

        self.path = stack
        if (self.map_size - 1, self.map_size - 1) not in self.path: self.path += [(self.map_size - 1, self.map_size - 1)]

        return self.__get_path()

    def __get_path(self) -> list[tuple[int, int]]:
        self.__remove_ghost_path()
        return self.path

    def __remove_ghost_path(self) -> None:
        remove: list = list()
        for i in range(1, len(self.path)):
            x = self.path[i][0]
            y = self.path[i][1]

            count: int = 0
            neighbor: list[str] = self.at(x, y).get_neighbor()

            for go_to in neighbor:
                if go_to == 'left' and (x - 1, y) not in self.path:
                    count += 1
                elif go_to == 'right' and (x + 1, y) not in self.path:
                    count += 1
                elif go_to == 'up' and (x, y - 1) not in self.path:
                    count += 1
                elif go_to == 'down' and (x, y + 1) not in self.path:
                    count += 1

            if len(neighbor) - count == 1:
                remove.append(i)

        for i in remove[::-1]:
            self.path.pop(i)

        if (self.map_size - 1, self.map_size - 1) not in self.path:
            self.path += [(self.map_size - 1, self.map_size - 1)]

    def show(self, vist_show: bool = False) -> None:
        screen.fill(PEACH)
        for y in range(self.map_size):
            for x in range(self.map_size):
                cell = self.at(x, y)
                if vist_show is True and cell.get_visited() is True:
                    pygame.draw.rect(screen, YELLOW, (x * self.size, y * self.size, self.size, self.size))
                if 'left' not in cell.neighbor:
                    pygame.draw.line(screen, BLACK, (x * self.size, y * self.size), (x * self.size, (y + 1) * self.size))
                if 'right' not in cell.neighbor:
                    pygame.draw.line(screen, BLACK, ((x + 1) * self.size, y * self.size), ((x + 1) * self.size, (y + 1) * self.size))
                if 'up' not in cell.neighbor:
                    pygame.draw.line(screen, BLACK, (x * self.size, y * self.size), ((x + 1) * self.size, y * self.size))
                if 'down' not in cell.neighbor:
                    pygame.draw.line(screen, BLACK, (x * self.size, (y + 1) * self.size), ((x + 1) * self.size, (y + 1) * self.size))
        for x, y in self.path:
            pygame.draw.circle(screen, RED, (x * size + size / 2, y * size + size / 2), 0.2 * size)
        pygame.display.flip()

def main() -> None:
    map= Maze(map_size, size)
    map.generate()
    solution_path = map.solve(True, speed, True)
    print('Solution path: ', solution_path)
    map.show(True)

    run1 = True
    while run1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run1 = False

if __name__ == '__main__':
    main()
