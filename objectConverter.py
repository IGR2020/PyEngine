from os import mkdir, listdir
from os.path import isdir
import shutil

def convertGUIObject(object):
    info = object.info
    object_pos = object.topleft
    if info["Type"] == "Button":
        return f"Button({object_pos}, object_assets['{info["Asset"]}'], {info["Scale"]}, {info})", f"Button({object_pos}, object_assets['{info["Asset"]}'], {info["Scale"]}, {info["Info"]})"
    raise Exception("Invalid Object Type")

def convertGUIObjects(objects):
    loadableConvertedObjects = "objects = [\n"
    usableConvertedObjects = "objects = [\n"
    
    for obj in objects:
        loadable_obj, usable_obj  = convertGUIObject(obj)
        loadableConvertedObjects += loadable_obj + ",\n"
        usableConvertedObjects += usable_obj + ",\n"

    loadableConvertedObjects += "]\n"
    usableConvertedObjects += "]\n"

    return loadableConvertedObjects, usableConvertedObjects

def sortConvertedGUIObject(convertedObject: str):
    objects = convertedObject.splitlines()
    objects.pop(0)
    objects.pop(-1)

    buttonObjects = "buttons = [\n"

    for obj in objects:
        if "Button" in obj:
            buttonObjects += obj + "\n"
    
    buttonObjects += "]\n"

    return (buttonObjects,)


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
    loadableConvertedObjects, usableConvertedObjects = convertGUIObjects(objects)
    sortedObjects = sortConvertedGUIObject(usableConvertedObjects)
    saveConvertedObjects((loadableConvertedObjects, *sortedObjects), path)

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


    