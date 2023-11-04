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

arduino = serial.Serial('COM4', 9600)
poti = 0

start_zeit = pygame.time.get_ticks()
print(start_zeit)
airplane = pygame.image.load("Airplane-from-behind.svg")
size_of_airplane = airplane.get_size()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw horizon
    pygame.draw.line(screen, grey, (5, 300), (790, 300), 1)

    zeit_innerhalb_des_spiels = pygame.time.get_ticks() - start_zeit
    zeit_innerhalb_der_untergrund_animation = zeit_innerhalb_des_spiels % 1000

    # 10 Linien, die sich langsam nach unten bewegen
    for i in range(10):
        n = (i + zeit_innerhalb_der_untergrund_animation / 1000)
        y = 300 + n * n * 5
        pygame.draw.line(screen, grey, (5, y), (790, y), int(n))

    # Read the serial port
    readline = arduino.readline()
    try:
        poti = int(readline)
        poti_signed = poti - 512
    except ValueError:
        pass

    centered_airplane = (width / 2 - size_of_airplane[0] / 2, height / 2 - size_of_airplane[1] / 2)
    airplane_rotated = pygame.transform.rotate(airplane, poti_signed / 32)
    screen.blit(airplane_rotated, centered_airplane)

    # Update the screen
    pygame.display.flip()

pygame.quit()
sys.exit()
