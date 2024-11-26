from os import listdir
from os.path import isfile
import pygame as pg


def loadAssets(path, scale=1, size=None) -> dict[str, pg.Surface]:
    assets = {}
    for file in listdir(path):
        if not isfile(f"{path}/{file}"):
            continue
        if size is None:
            assets[file.replace(".png", "")] = pg.transform.scale_by(pg.image.load(f"{path}/{file}"), scale)
            continue
        assets[file.replace(".png", "")] = pg.transform.scale(
            pg.transform.scale_by(pg.image.load(f"{path}/{file}"), scale), size)
    return assets