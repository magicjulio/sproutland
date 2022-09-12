from os import walk
import pygame

def import_folder(path):
    surfaces = []
    for _, __, img_files in walk(path):
        for img in img_files:
            full_path = path + "/" + img
            image_surface = pygame.image.load(full_path).convert_alpha()
            surfaces.append(image_surface)


    return  surfaces

def import_folder_dict(path):
    surface_dict = {}
    for _, __, img_files in walk(path):
        for img in img_files:
            full_path = f"{path}/{img}"
            image_surface = pygame.image.load(full_path).convert_alpha()
            surface_dict[img.split(".")[0]] = image_surface
    return surface_dict