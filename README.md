# spDown
CLI for downloading spotify songs through youtube using spotify API. 
it also allows you to download from youtube directly.

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
