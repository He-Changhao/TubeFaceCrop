import os
from moviepy.editor import VideoFileClip


def central_crop(clip, target_width=224, target_height=224):
    # Determine the aspect ratio after adjustment
    aspect_ratio = target_width / target_height

    # Get the original dimensions of the video
    original_width, original_height = clip.size

    # Calculate the adjusted dimensions
    if original_width / original_height > aspect_ratio:
        # If the original video has a larger aspect ratio, adjust based on height
        new_height = target_height
        new_width = int(target_height * original_width / original_height)
    else:
        # If the original video has a smaller or equal aspect ratio, adjust based on width
        new_width = target_width
        new_height = int(target_width * original_height / original_width)

    # Resize the video while maintaining aspect ratio
    resized_clip = clip.resize((new_width, new_height))

    # Central crop
    x_center = new_width // 2
    y_center = new_height // 2
    x_start = x_center - (target_width // 2)
    x_end = x_center + (target_width // 2)
    y_start = y_center - (target_height // 2)
    y_end = y_center + (target_height // 2)

    cropped_clip = resized_clip.crop(x1=x_start, y1=y_start, x2=x_end, y2=y_end)

    return cropped_clip
