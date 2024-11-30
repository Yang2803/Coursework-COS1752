# main.py
from tkinter import Tk
from mediaplayer import MediaPlayer
from tkinter import *
import pygame

pygame.mixer.init()

if __name__ == "__main__":
    root = Tk()
    media_player = MediaPlayer(root)
    root.mainloop()
