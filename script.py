import yt_dlp
from processors import get_video_formats, get_audio_formats
from utils import readable_size
from downloader import download_video, download_audio, download_thumbnail

from inputs import \
    get_output_path, \
    get_flag, \
    get_video_url, \
    get_user_selected_option, \
    get_user_preferred_audio_for_video

def download_youtube_video():
    output_path = get_output_path()
    flag = get_flag()
    
    while True:
        try:
            url = get_video_url()

            video_info = get_video_info(url)
            formats = video_info["formats"]
            
            print()
            print(video_info["title"], end="\n\n")

            video_formats = get_video_formats(formats)
            audio_formats = get_audio_formats(formats)

            if flag:
                download_with_flag(flag, url, video_formats, audio_formats, output_path)
            else:
                download_with_options(url, video_formats, audio_formats, output_path)

            print()
            print("Download successful")
            print("# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #\n")

        except Exception as e:
            print()
            print(f"Something went wrong: {e}")
            print("# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #\n")

def get_video_info(video_url):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'skip_download': True,
        'writeinfojson': True,
        'no_check_formats': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        video_info = ydl.extract_info(video_url, download=False)
        return video_info
    
def download_with_flag(flag, url, video_formats, audio_formats, output_path):
    if flag == 'best-v':
        handle_best_v_download(url, video_formats, audio_formats, output_path)
    elif flag == '1080p':
        handle_1080p_download(url, video_formats, audio_formats, output_path)
    elif flag == '1440p':
        handle_1440p_download(url, video_formats, audio_formats, output_path)
    elif flag == 'best-a':
        handle_best_a_download(url, audio_formats, output_path)
    elif flag == 'thumbnail':
        handle_thumbnail_download(url, output_path)

def download_with_options(url, video_formats, audio_formats, output_path):
    show_download_options(video_formats, audio_formats)
    user_choice = get_user_selected_option(video_formats, audio_formats)

    handle_selected_option_download(url, user_choice, video_formats, audio_formats, output_path)
    
def handle_best_v_download(url, video_formats, audio_formats, output_path):
    video_format_keys = list(video_formats.keys())
    best_video_format_key = video_format_keys[0]
    best_video_format = video_formats[best_video_format_key]
    video_format_id = best_video_format['format_id']

    audio_format_keys = list(audio_formats.keys())
    best_audio_format_key = audio_format_keys[0]
    best_audio_format = audio_formats[best_audio_format_key]
    audio_format_id = best_audio_format['format_id']

    print(f"Downloading {best_video_format_key} video with {best_audio_format_key} audio...")
    download_video(url, video_format_id, audio_format_id, output_path)

def handle_1080p_download(url, video_formats, audio_formats, output_path):
    video_format_keys = list(video_formats.keys())
    target_video_quality_format_key = [key for key in video_format_keys if "1080p" in key]

    if len(target_video_quality_format_key) == 0:
        video_format_keys[0]
    else:
        target_video_quality_format_key = target_video_quality_format_key[0]

    target_video_quality_format = video_formats[target_video_quality_format_key]
    target_video_id = target_video_quality_format['format_id']

    audio_format_keys = list(audio_formats.keys())
    best_audio_format_key = audio_format_keys[0]
    best_audio_format = audio_formats[best_audio_format_key]
    audio_format_id = best_audio_format['format_id']

    print(f"Downloading {target_video_quality_format_key} video with {best_audio_format_key} audio...")
    download_video(url, target_video_id, audio_format_id, output_path)

def handle_1440p_download(url, video_formats, audio_formats, output_path):
    video_format_keys = list(video_formats.keys())
    target_video_quality_format_key = [key for key in video_format_keys if "1440p" in key]

    if len(target_video_quality_format_key) == 0:
        video_format_keys[0]
    else:
        target_video_quality_format_key = target_video_quality_format_key[0]

    target_video_quality_format = video_formats[target_video_quality_format_key]
    target_video_id = target_video_quality_format['format_id']

    audio_format_keys = list(audio_formats.keys())
    best_audio_format_key = audio_format_keys[0]
    best_audio_format = audio_formats[best_audio_format_key]
    audio_format_id = best_audio_format['format_id']

    print(f"Downloading {target_video_quality_format_key} video with {best_audio_format_key} audio...")
    download_video(url, target_video_id, audio_format_id, output_path)

def handle_best_a_download(url, audio_formats, output_path):
    audio_format_keys = list(audio_formats.keys())
    best_audio_format_key = audio_format_keys[0]
    best_audio_format = audio_formats[best_audio_format_key]
    audio_format_id = best_audio_format['format_id']

    print(f"Downloading {best_audio_format_key} audio...")
    download_audio(url, audio_format_id['format_id'], output_path)

def handle_thumbnail_download(url, output_path):
    print("Downloading thumbnail...")
    download_thumbnail(url, output_path)
    
def show_download_options(video_formats, audio_formats):
    show_options_list(video_formats)
    print()

    audio_options_start_index = len(list(video_formats.keys()))
    show_options_list(audio_formats, audio_options_start_index)
    print()

    thumbnail_option_index = audio_options_start_index + len(list(audio_formats.keys()))
    print(f"[ {thumbnail_option_index} ] Video Thumbnail")
    print()


def show_options_list(formats: dict, start_index: int = 0):
    formats_keys = list(formats.keys())
    for i in range(len(formats_keys)):
        frmt = formats[formats_keys[i]]
        filesize = readable_size(frmt['filesize'])
        ext = frmt['ext']
        print(f"[ {start_index + i} ] {formats_keys[i]} . {ext} - {filesize}")

def handle_selected_option_download(url, user_choice, video_formats, audio_formats, output_path):
    video_options_count = len(list(video_formats.keys()))
    audio_options_count = len(list(audio_formats.keys()))
    options_count = video_options_count + audio_options_count

    if user_choice in range(video_options_count):
        audio_choice = get_user_preferred_audio_for_video(video_formats, audio_formats)
        print()

        video_format_keys = list(video_formats.keys())
        selected_video_format_key = video_format_keys[user_choice]
        selected_video_format = video_formats[selected_video_format_key]

        audio_format_keys = list(audio_formats.keys())
        selected_audio_format_key = audio_format_keys[audio_choice - video_options_count]
        selected_audio_format = audio_formats[selected_audio_format_key]

        print(f"Downloading {selected_video_format_key} video with {selected_audio_format_key} audio...")

        video_format_id = selected_video_format['format_id']
        audio_format_id = selected_audio_format['format_id']
        download_video(url, video_format_id, audio_format_id, output_path)
    
    elif user_choice in range(video_options_count, options_count):
        audio_format_keys = list(audio_formats.keys())
        selected_audio_format_key = audio_format_keys[user_choice - video_options_count]
        selected_audio_format = audio_formats[selected_audio_format_key]

        print()
        print(f"Downloading {selected_audio_format_key} audio...")

        audio_format_id = selected_audio_format['format_id']
        download_audio(url, selected_audio_format['format_id'], output_path)

    else:
        print()
        print("Downloading thumbnail...")
        download_thumbnail(url, output_path)

if __name__ == "__main__":
    download_youtube_video()