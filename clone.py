import pygame

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((480, 360))

running = True

i = 0
radius = 40
while running:
    dt = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    # 1. Draw a yellow circle here
    pygame.draw.circle(screen, "yellow", (240, 180), 40)

    # 2. Draw a black triangle over the circle here

    # I understand I new thing (cx, cy) -> (center of the circle) if we add the radius ->
    
    if i == 20:
        direction = -1
    elif i == 0:
        direction = 1
    i += direction

    pygame.draw.polygon(screen, "black", [(240, 180), (240 + i, 180 + radius), (240 - i, 180 + radius)])

    pygame.display.flip()

pygame.quit()
