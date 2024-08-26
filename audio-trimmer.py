import os
import re
import subprocess

def trim_and_fade(input_folder, output_folder):
    for filename in sorted(os.listdir(input_folder)):
        name, extension = os.path.splitext(filename)
        if extension.lower() != '.ogg':
            continue

        input_path = os.path.join(input_folder, filename)

        try:
            result = subprocess.run([
                'ffprobe',
                '-v',
                'info',
                '-show_entries',
                'format_tags=title',
                '-of',
                'default=noprint_wrappers=1:nokey=1',
                input_path
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
            print(f"Error extracting title from file {input_path}: {e}")
            title = None

        # Rename the output file to all lowercase and replace whitespace with dashes
        title = re.sub(r'[^a-zA-Z0-9]', ' ', title)
        title = re.sub(r'\s+', ' ', title)
        title = title.lower().strip().replace(' ', '-')
        output_path = os.path.join(output_folder, f"{title}{extension}")

        try:
            subprocess.run([
                'ffmpeg',
                '-i', input_path,
                '-af', 'afade=t=in:ss=0:d=5,afade=t=out:st=595:d=5',
                '-t', '600',
                output_path
            ], check=True)
            print(f"Processed '{input_path}' to '{output_path}'")
        except subprocess.CalledProcessError as e:
            print(f"Error processing file {input_path}: {e}")

# Example usage
trim_and_fade('raw', 'processed')
