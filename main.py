import pygame as pg
from engineFunctions import blit_text, save_data, load_data
from objects import *
from environment import *
from os.path import isdir
from assets import *


window = pg.display.set_mode((1300, 800), flags=pg.RESIZABLE)
window_width, window_height = window.get_size()

game_width, game_height = 1200, 700

pg.display.set_caption("PyEngine")

# decorational
command_actions_div_rect = pg.Rect(game_width+1, 0, 5, window_height)
object_button_div_rect = pg.Rect(0, game_height+1, command_actions_div_rect.left, 5)

# buttons
object_button_spacing = 5
object_buttons = []
i = 0
for asset in object_button_assets:
    if "Pressed" in asset:
        continue
    object_buttons.append(
        Button(
            (
                i * button_width + i * object_button_spacing,
                object_button_div_rect.bottom,
            ),
            asset,
            f"{asset} Pressed",
            asset,
        )
    )
    i += 1


run = True
engine_fps = 60
clock = pg.time.Clock()

# GUI movement and selection
selected_object = None

# action buttons
upload_button = Button((command_actions_div_rect.right, 0), "Upload", "Upload Pressed")
delete_button = Button((upload_button.rect.right, 0), "Trash", "Trash Pressed")

# Creation of project
project_name = "TestProject"
if not isdir(project_name):
    createEnvironment(project_name)

try:
    objects = load_data(f"{project_name}/objects.pkl")
except:
    objects = []

for obj in objects:
    obj.unpack(game_width, game_height)

def display():
    window.fill((30, 30, 30))

    # game objects
    for obj in objects:
        obj.display(window)

    # color coding & border layout
    pg.draw.rect(window, (80, 80, 80), object_button_div_rect)
    pg.draw.rect(window, (80, 80, 80), command_actions_div_rect)
    window.fill(
        (60, 60, 60), (0, object_button_div_rect.bottom, window_width, window_height)
    )
    window.fill(
        (60, 60, 60), (command_actions_div_rect.right, 0, window_width, window_height)
    )

    # object buttons
    for button in object_buttons:
        button.display(window)

    upload_button.display(window)
    delete_button.display(window)

    blit_text(window, project_name, (0, 0), (120, 120, 120), 30)

    pg.display.update()


# main script
while run:

    clock.tick(engine_fps)


    # delete button
    delete_button.clicked()
    if delete_button.released():
        if selected_object is not None:
            objects.pop(selected_object)
    delete_button.pressed()

    for event in pg.event.get():

        if event.type == pg.QUIT:
            run = False

        if event.type == pg.VIDEORESIZE:
            window_width, window_height = event.dict["size"]

        if event.type == pg.MOUSEBUTTONDOWN:

            mouse_x, mouse_y = pg.mouse.get_pos()

            for i, obj in enumerate(objects):
                if delete_button.rect.collidepoint((mouse_x, mouse_y)):
                    break
                if obj.rect.collidepoint((mouse_x, mouse_y)):
                    selected_object = i
                    break
            else:
                selected_object = None

        if event.type == pg.KEYDOWN:
            if selected_object is not None and objects[selected_object].type == "Text":
                if event.key == pg.K_BACKSPACE:
                    objects[selected_object].text = objects[selected_object].text[:-1]
                else:
                    objects[selected_object].text += event.unicode

                objects[selected_object].reload()
                

    # button animation
    upload_button.clicked()

    for button in object_buttons:
        if selected_object is not None:
            continue
        button.clicked()

    # button released
    if upload_button.released():

        # packing objects
        for obj in objects:
            obj.pack(game_width, game_height)

        # saving objects
        save_data(objects, f"{project_name}/objects.pkl")

        # unpacking objects
        for obj in objects:
            obj.unpack(game_width, game_height)


    for button in object_buttons:
        if button.released() and selected_object is None:
            print(selected_object)
            if button.info == "Button":
                objects.append(
                    Button(
                        (window_width / 2, window_height / 4),
                        "Blank Button",
                        "Blank Button Pressed",
                        )
                    )
                
            if button.info == "Text":
                objects.append(
                    Text(
                        "Abc",
                        game_width/2, game_height/2, (200, 120, 120), 30, "ArialBlack", True

                    )
                )
            break



    # object movement
    mouse_rel_x, mouse_rel_y = pg.mouse.get_rel()
    left_mouse_button_down = pg.mouse.get_pressed()[0]
    if left_mouse_button_down:
        if selected_object is not None:
            objects[selected_object].rect.x += mouse_rel_x
            objects[selected_object].rect.y += mouse_rel_y

    # button pressed update
    for button in object_buttons:
        if selected_object is not None:
            continue
        button.pressed()

    upload_button.pressed()

    display()

pg.quit()
quit()
