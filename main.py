import pygame as pg
from engineFunctions import load_assets, Button

window = pg.display.set_mode((1000, 600))
window_width, window_height = window.get_size()

pg.display.set_caption("PyEngine")

# assets
object_button_width = 64
object_button_height = 72
object_button_assets = load_assets(
    "assets/Buttons", (object_button_width, object_button_height), 2
)

# decorational
object_button_div_rect = pg.Rect(0, window_height * 0.6, window_width, 5)

# buttons
object_button_spacing = 5
object_buttons = []
i = 0
for  asset in object_button_assets:
    if "Pressed" in asset:
        continue
    object_buttons.append(
        Button(
            (
                i * object_button_width + i * object_button_spacing,
                object_button_div_rect.bottom,
            ),
            object_button_assets[asset],
            1,
            asset
        )
    )
    i += 1

run = True
engine_fps = 60
clock = pg.time.Clock()


def display():
    window.fill((0, 0, 0))

    # color coding
    pg.draw.rect(window, (40, 40, 40), object_button_div_rect)
    window.fill((30, 30, 30), (0, object_button_div_rect.bottom, window_width, window_height))

    # object buttons
    for button in object_buttons:
        button.display(window)

    pg.display.update()


# main script
while run:

    clock.tick(engine_fps)

    for event in pg.event.get():

        if event.type == pg.QUIT:
            run = False

        if event.type == pg.MOUSEBUTTONDOWN:

            mouse_x, mouse_y = pg.mouse.get_pos()

            for i, button in enumerate(object_buttons):
                if button.collidepoint(mouse_x, mouse_y):
                    button.image = object_button_assets[button.info + " Pressed"]
                    button.y += object_button_height - object_button_width
                    selected_object_button = i

        if event.type == pg.MOUSEBUTTONUP:
            object_buttons[selected_object_button].image = object_button_assets[object_buttons[selected_object_button].info]
            button.y -= object_button_height - object_button_width
    display()

pg.quit()
quit()
