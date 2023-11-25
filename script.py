import os
import sys
import re
import yt_dlp

def download_youtube_video(output_path):
    url = get_video_url()

    video_formats, audio_formats = get_video_details(url)

    video_formats_keys = list(video_formats.keys())
    audio_formats_keys = list(audio_formats.keys())

    video_options_len = len(video_formats_keys)
    video_audio_options_len = video_options_len + len(audio_formats_keys)

    show_formats(video_formats)
    show_formats(audio_formats, video_options_len)

    print()
    print(f"[ {video_audio_options_len} ] Video Thumbnail", end="\n\n")

    user_choice = int(input("Enter the number you want to download: "))

    if user_choice < video_options_len:
        audio_choice = int(input("Enter the number for the aduio to mix with this video: "))
        print()

        selected_video_format = video_formats[video_formats_keys[user_choice]]
        selected_audio_format = audio_formats[audio_formats_keys[audio_choice - video_options_len]]

        print(f"Downloading: {video_formats_keys[user_choice]} with {audio_formats_keys[audio_choice - video_options_len]} audio...")
        download_video(url, selected_video_format['format_id'], selected_audio_format['format_id'], output_path)

    elif user_choice < video_audio_options_len:
        selected_audio_format = audio_formats[audio_formats_keys[user_choice - video_options_len]]
        print(f"\nDownloading: {audio_formats_keys[user_choice - video_options_len]}...")
        download_audio(url, selected_audio_format['format_id'], output_path)

    elif user_choice == video_audio_options_len + 1:
        print("\nDownloading thumbnail...")
        download_thumbnail(url, output_path)

    else:
        print("The number you have selected is not in this list!")

    print()
    print("Download successful")

def get_output_path():
    while True:
        path = input("Enter the directory path for downloads or press Enter to place them in the current directory: ").strip()
        if path == "":
            print("Downloaded files will be place in the same directory!")
            return None
        if os.path.isdir(path):
            print(f'Downloaded files will be place in "{path}"!')
            return path
        else:
            print("Invalid path or the directory does not exist. Please try again.\n")

def get_video_url():
    url = input("Enter the video URL: ")

    video_id_match = re.search(
        r'(?:https?:\/\/)?(?:www\.)?(?:m\.)?(?:youtube\.com\/watch\?v=|youtube\.com\/v\/|youtube\.com\/embed\/|youtu\.be\/)([a-zA-Z0-9_-]{11})',
        url
    )

    if video_id_match:
        return f'https://www.youtube.com/watch?v={video_id_match.group(1)}'
    else:
        print("Invalid url!")
        sys.exit()

def get_video_details(video_url):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'skip_download': True,
        'writeinfojson': True,
        'no_check_formats': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=False)

        print(info_dict["title"])

        all_formats = info_dict["formats"]
        all_formats_reversed = all_formats.copy()
        all_formats_reversed.reverse()

        video_formats = find_video_formats(all_formats_reversed)
        audio_formats = find_audio_formats(all_formats_reversed)

        return video_formats, audio_formats
    
def find_video_formats(formats):
    video_formats = {}
    for frmt in formats:
        vcodec = frmt.get('vcodec', 'none')
        acodec = frmt.get('acodec', 'none')
        protocol = frmt.get('protocol', 'none')
        if vcodec == 'none' or acodec != 'none' or protocol != 'https':
            continue

        height = frmt.get('height')
        fps = frmt.get('fps')
        format_key = f"{height}p . {fps}fps"

        video_formats_keys = video_formats.keys()
        if format_key not in video_formats_keys:
            video_formats[format_key] = frmt
        else:
            duplicate_format = video_formats[format_key]
            if duplicate_format['filesize'] < frmt['filesize']:
                video_formats[format_key] = frmt

    return video_formats

def find_audio_formats(formats):
    audio_formats = {}
    for frmt in formats:
        vcodec = frmt.get('vcodec', 'none')
        acodec = frmt.get('acodec', 'none')
        if vcodec != 'none' or acodec == 'none':
            continue

        format = frmt.get('format')
        if 'drc' in format:
            continue
        
        abr = frmt.get('abr')
        format_key = f"{abr}kbp"
        audio_formats[format_key] = frmt

    audio_formats_sorted = sort_audio_formats(audio_formats)
    audio_formats_clean = remove_close_audio_formats(audio_formats_sorted)

    return audio_formats_clean

def sort_audio_formats(audio_formats):
    audio_formats_sorted = {}
    audio_formats_keys = sorted([float(a.split('kbp')[0]) for a in audio_formats], reverse=True)
    for new_format in audio_formats_keys:
        key = f"{new_format}kbp"
        audio_formats_sorted[key] = audio_formats[key]

    return audio_formats_sorted

def remove_close_audio_formats(audio_formats: dict):
    format_keys = list(audio_formats.keys())
    last_key = format_keys[0]
    for key in format_keys[1:]:
        key_num = float(key.split('kbp')[0])
        last_key_num = float(last_key.split('kbp')[0])

        if abs(key_num - last_key_num) < 10:
            format_keys.remove(key)
        else:
            last_key = key

    audio_formats_clean = {}
    for key in format_keys:
        audio_formats_clean[key] = audio_formats[key]
    
    return audio_formats_clean

def show_formats(formats: dict, start_index: int = 0):
    formats_keys = list(formats.keys())
    print()
    for i in range(len(formats_keys)):
        frmt = formats[formats_keys[i]]
        filesize = readable_size(frmt['filesize'])
        ext = frmt['ext']
        print(f"[ {start_index + i} ] {formats_keys[i]} . {ext} - {filesize}")

def readable_size(size):
    KB = 1024
    MB = KB * KB
    GB = MB * KB

    if size < MB:
        return f"{size/KB:.2f} KB"
    elif size < GB:
        return f"{size/MB:.2f} MB"
    else:
        return f"{size/GB:.2f} GB"

def download_video(url, video_format_id, audio_format_id, output_path):
    outtmpl = '%(title)s.%(ext)s' if output_path is None else os.path.join(output_path, '%(title)s.%(ext)s')

    if audio_format_id:
        options = {
            'format': f'{video_format_id}+{audio_format_id}',
            'outtmpl': outtmpl,
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
            'merge_output_format': 'mp4',
        }
    else:
        options = {
            'format': video_format_id,
            'outtmpl': '%(title)s.%(ext)s',
        }

    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])

def download_audio(url, format_id, output_path):
    outtmpl = '%(title)s.%(ext)s' if output_path is None else os.path.join(output_path, '%(title)s.%(ext)s')

    ydl_opts = {
        'format': f'{format_id}',
        # 'postprocessors': [{    # add this to get only mp3 audio instead of the original format
        #     'key': 'FFmpegExtractAudio',
        #     'preferredcodec': 'mp3',
        # }],
        'outtmpl': outtmpl,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def download_thumbnail(video_url, output_path):
    outtmpl = 'thumbnail.%(ext)s' if output_path is None else os.path.join(output_path, 'thumbnail.%(ext)s')
    
    ydl_opts = {
        'skip_download': True,
        'outtmpl': outtmpl,
        'postprocessors': [{
            'key': 'FFmpegMetadata',
        }],
        'writethumbnail': True,
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

if __name__ == "__main__":
    output_path = get_output_path()
    print()

    while True:
        download_youtube_video(output_path)
        print("# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #\n")