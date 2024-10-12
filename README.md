# Alchemy Audio Converter

Batch converts audio files into a format optimized for Alchemy RPG.

## Features

- Converts audio files to the specified format (default: `ogg`).
- Optionally applies fade-in and fade-out effects to the audio files.
- Normalizes the audio volume using `ffmpeg`.
- Renames output files to the title extracted from the metadata using `ffprobe`.

## Requirements

- Python 3.x
- `ffmpeg` and `ffprobe` installed and available in the system PATH.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/alchemy-audio-converter.git
    cd alchemy-audio-converter
    ```

2. Ensure `ffmpeg` and `ffprobe` are installed. You can download them from [FFmpeg's official website](https://ffmpeg.org/download.html).

## Usage

1. Copy audio files into the `/raw` folder.

2. Run the following command to convert the files to OGG format and apply fade-in/out effects for 5 seconds:
    ```bash
    python converter.py raw processed --output_format ogg --fade_duration 5
    ```

3. Check the `/processed` folder for the converted OGG files.

## Command-Line Arguments

- `input_folder`: Path to the input folder containing raw audio files.
- `output_folder`: Path to the output folder for processed audio files.
- `--output_format`: Output audio format (default: `ogg`).
- `--fade_duration`: Duration of fade-in and fade-out in seconds (default: `0`).
- `--sample_rate`: Sample rate for the output audio files (default: `128k`).

## Example

To convert audio files in the `raw` folder to OGG format with a 10-second fade-in and fade-out, run:
```bash
python converter.py raw processed --output_format ogg --fade_duration 10 --sample_rate 192k
