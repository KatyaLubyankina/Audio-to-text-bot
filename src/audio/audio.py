from pytube import YouTube, exceptions


def download_audio(link: str) -> dict:
    yt = YouTube(link)
    title = yt.title
    yt = yt.streams.get_audio_only()
    path = f"src/video/{title}.mp4"
    try:
        yt.download(output_path="src/video/")
    except exceptions.PytubeError("Unable to download a video."):
        path = None
    return {"path": path}
