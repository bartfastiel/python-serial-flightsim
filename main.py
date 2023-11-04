import pygame
import sys
import serial

# Initialize pygame
pygame.init()

# Set the screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))

# Set the color (black in RGB)
black = (0, 0, 0)
grey = (128, 128, 128)

# Set the line width
line_width = 5

arduino = serial.Serial('COM4', 9600)
intValue = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw horizon
    pygame.draw.line(screen, grey, (5, 300), (790, 300), line_width)

    # Read the serial port
    readline = arduino.readline()
    # Try to parse as int
    try:
        intValue = int(readline)
    except ValueError:
        pass
    print(intValue)

    # move end_point up, start_point down
    start_point = (100, 300 + intValue - 512)
    end_point = (700, 300 - intValue + 512)

    # Draw the black horizontal line
    pygame.draw.line(screen, black, start_point, end_point, line_width)

    # Update the screen
    pygame.display.flip()

pygame.quit()
sys.exit()
