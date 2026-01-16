# SPDX-FileCopyrightText: 2025 stharrold
# SPDX-License-Identifier: Apache-2.0

import os
import sys

from PIL import Image, ImageDraw, ImageFont


def get_font(size):
    # Common font paths on macOS and Linux
    font_paths = [
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/liberation/LiberationSans-Regular.ttf",
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def overlay_labels(input_path, output_path):
    try:
        img = Image.open(input_path)
    except FileNotFoundError:
        print(f"Error: Input file not found: {input_path}")
        sys.exit(1)

    draw = ImageDraw.Draw(img)

    # Image dimensions
    w, h = img.size
    print(f"Image size: {w}x{h}")

    # Configuration: Label text and approximate center coordinates (x, y)
    # Assuming triangular layout based on prompt: Top, Bottom-Left, Bottom-Right, Center
    # Adjust these coordinates based on the actual image visual if needed.
    labels = [
        {
            "text": "Analytics Maturity",
            "pos": (w // 2, int(h * 0.15)),  # Top Center
            "color": "teal",
        },
        {
            "text": "Workforce Agility",
            "pos": (int(w * 0.20), int(h * 0.80)),  # Bottom Left
            "color": "slate blue",  # approximate
        },
        {
            "text": "Technical Enablement",
            "pos": (int(w * 0.80), int(h * 0.80)),  # Bottom Right
            "color": "cyan",  # approximate
        },
        {
            "text": "Knowledge Preservation",
            "pos": (w // 2, int(h * 0.55)),  # Center
            "color": "black",
        },
    ]

    # Font settings
    font_size = 24  # Adjust size as needed
    font = get_font(font_size)

    padding = 10

    for item in labels:
        text = item["text"]
        cx, cy = item["pos"]

        # Calculate text bounding box using getbbox (left, top, right, bottom)
        bbox = font.getbbox(text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Define background box coordinates (centered on pos)
        box_left = cx - (text_width // 2) - padding
        box_top = cy - (text_height // 2) - padding
        box_right = cx + (text_width // 2) + padding
        box_bottom = cy + (text_height // 2) + padding

        # Draw white rectangle background
        draw.rectangle(
            [box_left, box_top, box_right, box_bottom], fill="white", outline="gray", width=1
        )

        # Draw text
        # Align text to center
        draw.text(
            (cx - text_width // 2, cy - text_height // 2 - bbox[1]),  # Adjust for baseline
            text,
            font=font,
            fill="black",  # Using black for max readability on white box
        )

    img.save(output_path)
    print(f"Saved labeled image to: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python overlay_labels.py <input_image> <output_image>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    overlay_labels(input_file, output_file)
