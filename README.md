#Flappy Bird Clone
A simple Flappy Bird clone built using Python and Pygame.
This project demonstrates sprite animation, gravity physics, collision detection, pipe generation, and score tracking using delta time (dt) for smooth gameplay.

##Features
-Smooth bird movement using delta time
-Animated bird (wing up / wing down)
-Infinite scrolling ground
-Random pipe generation
-Collision detection (pipes & ground)
-Score tracking system
-Restart button after game over
-FPS control using pygame.time.Clock()

##Built With
-Python 3.x
-Pygame

## Internal Architecture
The project is divided into modular components for clean separation of responsibilities:

## 1. Game Core (main.py)
-Manages the main game loop
-Handles delta-time (dt) calculation
-Controls game state (start, running, game over)
-Coordinates bird, pipes, and ground movement
-Implements scoring and collision detection

###Core Systems:
-Event handling
-Frame-rate control using pygame.time.Clock()
-Game restart system
-Pipe spawning system

## 2. Bird System (bird.py)
The Bird class extends pygame.sprite.Sprite.

### Physics Engine:
-Gravity-based vertical acceleration
-Flap impulse velocity
-Boundary detection (top & ground)

### Animation System:
-Alternates between two wing sprites
-Frame-based animation counter

### State Controls:
-update_on flag prevents movement before game starts
-Reset system restores position and velocity

## 3.Pipe System (pipe.py)

Handles obstacle generation and movement.

### Pipe Mechanics:
-Random vertical positioning
-Fixed gap between upper and lower pipes
-Continuous leftward movement using delta time
-Automatic removal when off-screen

### Collision System:
-Rectangle-based collision detection
-Checks both upper and lower pipe segments

## Controls & Input Handling
|Key	 |Action |Internal Logic                                   |
|------|-------|-------------------------------------------------|
|Enter |Start  |Game	Enables bird physics (update_on = True)    |
|Space |Flap	 |Applies upward velocity impulse                  |
|Mouse |Click	 |Restart	Resets score, pipes, and bird state      |
|Close |Window |Exit Game	Safely quits Pygame and system process |

