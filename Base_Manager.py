
from tkinter import *
import pygame

pygame.mixer.init()

class BaseManager:
    def load(self, filename):
        raise NotImplementedError("Load method not implemented.")

    def save(self, filename, data):
        raise NotImplementedError("Save method not implemented.")