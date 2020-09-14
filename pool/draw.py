import pygame

from . import balls

def draw():
    pygame.init()

    x_bounds = [0, 700]
    y_bounds = [0, 500]
    size = [x_bounds[1], y_bounds[1]]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Drawing test")
    done = False

    clock = pygame.time.Clock()

    TestBalls = balls.Balls(10)

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        
        # Move balls
        balls.move(TestBalls, x_bounds, y_bounds)

        # Draw background and balls
        screen.fill((0, 0, 0))
        TestBalls.draw(screen)

        # Limit FPS
        clock.tick(60)

        # Update screen
        pygame.display.flip()
    
    pygame.quit()