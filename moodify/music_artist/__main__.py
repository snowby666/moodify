import sys
from music_artist import MusicArtist

def main():
    try:
        artist_name = sys.argv[1]
        artist = MusicArtist(artist_name)
        print(f"***Showing Results for {artist.name}***")
        print("***Genres:***")
        print(artist.genres())
        print("***Albums:***")
        print(artist.albums())
        print("***Singles:***")
        print(artist.singles())
        print("***Top Hits:***")
        print(artist.tophits())
        print("***Similar Artists:***")
        print(artist.similar())
    except IndexError:
        print("The name of an artist is a required parameter.")