# playlist_manager.py
import csv
import csv
from Base_Manager import BaseManager
from tkinter import *
import pygame
import csv
import os

pygame.mixer.init()

class PlaylistManager(BaseManager):
    def __init__(self):
        self.playlists = {}

    def load(self):
        if os.path.exists('playlists.csv'):
            with open('playlists.csv', 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    playlist_name = row[0]
                    songs = row[1:]  # Remaining items are song names
                    self.playlists[playlist_name] = songs

    def save(self):
        with open('playlists.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for playlist_name, songs in self.playlists.items():
                writer.writerow([playlist_name] + songs)