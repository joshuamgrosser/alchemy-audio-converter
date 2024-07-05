import os
import re
import subprocess


def convert(input_folder, output_folder):
    for filename in sorted(os.listdir(input_folder)):
        name, extension = os.path.splitext(filename)
        if not extension.lower() in ['.mp3', '.wav']:
            continue

        try:
            path = os.path.join(input_folder, filename)
            result = subprocess.run([
                'ffprobe',
                '-v',
                'info',
                '-show_entries',
                'format_tags=title',
                '-of',
                'default=noprint_wrappers=1:nokey=1',
                path
            ], stderr=subprocess.PIPE, stdout=subprocess.PIPE)

            output_lines = result.stderr.decode('utf-8').strip().split('\n')
            output_lines = [line.strip() for line in output_lines if line.strip()]
            title = None
            for line in output_lines:
                if 'title' in line:
                    pattern = r"title\s*:\s*(.+)"
                    match = re.search(pattern, line)
                    if match:
                        title = match.group(1)
                        print(title)
                    break

            if title is None:
                print(f"No title found for {filename}")
                title = name
        except subprocess.CalledProcessError as e:
            print(f"Error extracting title from file {path}: {e}")
            title = None

        try:
            raw = f"{input_folder}/{filename}"
            processed = f"{output_folder}/{title}.ogg"
            subprocess.run(['ffmpeg', '-i', raw, processed], check=True)
            print(f"Converted '{raw}' to '{processed}'")
        except subprocess.CalledProcessError as e:
            print(f"Error converting file {input_folder}: {e}")


convert("raw", "processed")
