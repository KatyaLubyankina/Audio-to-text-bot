import pytest

from src.audio import audio


@pytest.fixture()
def download_audio(request):
    result = audio.download_audio(request.param)
    return result
