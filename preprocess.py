import argparse
import os
import typing as t
import subprocess
from pathlib import Path
import shutil
import sys
from to_srt import xml_to_srt

SUPPORTED_FILE_FORMATS = {'.nfv': 'Video', '.nfa': 'Audio', '.nfs': 'Subtitle'}


def parse_arguments() -> t.Tuple:
    """Parses command line arguments and returns args namespace."""
    parser = argparse.ArgumentParser(description='Preprocess the netflix directory.')
    parser.add_argument('-f','--folder', help='Video folder', required=True)
    parser.add_argument('-n','--name', help='Video name', required=True)
    args = parser.parse_args()
    folder, name = args.folder, args.name
    return (folder, name)


def get_files(folder: str) -> t.Tuple:
    """Confirms the file to be considered from the user and returns their filenames."""
    files_to_consider = ()

    print(f'\n{"-"*10} FILES {"-"*10}')
    for format, format_type in SUPPORTED_FILE_FORMATS.items():
        all_files = [f for f in os.listdir(folder) if f.endswith(format)]
        file_count = len(all_files)

        print(f'{" "*(8-len(format_type))}{format_type} file(s): ({file_count}) {all_files if file_count > 0 else "N/A"}')

        def get_file_to_be_considered():
            if file_count == 0:
                return None
            if file_count == 1:
                return all_files[0]
            # Confirms from the user which file to be considered.
            if file_count > 1:
                while True:
                    file = all_files[int(input(f'Which {format_type.lower()} file should I consider? (Enter index): '))]
                    return file
        
        files_to_consider += (get_file_to_be_considered(),)
    
    return files_to_consider


def validate_args(folder: str, name: str):
    """Validates command line arguments."""
    if not os.path.isdir(folder):
        raise Exception(f'Directory "{folder}" not found!')


def create_new_folder(folder: str, name: str) -> str:
    """Creates a new folder for the converted files."""
    folder_parent = Path(folder).parent.absolute()
    new_folder = os.path.join(folder_parent, name)
    if os.path.isdir(new_folder):
        print(f'The folder "{new_folder}" already exists. Should I delete it or create a new folder?\nEnter "d": To delete the existing folder first.\nEnter "n": To create a new folder.\nEnter "t": To terminate the process.')
        choice = input('Your choice: ')
        if choice == 'd':
            shutil.rmtree(new_folder)
        elif choice == 'n':
            name = input('Very well! What should I name the new directory to? ')
            new_folder = os.path.join(folder_parent, name)
        elif choice == 't':
            sys.exit(0)

    os.makedirs(new_folder)
    print(f'Cool! Processing "{name}"...')
    return name, new_folder


def parse_subtitle_file(subtitle_file_path, new_subtitle_file_path):
    """Parses xml file and converts it into .srt file format."""
    with open(subtitle_file_path) as xml_file:
        subtitles = xml_to_srt(xml_file.read())

    with open(new_subtitle_file_path, 'w') as srt_file:
        srt_file.write(subtitles)


def main():
    # Process arguments.
    folder, name = parse_arguments()
    validate_args(folder, name)

    # Get the supported files from the folder.
    video_file, audio_file, subtitle_file = get_files(folder)

    # Create a new folder.
    name, new_folder = create_new_folder(folder, name)

    # Process the video file.
    if video_file:
        video_file_path = os.path.join(folder, video_file)
        new_video_file_path = os.path.join(new_folder, f'{name}.mp4')
        command = ['ffmpeg', '-i', video_file_path, '-c:v', 'copy', os.path.join(new_folder, new_video_file_path)]
        p = subprocess.Popen(command)
        print('Processing video file...')
        p.communicate()
        print(f'Processed video file successfully.')

    # I couldn't find a way to convert audio file.
    # Copy as it is at the moment.
    if audio_file:
        audio_file_path = os.path.join(folder, audio_file)
        new_audio_file_path = os.path.join(new_folder, f'{name}.nfa')
        shutil.copyfile(audio_file_path, new_audio_file_path)
        print(f'Processed audio file successfully.')

    # Parse subtitle file and convert it to .srt.
    if subtitle_file:
        subtitle_file_path = os.path.join(folder, subtitle_file)
        new_subtitle_file_path = os.path.join(new_folder, f'{name}.srt')
        parse_subtitle_file(subtitle_file_path, new_subtitle_file_path)
        print(f'Processed subtitle file successfully.')


if __name__ == "__main__":
    main()
