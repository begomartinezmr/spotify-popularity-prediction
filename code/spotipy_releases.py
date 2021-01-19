import socket
import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials

sp_client_id = 'YOUR_CLIENT_ID'
sp_client_secret = 'YOUR_CLIENT_SECRET'

client_auth = SpotifyClientCredentials(client_id = sp_client_id, client_secret=sp_client_secret)

sp = spotipy.Spotify(auth_manager=client_auth)

def process_album(album):
    print("--------- NEW %s RELEASED ---------" % (album['album_type'].upper()))
    print("- Name: %s\n- Year: %s\n- Tracks: " % (album['name'], album['release_date'].split('-')[0]))
    album_data = pd.DataFrame(columns=['name', 'year', 'acousticness', 'energy', 'loudness'])
    for track in sp.album_tracks(album['uri'])['items']:
        print("--- %s" % (track['name']))
        audio_features = sp.audio_features([track['uri']])[0]
        album_data = album_data.append({'name'          : track['name'].replace(',',' '),
                                        'year'          : album['release_date'].split('-')[0],
                                        'acousticness'  : audio_features['acousticness'],
                                        'energy'        : audio_features['energy'],
                                        'loudness'      : audio_features['loudness']    }, ignore_index=True)

    album_data.dropna(axis=0)
    csv_data = album_data.to_csv(sep=',', header=False, index=False)

    print("------------------------------------------\n")

    return csv_data.encode('ascii', errors="ignore")

# Connection establishment
TCP_IP = "localhost"
TCP_PORT = 9009
conn = None
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
print("Waiting for TCP connection...")
conn, addr = s.accept()
print("Connection established. Starting to receive new releases...")

release_offset = 99
last_id = ""
waiting = False

while True:
    new_album = sp.new_releases(country='ES', limit=1, offset=release_offset)['albums']['items'][0]

    if last_id != new_album['id']:
        waiting = False
        albumCSV = process_album(new_album)
        conn.send(albumCSV)
        last_id = new_album['id']
        if release_offset > 0:
            release_offset -= 1
    elif not waiting:
        print("------- WAITING FOR NEW RELEASE -------\n")
        waiting = True
