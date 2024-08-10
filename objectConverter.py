from os import mkdir, listdir
from os.path import isdir
import shutil

def convertGUIObject(object):
    info = object.info
    object_pos = object.topleft
    if info["Type"] == "Button":
        return f"Button({object_pos}, object_assets['{info["Asset"]}'], {info["Scale"]})" 
    raise Exception("Invalid Object Type")

def convertGUIObjects(objects):
    convertedObjects = "objects = [\n"
    for obj in objects:
        convertedObjects += convertGUIObject(obj) + ",\n"
    convertedObjects += "]\n"

    return convertedObjects

def saveConvertedObjects(convertedObjects, path):
    with open(path, "w") as file:
        file.write("")
        file.close()
    with open(path, "a") as file:
        file.write("import pygame as pg\nfrom engineFunctions import *\nobject_assets = load_assets('assets/Object Assets', None, 2)\n")
        for cObj in convertedObjects:
            file.write(cObj)
        file.close()

def saveGUIObjects(objects, path):
    convertedObjects = convertGUIObjects(objects)
    saveConvertedObjects(convertedObjects, path)

def createStarterScript(path):
    with open(path, "w") as file:
        file.write("")
        file.close()
    with open(path, "a") as file:
        file.write("import pygame as pg\nfrom objects import *")

def createStarterObjectScript(path):
    with open(path, "w") as file:
        file.write("")
        file.close()
    with open(path, "a") as file:
        file.write("import pygame as pg\nfrom engineFunctions import *\nobject_assets = load_assets('assets/Object Assets', None, 2)\nobjects = []")

def createEnvironment(name):
    
    # creating required directories
    mkdir(name)
    mkdir(f"{name}/assets")
    mkdir(f"{name}/assets/Object Assets")

    # copying assets
    for file in listdir("assets/Object Assets"):
        shutil.copy(f"assets/Object Assets/{file}", f"{name}/assets/Object Assets/")    

    # copying functions
    shutil.copy("engineFunctions.py", f"{name}/")

    createStarterObjectScript(f"{name}/objects.py")


    