# Example file showing a basic pygame "game loop"
import mygame

# pygame setup
mygame.init()
screen = mygame.display.set_mode((1280, 720))
clock = mygame.time.Clock()
running = True

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in mygame.event.get():
        if event.type == mygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    mygame.display.flip()

    clock.tick(60)  # limits FPS to 60

mygame.quit()