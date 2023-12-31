# Andri Maasing IT-21 - Particle Demo

import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Windows and Particle size customisation
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (0, 0, 0)
PARTICLE_RADIUS = 3

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Random Color Particle Generator Demo")

# Particle parameters
particles = []
particle_lifetime = 100
particle_speed = 2

clock = pygame.time.Clock()

def create_particle(x, y):
    return {
        'x': x,
        'y': y,
        'vx': random.uniform(-particle_speed, particle_speed),
        'vy': random.uniform(-particle_speed, particle_speed),
        'lifetime': particle_lifetime,
        'color': (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    }

def update_particles():
    global particles

    new_particles = []
    for particle in particles:
        particle['x'] += particle['vx']
        particle['y'] += particle['vy']
        particle['lifetime'] -= 1

        if particle['lifetime'] > 0:
            new_particles.append(particle)

    particles = new_particles

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Clear the screen
    screen.fill(BACKGROUND_COLOR)

    # Generate new particles at the mouse cursor
    if pygame.mouse.get_pressed()[0]:
        x, y = pygame.mouse.get_pos()
        particles.append(create_particle(x, y))

    # Update and draw particles
    update_particles()
    for particle in particles:
        pygame.draw.circle(screen, particle['color'], (int(particle['x']), int(particle['y'])), PARTICLE_RADIUS)

    pygame.display.flip()
    clock.tick(60)
