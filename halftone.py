from PIL import Image, ImageDraw, ImageSequence
import numpy as np
import os

def halftone_frame(img, dot_size):
    width, height = img.size
    pixels = np.array(img)

    frame = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(frame)

    for y in range(0, height, dot_size):
        for x in range(0, width, dot_size):
            region = pixels[y:y + dot_size, x:x + dot_size]
            avg = np.mean(region)
            radius = (1 - avg / 255) * (dot_size / 2)
            draw.ellipse(
                (x + dot_size/2 - radius, y + dot_size/2 - radius,
                 x + dot_size/2 + radius, y + dot_size/2 + radius),
                fill="black"
            )

    return frame

def create_halftone_animation(image_path, output_gif="halftone_animation.gif",
                              start_dot=20, end_dot=3, steps=10):
    img = Image.open(image_path).convert("L")  # grayscale
    img = img.resize((300, 300))  # Resize for speed and visibility

    dot_sizes = np.linspace(start_dot, end_dot, steps).astype(int)
    frames = []

    for i, dot_size in enumerate(dot_sizes):
        print(f"Generating frame {i+1} with dot size {dot_size}")
        frame = halftone_frame(img, dot_size)
        frames.append(frame)

    # Save as GIF
    frames[0].save(output_gif, save_all=True, append_images=frames[1:], duration=200, loop=0)
    print(f"Saved animation as {output_gif}")

# Example usage
create_halftone_animation("before.jpg", steps=12) #Change the file path
