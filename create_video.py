import cv2
import numpy as np

# Video parameters
width, height = 1080, 1920  # 9:16 aspect ratio
fps = 30
duration = 5
frames = fps * duration
output_filename = "blood_types_video.mp4"

# --- MODIFICATION START ---
# Text parameters - We split the text into lines using "\n"
text = "blood types are these\na, b, o"
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 3
color = (255, 255, 255)  # white
thickness = 6 # Made it a bit thicker for visibility
line_spacing = 20 # The space in pixels between the lines of text
# --- MODIFICATION END ---

# Create video writer
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter(output_filename, fourcc, fps, (width, height))

print(f"Generating {frames} frames for the video...")

# Split the text into a list of lines
text_lines = text.split('\n')

# Calculate the total height of the text block to center it vertically
(text_width, text_height), baseline = cv2.getTextSize(text_lines[0], font, font_scale, thickness)
total_text_height = len(text_lines) * (text_height + baseline + line_spacing)
start_y = (height - total_text_height) // 2


for _ in range(frames):
    # Create black background for each frame
    frame = np.zeros((height, width, 3), dtype=np.uint8)

    # --- MODIFICATION START ---
    # Loop through each line and draw it on the frame
    y = start_y # Reset y-position for each frame
    for i, line in enumerate(text_lines):
        # Get the size of the current line to center it horizontally
        (line_width, line_height), baseline = cv2.getTextSize(line, font, font_scale, thickness)
        
        # Calculate x and y for this specific line
        x = (width - line_width) // 2
        y += line_height + baseline

        # Put the text on the frame
        cv2.putText(frame, line, (x, y), font, font_scale, color, thickness, cv2.LINE_AA)

        # Add spacing for the next line
        y += line_spacing
    # --- MODIFICATION END ---


    # Write the completed frame to the video file
    out.write(frame)

print(f"Finished writing frames. Releasing video file: {output_filename}")
out.release()
print("Video generation complete.")
