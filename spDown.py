import requests
import json
import time
import os
import yt_dlp
import subprocess
import zipfile
import sys

spotifyClientId = ""
SpotifyClientSecret = ""

ascii_art = [
"      _____       ____                    ",
"     / ___/____  / __ \\____ _      ______ ",
"     \\__ \\/ __ \\/ / / / __ \\ | /| / / __ \\",
"    ___/ / /_/ / /_/ / /_/ / |/ |/ / / / /",
"   /____/ .___/_____/\\____/|__/|__/_/ /_/  by _DaNine_",
"       /_/                                 ",
]

start_color = (100, 255, 100)
end_color   = (100, 100, 255)

#USER VARIABLES

#path to ffmpeg binary
FFMPEG_DIR = r"C:\ffmpeg\ffmpeg-8.1-essentials_build\bin"
FFMPEG_EXE = r"C:\ffmpeg\ffmpeg-8.1-essentials_build\bin\ffmpeg.exe"
ZIP_PATH = r"C:\ffmpeg\ffmpeg.zip"

ffmpeg_path = FFMPEG_EXE

def find_ffmpeg():
    if os.path.exists(FFMPEG_EXE):
        print("FFmpeg found")
    else:
        print("FFmpeg NOT found")
        install_ffmpeg()



def install_ffmpeg():
    print("Installing FFmpeg to C:\\ffmpeg\\bin ...")

    url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"

    # make folders
    os.makedirs(FFMPEG_DIR, exist_ok=True)

    r = requests.get(url, stream=True)
    total_size = int(r.headers.get('content-length', 0))
    downloaded = 0
    start_time = time.time()

    with open(ZIP_PATH, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)

                # progress %
                percent = (downloaded / total_size * 100) if total_size else 0

                # progress bar
                bar_length = 30
                filled = int(bar_length * downloaded // total_size) if total_size else 0
                bar = "█" * filled + "-" * (bar_length - filled)

                # speed (KB/s)
                elapsed = time.time() - start_time
                speed = (downloaded / 1024 / elapsed) if elapsed > 0 else 0

                # print in one line
                sys.stdout.write(f"\r[{bar}] {percent:.1f}% ({speed:.1f} KB/s)")
                sys.stdout.flush()

    print("\nDownload complete!")

    print("Extracting...")

    with zipfile.ZipFile(ZIP_PATH, "r") as zip_ref:
        zip_ref.extractall(r"C:\ffmpeg")

    print("Done!")



find_ffmpeg()


def getToken():
    
    global token
    print("Refreshing Token...")
    print()
    url = "https://accounts.spotify.com/api/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": spotifyClientId,
        "client_secret": SpotifyClientSecret
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post(url, headers=headers, data=data)  
    if response.status_code == 200:
        data = response.json()
        token = response.json()["access_token"]


    else:
        print("HTTP error:", response.status_code)
        print(response.text) 

        print()
        promptSpData()


def promptSpData():
    global spotifyClientId, SpotifyClientSecret
    
    print("\033[91mSpotify API authentication required.\033[0m")
    print("\033[91mHead to\033[0m https://developer.spotify.com/dashboard \033[91m to get a client ID and secret \033[0m")
    print()

    client_id = input("Client Id >>> ")
    client_secret = input("Client Secret >>> ")
    spotifyClientId = client_id
    SpotifyClientSecret = client_secret



    lines = [client_id, client_secret]
    with open("spauth.txt", "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")

    getToken()



if os.path.exists("spauth.txt"):
    
    #spotify client info
    with open("spauth.txt", "r", encoding="utf-8") as f:

        spotifyClientId = f.readline().strip() 
        SpotifyClientSecret = f.readline().strip() 

        if(spotifyClientId == "" or SpotifyClientSecret == ""):
            promptSpData() 

else:
    promptSpData()

#path to the folder where the songs will be stored, where the path specified in the cli will be the subfolder (leave empty for no subfolder)
rootDlPath = music_path = os.path.join(os.path.expanduser("~"), "Music") #MUSIC FOLDER, change this if you want to output to a different folder

#FILL THESE IN ^^^^^^



token = ""
path = ""

def loop():
    global path

    print()
    print()
    print()
    print()
    print()

    ascii()
    print()
    print("\033[38;2;100;100;255mInsert:\n     - A Spotify track or playlist\n     - A YouTube link\n     - A Song name\033[0m")
    print()

    url = input(f"\033[38;2;100;100;255mInsert Url / Song Name >>> \033[0m")
    print()
    print("Tip: Path specifies the subfolder on which the output will be stored, leave empty to store in the root download folder")
    path = input(f"\033[38;2;100;100;255mInsert Path >>> \033[0m")

    print()
    
    if "youtube" in url:
        downloadYtUrl(url)
    elif "spotify" in url:
        getSpData(url)
    else:
        querySp(url)

    
        

    loop()

def interpolate(start, end, t):
    return int(start + (end - start) * t)

def ascii():
    for i, line in enumerate(ascii_art):
        t = i / (len(ascii_art) - 1)
        r = interpolate(start_color[0], end_color[0], t)
        g = interpolate(start_color[1], end_color[1], t)
        b = interpolate(start_color[2], end_color[2], t)

        color = f"\033[38;2;{r};{g};{b}m"
        print(color + line)

def getToken():
    
    global token
    print("Refreshing Token...")
    print()
    url = "https://accounts.spotify.com/api/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": spotifyClientId,
        "client_secret": SpotifyClientSecret
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post(url, headers=headers, data=data)  
    if response.status_code == 200:
        data = response.json()
        token = response.json()["access_token"]


    else:
        print("HTTP error:", response.status_code)
        print(response.text) 

        print()
        promptSpData()


def querySp(query):

    global token

    url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "q": query,
        "type": "track",
        "limit": 1
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    song = data["tracks"]["items"][0]


    songLink = song["external_urls"]["spotify"]
    authors = [artist["name"] for artist in song["artists"]]
    authorsClean = ", ".join(authors)
    album = song["album"]["name"]
    name = song["name"]

    print(f"Found Song: {name} : {authorsClean} ({album})")
    query2 = f"{name} - {authorsClean} - topic"

    downloadYt(query2, name, authorsClean, album, True)


    





def downloadYtUrl(url):
    print("\033[31mYouTube Download...\033[0m\n")

    global path

    if "&list" in url:
        url_clean = url.split("&list")[0]
    else:
        url_clean = url

    ydl_opts = {
        "ffmpeg_location": ffmpeg_path,
        "format": "bestaudio/best",
        "outtmpl": fr"{rootDlPath}\{path}\%(title)s.%(ext)s",
        "quiet": True,
        "no_warnings": True,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "320",
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url_clean, download=True)
        songFp = ydl.prepare_filename(info)

    # convert to mp3
    songFp = os.path.splitext(songFp)[0] + ".mp3"

    print(f"Downloaded: {info.get('title')}")

    subprocess.run(['explorer', '/select,', songFp])

def downloadYt(query, song,artist, album, showOnEnd):

    print("\033[31mYouTube Download...\033[0m")
    print()
    
    global path

    # Options for yt_dlp
    ydl_opts = {
        "ffmpeg_location": ffmpeg_path,
        "format": "bestaudio/best",
        "outtmpl": fr"C:\Users\danon\Music\{path}\%(title)s.%(ext)s",
        "quiet": True,
        "no_warnings": True,
        "noplaylist":True,

        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "320",
        }],

        "postprocessor_args": [
            "-metadata", f"title={song}",
            "-metadata", f"artist={artist}",
            "-metadata", f"album={album}",
        ],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # Search YouTube for the query and take the first result
        info = ydl.extract_info(f"ytsearch1:{query}", download=True)
        video = info["entries"][0]
        print(f"Downloaded: {video['title']}")
        print(f"URL: {video['webpage_url']}")

    if (showOnEnd == True):
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch1:{query}", download=True)
            video = info["entries"][0]

            songFp = ydl.prepare_filename(video)

        songFp = os.path.splitext(songFp)[0] + ".mp3"

        subprocess.run(['explorer', '/select,', songFp])



def getSpData(url):

    global token

    #determine if the spotify link is of a song or a playlist
    if "playlist" in url:
        print("Spotify playlist detected")
        plst = url.split("/playlist/")[1]
        playlist_id = plst.split("?")[0]

        playListApi = f"https://api.spotify.com/v1/playlists/{playlist_id}/items"
        headers = {"Authorization": f"Bearer {token}"}

        songs = []
        url_api = playListApi

        while url_api:
            print("getting data")
            response = requests.get(url_api, headers=headers)
            data = response.json()

            for item in data["items"]:
                track = item["track"]
                if track:  # make sure track exists
                    display_str = f'{track["name"]} - {", ".join(a["name"] for a in track["artists"])}'
                    album_name = track["album"]["name"]

                    songs.append({
                        "artist": ", ".join(a["name"] for a in track["artists"]),
                        "name": track["name"],
                        "album": album_name
                    })

            url_api = data["next"]  # next page of playlist

        areYouSure = input(f"Are you sure you want to download {len(songs)} songs (Y / N) >> ")
        
        if areYouSure.lower() == "y":
            print("This might take a while")

            total = len(songs)

            for i, song in enumerate(songs, start=1):
                # extract variables
                name = song['name']
                artist = song['artist']
                album = song['album']

                # display progress
                display_str = f"{i}/{total} {name} - {artist} [{album}]"
                print(display_str)  # \033[K clears the line

                # build query
                query = f"{name} - {artist} - topic"

                downloadYt(query, name, artist, album, False)

        else:
            loop()

    elif "track" in url:
        print("songs detected")
        getSongInfo(url)

def getSongInfo(url):

    print("\033[32mSpotify Search...\033[0m")
    print()
    
    
    global token



    track_part = url.split("/track/")[1]  # everything after "/track/"
    track_id = track_part.split("?")[0]   # remove any query string
    api_url = f"https://api.spotify.com/v1/tracks/{track_id}"


    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(api_url, headers=headers)
    data = response.json()

    if response.status_code == 200:
        data = response.json()
        if "error" in data:
            print("Spotify API error:", data["error"]["message"])
        else:
            song = data["name"]
            album = data["album"]["name"]
            artist = ", ".join([a["name"] for a in data["artists"]])

            print("Found Song:")
            print(">>   Song:", song)
            print(">>   Album:", album)
            print(">>   Artist:", artist)
            print()

            title = f"{song} - {artist} - topic"


            downloadYt(title, song, artist, album, True)
    else:
        print("\033[31mThe token has expired, refreshing token...\033[0m")
        getSongInfo()


            


getToken()
loop()

