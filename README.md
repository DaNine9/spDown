# SpDown
CLI for downloading Spotify <b>songs</b> and <b>playlists</b> in seconds through YouTube using Spotify API and yt_dlp library. <b>Perfect for DJs!</b>

It allows you to input a Spotify or YouTube URL or Song Name, and itll find the best yt video match to download automatically to your music folder.

<img width="886" height="300" alt="Captura de pantalla 2026-03-17 133148" src="https://github.com/user-attachments/assets/986f437d-c539-4498-b6ad-5a647f4818e1" />

To download spotify songs, it fetches their data from the Spotify api and then querys YouTube with yt_dlp. 


# Requirements
Python libraries:
  - requests
  - yt_dlp

Programs:
  - ffmpeg ( https://www.ffmpeg.org/download.html )

# Usage
To use spDown, you need to go in the code and specify:
  - ffmpeg location
  - Spotify API ClientId and ClientSecret, for which you need to create a Spotify Developer account and then an APP - ( https://developer.spotify.com/documentation/web-api/concepts/apps )

  - (OPTIONAL) change the root download folder, in default setting, its the Music folder. When the CLI prompts for path, its the subfolder inside the specified download folder. Leave empty for downloading to root download folder
