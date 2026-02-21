import pygame as pg
import sys, time
from bird import Bird
from pipe import Pipe

pg.init()  # initialize pygame

class Game:
    def __init__(self):  # constructor (runs when object is created)

        # ---------------- WINDOW SETTINGS ----------------
        self.width = 600
        self.height = 768
        self.scale_factor = 1.5
        self.win = pg.display.set_mode((self.width, self.height))  # create game window
        self.clock = pg.time.Clock()  # controls FPS

        # ---------------- GAME VARIABLES ----------------
        self.move_speed = 250  # ground and pipe speed
        self.bird = Bird(self.scale_factor)  # create bird object
        self.start_monitoring = False  # used for score tracking
        self.score = 0  # initial score

        # ---------------- FONT & TEXT ----------------
        self.font = pg.font.Font("assets/font.ttf", 24)
        self.score_text = self.font.render("Score: 0", True, (255, 255, 255))
        self.score_text_rect = self.score_text.get_rect(center=(100, 50))

        # Restart text
        self.restart_text = self.font.render("Restart", True, (255, 255, 255))
        self.restart_text_rect = self.restart_text.get_rect(center=(300, 700))

        # ---------------- GAME STATE ----------------
        self.is_enter_pressed = False  # check if game started
        self.is_game_started = True
        self.pipes = []  # list to store pipes
        self.pipe_generate_counter = 7  # pipe spawn counter

        # setup background and ground
        self.setupBgAndGround()

        # start game loop
        self.gameLoop()

    # ---------------- MAIN GAME LOOP ----------------
    def gameLoop(self):

        last_time = time.time()  # store previous time

        while True:

            # calculate delta time (time between frames)
            new_time = time.time()
            dt = new_time - last_time
            last_time = new_time

            # ---------------- EVENT HANDLING ----------------
            for event in pg.event.get():

                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                if event.type == pg.KEYDOWN:

                    # start game when Enter pressed
                    if event.key == pg.K_RETURN:
                        self.is_enter_pressed = True
                        self.bird.update_on = True

                    # bird flap when Space pressed
                    if event.key == pg.K_SPACE and self.is_enter_pressed:
                        self.bird.flap(dt)

                # restart game when restart text clicked
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.restart_text_rect.collidepoint(pg.mouse.get_pos()):
                        self.restartGame()

            # update game elements
            self.update_Everything(dt)
            self.check_collision()
            self.check_score()
            self.draw_everything()

            pg.display.update()  # refresh screen
            self.clock.tick(60)  # limit FPS to 60

    # ---------------- DRAW EVERYTHING ----------------
    def draw_everything(self):

        # draw background
        self.win.blit(self.bg_img, (0, -300))

        # draw pipes
        for pipe in self.pipes:
            pipe.draw(self.win)

        # draw ground
        self.win.blit(self.ground1_img, self.ground1_rect)
        self.win.blit(self.ground2_img, self.ground2_rect)

        # draw bird
        self.win.blit(self.bird.image, self.bird.rect)

        # draw score
        self.win.blit(self.score_text, self.score_text_rect)

        # show restart text when game over
        if not self.is_game_started:
            self.win.blit(self.restart_text, self.restart_text_rect)

    # ---------------- BACKGROUND & GROUND SETUP ----------------
    def setupBgAndGround(self):

        # load and scale background
        self.bg_img = pg.transform.scale_by(
            pg.image.load("assets/bg.png").convert(),
            self.scale_factor
        )

        # load ground images
        self.ground1_img = pg.transform.scale_by(
            pg.image.load("assets/ground.png").convert(),
            self.scale_factor
        )
        self.ground2_img = pg.transform.scale_by(
            pg.image.load("assets/ground.png").convert(),
            self.scale_factor
        )

        # get rectangles
        self.ground1_rect = self.ground1_img.get_rect()
        self.ground2_rect = self.ground2_img.get_rect()

        # position ground
        self.ground1_rect.x = 0
        self.ground2_rect.x = self.ground1_rect.right
        self.ground1_rect.y = 568
        self.ground2_rect.y = 568

    # ---------------- COLLISION CHECK ----------------
    def check_collision(self):

        if len(self.pipes):

            # ground collision
            if self.bird.rect.bottom > 568:
                self.bird.update_on = False
                self.is_enter_pressed = False
                self.is_game_started = False

            # pipe collision
            if (self.bird.rect.colliderect(self.pipes[0].rect_down) or
                self.bird.rect.colliderect(self.pipes[0].rect_up)):
                self.is_enter_pressed = False
                self.is_game_started = False

    # ---------------- SCORE CHECK ----------------
    def check_score(self):

        if len(self.pipes) > 0:

            # detect bird inside pipe region
            if (self.bird.rect.left > self.pipes[0].rect_down.left and
                not self.start_monitoring and
                self.bird.rect.right < self.pipes[0].rect_down.right):

                self.start_monitoring = True

            # increase score after passing pipe
            if self.bird.rect.left > self.pipes[0].rect_down.right and self.start_monitoring:
                self.start_monitoring = False
                self.score += 1
                self.score_text = self.font.render(
                    f"Score: {self.score}", True, (255, 255, 255)
                )

    # ---------------- RESTART GAME ----------------
    def restartGame(self):

        self.score = 0
        self.score_text = self.font.render("Score: 0", True, (255, 255, 255))
        self.is_enter_pressed = False
        self.is_game_started = True
        self.bird.resetposition()
        self.pipes.clear()
        self.pipe_generate_counter = 71
        self.bird.update_on = False

    # ---------------- UPDATE EVERYTHING ----------------
    def update_Everything(self, dt):

        # update bird
        self.bird.update(dt)

        if self.is_enter_pressed:

            # move ground
            self.ground1_rect.x -= int(self.move_speed * dt)
            self.ground2_rect.x -= int(self.move_speed * dt)

            # loop ground infinitely
            if self.ground1_rect.right < 0:
                self.ground1_rect.x = self.ground2_rect.right
            if self.ground2_rect.right < 0:
                self.ground2_rect.x = self.ground1_rect.right

            # generate new pipes
            if self.pipe_generate_counter >= 70:
                self.pipes.append(Pipe(self.scale_factor, self.move_speed))
                self.pipe_generate_counter = 0

            self.pipe_generate_counter += 1

            # update pipes
            for pipe in self.pipes:
                pipe.update(dt)

            # remove pipes if off screen
            if len(self.pipes) != 0:
                if self.pipes[0].rect_up.right < 0:
                    self.pipes.pop(0)


# create game object
if __name__ == "__main__":
    game = Game()


