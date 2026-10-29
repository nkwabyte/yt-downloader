# YouTube Downloader CLI

A minimal, self-contained CLI tool for downloading YouTube videos and playlists as highest-quality MP4 files using [`yt-dlp`](https://github.com/yt-dlp/yt-dlp) and [`uv`](https://docs.astral.sh/uv/).

## Project Structure

```text
.
├── downloader.py              # Standalone Python CLI (PEP 723 uv script)
└── scripts/
    ├── download.sh            # Download a video or playlist
    ├── download_video.sh      # Force single-video download (--no-playlist)
    └── download_playlist.sh   # Download a full playlist
```

## Requirements

- [uv](https://docs.astral.sh/uv/) (`brew install uv`)

No manual virtual environment setup or global `ffmpeg` installation is required—`downloader.py` uses inline script metadata to automatically fetch `yt-dlp` and a bundled `ffmpeg` binary (`imageio-ffmpeg`) on the fly.

## Usage

All commands default to saving files in `~/Downloads` if no destination folder is provided.
- **Playlists** are automatically numbered (`01 - Video Title.mp4`, `02 - Video Title.mp4`, ...).
- **Single videos** are saved by title (`Video Title.mp4`).

### Using the Bash Scripts

```bash
# Download a video or playlist to ~/Downloads
./scripts/download.sh "https://www.youtube.com/watch?v=..."

# Download a playlist to a custom directory
./scripts/download_playlist.sh "https://www.youtube.com/playlist?list=..." ~/Downloads/ThinkerCad

# Download ONLY the single video (even if the URL includes &list=...)
./scripts/download_video.sh "https://www.youtube.com/watch?v=...&list=..." ~/Downloads/Videos
```

### Using `downloader.py` Directly

```bash
# Default output directory (~/Downloads)
./downloader.py "https://www.youtube.com/watch?v=..."

# Custom output directory (positional or -o/--output)
./downloader.py "https://www.youtube.com/playlist?list=..." ~/Downloads/ThinkerCad
./downloader.py "https://www.youtube.com/playlist?list=..." -o ~/Downloads/ThinkerCad

# Force single video only
./downloader.py "https://www.youtube.com/watch?v=...&list=..." --no-playlist
```

## Optional: Use from Anywhere on Your CLI

Add the `scripts` folder to your `PATH` in `~/.zshrc`:

```bash
export PATH="$HOME/Dev/YoutubeDownloader/scripts:$PATH"
```

Then reload your shell (`source ~/.zshrc`) and run from any directory:

```bash
download.sh "https://www.youtube.com/watch?v=..."
download_playlist.sh "https://www.youtube.com/playlist?list=..." ~/Downloads/MyFolder
download_video.sh "https://www.youtube.com/watch?v=...&list=..."
```

