import pygame as pg


class Bird(pg.sprite.Sprite):  # Bird class inherits from pygame Sprite

    def __init__(self, scale_factor):
        super(Bird, self).__init__()  # initialize parent Sprite class

        # ---------------- LOAD BIRD IMAGES ----------------
        # Two images for animation (wing up and wing down)
        self.img_list = [
            pg.transform.scale_by(pg.image.load("assets/birdup.png").convert_alpha(),scale_factor),
            pg.transform.scale_by(pg.image.load("assets/birddown.png").convert_alpha(),scale_factor)
        ]

        # ---------------- IMAGE SETTINGS ----------------
        self.image_index = 0  # current image index
        self.image = self.img_list[self.image_index]  # set initial image
        self.rect = self.image.get_rect(center=(100, 100))  # bird starting position

        # ---------------- PHYSICS VARIABLES ----------------
        self.y_velocity = 0      # vertical speed of bird
        self.gravity = 10        # gravity force
        self.flap_speed = 250    # upward force when flapping

        # ---------------- ANIMATION CONTROL ----------------
        self.image_counter = 0   # controls animation switching speed

        # ---------------- GAME CONTROL ----------------
        self.update_on = False   # bird moves only when game starts

    # ---------------- UPDATE FUNCTION ----------------
    # Runs every frame from main game loop
    def update(self, dt):

        if self.update_on:
            self.play_animation()      # animate wings
            self.apply_gravity(dt)     # apply gravity effect

        # Prevent bird from going above top of screen
        if self.rect.top < 0:
            self.rect.top = 0
            self.y_velocity = 0

    # ---------------- APPLY GRAVITY ----------------
    def apply_gravity(self, dt):

        # Increase velocity due to gravity
        self.y_velocity += self.gravity * dt

        # Move bird downward based on velocity
        self.rect.y += self.y_velocity

    # ---------------- FLAP FUNCTION ----------------
    # Called when player presses SPACE
    def flap(self, dt):

        # Give bird upward velocity
        self.y_velocity = -self.flap_speed * dt

    # ---------------- ANIMATION FUNCTION ----------------
    def play_animation(self):

        # Change image every 5 frames
        if self.image_counter == 5:

            # Toggle between 0 and 1
            if self.image_index == 0:
                self.image_index = 1
            else:
                self.image_index = 0

            # Update current image
            self.image = self.img_list[self.image_index]

            # Reset counter
            self.image_counter = 0

        # Increase frame counter
        self.image_counter += 1

    # ---------------- RESET POSITION ----------------
    # Called when game restarts
    def resetposition(self):

        self.rect.center = (100, 100)  # reset position
        self.y_velocity = 0            # reset velocity
        self.image_counter = 0         # reset animation counter
