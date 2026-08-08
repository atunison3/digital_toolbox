import shutil
import subprocess
from pathlib import Path
from typing import TypeAlias

TimeValue: TypeAlias = int | float | str


def _get_video_duration(input_path: Path) -> float | None:
    """Return the video duration in seconds, if ffprobe can determine it."""
    if shutil.which("ffprobe") is None:
        return None

    command = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        str(input_path),
    ]

    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError:
        return None

    duration_text = result.stdout.strip()
    if not duration_text:
        return None

    try:
        return float(duration_text)
    except ValueError:
        return None


def _is_valid_output(path: Path) -> bool:
    """Return whether the output file looks like a real MP4 with at least one stream."""
    if not path.exists() or path.stat().st_size < 1024:
        return False

    if shutil.which("ffprobe") is None:
        return True

    command = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "stream=index",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        str(path),
    ]

    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError:
        return False

    return bool(result.stdout.strip())


def trim_mp4(
    input_path: Path,
    start_time: TimeValue,
    stop_time: TimeValue,
    output_path: Path,
) -> Path:
    """Trim an MP4 into a QuickTime-friendly MP4 file."""
    input_path = Path(input_path).expanduser().resolve()
    output_path = Path(output_path).expanduser().resolve()

    if not input_path.is_file():
        raise FileNotFoundError(f"Input video does not exist: {input_path}")

    if input_path.suffix.lower() != ".mp4":
        raise ValueError(f"Input file must be an MP4: {input_path}")

    if output_path.suffix.lower() != ".mp4":
        raise ValueError("Output path must have an .mp4 extension.")

    if input_path == output_path:
        raise ValueError("Input and output paths must be different.")

    if shutil.which("ffmpeg") is None:
        raise RuntimeError("FFmpeg is not installed or not available on PATH.")

    start_seconds = _time_to_seconds(start_time)
    stop_seconds = _time_to_seconds(stop_time)

    if start_seconds < 0:
        raise ValueError("Start time cannot be negative.")

    if stop_seconds <= start_seconds:
        raise ValueError("Stop time must be greater than start time.")

    source_duration = _get_video_duration(input_path)
    if source_duration is not None:
        if start_seconds >= source_duration:
            raise ValueError(
                f"Start time {start_time!r} ({start_seconds:.3f}s) exceeds the source video duration "
                f"({source_duration:.3f}s)."
            )
        stop_seconds = min(stop_seconds, source_duration)

    duration = stop_seconds - start_seconds
    output_path.parent.mkdir(parents=True, exist_ok=True)

    command = [
        "ffmpeg",
        "-y",
        "-hide_banner",
        "-loglevel",
        "error",
        "-i",
        str(input_path),
        "-ss",
        str(start_seconds),
        "-t",
        str(duration),
        "-map",
        "0:v:0",
        "-map",
        "0:a?",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-profile:v",
        "high",
        "-level",
        "4.0",
        "-preset",
        "slow",
        "-crf",
        "20",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-ac",
        "2",
        "-tag:v",
        "avc1",
        "-movflags",
        "+faststart",
        "-f",
        "mp4",
        str(output_path),
    ]

    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as error:
        if output_path.exists():
            output_path.unlink()
        message = error.stderr.strip() or "Unknown FFmpeg error"
        raise RuntimeError(f"Failed to trim video:\n{message}") from error

    if not _is_valid_output(output_path):
        if output_path.exists():
            output_path.unlink()
        raise RuntimeError(
            "FFmpeg produced an invalid or empty output file. Check your start/stop times and the source duration."
        )

    return output_path


def _time_to_seconds(value: TimeValue) -> float:
    """Convert seconds, MM:SS, or HH:MM:SS to seconds."""
    if isinstance(value, (int, float)):
        return float(value)

    parts = value.strip().split(":")

    try:
        if len(parts) == 1:
            return float(parts[0])

        if len(parts) == 2:
            minutes, seconds = map(float, parts)
            return minutes * 60 + seconds

        if len(parts) == 3:
            hours, minutes, seconds = map(float, parts)
            return hours * 3600 + minutes * 60 + seconds
    except ValueError as error:
        raise ValueError(f"Invalid time value: {value!r}") from error

    raise ValueError(f"Invalid time format: {value!r}")
