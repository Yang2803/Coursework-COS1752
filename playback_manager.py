# playback_manager.py

import vlc
from tkinter import *
import pygame
import random

pygame.mixer.init()

class PlaybackManager:
    def __init__(self, media_player):
        self.media_player = media_player
        self.player = None
        self.is_paused = False
        self.repeat = False
        self.shuffle = False
        self.shuffle_order = []
        self.current_shuffle_index = 0
        self.speed = 1.0

    def play_song(self, song_name=None):
        if song_name is None:
            song_name = self.media_player.ui_manager.song_box.get(ACTIVE)

        if song_name in self.media_player.song_manager.song_dict:
            song_path = self.media_player.song_manager.song_dict[song_name]
            if self.player:
                self.player.stop()

            self.player = vlc.MediaPlayer(song_path)
            self.player.set_mrl(f"file:///{song_path}?cache=1000")  # Enable caching
            self.player.set_hwnd(self.media_player.ui_manager.video_frame.winfo_id())
            self.player.play()
            self.is_paused = False
            
            # Set the initial playback speed
            self.set_speed(self.speed)  # Set the speed right after playing the song

            self.setup_event_listeners()  # Attach event listeners after the player is ready
        
        

    def set_speed(self, speed):
        """ Set the playback speed of the song. """
        self.speed = speed
        if self.player:
            try:
                self.player.set_rate(self.speed)  # VLC uses set_rate to adjust speed
            except Exception as e:
                print(f"Error setting playback speed: {e}")

    def setup_event_listeners(self):
        self.player.event_manager().event_attach(vlc.EventType.MediaPlayerPlaying, self.on_playing)
        self.player.event_manager().event_attach(vlc.EventType.MediaPlayerEncounteredError, self.on_error)
            # Attach event handlers
        self.player.event_manager().event_attach(vlc.EventType.MediaPlayerEndReached, self.media_player.on_song_end)



    def toggle_pause(self):
        if self.player:
            if self.is_paused:
                self.player.play()
                self.is_paused = False
            else:
                self.player.pause()
                self.is_paused = True

    def stop_song(self):
        if self.player:
            self.player.stop()
            self.is_paused = False
    
    def next_song(self):
        if self.media_player.playback_manager.repeat:
        # If repeat is on, play the current song again from the start
            current_index = self.media_player.ui_manager.song_box.curselection()
            if not current_index:
                return
            current_index = current_index[0]
            current_song_name = self.media_player.ui_manager.song_box.get(current_index)
            self.play_song(current_song_name)
        else:
            if self.shuffle:
            # Shuffle mode: Pick a random song from the song_box
                song_count = self.media_player.ui_manager.song_box.size()
                if song_count > 0:
                    random_index = random.randint(0, song_count - 1)
                    next_song_name = self.media_player.ui_manager.song_box.get(random_index)
                    self.media_player.ui_manager.song_box.select_clear(0, END)  # Clear any selection
                    self.media_player.ui_manager.song_box.select_set(random_index)  # Select the new song
                    self.play_song(next_song_name)
            else:
            # Sequential mode: Move to the next song in the list
                current_index = self.media_player.ui_manager.song_box.curselection()
                if not current_index:
                    return
                current_index = current_index[0]
                next_index = (current_index + 1) % self.media_player.ui_manager.song_box.size()  # Loop back to start if at the end
                next_song_name = self.media_player.ui_manager.song_box.get(next_index)

                self.media_player.ui_manager.song_box.select_clear(current_index)
                self.media_player.ui_manager.song_box.select_set(next_index)
                self.play_song(next_song_name)

    def previous_song(self):
        if self.media_player.playback_manager.repeat:
        # If repeat is on, play the current song again from the start
            current_index = self.media_player.ui_manager.song_box.curselection()
            if not current_index:
                return
            current_index = current_index[0]
            current_song_name = self.media_player.ui_manager.song_box.get(current_index)
            self.play_song(current_song_name)
        else:
            if self.shuffle:
            # Shuffle mode: Pick a random song from the song_box
                song_count = self.media_player.ui_manager.song_box.size()
                if song_count > 0:
                    random_index = random.randint(0, song_count - 1)
                    prev_song_name = self.media_player.ui_manager.song_box.get(random_index)
                    self.media_player.ui_manager.song_box.select_clear(0, END)  # Clear any selection
                    self.media_player.ui_manager.song_box.select_set(random_index)  # Select the new song
                    self.play_song(prev_song_name)
            else:
            # Sequential mode: Move to the previous song in the list
                current_index = self.media_player.ui_manager.song_box.curselection()
                if not current_index:
                    return
                current_index = current_index[0]
                prev_index = (current_index - 1) % self.media_player.ui_manager.song_box.size()  # Loop back to end if at the start
                prev_song_name = self.media_player.ui_manager.song_box.get(prev_index)

                self.media_player.ui_manager.song_box.select_clear(current_index)
                self.media_player.ui_manager.song_box.select_set(prev_index)
                self.play_song(prev_song_name)


    
    def get_song_duration(self):
        if self.player:
            return self.player.get_length()  # Duration in milliseconds
        return 0

    def get_current_position(self):
        if self.player:
            return self.player.get_time()  # Current position in milliseconds
        return 0