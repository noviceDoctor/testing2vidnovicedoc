import cv2
import numpy as np

# Video parameters
width, height = 1080, 1920  # 9:16 aspect ratio
fps = 30
duration = 5
frames = fps * duration
output_filename = "blood_types_video.mp4"

# Text parameters
text = "blood types are these a, b, o"
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 3
color = (255, 255, 255)  # white
thickness = 5

# Create video writer
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter(output_filename, fourcc, fps, (width, height))

print(f"Generating {frames} frames for the video...")

for _ in range(frames):
    # Create black background
    frame = np.zeros((height, width, 3), dtype=np.uint8)

    # Get boundary of text for centering
    (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, thickness)

    # Calculate center position
    x = (width - text_width) // 2
    y = (height + text_height) // 2

    # Put text on frame
    cv2.putText(frame, text, (x, y), font, font_scale, color, thickness, cv2.LINE_AA)

    # Write frame to video file
    out.write(frame)

print(f"Finished writing frames. Releasing video file: {output_filename}")
out.release()
print("Video generation complete.")
