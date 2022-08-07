import sys
import argparse
import typing as t
import os
import subprocess

SUPPORTED_FILE_FORMATS = {'.mp4': 'Video', '.nfa': 'Audio', '.srt': 'Subtitle'}

def parse_arguments() -> t.Tuple:
    """Parses command line arguments and returns args namespace."""
    parser = argparse.ArgumentParser(description='Preprocess the netflix directory.')
    parser.add_argument('-f','--folder', help='Video folder', required=True)
    args = parser.parse_args()
    folder = args.folder
    return (folder,)


def validate_args(folder: str):
    """Validates command line arguments."""
    if not os.path.isdir(folder):
        raise Exception(f'Directory "{folder}" not found!')


def get_files(folder: str) -> t.Tuple:
    """Returns netflix files."""
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


def main():
    # Process arguments.
    folder, = parse_arguments()
    validate_args(folder)

    # Get the supported files from the folder.
    video_file, audio_file, subtitle_file = get_files(folder)

    # Open files at once.
    audio_command, video_command = None, None
    if audio_file:
        audio_command = ['totem', os.path.join(folder, audio_file)]
    if video_file:
        video_command = ['vlc', os.path.join(folder, video_file), '-f', '--no-audio']
        if subtitle_file:
            video_command += ['--sub-file', os.path.join(folder, subtitle_file)]

    if audio_file:
        p_audio = subprocess.Popen(audio_command)
    if video_file:
        p_video = subprocess.Popen(video_command)
        
    print('Started netflix...')
    if audio_file:
        p_audio.communicate()
    if video_file:
        p_video.communicate()


if __name__ == "__main__":
    main()
