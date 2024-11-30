# song_manager.py
import csv
from Base_Manager import BaseManager
from tkinter import *
import pygame
import os



pygame.mixer.init()


class SongManager(BaseManager):
    def __init__(self):
        self.song_dict = {}

    def load(self):
        if os.path.exists('songs.csv'):
            with open('songs.csv', 'r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) >= 2:
                        song_name = row[0]
                        song_path = row[1]
                        self.song_dict[song_name] = song_path

    def save(self):
        with open('songs.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for song_name, song_path in self.song_dict.items():
                writer.writerow([song_name, song_path])