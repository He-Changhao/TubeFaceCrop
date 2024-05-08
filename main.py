import pandas as pd
import os
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore")

from download import download_video
from recognition import remove_faces
from slice_video import slice_video

# Step 1: Crawl related videos from YouTube
df = pd.read_excel("name.xlsx")
for _, row in df.iterrows():
    keywords = row[0]
    filename = f"videos\\{keywords}.mp4"
    download_video(keywords, filename, min_length=60, max_length=3600)

# Step 2: Detect and remove faces from videos, perform central crop, and slice the videos into 5-second segments
input_folder_path = "./videos"
output_folder_path = "./results"

# Get a list of all video filenames in the input folder
video_files = [f for f in os.listdir(input_folder_path) if f.endswith('.mp4')]
for video_file in video_files:
    video_path = os.path.join(input_folder_path, video_file)
    # Call the remove_faces function to detect and remove faces from the video, then perform central crop. Note: This step will generate a temp.mp4 file as the result.
    remove_faces(video_path)

    # Call the slice_video function to slice the video into 5-second segments
    output_folder = os.path.join(output_folder_path, os.path.splitext(video_file)[0])
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    slice_video(output_folder)

    # Delete the temporary generated video file
    os.remove("temp.mp4")
