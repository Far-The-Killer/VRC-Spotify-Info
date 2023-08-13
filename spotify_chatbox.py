'''
Script for putting current Spotify track info into VRC Chatbox
'''

from time import sleep
from random import Random
from pythonosc import udp_client
from spotify_listener import SpotifyConnection, TrackInfo

DEBUG_ON = False
PRINT_OUTPUT = True

def format_time(time_ms, seperator=':'):
    '''
    Take time in milliseconds and convert to minutes:seconds
    '''
    second, _ = divmod(time_ms, 1000)
    minute, second = divmod(second, 60)
    return f"{int(minute):02d}{seperator}{int(second):02d}"

def format_track_vrc(song_data_obj:TrackInfo) -> str:
    '''
    Format the current track data so it fits within
    VRChat's 144 max char limit for messages
    '''
    max_chr_count = 144
    max_chr_per_line = int(max_chr_count / 3)
    artists = song_data_obj.artists
    # Format the artist info
    a_str = "Artists: "
    a_split_str = " \\ "
    for artist in artists:
        a_str += artist + a_split_str
    a_str = a_str[:-len(a_split_str)]
    if len(a_str) > max_chr_per_line:
        a_str = a_str[:max_chr_per_line - 2] + ' '
    else:
        a_str += ' ' * (max_chr_per_line - len(a_str)) # fill in with spaces

    # Format the song name
    track_name_str = "Song: " + song_data_obj.track_name
    if len(track_name_str) < max_chr_per_line:
        track_name_str += ' ' * (max_chr_per_line - len(track_name_str))
    elif len(track_name_str) > max_chr_per_line:
        track_name_str = track_name_str[:max_chr_per_line - 2] + ' '

    # Format the playback info
    time_info_str = ""
    if song_data_obj.is_playing:
        time_info_str += "▶"
    else:
        time_info_str += "⏸︎"
    time_info_str += f"  {format_time(song_data_obj.current_pos_ms)}/{format_time(song_data_obj.track_dur_ms)}"
    if len(time_info_str) < max_chr_per_line:
        time_info_str += ' ' * (max_chr_per_line - len(time_info_str))
    elif len(time_info_str) > max_chr_per_line:
        time_info_str = time_info_str[:max_chr_per_line - 2] + ' '

    if DEBUG_ON:
        output = a_str + track_name_str + time_info_str
        print("----DEBUG----")
        print("string length: " + str(len(output)))
        print(a_str)
        print(track_name_str)
        print(time_info_str)
        print("----DEBUG----\n")

    return a_str + track_name_str + time_info_str    
if __name__ == "__main__":
    rng = Random()
    spotify = SpotifyConnection()
    client = udp_client.SimpleUDPClient("127.0.0.1", 9000)
    while True:
        spotify.update()
        track_info = spotify.get_current_track()
        track_string = format_track_vrc(track_info)
        if PRINT_OUTPUT:
            print(track_string)
        client.send_message("/chatbox/input",[track_string, True, False])
        if DEBUG_ON:
            sleep(5.0)
        else:
            sleep(rng.randint(5, 30)) # try to trick VRC into not detecting this as spam
