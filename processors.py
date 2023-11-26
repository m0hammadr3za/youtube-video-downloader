import copy

def get_video_formats(formats: list):
    all_formats = copy.deepcopy(formats)
    all_formats.reverse()

    video_formats = {}
    for frmt in all_formats:
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

def get_audio_formats(formats: list):
    all_formats = copy.deepcopy(formats)
    all_formats.reverse()

    audio_formats = {}
    for frmt in all_formats:
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