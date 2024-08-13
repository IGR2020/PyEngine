import pygame as pg
from os import listdir
from os.path import join, isfile, isdir
import pickle

def save_data(data, path):
    with open(path, "wb") as file:
        pickle.dump(data, file)
        file.close()

def load_data(path):
    with open(path, "rb") as file:
        data = pickle.load(file)
        file.close()
    return data


pg.font.init()


def blit_text(
    win,
    text,
    pos,
    colour=(0, 0, 0),
    size=30,
    font="arialblack",
    blit=True,
    centerx=False,
    centery=False,
    center=False,
):
    text = str(text)
    x, y = pos
    font_style = pg.font.SysFont(font, size)
    text_surface = font_style.render(text, True, colour)
    if center:
        x -= text_surface.get_width() // 2
        y -= text_surface.get_height() // 2
    else:
        if centerx:
            x -= text_surface.get_width() // 2
        if centery:
            y -= text_surface.get_height() // 2
    if blit:
        win.blit(text_surface, (x, y))
    return text_surface


def load_assets(path, size: int = None, scale: float = None, getSubDirsAsList=False):
    sprites = {}
    for file in listdir(path):
        if getSubDirsAsList and isdir(join(path, file)):
            sprites[file.replace(".png", "")] = load_assets_list(
                join(path, file), size, scale
            )
            continue
        elif not isfile(join(path, file)):
            continue
        if size is None and scale is None:
            sprites[file.replace(".png", "")] = pg.image.load(join(path, file))
        elif scale is not None:
            sprites[file.replace(".png", "")] = pg.transform.scale_by(
                pg.image.load(join(path, file)), scale
            )
        else:
            sprites[file.replace(".png", "")] = pg.transform.scale(
                pg.image.load(join(path, file)), size
            )
    return sprites


def load_assets_list(path, size: int = None, scale: float = None):
    sprites = []
    for file in listdir(path):
        if not isfile(join(path, file)):
            continue
        if size is None and scale is None:
            sprites.append(pg.image.load(join(path, file)))
        elif scale is not None:
            sprites.append(
                pg.transform.scale_by(pg.image.load(join(path, file)), scale)
            )
        else:
            sprites.append(pg.transform.scale(pg.image.load(join(path, file)), size))
    return sprites


def flip(sprites):
    return [pg.transform.flip(sprite, True, False) for sprite in sprites]


def load_sprite_sheets(
    path, width, height, direction=True, resize=None, autocrop=False
):
    images = [f for f in listdir(path) if isfile(join(path, f))]
    all_sprites = {}

    for image in images:
        sprite_sheet = pg.image.load(join(path, image)).convert_alpha()
        sprites = []

        for i in range(sprite_sheet.get_width() // width):
            for j in range(sprite_sheet.get_height() // height):
                surface = pg.Surface((width, height), pg.SRCALPHA, 32)
                rect = pg.Rect(i * width, j * height, width, height)
                surface.blit(sprite_sheet, (0, 0), rect)
                sprites.append(pg.transform.scale2x(surface))

        if resize is not None:
            sprites = [pg.transform.scale(surface, resize) for surface in sprites]

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites
