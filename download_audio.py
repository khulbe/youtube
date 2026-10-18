import os
import sys
import subprocess
import yt_dlp

def download_and_convert(video_url):
    try:
        print("Extracting video information...")
        # Extract metadata to gather the safe filename and source audio bitrate
        with yt_dlp.YoutubeDL({'noplaylist': True, 'quiet': True}) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            video_title = ydl.prepare_filename(info_dict).rsplit('.', 1)[0]
            
            # Fetch source average audio bitrate (abr)
            source_abr = info_dict.get('abr')
            if source_abr:
                bitrate_str = f"{int(source_abr)}k"
                print(f"Detected source audio bitrate: {bitrate_str}")
            else:
                bitrate_str = "320k"
                print(f"Audio bitrate not found in metadata. Defaulting to: {bitrate_str}")

        output_mp3 = f"{video_title}.mp3"

        # Download configuration
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f"{video_title}.%(ext)s",
            'overwrites': True,
            'noplaylist': True,
            'quiet': False
        }

        print("Downloading audio stream...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            downloaded_file = ydl.prepare_filename(info)
        
        print(f"Download complete! Saved temporary file as '{downloaded_file}'.")

        # Convert to MP3 using the dynamic bitrate via FFmpeg
        print(f"Converting to '{output_mp3}' via FFmpeg at {bitrate_str}...")
        ffmpeg_command = ["ffmpeg", "-y", "-i", downloaded_file, "-vn", "-ab", bitrate_str, output_mp3]
        subprocess.run(ffmpeg_command, check=True)
        print("Conversion successful!")

        # Clean up the original downloaded file (webm/m4a/etc.)
        if os.path.exists(downloaded_file) and downloaded_file != output_mp3:
            os.remove(downloaded_file)
            print(f"Cleaned up temporary file: '{downloaded_file}'")

    except subprocess.CalledProcessError as e:
        print(f"FFmpeg conversion failed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: Missing YouTube URL.")
        print("Usage: python download_audio.py <YOUTUBE_URL>")
        sys.exit(1)
        
    url = sys.argv[1]
    download_and_convert(url)
