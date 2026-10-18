# YouTube Audio Downloader & Dynamic MP3 Converter

A production-ready Python utility that extracts audio streams directly from YouTube links, determines the source bitrate automatically, and transcodes them into standard MP3 files using FFmpeg.

## Features

- **Dynamic Bitrate Extraction**: Inspects the stream metadata (`abr`) so the transcode matches the original source quality.
- **Auto Cleanup**: Discards the intermediate download container (`.webm`, `.m4a`) seamlessly after transcoding completes.
- **Safe Naming**: Utilizes `yt-dlp` routines to guarantee file names are valid across multiple operational environments.

## Prerequisites

Ensure you have **FFmpeg** installed and added to your system's `PATH`.

- **Windows**: Install via `winget install Gyan.FFmpeg` or download from [Gyan.dev](https://www.gyan.dev/ffmpeg/builds/).
- **macOS**: Install via `brew install ffmpeg`.
- **Linux**: Install via `sudo apt install ffmpeg`.

## Installation

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Provide the targeted YouTube link as a command-line argument:
```bash
python download_audio.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```
