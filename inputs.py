import os
import re

def get_output_path():
    while True:
        path = input("Enter the directory path for downloads or press Enter to place them in the current directory: ").strip()
        if path == "":
            print("Downloaded files will be place in the same directory!\n")
            return None
        if os.path.isdir(path):
            print(f'Downloaded files will be place in "{path}"!\n')
            return path
        else:
            print("Invalid path or the directory does not exist. Please try again!\n")

def get_flag():
    print("You can user a flag to automatically select download options. Available flags are: ")
    print(f"    [best-v] download best video with best audio")
    print(f"    [best-a] download best audio")
    print(f"    [thumbnail] download thumbnail")
    print()
    
    while True:
        user_flag = input("Enter the flag you want to add, like \"best-v\". If you don't want to add any flags just press enter: ")

        if user_flag == '':
            print("You didn't add any flags.\n")
            return None
        
        if 'best-v' in user_flag:
            print("Now for every link you enter the best video quality with the best audio quality will be selected for download automatically.\n")
            return 'best-v'
        
        if 'best-a' in user_flag:
            print("Now for every link you enter the best audio quality will be selected for download automatically.\n")
            return 'best-v'
        
        if 'best-v' in user_flag:
            print("Now for every link you enter the thumbnail of the video will be downloaded.\n")
            return 'thumbnail'
            
        print("Invalid flag!\n")

def get_video_url():
    while True:
        url = input("Enter the video URL: ")

        video_id_match = re.search(
            r'(?:https?:\/\/)?(?:www\.)?(?:m\.)?(?:youtube\.com\/watch\?v=|youtube\.com\/v\/|youtube\.com\/embed\/|youtu\.be\/)([a-zA-Z0-9_-]{11})',
            url
        )

        if video_id_match:
            return f'https://www.youtube.com/watch?v={video_id_match.group(1)}'
        else:
            print("Invalid url!\n")

def get_user_selected_option(video_formats, audio_formats):
    while True:
        try:
            user_choice = int(input("Enter the index for the aduio to mix with this video: "))

            video_options_count = len(list(video_formats.keys()))
            audio_options_count = len(list(audio_formats.keys()))
            options_count = video_options_count + audio_options_count

            if user_choice in range(options_count + 1):
                return user_choice
            else:
                print(f"Please choose an index from 0 to {options_count}!\n")

        except Exception as e:
            print(f"Invalid input: {e}\n")

def get_user_preferred_audio_for_video(video_formats, audio_formats):
    while True:
        try:
            audio_choice = int(input("Enter the index for the aduio to mix with this video: "))

            video_options_count = len(list(video_formats.keys()))
            audio_options_count = len(list(audio_formats.keys()))
            options_count = video_options_count + audio_options_count

            if audio_choice in range(video_options_count, options_count):
                return audio_choice
            else:
                print(f"Please choose an index from {video_options_count} to {options_count - 1}!\n")
            
        except Exception as e:
            print(f"Invalid input: {e}\n")