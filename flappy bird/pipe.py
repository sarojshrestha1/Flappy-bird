import pygame as pg
from random import randint  # used to randomize pipe height

class Pipe:
    def __init__(self, scale_factor, move_speed):
        # ---------------- LOAD PIPE IMAGES ----------------
        # Top pipe (facing down)
        self.img_up = pg.transform.scale_by(
            pg.image.load("assets/pipeup.png").convert_alpha(),scale_factor
        )
        # Bottom pipe (facing up)
        self.img_down = pg.transform.scale_by(
            pg.image.load("assets/pipedown.png").convert_alpha(),scale_factor
        )

        # ---------------- RECTANGLES ----------------
        # Rectangles for collision detection
        self.rect_up = self.img_up.get_rect()
        self.rect_down = self.img_down.get_rect()

        # ---------------- PIPE SETTINGS ----------------
        self.pipe_distance = 150  # distance between top and bottom pipes

        # Random vertical position of top pipe
        self.rect_up.y = randint(250, 520)
        self.rect_up.x = 600  # start off-screen to the right

        # Calculate bottom pipe y based on top pipe
        self.rect_down.y = self.rect_up.y - self.pipe_distance - self.rect_up.height
        self.rect_down.x = 600  # start off-screen to the right

        # Movement speed of pipes (same as ground speed)
        self.move_speed = move_speed

    # ---------------- DRAW PIPE ----------------
    def draw(self, win):

        #Draw both top and bottom pipes on the game window

        win.blit(self.img_up, self.rect_up)
        win.blit(self.img_down, self.rect_down)

    # ---------------- UPDATE PIPE ----------------
    def update(self, dt):

        #Move the pipes left based on move_speed and delta time
        self.rect_up.x -= int(self.move_speed * dt)     # move top pipe
        self.rect_down.x -= int(self.move_speed * dt)   # move bottom pipe
