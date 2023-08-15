from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from pytube import YouTube, exceptions

import src.config as config


def download_audio(url: str) -> str:
    """Downloads audio track from video

    Downloads audio from video clip only from Youtube to /src/tracks directory.

    Args:
        url (str): url for video (Youtube only)

    Returns:
        Path to downloaded audio track as string
    """
    yt = YouTube(url)
    title = yt.title
    yt = yt.streams.get_audio_only()
    path = f"src/tracks/{title}.mp4"
    try:
        yt.download(output_path="src/tracks/")
    except exceptions.PytubeError("Unable to download a video."):
        path = None
    return path


def cut_audio(path: str) -> str:
    """Cuts audio track.

    Function returns only first minutes of audio file.
    Duration of cropped audio is specified in config file.
    New file name is 'crop_{audio_filename}.mp4'

    Args:
        path (str): path to audio

    Returns:
        Path to cropped audio file
    """
    end_time = config.get_settings().end_of_audio_time
    path_to_cut_file = "src/tracks/" + "crop_" + path.split("/")[-1]
    ffmpeg_extract_subclip(path, 0, end_time, targetname=path_to_cut_file)
    return path_to_cut_file
