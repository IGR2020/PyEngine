from engineFunctions import load_assets

# assets
button_width = 64
button_height = 72
object_button_assets = load_assets(
    "assets/Object Buttons", (button_width, button_height), 2
)
object_assets = load_assets("assets/Object Assets", None, 2)
button_assets = load_assets("assets/Buttons", (button_width, button_height), 2)
assets = {}
assets.update(button_assets), assets.update(object_assets), assets.update(object_button_assets)
