# mediaplayer.py
import os
import random
import csv
from tkinter import *
from tkinter import filedialog, messagebox
from song_manager import SongManager
from playlist_manager import PlaylistManager
from playback_manager import PlaybackManager
from ui_manager import UIManager
import pygame

pygame.mixer.init()

class MediaPlayer:
    def __init__(self, root):
        self.root = root
        self.song_manager = SongManager()
        self.playlist_manager = PlaylistManager()
        self.playback_manager = PlaybackManager(self)
        self.ui_manager = UIManager(self)  # Properly initialize UIManager

        self.load_data()

    def load_data(self):
        # Load songs and playlists
        self.song_manager.load()  # Load songs from the CSV
        self.playlist_manager.load()  # Load playlists from the CSV
        
        self.ui_manager.song_box.delete(0, END)  # Clear existing songs from the Listbox
        for song_name in self.song_manager.song_dict.keys():
            self.ui_manager.song_box.insert(END, song_name)  # Add each song to the Listbox
    
    
    def skip_10_seconds(self):
        """ Skip 10 seconds forward in the current song. """
        if self.playback_manager.player and self.playback_manager.player.is_playing():
            current_time = self.playback_manager.player.get_time()  # Get current playback time (in milliseconds)
            new_time = current_time + 10000  # Skip forward 10 seconds (10,000 ms)
            self.playback_manager.player.set_time(new_time)  # Set the new time
            print(f"Skipped forward by 10 seconds: {new_time} ms")

    def back_10_seconds(self):
        """ Rewind 10 seconds back in the current song. """
        if self.playback_manager.player and self.playback_manager.player.is_playing():
            current_time = self.playback_manager.player.get_time()  # Get current playback time (in milliseconds)
            new_time = max(current_time - 10000, 0)  # Don't go below 0
            self.playback_manager.player.set_time(new_time)  # Set the new time
            print(f"Rewound back by 10 seconds: {new_time} ms")

    def on_song_end(self, event):
        if self.playback_manager.repeat:
            current_song = self.ui_manager.song_box.get(ACTIVE)
            self.playback_manager.play_song(current_song)
        elif self.playback_manager.shuffle:
            # Play the next random song from the shuffled order
            if self.playback_manager.current_shuffle_index + 1 < len(self.playback_manager.shuffle_order):
                next_song = self.playback_manager.shuffle_order[self.playback_manager.current_shuffle_index + 1]
                self.playback_manager.play_song(next_song)
                self.playback_manager.current_shuffle_index += 1
            else:
                # If it's the last song in the shuffle order, restart shuffle
                random.shuffle(self.playback_manager.shuffle_order)
                self.playback_manager.current_shuffle_index = 0
                next_song = self.playback_manager.shuffle_order[0]
                self.playback_manager.play_song(next_song)
        else:
            # Play the next song in the list
            current_song_index = self.ui_manager.song_box.curselection()
            next_song_index = current_song_index[0] + 1 if current_song_index else 0

            if next_song_index < self.ui_manager.song_box.size():
                next_song = self.ui_manager.song_box.get(next_song_index)
                self.playback_manager.play_song(next_song)
            else:
                # If we're at the end of the song list, play the first song again
                first_song = self.ui_manager.song_box.get(0)
                self.playback_manager.play_song(first_song)


    def add_many_songs(self):
        songs = filedialog.askopenfilenames(initialdir='audio/', title="Choose Songs", filetypes=(("MP3 and MP4 Files", "*.mp3;*.mp4"),))
        for song in songs:
            song_name = os.path.basename(song).replace(".mp3", "").replace(".mp4", "")
            if song_name not in self.song_manager.song_dict:  # Ensure not to add duplicates
                self.ui_manager.song_box.insert(END, song_name)
                self.song_manager.song_dict[song_name] = song  # Save the song path in the dictionary
        self.song_manager.save()  # Save updated song list to CSV after adding all songs
        
    
    def create_playlist(self):
        self.playlist_window = Toplevel(self.root)
        self.playlist_window.title("Create New Playlist")
        self.playlist_window.geometry("400x200")
        self.playlist_window.attributes('-topmost', True)

        self.playlist_name_entry = Entry(self.playlist_window, width=50)
        self.playlist_name_entry.pack(pady=20)

        create_button = Button(self.playlist_window, text="Create Playlist", command=self.save_playlist)
        create_button.pack(pady=10)

    def save_playlist(self):
        playlist_name = self.playlist_name_entry.get()
        if playlist_name:
            self.playlist_manager.playlists[playlist_name] = []
            self.playlist_manager.save()
            messagebox.showinfo("Playlist Created", f"Playlist '{playlist_name}' created!")
            self.playlist_window.destroy()
        else:
            messagebox.showwarning("Warning", "Please enter a playlist name.")

    def manage_playlists(self):
        self.manage_window = Toplevel(self.root)
        self.manage_window.title("Manage Playlists")
        self.manage_window.geometry("400x700")

        self.manage_window.attributes('-topmost', True)

        self.playlist_listbox = Listbox(self.manage_window, bg="black", fg="green")
        self.playlist_listbox.pack(pady=10, fill=BOTH, expand=True)

        for playlist in self.playlist_manager.playlists.keys():
            self.playlist_listbox.insert(END, playlist)

        self.song_listbox = Listbox(self.manage_window, bg="black", fg="green")
        self.song_listbox.pack(pady=10, fill=BOTH, expand=True)

        self.playlist_listbox.bind("<<ListboxSelect>>", self.display_songs_in_playlist)

        add_songs_button = Button(self.manage_window, text="Add Selected Songs to Playlist", command=self.add_songs_to_playlist)
        add_songs_button.pack(pady=10)

        play_playlist_button = Button(self.manage_window, text="Play Selected Playlist", command=self.play_selected_playlist)
        play_playlist_button.pack(pady=10)

        delete_playlist_button = Button(self.manage_window, text="Delete Selected Playlist", command=self.delete_selected_playlist)
        delete_playlist_button.pack(pady=10)

        delete_song_button = Button(self.manage_window, text="Delete Selected Song from Playlist", command=self.delete_song_from_playlist)
        delete_song_button.pack(pady=10)

    def display_songs_in_playlist(self, event):
        self.song_listbox.delete(0, END)
        selected_playlist = self.playlist_listbox.get(ACTIVE)

        if selected_playlist in self.playlist_manager.playlists:
            for song in self.playlist_manager.playlists[selected_playlist]:
                self.song_listbox.insert(END, song)

    def add_songs_to_playlist(self):
        selected_playlist = self.playlist_listbox.get(ACTIVE)
        selected_songs = self.ui_manager.song_box.curselection()
        
        if selected_playlist and selected_songs:
            for index in selected_songs:
                song_name = self.ui_manager.song_box.get(index)
                if song_name not in self.playlist_manager.playlists[selected_playlist]:
                    self.playlist_manager.playlists[selected_playlist].append(song_name)
            self.playlist_manager.save()
            messagebox.showinfo("Success", "Songs added to the playlist.")

    def play_selected_playlist(self):
        selected_playlist = self.playlist_listbox.get(ACTIVE)
        if selected_playlist and selected_playlist in self.playlist_manager.playlists:
            songs = self.playlist_manager.playlists[selected_playlist]
            self.ui_manager.song_box.delete(0, END)  # Clear the song box
            for song in songs:
                self.ui_manager.song_box.insert(END, song)  # Add songs to the song box
            
            if songs:
                self.playback_manager.play_song(songs[0])  # Play the first song in the selected playlist

    def delete_selected_playlist(self):
        selected_playlist = self.playlist_listbox.get(ACTIVE)
        if selected_playlist in self.playlist_manager.playlists:
            del self.playlist_manager.playlists[selected_playlist]
            self.playlist_manager.save()
            self.playlist_listbox.delete(ACTIVE)
            self.song_listbox.delete(0, END)
            messagebox.showinfo("Success", "Playlist deleted.")

    def delete_song_from_playlist(self):
        selected_playlist = self.playlist_listbox.get(ACTIVE)
        selected_song = self.song_listbox.get(ACTIVE)
        
        if selected_playlist in self.playlist_manager.playlists and selected_song in self.playlist_manager.playlists[selected_playlist]:
            self.playlist_manager.playlists[selected_playlist].remove(selected_song)
            self.playlist_manager.save()
            self.display_songs_in_playlist(None)  # Refresh song list
            messagebox.showinfo("Success", "Song removed from playlist.")

    def repeat_song(self):
        self.playback_manager.repeat = not self.playback_manager.repeat
        state = "on" if self.playback_manager.repeat else "off"
        messagebox.showinfo("Repeat", f"Repeat is now {state}.")

    def shuffle_song(self):
        if self.playback_manager.shuffle:
            self.playback_manager.shuffle = False
            self.playback_manager.shuffle_order = []
            messagebox.showinfo("Shuffle", "Shuffle is now off.")
        else:
            self.playback_manager.shuffle = True
            self.playback_manager.shuffle_order = list(self.song_manager.song_dict.keys())
            random.shuffle(self.playback_manager.shuffle_order)
            self.playback_manager.current_shuffle_index = 0
            messagebox.showinfo("Shuffle", "Shuffle is now on.")
    # Immediately play a random song after enabling shuffle
            song_count = self.ui_manager.song_box.size()
            if song_count > 0:
                random_index = random.randint(0, song_count - 1)
                random_song_name = self.ui_manager.song_box.get(random_index)
                self.playback_manager.play_song(random_song_name)  # Play the random song
                
    def delete_song(self):
        # Get the currently selected song in the song_box
        selected_song_index = self.ui_manager.song_box.curselection()
        if selected_song_index:
            song_name = self.ui_manager.song_box.get(selected_song_index)

            # Remove the song from the song_box and song_dict
            self.ui_manager.song_box.delete(selected_song_index)
            if song_name in self.song_manager.song_dict:
                song_path = self.song_manager.song_dict[song_name]  # Get the song path to save it in recycle bin
                self.move_to_recycle_bin(song_name, song_path)  # Move to recycle bin
                del self.song_manager.song_dict[song_name]  # Remove from song dict

            # Update the songs.csv file to reflect the changes
            self.song_manager.save()  # Save updated song list to CSV
            messagebox.showinfo("Song Deleted", f"'{song_name}' has been moved to the recycle bin.")
        else:
            messagebox.showwarning("No Selection", "Please select a song to delete.")

    def move_to_recycle_bin(self, song_name, song_path):
        # Append the song to the recycle_bin.csv file
        with open('recycle_bin.csv', 'a', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([song_name, song_path])  # Save the song name and path in the recycle bin
            
    def manage_recycle_bin(self):
        self.recycle_bin_window = Toplevel(self.root)
        self.recycle_bin_window.title("Recycle Bin")
        self.recycle_bin_window.geometry("400x400")
        
        # Ensure the recycle bin window stays on top
        self.recycle_bin_window.attributes('-topmost', True)
        
        self.recycle_bin_listbox = Listbox(self.recycle_bin_window, bg="black", fg="green")
        self.recycle_bin_listbox.pack(pady=10, fill=BOTH, expand=True)

        self.load_recycle_bin()

        restore_button = Button(self.recycle_bin_window, text="Restore Selected Song", command=self.restore_song)
        restore_button.pack(pady=10)

        delete_forever_button = Button(self.recycle_bin_window, text="Delete Forever", command=self.delete_forever)
        delete_forever_button.pack(pady=10)

    def load_recycle_bin(self):
        if os.path.exists('recycle_bin.csv'):
            with open('recycle_bin.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    song_name = row[0]
                    self.recycle_bin_listbox.insert(END, song_name)

    def restore_song(self):
        selected_index = self.recycle_bin_listbox.curselection()
        if selected_index:
            song_name = self.recycle_bin_listbox.get(selected_index)
            # Find the song path in recycle_bin.csv
            song_path = self.find_song_path_in_recycle_bin(song_name)

            if song_path:
                # Add the song back to the main list and save
                self.song_manager.song_dict[song_name] = song_path
                self.ui_manager.song_box.insert(END, song_name)  # Add it to the UI list
                self.song_manager.save()  # Save updated song list
                self.remove_from_recycle_bin(song_name)  # Remove from recycle bin
                 # Immediately remove the song from the recycle bin listbox
                self.recycle_bin_listbox.delete(selected_index)
                messagebox.showinfo("Restored", f"'{song_name}' has been restored.")
                
                
            else:
                messagebox.showwarning("Warning", "Could not find song path.")
        else:
            messagebox.showwarning("No Selection", "Please select a song to restore.")

    def delete_forever(self):
        selected_index = self.recycle_bin_listbox.curselection()
        if selected_index:
            song_name = self.recycle_bin_listbox.get(selected_index)
            self.remove_from_recycle_bin(song_name)  # Permanently delete from recycle bin
            self.recycle_bin_listbox.delete(selected_index)  # Remove from UI list
            messagebox.showinfo("Deleted", f"'{song_name}' has been permanently deleted.")
        else:
            messagebox.showwarning("No Selection", "Please select a song to delete.")

    def find_song_path_in_recycle_bin(self, song_name):
        with open('recycle_bin.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == song_name:
                    return row[1]  # Return the song path
        return None

    def remove_from_recycle_bin(self, song_name):
        # Read current recycle bin content
        with open('recycle_bin.csv', 'r') as file:
            lines = file.readlines()

        # Write back all lines except the one to be removed
        with open('recycle_bin.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for line in lines:
                if line.strip().split(',')[0] != song_name:  # Avoid writing the deleted song
                    writer.writerow(line.strip().split(','))