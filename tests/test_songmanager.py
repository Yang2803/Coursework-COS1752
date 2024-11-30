# test_song_manager.py
import pytest
from song_manager import SongManager

@pytest.fixture
def song_manager():
    manager = SongManager()
    manager.song_dict = {"song1": "path/to/song1.mp3", "song2": "path/to/song2.mp3"}
    return manager

def test_load_songs(song_manager):
    song_manager.load()
    assert "song1" in song_manager.song_dict
    assert song_manager.song_dict["song1"] == "path/to/song1.mp3"

def test_save_songs(song_manager):
    song_manager.save()
    assert "song1" in song_manager.song_dict
    assert song_manager.song_dict["song1"] == "path/to/song1.mp3"

def test_add_song(song_manager):
    song_manager.song_dict["new_song"] = "path/to/new_song.mp3"
    assert "new_song" in song_manager.song_dict

def test_remove_song(song_manager):
    del song_manager.song_dict["song1"]
    assert "song1" not in song_manager.song_dict
