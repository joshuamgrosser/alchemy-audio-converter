import os
import shlex
import subprocess


# Function to rename and convert files in a specified directory
def rename_and_convert_files_in_directory(input_path, output_path):
    # order the filenames by name and loop through them
    for filename in sorted(os.listdir(input_path)):
        # split the filename into the name and extension
        name, extension = os.path.splitext(filename)

        # Grab the track title from ffmpeg
        try:
            path = os.path.join(input_path, filename)
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

            # Decode stdout to string and split into lines
            output_lines = result.stderr.decode('utf-8').strip().split('\n')
            # Filter out empty lines and strip each line
            output_lines = [line.strip() for line in output_lines if line.strip()]
            # Initialize title as None
            title = None
            # Iterate through each line to find the title
            for line in output_lines:
                if 'title' in line:
                    # Extract title after 'title'
                    title = line.split('title', 1)[1]
                    # Strip non-alphanumeric characters from title
                    title = ''.join(e for e in title if e.isalnum() or e.isspace())
                    title = title.strip()
                    break

            if title is None:
                print(f"No title found for {filename}")
                title = name  # Fallback to filename without extension if no title found
        except subprocess.CalledProcessError as e:
            print(f"Error extracting title from file {path}: {e}")
            title = None

        # if the file is not an mp3 or wav file, skip it
        if filename.endswith(".mp3") or filename.endswith(".wav"):
            try:
                raw = f"{input_path}/{filename}"
                processed = f"{output_path}/{title}.ogg"
                subprocess.run(['ffmpeg', '-i', raw, processed], check=True)
                print(f"Converted '{raw}' to '{processed}'")
            except subprocess.CalledProcessError as e:
                print(f"Error converting file {input_path}: {e}")
        else:
            # save the file without converting it
            raw = f"{input_path}/{filename}"
            processed = f"{output_path}/{title}{extension}"
            os.rename(raw, processed)
            print(f"Saved '{raw}' to '{processed}'")


# Kick off the process by calling the function with the input and output directories
rename_and_convert_files_in_directory("raw", "processed")
