import yt_dlp
from inputs import get_output_path, get_video_url, get_user_selected_option, get_user_preferred_audio_for_video
from processors import get_video_formats, get_audio_formats
from utils import readable_size
from downloader import download_video, download_audio, download_thumbnail

def download_youtube_video():
    output_path = get_output_path()
    
    while True:
        try:
            url = get_video_url()

            video_info = get_video_info(url)
            formats = video_info["formats"]
            
            print()
            print(video_info["title"], end="\n\n")

            video_formats = get_video_formats(formats)
            audio_formats = get_audio_formats(formats)

            show_download_options(video_formats, audio_formats)
            user_choice = get_user_selected_option(video_formats, audio_formats)

            handle_selected_option_download(url, user_choice, video_formats, audio_formats, output_path)

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