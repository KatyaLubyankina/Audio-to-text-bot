import os
import traceback

import pytube
from loguru import logger
from minio import Minio
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

import src.config as config


def download_audio(url: str) -> dict:
    """Downloads audio track from video.

    Downloads audio from video clip only from Youtube to /src/tracks directory.

    Args:
        url (str): url for video (Youtube only)

    Returns:
        Dict with path to file and duration of audio in seconds.
        {"path": path, "duration": duration}
    """
    yt = pytube.YouTube(url)
    title = yt.title
    yt_audio = yt.streams.get_audio_only()
    path = f"src/tracks/{title}.mp4"
    duration = yt.length
    try:
        yt_audio.download(output_path="src/tracks/")
    except Exception:
        logger.debug(traceback.format_exc())
        duration = 0
        path = None
    finally:
        return {"path": path, "duration": duration}


def cut_audio(audio_info: dict) -> dict:
    """Cuts audio track.

    Function returns only first minutes of audio file.
    Duration of cropped audio is specified in config.py file.
    New filename is 'crop_{audio_filename}.mp4'

    Args:
        audio_info (dict): path to audio

    Returns:
        Path to cropped audio file as dict with "path_to_cut_file" key
    """
    path = audio_info["path"]
    duration = audio_info["duration"]
    end_time = config.get_settings().end_of_audio_time
    file_name = "crop_" + path.split("/")[-1]
    path_to_cut_file = "src/tracks/" + file_name
    end_time = min(duration, end_time)
    ffmpeg_extract_subclip(path, 0, end_time, targetname=path_to_cut_file)
    minio_client = Minio(
        endpoint=f"{config.get_settings().minio_host_name}:9000",
        access_key=config.get_settings().access_key_s3,
        secret_key=config.get_settings().secret_key_s3.get_secret_value(),
        secure=False,
    )
    found = minio_client.bucket_exists("audio")
    if not found:
        minio_client.make_bucket("audio")
    minio_client.fput_object("audio", file_name, path_to_cut_file)
    os.remove(path)
    os.remove(path_to_cut_file)
    return {"Bucket name": "audio", "file_name": file_name}
