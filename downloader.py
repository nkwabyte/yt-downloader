#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "yt-dlp",
#     "imageio-ffmpeg",
# ]
# ///
"""Minimal standalone CLI to download a YouTube video or playlist."""

import argparse
from pathlib import Path
import shutil
import sys
import tempfile
import imageio_ffmpeg
import yt_dlp


DEFAULT_OUT_DIR = Path.home() / "Downloads"


def get_working_ffmpeg() -> str:
    """Return a path to a working ffmpeg executable for yt-dlp."""
    ffmpeg_exe = Path(imageio_ffmpeg.get_ffmpeg_exe())
    bin_dir = Path(tempfile.gettempdir()) / "yt-dlp-ffmpeg"
    bin_dir.mkdir(parents=True, exist_ok=True)
    target = bin_dir / "ffmpeg"
    if not target.exists():
        try:
            target.symlink_to(ffmpeg_exe)
        except OSError:
            shutil.copy2(ffmpeg_exe, target)
    return str(target)


def download(url: str, output_dir: Path, no_playlist: bool = False) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    ffmpeg_path = get_working_ffmpeg()

    ydl_opts = {
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "merge_output_format": "mp4",
        "ffmpeg_location": ffmpeg_path,
        "outtmpl": str(output_dir / "%(playlist_index&{:02d} - |)s%(title)s.%(ext)s"),
        "noplaylist": no_playlist,
        "ignoreerrors": True,
        "continuedl": True,
    }

    mode = "video" if no_playlist else "video/playlist"
    print(f"Downloading {mode} to: {output_dir}")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download([url])
        if error_code != 0:
            sys.exit(error_code)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download a YouTube video or playlist (defaults to ~/Downloads)."
    )
    parser.add_argument(
        "url",
        help="YouTube video or playlist URL",
    )
    parser.add_argument(
        "location",
        nargs="?",
        default=None,
        help="Download directory (default: ~/Downloads)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Download directory (alternative flag to positional location)",
    )
    parser.add_argument(
        "--no-playlist",
        action="store_true",
        help="Download only the single video even if the URL contains a playlist",
    )
    args = parser.parse_args()

    out_path = args.output or (Path(args.location) if args.location else DEFAULT_OUT_DIR)
    download(args.url, out_path.expanduser().resolve(), no_playlist=args.no_playlist)


if __name__ == "__main__":
    main()
