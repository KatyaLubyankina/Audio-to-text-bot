from typing import BinaryIO

from faster_whisper import WhisperModel


def transcribe_text(audio_bytes: BinaryIO, output_file: str):
    """Converts audio input into text via Whisper.

    Args:
        audio_bytes (BinaryIO): bytes from audio file.
        output_file (str): where text will be stored.
    """
    MODEL_SIZE = "large-v2"
    model = WhisperModel(
        MODEL_SIZE,
        device="cuda",
        compute_type="int8_float16",
        local_files_only=True,
        download_root="src/whisper/whisper_models",
    )
    predict_generator = model.transcribe(audio_bytes, without_timestamps=True)[0]

    transcribed_text = "".join([segment.text for segment in predict_generator])
    with open(output_file, "w") as output:
        output.write(transcribed_text)
