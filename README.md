# Python YouTube Video Downloader

This Python application enables users to download videos, audio, and thumbnails from YouTube. It uses the `yt_dlp` library to extract video details, choose the desired format, and handle the download process.

## Requirements

- Python 3.x
- yt_dlp library (`pip install yt_dlp`)

## Usage

1. **Start the Application**: Run the script to initiate the application.
2. **Input Video URL**: When prompted, enter the YouTube video URL.
3. **Select Format**: Choose from the provided video and audio formats.
   - If a video format is chosen, you'll need to select an accompanying audio format.
   - Choosing an audio format will download only the audio.
   - There's also an option to download the video thumbnail.
4. **Download**: The selected content will be downloaded to your system.

## Customization

- **Audio Only**: Uncomment the postprocessor section in `download_audio()` to exclusively download audio in MP3 format.
- **Output Format**: You can modify the `outtmpl` in `download_video()` and `download_audio()` to alter the output file name template.

## Error Handling

- The application checks for valid YouTube URLs and format selections.
- Appropriate messages are displayed in case of invalid inputs.

## Looping Mechanism

- The application restarts after each download, allowing multiple downloads in one session.
