import os
import shutil


def copy_image_files(src_directory: str, dest_directory: str):
    print(f"Scanning directory: {src_directory}")
    if not os.path.exists(src_directory):
        print(f"Source directory does not exist: {src_directory}")
        return
    if not os.path.isdir(src_directory):
        print(f"Not a directory: {src_directory}")
        return

    if not os.path.exists(dest_directory):
        os.makedirs(dest_directory)
        print(f"Created destination directory: {dest_directory}")

    try:
        for root, dirs, files in os.walk(src_directory):
            print(f"Entering directory: {root}")
            for file in files:
                if file.lower().endswith(('.png', '.webp')):
                    src_file_path = os.path.join(root, file)
                    dest_file_path = os.path.join(dest_directory, file)
                    shutil.copy2(src_file_path, dest_file_path)
                    print(f"Copied file: {src_file_path} to {dest_file_path}")
    except PermissionError as e:
        print(f"Permission error: {e}")


if __name__ == "__main__":
    src_directory = input("Enter the source directory path: ").strip('"')
    dest_directory = input("Enter the destination directory path: ").strip('"')
    copy_image_files(src_directory, dest_directory)
