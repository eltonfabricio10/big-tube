# -*- coding: utf-8 -*-
from i18n import _
import yt_dlp
import os


def download_video(url, output_dir, media_format):
    ydl_opts = {
        'format': media_format,
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'postprocessors': [],
    }

    if media_format in ["mp3", "aac", "ogg", "wav", "flac"]:
        # Extrair áudio
        ydl_opts['postprocessors'].append({
            'key': 'FFmpegExtractAudio',
            'preferredcodec': media_format,
            'preferredquality': '192',
        })

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
            print(f"Downloaded successfully: {url}")
        except Exception as e:
            print(f"Error downloading {url}: {e}")


def download_subtitles(url, language="en", output_dir="."):
    ydl_opts = {
        'writesubtitles': True,
        'subtitleslangs': [language],
        'skip_download': True,
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
