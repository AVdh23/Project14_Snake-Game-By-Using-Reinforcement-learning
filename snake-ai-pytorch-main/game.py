import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()
font = pygame.font.Font('arial.ttf', 25)
# font = pygame.font.SysFont('arial', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

# rgb colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)

BLOCK_SIZE = 20
SPEED = 40

class SnakeGameAI:

    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.reset()


    def reset(self):
        # init game state
        self.direction = Direction.RIGHT

        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head,
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]

        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0


    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()


    def play_step(self, action):
        self.frame_iteration += 1
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        # 2. move
        self._move(action) # update the head
        self.snake.insert(0, self.head)
        
        # 3. check if game over
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()
        
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return reward, game_over, self.score


    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # hits boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        # hits itself
        if pt in self.snake[1:]:
            return True

        return False


    def _update_ui(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))

        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        # Load and blit the graphics
        body_horizontal = pygame.image.load("C:\\Users\\Acer pc\\Downloads\\snake-ai-pytorch-main\\snake-ai-pytorch-main\\Graphics\\body_horizontal.png")
        body_tl = pygame.image.load("C:\\Users\\Acer pc\\Downloads\\snake-ai-pytorch-main\\snake-ai-pytorch-main\\Graphics\\body_tl.png")
        body_tr = pygame.image.load("C:\\Users\\Acer pc\\Downloads\\snake-ai-pytorch-main\\snake-ai-pytorch-main\\Graphics\\body_tr.png")
        body_vertical = pygame.image.load("C:\\Users\\Acer pc\\Downloads\\snake-ai-pytorch-main\\snake-ai-pytorch-main\\Graphics\\body_vertical.png")
        head_down = pygame.image.load("C:\\Users\\Acer pc\\Downloads\\snake-ai-pytorch-main\\snake-ai-pytorch-main\\Graphics\\head_down.png")
        head_left = pygame.image.load("C:\\Users\\Acer pc\\Downloads\\snake-ai-pytorch-main\\snake-ai-pytorch-main\\Graphics\\head_left.png")
        head_right = pygame.image.load("C:\\Users\\Acer pc\\Downloads\\snake-ai-pytorch-main\\snake-ai-pytorch-main\\Graphics\\head_right.png")
        head_up = pygame.image.load("C:\\Users\\Acer pc\\Downloads\\snake-ai-pytorch-main\\snake-ai-pytorch-main\\Graphics\\head_up.png")
        tail_down = pygame.image.load("C:\\Users\\Acer pc\\Downloads\\snake-ai-pytorch-main\\snake-ai-pytorch-main\\Graphics\\tail_down.png")
        tail_left = pygame.image.load("C:\\Users\\Acer pc\\Downloads\\snake-ai-pytorch-main\\snake-ai-pytorch-main\\Graphics\\tail_left.png")
        tail_right = pygame.image.load("C:\\Users\\Acer pc\\Downloads\\snake-ai-pytorch-main\\snake-ai-pytorch-main\\Graphics\\tail_right.png")
        tail_up = pygame.image.load("C:\\Users\\Acer pc\\Downloads\\snake-ai-pytorch-main\\snake-ai-pytorch-main\\Graphics\\tail_up.png")
        apple = pygame.image.load("C:\\Users\\Acer pc\\Downloads\\snake-ai-pytorch-main\\snake-ai-pytorch-main\\Graphics\\apple.png")
        body_bl = pygame.image.load("C:\\Users\\Acer pc\\Downloads\\snake-ai-pytorch-main\\snake-ai-pytorch-main\\Graphics\\body_bl.png")
        body_br = pygame.image.load("C:\\Users\\Acer pc\\Downloads\\snake-ai-pytorch-main\\snake-ai-pytorch-main\\Graphics\\body_br.png")

        graphics_mapping = {
            "horizontal": body_horizontal,
            "tl": body_tl,
            "tr": body_tr,
            "vertical": body_vertical,
            "head_down": head_down,
            "head_left": head_left,
            "head_right": head_right,
            "head_up": head_up,
            "tail_down": tail_down,
            "tail_left": tail_left,
            "tail_right": tail_right,
            "tail_up": tail_up,
            "apple": apple,
            "bl": body_bl,
            "br": body_br
        }

        for idx, pt in enumerate(self.snake):
            if idx == 0:  # Head of the snake
                if self.direction == Direction.RIGHT:
                    self.display.blit(graphics_mapping["head_right"], (pt.x, pt.y))
                elif self.direction == Direction.LEFT:
                    self.display.blit(graphics_mapping["head_left"], (pt.x, pt.y))
                elif self.direction == Direction.UP:
                    self.display.blit(graphics_mapping["head_up"], (pt.x, pt.y))
                elif self.direction == Direction.DOWN:
                    self.display.blit(graphics_mapping["head_down"], (pt.x, pt.y))
            elif idx == len(self.snake) - 1:  # Tail of the snake
                prev_pt = self.snake[idx - 1]
                if pt.x < prev_pt.x and pt.y == prev_pt.y:
                    self.display.blit(graphics_mapping["tail_right"], (pt.x, pt.y))
                elif pt.x > prev_pt.x and pt.y == prev_pt.y:
                    self.display.blit(graphics_mapping["tail_left"], (pt.x, pt.y))
                elif pt.y < prev_pt.y and pt.x == prev_pt.x:
                    self.display.blit(graphics_mapping["tail_down"], (pt.x, pt.y))
                elif pt.y > prev_pt.y and pt.x == prev_pt.x:
                    self.display.blit(graphics_mapping["tail_up"], (pt.x, pt.y))
            else:  # Body of the snake
                next_pt = self.snake[idx + 1]
                prev_pt = self.snake[idx - 1]
                if prev_pt.y > next_pt.y:
                    if pt.y == next_pt.y and pt.x < prev_pt.x:
                        self.display.blit(graphics_mapping["horizontal"], (pt.x, pt.y))
                    elif pt.x == next_pt.x and pt.y < prev_pt.y:
                        self.display.blit(graphics_mapping["vertical"], (pt.x, pt.y))
                    elif pt.y == next_pt.y and pt.x > prev_pt.x:
                        self.display.blit(graphics_mapping["horizontal"], (pt.x, pt.y))
                    elif pt.x == next_pt.x and pt.y > prev_pt.y:
                        self.display.blit(graphics_mapping["vertical"], (pt.x, pt.y))
                    else:
                        self.display.blit(graphics_mapping["tl"], (pt.x, pt.y))
                elif prev_pt.y < next_pt.y:
                    if pt.y == next_pt.y and pt.x < prev_pt.x:
                        self.display.blit(graphics_mapping["horizontal"], (pt.x, pt.y))
                    elif pt.x == next_pt.x and pt.y < prev_pt.y:
                        self.display.blit(graphics_mapping["vertical"], (pt.x, pt.y))
                    elif pt.y == next_pt.y and pt.x > prev_pt.x:
                        self.display.blit(graphics_mapping["horizontal"], (pt.x, pt.y))
                    elif pt.x == next_pt.x and pt.y > prev_pt.y:
                        self.display.blit(graphics_mapping["vertical"], (pt.x, pt.y))
                    else:
                        self.display.blit(graphics_mapping["tr"], (pt.x, pt.y))
                elif prev_pt.x > next_pt.x:
                    if pt.y == next_pt.y and pt.x < prev_pt.x:
                        self.display.blit(graphics_mapping["vertical"], (pt.x, pt.y))
                    elif pt.x == next_pt.x and pt.y < prev_pt.y:
                        self.display.blit(graphics_mapping["horizontal"], (pt.x, pt.y))
                    elif pt.y == next_pt.y and pt.x > prev_pt.x:
                        self.display.blit(graphics_mapping["vertical"], (pt.x, pt.y))
                    elif pt.x == next_pt.x and pt.y > prev_pt.y:
                        self.display.blit(graphics_mapping["horizontal"], (pt.x, pt.y))
                    else:
                        self.display.blit(graphics_mapping["bl"], (pt.x, pt.y))
                elif prev_pt.x < next_pt.x:
                    if pt.y == next_pt.y and pt.x < prev_pt.x:
                        self.display.blit(graphics_mapping["vertical"], (pt.x, pt.y))
                    elif pt.x == next_pt.x and pt.y < prev_pt.y:
                        self.display.blit(graphics_mapping["horizontal"], (pt.x, pt.y))
                    elif pt.y == next_pt.y and pt.x > prev_pt.x:
                        self.display.blit(graphics_mapping["vertical"], (pt.x, pt.y))
                    elif pt.x == next_pt.x and pt.y > prev_pt.y:
                        self.display.blit(graphics_mapping["horizontal"], (pt.x, pt.y))
                    else:
                        self.display.blit(graphics_mapping["br"], (pt.x, pt.y))

        self.display.blit(graphics_mapping["apple"], (self.food.x, self.food.y))

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()


    def _move(self, action):
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx]  # no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4  # right turn r -> d -> l -> u
            new_dir = clock_wise[next_idx]
        else:  # [0, 0, 1]
            next_idx = (idx - 1) % 4  # left turn r -> u -> l -> d
            new_dir = clock_wise[next_idx]

        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)
