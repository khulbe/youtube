import os
import subprocess
import yt_dlp
import sys
# 1. Configuration
# video_url = "https://www.youtube.com/watch?v=E4ZJxhyAaH8&list=RDE4ZJxhyAaH8&start_radio=1"

if len(sys.argv) < 2:
    print("Error: Missing YouTube URL.")
    print("Usage: python download_youtube.py <YOUTUBE_URL>")
    sys.exit(1)

video_url = sys.argv[1]

try:
    # 2. Extract video info to get the proper clean title
    print("Extracting video information...")
    # 'noplaylist': True ensures it only reads the single video even if it's a playlist URL
    with yt_dlp.YoutubeDL({'noplaylist': True}) as ydl:
        info_dict = ydl.extract_info(video_url, download=False)
        # Gets the safe version of the video title without any extension
        video_title = ydl.prepare_filename(info_dict).rsplit('.', 1)[0]

    output_mp3 = f"{video_title}.mp3"

    # 3. Setup download options 
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f"{video_title}.%(ext)s", # Dynamically grabs the true extension
        'overwrites': True,
        'noplaylist': True,                 # Forces yt-dlp to download only the single video
    }

    # 4. Download the file
    print("Downloading single video audio...")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=True)
        # Dynamically capture the exact filename that was saved on disk
        downloaded_file = ydl.prepare_filename(info)
    
    print(f"Download complete! Saved as '{downloaded_file}'.")

    # 5. Run your exact FFmpeg command with the captured input file and dynamic output name
    print(f"Converting to '{output_mp3}' via FFmpeg...")
    ffmpeg_command = ["ffmpeg", "-i", downloaded_file, "-vn", "-ab", "320k", output_mp3]
    subprocess.run(ffmpeg_command, check=True)
    print("Conversion successful!")

    # 6. Delete the dynamically captured temporary file
    if os.path.exists(downloaded_file):
        os.remove(downloaded_file)
        print(f"Cleaned up temporary file: '{downloaded_file}'")

except subprocess.CalledProcessError as e:
    print(f"FFmpeg conversion failed: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
