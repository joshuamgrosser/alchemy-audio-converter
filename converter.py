import os
import re
import subprocess

# List of common audio file extensions
COMMON_AUDIO_EXTENSIONS = ['.ogg', '.mp3', '.wav', '.flac', '.aac', '.m4a']

def alchemy_audio_converter(input_folder, output_folder, output_format='ogg', fade_duration=0):
    for filename in sorted(os.listdir(input_folder)):
        name, extension = os.path.splitext(filename)
        if extension.lower() not in COMMON_AUDIO_EXTENSIONS:
            continue

        input_path = os.path.join(input_folder, filename)

        try:
            # extract metadata from the file
            probe_results = run_ffprobe(input_path)

            # determine the title of the file from the file metadata
            title = parse_title(name, probe_results)

            # determine the duration of the audio file
            duration = float(probe_results.stdout.decode('utf-8').strip().split('\n')[0])

            # determine the output path for the converted file
            output_path = os.path.join(output_folder, f"{title}.{output_format}")

            # convert the audio file
            run_ffmpeg(input_path, output_path, fade_duration, duration)
        except subprocess.CalledProcessError as ex:
            print(f"Error extracting metadata from file {input_path}: {ex}")
            continue

def parse_title(filename, result):
    try:
        output_lines = result.stderr.decode('utf-8').strip().split('\n')
        output_lines = [line.strip() for line in output_lines if line.strip()]
        title = None
        for line in output_lines:
            if re.search(r'title\s*:', line, re.IGNORECASE):
                pattern = r"title\s*:\s*(.+)"
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    title = match.group(1)
                    return title
                break

        if title is None:
            title = filename
        return title
    except subprocess.CalledProcessError as e:
        print(f"Error extracting title from file {filename}: {e}")


def run_ffprobe(input_path):
    result = subprocess.run([
        'ffprobe',
        '-v',
        'info',
        '-show_entries',
        'format=duration,format_tags=title',
        '-of',
        'default=noprint_wrappers=1:nokey=1',
        input_path
    ], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    return result

def run_ffmpeg(input_path, output_path, fade_duration=0, audio_length=0.0):
    try:
        # Prepare ffmpeg command
        args = ['ffmpeg', '-i', input_path]

        # Add normalization filter
        filters = ['loudnorm']

        # Add fade-in and fade-out filters if specified
        if fade_duration > 0 and audio_length > 0:
            fade_in = f'afade=t=in:ss=0:d={fade_duration}'
            fade_out = f'afade=t=out:st={audio_length-fade_duration}:d={fade_duration}'
            filters.append(fade_in)
            filters.append(fade_out)

        # Combine filters
        if filters:
            args.extend(['-af', ','.join(filters)])

        # Add output path
        args.append(output_path)

        # Run ffmpeg command
        subprocess.run(args, check=True)
        print(f"Converted '{input_path}' to '{output_path}'")
    except subprocess.CalledProcessError as e:
        print(f"Error converting file {input_path}: {e}")

# Example usage
alchemy_audio_converter('raw', 'processed', 'ogg', 5)
