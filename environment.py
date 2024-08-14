from os import mkdir, listdir
from os.path import isdir
import shutil

def createStarterScript(path, name):
    with open(path, "w") as file:
        file.write("")
        file.close()
    with open(path, "a") as file:
        file.write(f"""
import pygame as pg
from assets import *
from engineFunctions import *
from objects import * 


window = pg.display.set_mode()
window_width, window_height = window.get_size()
pg.display.set_caption('{name}')

try:
    objects = load_data("objects.pkl")
except:
    objects = load_data("{name}/objects.pkl")
for obj in objects:
    obj.unpack(window_width, window_height)

clock = pg.time.Clock()
fps = 60
run = True

selected_button = None

def display():
    window.fill((255, 255, 255))

    for obj in objects:
        obj.display(window)

    pg.display.update()

while run:
    
    clock.tick(fps)

    for event in pg.event.get():

        if event.type == pg.QUIT:
            run = False

    for obj in objects:
        if obj.type == "Button":
            obj.clicked()
            obj.released()
            obj.pressed()

    display()

pg.quit()
quit()
                   """)
        file.close()
        

def createAssetsFile(path):
    with open(path, "w") as file:
        file.write("")
        file.close()
    with open(path, "a") as file:
        file.write("""
from engineFunctions import load_assets
assets = load_assets("assets/Object Assets", None, 2)
""")
        file.close()


def createEnvironment(name):
    
    # creating required directories
    mkdir(name)
    mkdir(f"{name}/assets")
    mkdir(f"{name}/assets/Object Assets")

    # copying assets
    for file in listdir("assets/Object Assets"):
        shutil.copy(f"assets/Object Assets/{file}", f"{name}/assets/Object Assets/")    

    # copying files
    shutil.copy("engineFunctions.py", f"{name}/")
    shutil.copy("objects.py", f"{name}/")

    createStarterScript(f"{name}/main.py", name)
    createAssetsFile(f"{name}/assets.py")


    