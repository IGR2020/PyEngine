import pygame as pg
from engineFunctions import load_assets, Button
from objectConverter import *

window = pg.display.set_mode((1000, 600), flags=pg.RESIZABLE)
window_width, window_height = window.get_size()

pg.display.set_caption("PyEngine")

# assets
button_width = 64
button_height = 72
object_button_assets = load_assets(
    "assets/Object Buttons", (button_width, button_height), 2
)

object_assets = load_assets("assets/Object Assets", None, 2)
button_assets = load_assets("assets/Buttons", (button_width, button_height), 2)

# decorational
object_button_div_rect = pg.Rect(0, window_height * 0.7, window_width, 5)

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
            object_button_assets[asset],
            1,
            asset,
        )
    )
    i += 1

objects = []

run = True
engine_fps = 60
clock = pg.time.Clock()

# GUI movement and selection
selected_object_button = None
selected_object = None
upload_button_clicked = False


# Creation of project
upload_button = Button((window_width-button_width, 0), button_assets["Upload"])
project_name = "TestProject"
if not isdir(project_name):
    createEnvironment(project_name)
exec(f"from {project_name}.objects import objects")


def display():
    window.fill((30, 30, 30))

    # color coding
    pg.draw.rect(window, (80, 80, 80), object_button_div_rect)
    window.fill(
        (60, 60, 60), (0, object_button_div_rect.bottom, window_width, window_height)
    )

    # object buttons
    for button in object_buttons:
        button.display(window)

    # added objects
    for obj in objects:
        obj.display(window)

    upload_button.display(window)

    pg.display.update()


# main script
while run:

    clock.tick(engine_fps)

    for event in pg.event.get():

        if event.type == pg.QUIT:
            run = False

        if event.type == pg.MOUSEBUTTONDOWN:

            mouse_x, mouse_y = pg.mouse.get_pos()

            for i, obj in enumerate(objects):
                if obj.collidepoint((mouse_x, mouse_y)):
                    selected_object = i

            for i, button in enumerate(object_buttons):
                if button.clicked():
                    button.image = object_button_assets[button.info + " Pressed"]
                    button.y += button_height - button_width
                    selected_object_button = i

            if upload_button.clicked():
                upload_button.image = button_assets["Upload Pressed"]
                upload_button.y += button_height - button_width
                upload_button_clicked = True

        if event.type == pg.MOUSEBUTTONUP:

            if upload_button_clicked:

                # button reseting
                upload_button.image = button_assets["Upload"]
                upload_button.y -= button_height - button_width
                upload_button_clicked = False

                # saving GUI objects
                saveGUIObjects(objects, f"{project_name}/objects.py")



            if selected_object_button is not None:
                objects.append(
                    Button(
                        (window_width / 2, window_height / 4),
                        object_assets["Blank Button"],
                        1,
                        {"Asset": "Blank Button", "Scale": 1, "Type": "Button", "Info": ()}
                    )
                )

                object_buttons[selected_object_button].image = object_button_assets[
                    object_buttons[selected_object_button].info
                ]
                object_buttons[selected_object_button].y -= (
                    button_height - button_width
                )
                selected_object_button = None

            if selected_object is not None:
                selected_object is None

    mouse_rel_x, mouse_rel_y = pg.mouse.get_rel()
    left_mouse_button_down = pg.mouse.get_pressed()[0]
    if left_mouse_button_down:
        if selected_object is not None:
            objects[selected_object].x += mouse_rel_x
            objects[selected_object].y += mouse_rel_y

    display()

pg.quit()
quit()
