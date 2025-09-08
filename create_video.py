import cv2
import numpy as np

def wrap_text(text, font, font_scale, thickness, width):
    """
    Wraps text to fit within a specified width.
    """
    words = text.split(' ')
    lines = []
    current_line = ""

    for word in words:
        # Check the size of the line with the new word
        test_line = f"{current_line} {word}".strip()
        (text_width, text_height), _ = cv2.getTextSize(test_line, font, font_scale, thickness)

        if text_width > width:
            lines.append(current_line)
            current_line = word
        else:
            current_line = test_line
    
    lines.append(current_line) # Add the last line
    return lines

# Video parameters
width, height = 1080, 1920  # 9:16 aspect ratio
fps = 30
duration = 5
frames = fps * duration
output_filename = "output_video.mp4"
margin = 80 # Add a margin to the sides

# Text parameters
text = "Constant information: Unlike current affairs, static topics like historical facts, geographical locations, and scientific principles remain the same, requiring consistent revision rather than tracking constant changes."
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 3
color = (255, 255, 255)  # white
thickness = 6
line_spacing = 20

# --- MODIFICATION START ---
# Automatically wrap the text to fit the frame width minus margins
wrapped_text = wrap_text(text, font, font_scale, thickness, width - (2 * margin))
# --- MODIFICATION END ---

# Create video writer
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter(output_filename, fourcc, fps, (width, height))

print(f"Generating {frames} frames for the video...")

# Calculate total height of the text block to center it vertically
total_text_height = 0
line_heights = []
for line in wrapped_text:
    (lw, lh), baseline = cv2.getTextSize(line, font, font_scale, thickness)
    line_heights.append(lh + baseline)
    total_text_height += lh + baseline + line_spacing

total_text_height -= line_spacing # Remove spacing after the last line
start_y = (height - total_text_height) // 2

# Generate frames
for _ in range(frames):
    frame = np.zeros((height, width, 3), dtype=np.uint8)
    
    y = start_y
    # Loop through each wrapped line and draw it on the frame
    for i, line in enumerate(wrapped_text):
        (line_width, _), _ = cv2.getTextSize(line, font, font_scale, thickness)
        
        # Calculate x and y for this line
        x = (width - line_width) // 2
        y += line_heights[i] # Move down by the height of the current line

        # Put the text on the frame
        cv2.putText(frame, line, (x, y), font, font_scale, color, thickness, cv2.LINE_AA)
        
        y += line_spacing # Add spacing for the next line

    out.write(frame)

out.release()
print(f"Video '{output_filename}' created successfully!")
