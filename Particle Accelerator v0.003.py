import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Window and Particle size customization
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 800
PARTICLE_RADIUS = 3

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Particle accelerator")

# Particle parameters
particles = []
default_particle_lifetime = 100
default_particle_speed = 2
particle_lifetime = default_particle_lifetime
particle_speed = default_particle_speed

# Create buttons
font = pygame.font.Font(None, 40)
lifetime_button = pygame.Rect(10, 10, 300, 50)
speed_button = pygame.Rect(10, 70, 300, 50)
reset_button = pygame.Rect(10, 130, 300, 50)
rainbow_button = pygame.Rect(10, 190, 328, 50)
time_multiplier_button = pygame.Rect(10, 250, 300, 50)  # Renamed button to "Time Multiplier"

# Button colors
lifetime_button_color = (128, 0, 128)
speed_button_color = (128, 0, 128)
reset_button_color = (128, 0, 128)
rainbow_button_color = (128, 0, 128)
time_multiplier_button_color = (128, 0, 128)  # Color for the Time Multiplier button

# Text labels
lifetime_text = font.render(f"Particle Lifetime: {particle_lifetime}", True, (255, 255, 255))
speed_text = font.render(f"Particle Speed: {particle_speed}", True, (255, 255, 255))
reset_text = font.render("Reset to Default", True, (255, 255, 255))
time_multiplier_text = font.render("Time Multiplier: 1x", True, (255, 255, 255))  # Initial value is 1x

# Create RGB buttons at the bottom
red_button = pygame.Rect(10, SCREEN_HEIGHT - 60, 100, 50)
green_button = pygame.Rect(120, SCREEN_HEIGHT - 60, 100, 50)
blue_button = pygame.Rect(230, SCREEN_HEIGHT - 60, 100, 50)

# Button colors
red_button_color = (255, 0, 0)  # Red color
green_button_color = (0, 255, 0)  # Green color
blue_button_color = (0, 0, 255)  # Blue color

# Color sliders
brightness_slider_x = 350
brightness_slider_y = SCREEN_HEIGHT - 50
brightness_slider_width = 200
brightness_slider_height = 20
brightness_slider_color = (128, 128, 128)
brightness_slider_button_radius = 10
brightness_slider_button_color = (255, 255, 255)
brightness_slider_value = 255  # Set brightness slider to maximum by default
brightness_slider_min = 0
brightness_slider_max = 255

color_slider_x = 350
color_slider_y = SCREEN_HEIGHT - 20
color_slider_width = 200
color_slider_height = 20
color_slider_color = (128, 128, 128)
color_slider_button_radius = 10
color_slider_button_color = (255, 0, 0)  # Initial color slider value (red)
color_slider_value = 0  # Default color slider value
color_slider_min = 0
color_slider_max = 360  # Degrees in the color wheel

# Variables for tracking slider dragging
dragging_brightness_slider = False
dragging_color_slider = False

clock = pygame.time.Clock()

# Background color variables
background_color = (0, 0, 0)  # Default background color (black)
red_value = 0
green_value = 0
blue_value = 0
selected_color = None

# Variable to track if the mouse is over a button
mouse_over_button = False

# Variable to track rainbow particles state
rainbow_particles_enabled = False

# Variable to track Time Multiplier
time_multiplier = 1  # Default is 1x

# Define rainbow_text here
rainbow_text = font.render("Rainbow Particles: OFF", True, (255, 0, 0))

def create_particle(x, y):
    if rainbow_particles_enabled:
        return {
            'x': x,
            'y': y,
            'vx': random.uniform(-particle_speed, particle_speed),
            'vy': random.uniform(-particle_speed, particle_speed),
            'lifetime': particle_lifetime,
            'color': (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        }
    else:
        # Generate particles with the selected color from the slider
        hue = color_slider_value
        saturation = 255
        value = brightness_slider_value
        r, g, b = color_hsv_to_rgb(hue, saturation, value)
        return {
            'x': x,
            'y': y,
            'vx': random.uniform(-particle_speed, particle_speed),
            'vy': random.uniform(-particle_speed, particle_speed),
            'lifetime': particle_lifetime,
            'color': (r, g, b)
        }

def update_particles():
    global particles

    new_particles = []
    for particle in particles:
        particle['x'] += particle['vx'] * time_multiplier  # Apply Time Multiplier to background scrolling
        particle['y'] += particle['vy'] * time_multiplier  # Apply Time Multiplier to background scrolling
        particle['lifetime'] -= 1

        if particle['lifetime'] > 0:
            new_particles.append(particle)

    particles = new_particles

# Function to change button colors individually
def change_button_color(button, new_color):
    pygame.draw.rect(screen, new_color, button, border_radius=10)

# Function to convert HSV to RGB
def color_hsv_to_rgb(hue, saturation, value):
    hi = int(hue / 60) % 6
    f = (hue / 60) - int(hue / 60)
    p = int(value * (1 - (saturation / 255)))
    q = int(value * (1 - f * (saturation / 255)))
    t = int(value * (1 - (1 - f) * (saturation / 255)))

    if hi == 0:
        return value, t, p
    elif hi == 1:
        return q, value, p
    elif hi == 2:
        return p, value, t
    elif hi == 3:
        return p, q, value
    elif hi == 4:
        return t, p, value
    else:
        return value, p, q

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Check for button clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            if lifetime_button.collidepoint(event.pos):
                # Handle lifetime button clicks
                if event.button == 4:  # Scroll up to increase lifetime
                    particle_lifetime += 10
                elif event.button == 5:  # Scroll down to decrease lifetime
                    if particle_lifetime >= 20:
                        particle_lifetime -= 10
                lifetime_text = font.render(f"Particle Lifetime: {particle_lifetime}", True, (255, 255, 255))
            elif speed_button.collidepoint(event.pos):
                # Handle speed button clicks
                if event.button == 4:  # Scroll up to increase speed
                    particle_speed += 1
                elif event.button == 5:  # Scroll down to decrease speed
                    if particle_speed >= 2:
                        particle_speed -= 1
                speed_text = font.render(f"Particle Speed: {particle_speed}", True, (255, 255, 255))
            elif reset_button.collidepoint(event.pos) and event.button == 1:
                # Handle reset button click
                particle_lifetime = default_particle_lifetime
                particle_speed = default_particle_speed
                lifetime_text = font.render(f"Particle Lifetime: {particle_lifetime}", True, (255, 255, 255))
                speed_text = font.render(f"Particle Speed: {particle_speed}", True, (255, 255, 255))
                brightness_slider_value = brightness_slider_max  # Set brightness slider to maximum
                color_slider_value = 0  # Reset color slider value
                rainbow_particles_enabled = False
                rainbow_text = font.render("Rainbow Particles: OFF", True, (255, 0, 0))  # Red color for OFF
            elif rainbow_button.collidepoint(event.pos) and event.button == 1:
                # Handle rainbow toggle button click
                rainbow_particles_enabled = not rainbow_particles_enabled
                # Update rainbow_text color based on the state
                rainbow_text = font.render("Rainbow Particles: ON" if rainbow_particles_enabled else "Rainbow Particles: OFF", True, (0, 255, 0) if rainbow_particles_enabled else (255, 0, 0))
            elif red_button.collidepoint(event.pos):
                selected_color = "R"
                if event.button == 4:  # Scroll up to increase the red value
                    red_value = min(red_value + 1, 255)
                elif event.button == 5:  # Scroll down to decrease the red value
                    red_value = max(red_value - 1, 0)
            elif green_button.collidepoint(event.pos):
                selected_color = "G"
                if event.button == 4:  # Scroll up to increase the green value
                    green_value = min(green_value + 1, 255)
                elif event.button == 5:  # Scroll down to decrease the green value
                    green_value = max(green_value - 1, 0)
            elif blue_button.collidepoint(event.pos):
                selected_color = "B"
                if event.button == 4:  # Scroll up to increase the blue value
                    blue_value = min(blue_value + 1, 255)
                elif event.button == 5:  # Scroll down to decrease the blue value
                    blue_value = max(blue_value - 1, 0)
            elif time_multiplier_button.collidepoint(event.pos) and event.button == 1:
                # Handle Time Multiplier button click
                time_multiplier = 10 if time_multiplier == 1 else 1  # Toggle between 1x and 10x
                time_multiplier_text = font.render(f"Time Multiplier: {time_multiplier}x", True, (255, 255, 255))

            # Update the background color based on the RGB values
            background_color = (red_value, green_value, blue_value)

            # Check if the mouse is over any slider and start dragging if clicked
            if (
                brightness_slider_x <= event.pos[0] <= brightness_slider_x + brightness_slider_width and
                brightness_slider_y <= event.pos[1] <= brightness_slider_y + brightness_slider_height
            ):
                dragging_brightness_slider = True

            if (
                color_slider_x <= event.pos[0] <= color_slider_x + color_slider_width and
                color_slider_y <= event.pos[1] <= color_slider_y + color_slider_height
            ):
                dragging_color_slider = True

        elif event.type == pygame.MOUSEBUTTONUP:
            # Stop dragging when mouse button is released
            dragging_brightness_slider = False
            dragging_color_slider = False

        # Handle slider dragging
        if dragging_brightness_slider:
            if event.type == pygame.MOUSEMOTION:
                x, _ = event.pos
                x = max(min(x, brightness_slider_x + brightness_slider_width), brightness_slider_x)
                brightness_slider_value = int(((x - brightness_slider_x) / brightness_slider_width) *
                                               (brightness_slider_max - brightness_slider_min)) + brightness_slider_min

        if dragging_color_slider:
            if event.type == pygame.MOUSEMOTION:
                x, _ = event.pos
                x = max(min(x, color_slider_x + color_slider_width), color_slider_x)
                color_slider_value = int(((x - color_slider_x) / color_slider_width) *
                                          (color_slider_max - color_slider_min)) + color_slider_min

    # Clear the screen
    screen.fill(background_color)

    # Generate new particles while the left mouse button is held down
    if pygame.mouse.get_pressed()[0]:
        x, y = pygame.mouse.get_pos()
        particles.append(create_particle(x, y))

    # Update and draw particles
    update_particles()
    for particle in particles:
        pygame.draw.circle(screen, particle['color'], (int(particle['x']), int(particle['y'])), PARTICLE_RADIUS)

    # Draw buttons with rounded corners and individual colors
    change_button_color(lifetime_button, lifetime_button_color)
    change_button_color(speed_button, speed_button_color)
    change_button_color(reset_button, reset_button_color)
    change_button_color(rainbow_button, rainbow_button_color)
    change_button_color(red_button, red_button_color)
    change_button_color(green_button, green_button_color)
    change_button_color(blue_button, blue_button_color)
    change_button_color(time_multiplier_button, time_multiplier_button_color)  # Color for Time Multiplier button

    # Draw the brightness slider
    pygame.draw.rect(screen, brightness_slider_color,
                     (brightness_slider_x, brightness_slider_y, brightness_slider_width, brightness_slider_height),
                     border_radius=brightness_slider_height // 2)
    brightness_slider_button_x = brightness_slider_x + int(
        (brightness_slider_value - brightness_slider_min) / (brightness_slider_max - brightness_slider_min) *
        brightness_slider_width)
    pygame.draw.circle(screen, brightness_slider_button_color,
                       (brightness_slider_button_x, brightness_slider_y + brightness_slider_height // 2),
                       brightness_slider_button_radius)

    # Draw the color slider
    pygame.draw.rect(screen, color_slider_color,
                     (color_slider_x, color_slider_y, color_slider_width, color_slider_height),
                     border_radius=color_slider_height // 2)
    color_slider_button_x = color_slider_x + int(
        (color_slider_value - color_slider_min) / (color_slider_max - color_slider_min) *
        color_slider_width)
    color_slider_button_color = color_hsv_to_rgb(color_slider_value, 255, 255)
    pygame.draw.circle(screen, color_slider_button_color,
                       (color_slider_button_x, color_slider_y + color_slider_height // 2),
                       color_slider_button_radius)

    # Highlight buttons when the mouse is over them
    if lifetime_button.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, (160, 32, 240), lifetime_button, border_radius=10)
    if speed_button.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, (160, 32, 240), speed_button, border_radius=10)
    if reset_button.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, (160, 32, 240), reset_button, border_radius=10)
    if rainbow_button.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, (160, 32, 240), rainbow_button, border_radius=10)
    if red_button.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, (160, 32, 240), red_button, border_radius=10)
    if green_button.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, (160, 32, 240), green_button, border_radius=10)
    if blue_button.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, (160, 32, 240), blue_button, border_radius=10)
    if time_multiplier_button.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, (160, 32, 240), time_multiplier_button, border_radius=10)  # Highlight Time Multiplier button

    # Text label for background color
    bg_color_text = font.render("Background color", True, (255, 255, 255))
    bg_color_text_rect = bg_color_text.get_rect()
    bg_color_text_rect.center = (175, SCREEN_HEIGHT - 80)

    # Update the text for RGB values, rainbow particles state, and Time Multiplier
    red_text = font.render(f"R: {red_value}", True, (255, 255, 255))
    green_text = font.render(f"G: {green_value}", True, (255, 255, 255))
    blue_text = font.render(f"B: {blue_value}", True, (255, 255, 255))

    screen.blit(rainbow_text, (15, 200))
    screen.blit(time_multiplier_text, (15, 260))  # Display Time Multiplier text

    screen.blit(lifetime_text, (15, 20))
    screen.blit(speed_text, (15, 80))
    screen.blit(reset_text, (15, 140))
    screen.blit(red_text, (18, SCREEN_HEIGHT - 50))
    screen.blit(green_text, (128, SCREEN_HEIGHT - 50))
    screen.blit(blue_text, (238, SCREEN_HEIGHT - 50))
    screen.blit(bg_color_text, bg_color_text_rect)

    pygame.display.flip()
    clock.tick(60)
