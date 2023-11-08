import np
import pygame
import sys
import serial

# Arduino verbinden
try:
    arduino = serial.Serial('COM4', 9600)
except serial.SerialException:
    print("Arduino not found!")
    sys.exit()
poti = 0
poti_signed = 0

# Spiel starten
pygame.init()
running = True

# Ganzer Bildschirm
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width = screen.get_width()
height = screen.get_height()

# Farben
black = (0, 0, 0)
grey = (128, 128, 128)

# Zeit
start_zeit = pygame.time.get_ticks()

# Bild laden
airplane = pygame.image.load("Airplane-from-behind.svg")

# Gebäude zeichnen
stadt = np.zeros(width * 4, dtype=int)
haus_groesse = 0
haus_abstand = 90
mindest_hoehe = 10
haus_hoehe = 0
for i in range(len(stadt)):
    if haus_hoehe > 0:
        haus_groesse = haus_groesse + 1
        stadt[i] = haus_hoehe
        if haus_groesse > mindest_hoehe and np.random.randint(0, 100) < 20:
            haus_hoehe = 0
            haus_groesse = 0
    if haus_hoehe == 0:
        if np.random.randint(0, 100) < 10:
            haus_hoehe = np.random.randint(30, 100)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw horizon
    pygame.draw.line(screen, grey, (0, height / 2), (width, height / 2), 1)

    zeit_innerhalb_des_spiels = pygame.time.get_ticks() - start_zeit
    zeit_innerhalb_der_untergrund_animation = zeit_innerhalb_des_spiels % 1000

    # schwarzes Rechteck (Gebäude), über dem Horizont
    # über ein drittel des himmels
    # allokiere eine liste mit 800 integern

    rotation = int(poti_signed / 32)
    # rotate skyline buildings in buffer
    stadt = np.roll(stadt, rotation)
    # what does np.roll do  ?
    # https://numpy.org/doc/stable/reference/generated/numpy.roll.html
    # draw the buffer as a line in the middle of the screen
    for i in range(len(stadt)):
        pygame.draw.line(screen, black, (i, height / 2), (i, height / 2 - stadt[i]), 1)

    # 10 Linien, die sich langsam nach unten bewegen
    for i in range(10):
        n = (i + zeit_innerhalb_der_untergrund_animation / 1000)
        y = height / 2 + n * n * 5
        pygame.draw.line(screen, grey, (0, y), (width, y), int(n))

    # Read the serial port
    readline = arduino.readline()
    try:
        poti = int(readline)
        poti_signed = poti - 512
    except ValueError:
        pass

    airplane_rotated = pygame.transform.rotate(airplane, poti_signed / 32)
    size_of_airplane = airplane_rotated.get_size()
    centered_airplane = (width / 2 - size_of_airplane[0] / 2, height / 2 - size_of_airplane[1] / 2)
    screen.blit(airplane_rotated, centered_airplane)

    # Update the screen
    pygame.display.flip()

pygame.quit()
sys.exit()
