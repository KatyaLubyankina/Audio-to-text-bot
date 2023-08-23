import os

import pytest

from src.audio import audio


@pytest.mark.parametrize(
    "download_audio", ["https://www.youtube.com/watch?v=xS9M6zQI3AU"], indirect=True
)
def test_download_audio_success(download_audio):
    result = download_audio
    path, duration = result["path"], result["duration"]
    assert path
    assert duration
    os.remove(path)


@pytest.mark.parametrize(
    "download_audio",
    [
        "https://www.youtube.com/watch?v=xS9M6zQI3AU",
        "https://www.youtube.com/watch?v=rWIqUBG7oLM",
    ],
    indirect=True,
)
def test_cut_audio_success(download_audio):
    result_download = download_audio
    result = audio.cut_audio(download_audio)
    assert result["path_to_cut_file"]
    os.remove(result_download["path"])
    os.remove(result["path_to_cut_file"])
