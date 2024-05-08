import os
from pytube import YouTube
from youtubesearchpython import VideosSearch
import threading
import logging


# Configure logging
logging.basicConfig(filename='download_log.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)


def download_with_timeout(stream, filename):
    try:
        stream.download(filename=filename)
    except Exception as e:
        logging.error(f"Error occurred during download: {str(e)}")
        if os.path.exists(filename):
            os.remove(filename)
            logging.info(f"Deleted {filename}")


def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining 
    percentage_of_completion = bytes_downloaded / total_size * 100
    logging.info(f'Downloaded {percentage_of_completion:.2f}%')


def on_complete(stream, file_path):
    logging.info(f'Download complete. File saved at {file_path}')


def download_video(keywords, filename, min_length=60, max_length=3600):
    if os.path.exists(filename):
        logging.info(filename+" exists")
        return
    
    videosSearch = VideosSearch(keywords, limit=5)
    results = videosSearch.result()["result"]
    
    for video in results:
        if video["duration"] is None:
            continue
        
        duration_parts = video["duration"].split(":")
        duration_sec = int(duration_parts[-1]) + int(duration_parts[-2]) * 60
        
        if min_length <= duration_sec <= max_length:
        
            try:
                yt = YouTube(video["link"], on_progress_callback=on_progress, on_complete_callback=on_complete)
                stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

                download_thread = threading.Thread(target=download_with_timeout, args=(stream, filename))
                download_thread.start()
                download_thread.join(timeout=1200)   # Interrupt the download if it's not completed within 1200s to prevent oversized videos

                if download_thread.is_alive():
                    logging.info("Download timed out. Exiting...")
                    os._exit(1)
                return
                
            except Exception as e:
                logging.info(f"Failed to download video: {video['link']}, Error: {str(e)}")
    
    logging.info(f"No suitable videos found related to {keywords}")

