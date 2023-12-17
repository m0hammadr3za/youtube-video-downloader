import os
import yt_dlp

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

def download_mp3_audio(url, format_id, output_path):
    outtmpl = '%(title)s.%(ext)s' if output_path is None else os.path.join(output_path, '%(title)s.%(ext)s')

    ydl_opts = {
        'format': f'{format_id}',
        'postprocessors': [{    # add this to get only mp3 audio instead of the original format
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }],
        'outtmpl': outtmpl,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def download_thumbnail(video_url, output_path):
    outtmpl = '%(title)s.%(ext)s' if output_path is None else os.path.join(output_path, '%(title)s.%(ext)s')
    
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