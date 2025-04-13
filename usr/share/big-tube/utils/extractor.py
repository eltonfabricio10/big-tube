# -*- coding: utf-8 -*-
from i18n import _
import subprocess
import os


def extract_audio(video_path, output_format="mp3"):
    output_path = os.path.splitext(video_path)[0] + f".{output_format}"
    command = [
        "ffmpeg",
        "-i", video_path,
        "-q:a", "0",
        "-map", "a",
        output_path
    ]
    subprocess.run(command)
    return output_path
