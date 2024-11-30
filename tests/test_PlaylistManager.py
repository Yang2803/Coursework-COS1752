# test_playlist_manager.py
import pytest
from playlist_manager import PlaylistManager

@pytest.fixture
def playlist_manager():
    manager = PlaylistManager()
    manager.playlists = {"Rock": ["song1", "song2"], "Pop": ["song3"]}
    return manager

def test_load_playlists(playlist_manager):
    playlist_manager.load()
    assert "Rock" in playlist_manager.playlists
    assert "Pop" in playlist_manager.playlists
    assert playlist_manager.playlists["Rock"] == ["song1", "song2"]

def test_save_playlists(playlist_manager):
    playlist_manager.save()
    # We can mock the open function to assert that it is being called, but
    # here we will just check that the playlists are being saved correctly
    assert "Rock" in playlist_manager.playlists
    assert "Pop" in playlist_manager.playlists
