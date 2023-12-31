# Example file showing a circle moving on screen
import pygame
import pygame_menu

# pygame setup
pygame.init()
window_width, window_height = 1280, 720
screen = pygame.display.set_mode((window_width, window_height))
clock = pygame.time.Clock()
running = True
dt = 0
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

# Offset variables for smooth dragging and resizing
drag_offset_x = 0
drag_offset_y = 0
resize_offset_x = 0
resize_offset_y = 0
is_dragging = False
is_resizing = False
selected_shape = None

# Final Vars
white = (255, 255, 255)
black = (0, 0, 0)
brown = (165, 42, 42)
yellow = (218,165,32)
object_color = (0, 0, 255)
selected_color = (0, 0, 200)
room_color = (220, 220, 220)
darker_room = (200, 200, 200)

# initialize room variables
room_width, room_height = 595, 510
room_x, room_y = window_width/2-50, 50
# bottom left shape of room
bl_cut_width, bl_cut_height = 259, 205
bl_cut_x, bl_cut_y = room_x, room_y + room_height - bl_cut_height

bl_add_width, bl_add_height = 140, 102
bl_add_x, bl_add_y = room_x, bl_cut_y

# Menu for creating shapes
creating = {'x': window_width/2 + 50, 'y': window_height/2, 'width': 100, 'height': 100, 'selected': False, 'name': "", "shape" : 1,'angle': 0}


def shape_name(value):
    creating['name'] = value

def shape_width(value):
    creating['width'] = value

def shape_height(value):
    creating['height'] = value

def shape_type(type, value):
    creating['shape'] = type[0][1]

def create_shape():
    shapes.append(creating.copy())

menu = pygame_menu.Menu('Create Shape', window_width/2-150, window_height,theme=pygame_menu.themes.THEME_DEFAULT,position=(0,0))
menu.add.text_input('Name :', default='', onchange=shape_name)
menu.add.text_input('Breite (in cm):', default='', input_type=pygame_menu.locals.INPUT_INT, onchange=shape_width)
menu.add.text_input('Höhe (in cm):', default='', input_type=pygame_menu.locals.INPUT_INT, onchange=shape_height)
menu.add.selector('Shape :', [('Rechteck', 1), ('L-form', 2), ('Kreis', 6)], onchange=shape_type)
menu.add.button('Create', create_shape)
menu.enable

# Objects
# Object shape properties
shapes = []

def draw_shape(shape):
    color = object_color
    if shape['selected']:
        color = selected_color
        
    if shape['shape'] == 1:
        rotated_surface = pygame.transform.rotate(pygame.Surface((shape['width'], shape['height'])), shape['angle'])
        rotated_rect = rotated_surface.get_rect(center=(shape['x'] + shape['width'] // 2, shape['y'] + shape['height'] // 2))
        pygame.draw.rect(screen, color, rotated_rect)
        screen.blit(pygame.font.SysFont('Arial', 15).render(shape['name'], True, (255,255,255)), (rotated_rect.x+ 10, rotated_rect.y+ 10))
    elif shape['shape'] == 2: #L
        rotated_surface = pygame.transform.rotate(pygame.Surface((shape['width'], shape['height'])), shape['angle'])
        rotated_rect = rotated_surface.get_rect(center=(shape['x'] + shape['width'] // 2, shape['y'] + shape['height'] // 2))
        if shape['angle'] == 0:
            pygame.draw.rect(screen, color, rotated_rect)
            pygame.draw.rect(screen, room_color, (rotated_rect.x +rotated_rect.width/2, rotated_rect.y, rotated_rect.width/2, rotated_rect.height/2))
        elif shape['angle'] == 90:
            pygame.draw.rect(screen, color, rotated_rect)
            pygame.draw.rect(screen, room_color, (rotated_rect.x+rotated_rect.width/2, rotated_rect.y+rotated_rect.height/2, rotated_rect.width/2, rotated_rect.height/2))
        elif shape['angle'] == 180:
            pygame.draw.rect(screen, color, rotated_rect)
            pygame.draw.rect(screen, room_color, (rotated_rect.x, rotated_rect.y+rotated_rect.height/2, rotated_rect.width/2, rotated_rect.height/2))
        else:
            pygame.draw.rect(screen, color, rotated_rect)
            pygame.draw.rect(screen, room_color, (rotated_rect.x, rotated_rect.y, rotated_rect.width/2, rotated_rect.height/2))
        screen.blit(pygame.font.SysFont('Arial', 15).render(shape['name'], True, (255,255,255)), (rotated_rect.x+ 10, rotated_rect.y+ 10))
    else:
        pygame.draw.ellipse(screen, color, (shape['x'], shape['y'], shape['width'], shape['height']))
        screen.blit(pygame.font.SysFont('Arial', 15).render(shape['name'], True, (255,255,255)), (shape['x'] + 10, shape['y'] + 10))

    


def is_shape_clicked(mouse_pos, shape):
    return shape['x'] < mouse_pos[0] < shape['x'] + shape['width'] and shape['y'] < mouse_pos[1] < shape['y'] + shape['height']


def draw_room():
    # Menu trennleine 
    pygame.draw.line(screen, (70, 70, 70),[window_width/2-150, window_height],[window_width/2-150, 0], 10)
    # Draw the main rectangle
    pygame.draw.rect(screen, room_color, (room_x, room_y, room_width, room_height))
    pygame.draw.rect(screen, darker_room, (room_x+room_width-290, room_y, 290, 510))

    # Draw bottom left part to be taken out
    pygame.draw.rect(screen, white, (bl_cut_x, bl_cut_y, bl_cut_width, bl_cut_height))
    pygame.draw.rect(screen, room_color, (bl_add_x, bl_add_y, bl_add_width, bl_add_height))

    # Draw surrounding lines + doors + heater + outlets
    pygame.draw.line(screen, (0, 0, 0),[room_x, room_y],[room_x+595, room_y], 5)
    screen.blit(pygame.font.SysFont('Arial', 10).render('595cm', True, (0,0,0)), ([room_x+290, room_y-15]))
    pygame.draw.line(screen, (0, 0, 0),[room_x+595, room_y],[room_x+595, room_y+510], 5)
    screen.blit(pygame.font.SysFont('Arial', 10).render('510cm', True, (0,0,0)), ([room_x+600, room_y+255]))
    pygame.draw.line(screen, (0, 0, 0),[room_x, room_y],[room_x, room_y+405], 5)
    screen.blit(pygame.font.SysFont('Arial', 10).render('405cm', True, (0,0,0)), ([room_x-35, room_y+202]))
    pygame.draw.line(screen, (0, 0, 0),[room_x, room_y+405],[room_x+140, room_y+405], 5)
    screen.blit(pygame.font.SysFont('Arial', 10).render('140cm', True, (0,0,0)), ([room_x+60, room_y+410]))
    pygame.draw.line(screen, (0, 0, 0),[room_x+140, room_y+405],[room_x+140, room_y+303], 5)
    screen.blit(pygame.font.SysFont('Arial', 10).render('102cm', True, (0,0,0)), ([room_x+145, room_y+350]))
    pygame.draw.line(screen, (0, 0, 0),[room_x+140, room_y+303],[room_x+259, room_y+303], 5)
    screen.blit(pygame.font.SysFont('Arial', 10).render('119cm', True, (0,0,0)), ([room_x+190, room_y+305]))
    pygame.draw.line(screen, (0, 0, 0),[room_x+259, room_y+303],[room_x+259, room_y+510], 5)
    screen.blit(pygame.font.SysFont('Arial', 10).render('205cm', True, (0,0,0)), ([room_x+230, room_y+405]))
    pygame.draw.line(screen, (0, 0, 0),[room_x+259, room_y+510],[room_x+595, room_y+510], 5)
    screen.blit(pygame.font.SysFont('Arial', 10).render('336cm', True, (0,0,0)), ([room_x+399, room_y+515]))

    # Doors
    pygame.draw.line(screen, brown,[room_x, room_y+190],[room_x, room_y+405], 2)
    pygame.draw.line(screen, brown,[room_x+150, room_y+303],[room_x+259, room_y+303], 2)
    # Heater
    pygame.draw.rect(screen, brown, (room_x+445, room_y+485, 140, 25))
    screen.blit(pygame.font.SysFont('Arial', 20).render('Heizung', True, (0,0,0)), (room_x+460, room_y+485))
    pygame.draw.rect(screen, brown, (room_x, room_y+385, 140, 20))
    screen.blit(pygame.font.SysFont('Arial', 15).render('Heizung', True, (0,0,0)), (room_x+20, room_y+385))
    # Outlets
    pygame.draw.line(screen, yellow,[room_x+595, room_y+40],[room_x+595, room_y+80], 2)
    pygame.draw.line(screen, yellow,[room_x+595, room_y+445],[room_x+595, room_y+425], 2)
    pygame.draw.line(screen, brown,[room_x+140, room_y+303],[room_x+150, room_y+303], 2)
    

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()

            # Check for resizing
            for shape in shapes:
                if shape['selected']:
                    if shape['x'] + shape['width'] - 10 < mouse_pos[0] < shape['x'] + shape['width'] and \
                            shape['y'] + shape['height'] - 10 < mouse_pos[1] < shape['y'] + shape['height']:
                        is_resizing = True
                        resize_offset_x = shape['x'] + shape['width'] - mouse_pos[0]
                        resize_offset_y = shape['y'] + shape['height'] - mouse_pos[1]
                        break

            if not is_resizing:
                # Check for selection
                selected_shape = None
                for shape in shapes:
                    if is_shape_clicked(mouse_pos, shape):
                        shape['selected'] = True
                        selected_shape = shape
                    else:
                        shape['selected'] = False

                    # Check for dragging
                    if selected_shape:
                        is_dragging = True
                        drag_offset_x = mouse_pos[0] - selected_shape['x']
                        drag_offset_y = mouse_pos[1] - selected_shape['y']

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            is_dragging = False
            is_resizing = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:  # Right mouse button
            if selected_shape:
                selected_shape['angle'] = (selected_shape['angle'] + 90) % 360
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE and selected_shape:
                shapes.remove(selected_shape)
                selected_shape = None

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")
    menu.update(events)
    menu.draw(screen)

    # Draw the room!
    draw_room()
    # Update shape position if dragging
    if is_dragging and selected_shape:
        mouse_pos = pygame.mouse.get_pos()
        selected_shape['x'] = mouse_pos[0] - drag_offset_x
        selected_shape['y'] = mouse_pos[1] - drag_offset_y

    # Update shape size if resizing
    if is_resizing and selected_shape:
        mouse_pos = pygame.mouse.get_pos()
        selected_shape['width'] = mouse_pos[0] - selected_shape['x'] + resize_offset_x
        selected_shape['height'] = mouse_pos[1] - selected_shape['y'] + resize_offset_y

    # Draw the objects
    for shape in shapes:
        draw_shape(shape)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
