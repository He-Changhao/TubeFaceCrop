import os
from mtcnn import MTCNN
from moviepy.editor import VideoFileClip
from central_crop import central_crop

# Initialize the MTCNN face detector
detector = MTCNN()

def detect_faces(frame):
    result = detector.detect_faces(frame)
    return len(result) > 0

def remove_faces(input_file, max_duration=10, frame_buffer_size=10):
    '''
    max_duration: The desired duration of the final video clip
    frame_buffer_size: The number of frames between each face detection
    '''
    clip = VideoFileClip(input_file)
    fps = clip.fps
    
    new_frames = []
    frame_buffer = []
    frame_count = 0
    total_frames = int(clip.duration * fps)

    for frame in clip.iter_frames(fps=fps):
        frame_buffer.append(frame)
        frame_count += 1
        print("Processing: {} / {}".format(frame_count, total_frames))
        print("Processed frames: {}".format(len(new_frames)))

        if len(frame_buffer) == frame_buffer_size:
            if detect_faces(frame_buffer[frame_buffer_size-1]):
                frame_buffer.clear()
            else:
                new_frames.extend(frame_buffer)
                frame_buffer.clear()
                if len(new_frames) / fps >= max_duration:
                    break

    # Create a video clip without faces
    new_clip = VideoFileClip(input_file, audio=False)
    new_clip = new_clip.set_fps(fps)
    new_clip = new_clip.set_duration(len(new_frames) / fps)
    new_clip = new_clip.set_make_frame(lambda t: new_frames[int(t * fps)])
    
    # Central crop
    cropped_clip = central_crop(new_clip)
    cropped_clip.write_videofile("temp.mp4", codec="libx264")
    
    clip.close()
    new_clip.close()
    cropped_clip.close()
