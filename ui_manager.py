from tkinter import Listbox, Scrollbar, Button, Tk
from tkinter import *
from PIL import ImageTk, Image
import pygame
import eyed3
from moviepy.editor import VideoFileClip
import os

pygame.mixer.init()

class UIManager:
    def __init__(self, media_player):
        self.media_player = media_player
        self.setup_ui()
        self.last_position_update = 0  # Track the last position update
        self.is_seeking = False  # Flag to indicate if we're seeking
        self.root = media_player.root
        # Tooltip label for song details
        self.details_label = Label(self.media_player.root, text="", bg="white", font=("Arial", 10), relief=SOLID, bd=1)
        self.details_label.place(x=0, y=0, width=200, height=50)
        self.details_label.lower()  # Hide the details initially
    def setup_ui(self):
        self.media_player.root.title('Jumping to my Dreaming World')
        self.media_player.root.geometry('1920x1080')
        self.media_player.root.configure(background='black')

        # Add background
        self.bg = ImageTk.PhotoImage(file='bg.jpg')
        bgmain = Label(self.media_player.root, image=self.bg, width="1920", height='870')
        bgmain.place(x=0, y=0)

        self.video_frame = Frame(self.media_player.root, width=1280, height=720)
        self.video_frame.place(x=320 , y=150)

        self.mp3_image = ImageTk.PhotoImage(Image.open('bg.jpg'))
        self.image_label = Label(self.video_frame, image=self.mp3_image, width=100, height=720)
        self.image_label.pack(fill=BOTH, expand=True)

        # Frame for song box and scrollbar
        self.song_frame = Frame(self.media_player.root)
        self.song_frame.pack(pady=0)

        # Search Entry
        self.search_entry = Entry(self.song_frame, width=50)
        self.search_entry.pack(pady=10)
        self.search_entry.bind("<KeyRelease>", self.filter_songs)  # Bind the entry to the filter method

        # Create Listbox
        self.song_box = Listbox(self.song_frame, bg="black", fg="green", width="60", selectbackground='gray', selectforeground='black')
        self.song_box.pack(side=LEFT, fill=BOTH, expand=True)

        # Create Scrollbar
        self.scrollbar = Scrollbar(self.song_frame)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        # Attach scrollbar to song_box
        self.song_box.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.song_box.yview)

        self.video_frame = Frame(self.media_player.root, width=1280, height=720)
        self.video_frame.place(x=200, y=150)

        self.mp3_image = ImageTk.PhotoImage(Image.open('bg.jpg'))

        self.image_label = Label(self.video_frame, image=self.mp3_image, width=1280, height=720)
        self.image_label.pack(fill=BOTH, expand=True)

        # Label to show song duration
        self.duration_label = Label(self.media_player.root, text="00:00 / 00:00", bg='white', font=("Arial", 12))
        self.duration_label.place(x=320, y=880)  # Adjust the position as needed

        # Scale for seeking
        self.seek_bar = Scale(self.media_player.root, from_=0, to=100, orient=HORIZONTAL, length=700, command=self.seek_song)
        self.seek_bar.place(x=220, y=910)  # Adjust the position as needed
        
        self.delete_song = Button(self.media_player.root, text="Delete song", command=self.delete_song)
        self.delete_song.pack(pady=30)
        self.delete_song.place(x=1050, y=120)

         # Add speed control slider (range from 0.5x to 2.0x speed)
        self.speed_slider = Scale(self.media_player.root, from_=0.5, to=2.0, orient=HORIZONTAL, resolution=0.1, length=300, label="Speed", command=self.change_speed)
        self.speed_slider.set(1.0)  # Default to normal speed
        self.speed_slider.place(x=930, y=893)  # Position the speed slider
        

        self.create_buttons()
        self.create_menu()

        # Start the update loop
        self.update_duration_and_position()
        
        self.populate_song_list()
    def populate_song_list(self):
        # Assuming the song_dict is already populated in the song_manager
        for song_name in self.media_player.song_manager.song_dict.keys():
            self.song_box.insert(END, song_name)  # Add song names to the Listbox

        # Bind the click event to each song item
        self.song_box.bind("<Button-1>", self.on_song_click)  # To show details on click

    def change_speed(self, speed_value):
        """ Adjust the speed slider value. """
        self.media_player.playback_manager.set_speed(float(speed_value))

    def on_song_click(self, event):
        """ Show the details when a song or video is clicked. """
    # Get the item clicked in the Listbox
        index = self.song_box.nearest(event.y)
        media_name = self.song_box.get(index)

    # Debugging: Print the song name or video name
        print(f"Clicked on media: {media_name}")

        if media_name in self.media_player.song_manager.song_dict:
            media_path = self.media_player.song_manager.song_dict[media_name]

        # Check if it's an audio file or a video file
            if media_path.lower().endswith(('.mp3', '.wav', '.flac')):  # Audio file
                artist_name, song_duration = self.get_song_details(media_path)
                media_details = f"Artist: {artist_name}\nDuration: {self.format_time(song_duration)}"
            elif media_path.lower().endswith(('.mp4', '.avi', '.mkv')):  # Video file
                video_title, resolution, video_duration = self.get_video_details(media_path)
                media_details = f"Title: {video_title}\nResolution: {resolution}\nDuration: {self.format_time(video_duration)}"

        # Update the details label
            self.details_label.config(text=media_details)

        # Position the label near the mouse cursor
            self.details_label.place(x=event.x + 10, y=event.y + 10)
            self.details_label.lift()  # Bring the label to the front
            
    def get_video_details(self, video_path):
        """ Get video details such as title, resolution, and duration. """
        try:
            video_clip = VideoFileClip(video_path)
            video_title = os.path.basename(video_path)  # Get the video file name
            video_duration = video_clip.duration * 1000  # Duration in milliseconds
            resolution = f"{video_clip.w}x{video_clip.h}"  # Resolution: Width x Height
            return video_title, resolution, video_duration
        except Exception as e:
            print(f"Error getting video details: {e}")
            return "Unknown Title", "Unknown Resolution", 0  # Return default values if there's an error


    def get_song_details(self, song_path):
        """ Get the artist name and song duration from the song's metadata. """
        try:
            audio_file = eyed3.load(song_path)
            artist_name = audio_file.tag.artist if audio_file.tag.artist else "Unknown Artist"
            song_duration = audio_file.info.time_secs * 1000  # Duration in milliseconds
            return artist_name, song_duration
        except Exception as e:
            print(f"Error getting song details: {e}")
            return "Unknown Artist", 0  # Return default values if there's an error
            
    def update_duration_and_position(self):
        if self.media_player.playback_manager.player:
            current_position = self.media_player.playback_manager.get_current_position()
            duration = self.media_player.playback_manager.get_song_duration()

            if duration > 0:  # Ensure duration is valid
                self.seek_bar.config(to=duration)
                self.seek_bar.set(current_position)
                self.duration_label.config(text=f"{self.format_time(current_position)} / {self.format_time(duration)}")
                if current_position >= duration - 1:  # 1 second tolerance
                    self.play_next_song() 
    
    

    # Schedule the next update
        self.media_player.root.after(1, self.update_duration_and_position)  # Every 200ms, adjust as necessary

    def format_time(self, milliseconds):
        seconds = milliseconds // 1000
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02}:{seconds:02}"

    def on_seek(self, position):
        self.is_seeking = True  # Set the flag to indicate we're seeking
        position = int(position)

        if self.media_player.playback_manager.player:
            # Only seek if the position is significantly different
            current_position = self.media_player.playback_manager.get_current_position()
            if abs(current_position - position) > 500:  # Adjust threshold as needed
                self.media_player.playback_manager.player.set_time(position)

    def delete_song(self):
        self.media_player.delete_song()
        
        
    def seek_song(self, position):
        self.is_seeking = False  # Reset the flag after seeking

    def filter_songs(self, event=None):
        search_term = self.search_entry.get().lower()  # Get the current text from the search entry
        self.song_box.delete(0, END)  # Clear the current song list

        for song_name in self.media_player.song_manager.song_dict.keys():
            if search_term in song_name.lower():  # Check if the search term is in the song name
                self.song_box.insert(END, song_name)  # Insert matching song names

    def skip_10_seconds(self):
        """ Skip the current song forward by 10 seconds. """
        self.media_player.skip_10_seconds()

    def back_10_seconds(self):
        """ Rewind the current song by 10 seconds. """
        self.media_player.back_10_seconds()

    def create_buttons(self):
        button_configs = [
            ('play.png', self.media_player.playback_manager.play_song, 800, 955),
            ('pause.png', self.media_player.playback_manager.toggle_pause,640 , 955),
            ('stop.png', self.media_player.playback_manager.stop_song, 960, 955),
            ('next.png', self.media_player.playback_manager.next_song, 1040, 955),
            ('previous.png', self.media_player.playback_manager.previous_song, 560, 955),
            ('repeat .png', self.media_player.repeat_song, 1300, 897),
            ('shuffle.png', self.media_player.shuffle_song, 1240, 897),
            ('skip.jpg', self.media_player.skip_10_seconds, 880, 955),
            ('back.jpg', self.media_player.back_10_seconds, 720, 955)
        ] 

        for img, cmd, x, y in button_configs:
            button_image = ImageTk.PhotoImage(file=img)
            button = Button(self.media_player.root, image=button_image, width=50, height=50, command=cmd)
            button.image = button_image  # Keep a reference to avoid garbage collection
            button.place(x=x, y=y)

    def create_menu(self):
        my_menu = Menu(self.media_player.root)
        self.media_player.root.config(menu=my_menu)

        add_many_song_menu = Menu(my_menu)
        my_menu.add_cascade(label='Add Songs', menu=add_many_song_menu)
        add_many_song_menu.add_command(label="Add one or many Songs", command=self.media_player.add_many_songs)

        playlist_menu = Menu(my_menu)
        my_menu.add_cascade(label='Playlists', menu=playlist_menu)
        playlist_menu.add_command(label="Create New Playlist", command=self.media_player.create_playlist)
        playlist_menu.add_command(label="Manage Playlists", command=self.media_player.manage_playlists)

        my_menu.add_command(label='Manage Recycle Bin', command=self.media_player.manage_recycle_bin)  # New menu item
