import os
from moviepy.editor import VideoFileClip

def slice_video(output_folder, duration=5):
    os.makedirs(output_folder, exist_ok=True)
    clip = VideoFileClip("temp.mp4")
    num_segments = int(clip.duration / duration)

    for i in range(num_segments):
        start_time = i * duration
        end_time = min((i + 1) * duration, clip.duration)
        segment = clip.subclip(start_time, end_time)
        segment.write_videofile(os.path.join(output_folder, f"{i}.mp4"), codec="libx264")

    clip.close()
