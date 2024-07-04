import os
import subprocess


# Function to rename and convert files in a specified directory
def rename_and_convert_files_in_directory(input_path, output_path):
    # Iterate through all files in the specified directory
    for filename in os.listdir(input_path):

        # if the file is not an mp3 or wav file, skip it
        if not filename.endswith(".ogg") and not filename.endswith(".mp3") and not filename.endswith(".wav"):
            continue

        # split the filename into the name and extension
        name, extension = os.path.splitext(filename)

        # Grab the track title from ffmpeg
        try:
            result = subprocess.run([
                'ffprobe',
                '-v',
                'error',
                '-show_entries',
                'format_tags=title',
                '-of',
                'default=noprint_wrappers=1:nokey=1',
                f"{input_path}/{filename}"
            ], stdout=subprocess.PIPE)
            title = result.stdout.decode('utf-8').strip()
        except subprocess.CalledProcessError as e:
            print(f"Error getting title for file {filename}: {e}")
            title = name

        try:
            raw = f"{input_path}/{filename}"
            processed = f"{output_path}/{title}.ogg"
            subprocess.run(['ffmpeg', '-i', raw, processed], check=True)
            print(f"Converted '{raw}' to '{processed}'")
        except subprocess.CalledProcessError as e:
            print(f"Error converting file {input_path}: {e}")


# Kick off the process by calling the function with the input and output directories
rename_and_convert_files_in_directory("raw", "processed")
