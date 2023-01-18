import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Initialize Pygame
pygame.init()

# Create a Pygame window
screen = pygame.display.set_mode((640, 480), OPENGL | DOUBLEBUF)

# Set the OpenGL viewport
glViewport(0, 0, 640, 480)
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
glOrtho(-1.0, 1.0, -1.0, 1.0, -1.0, 1.0)
glMatrixMode(GL_MODELVIEW)

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Get the mouse position in screen coordinates
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Convert the mouse position to the coordinate system used by PyOpenGL
    mouse_x = (mouse_x / 640) * 2 - 1
    mouse_y = -(mouse_y / 480) * 2 + 1

    # Clear the screen
    glClear(GL_COLOR_BUFFER_BIT)

    # Draw a square at the mouse position
    glBegin(GL_QUADS)
    glVertex2f(mouse_x - 0.1, mouse_y - 0.1)
    glVertex2f(mouse_x - 0.1, mouse_y + 0.1)
    glVertex2f(mouse_x + 0.1, mouse_y + 0.1)
    glVertex2f(mouse_x + 0.1, mouse_y - 0.1)
    glEnd()

    # Update the screen
    pygame.display.flip()
