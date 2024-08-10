def convertGUIObject(object):
    info = object
    object_pos = object.topleft
    if info["Type"] == "Button":
        return f"Button({object_pos}, object_assets['{info["Asset"]}'], {info["Scale"]})" 
    raise Exception("Invalid Object Type")

def convertGUIObjects(objects):
    convertedObjects = "[\n"
    for obj in objects:
        convertedObjects += convertGUIObject(obj) + ",\n"
    convertedObjects += "]\n"

    return convertedObjects

def saveConvertedObjects(convertedObjects, path):
    with open(path, "w") as file:
        file.write("")
        file.close()
    with open(path, "a") as file:
        file.write("import pygame as pg\nfrom engineFunctions import *\n")
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

def createEnvironment(name):
    pass
