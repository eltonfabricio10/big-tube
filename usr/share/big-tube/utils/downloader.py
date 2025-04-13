# -*- coding: utf-8 -*-
import yt_dlp
import os


def download_video(url, output_dir, format="mp4"):
    ydl_opts = {
        'format': f'bestvideo+bestaudio/best',
        'outtmpl': os.path.join(output_dir, f'%(title)s.{format}'),
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return os.path.join(output_dir, f"{info['title']}.{format}")


def download_subtitles(url, language="en", output_dir="."):
    ydl_opts = {
        'writesubtitles': True,
        'subtitleslangs': [language],
        'skip_download': True,
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
