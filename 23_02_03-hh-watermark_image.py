# Script to add watermark to images in a folder
# Usage: python3 watermark.py <folder> <watermark.png>
# Example: python3 watermark.py images watermark.png

import os
import sys
from PIL import Image

def watermark_image(input_image_path, output_image_path, watermark_image_path, position):
    try:
        # Open the watermark image
        watermark = Image.open(watermark_image_path)
        # Open the input image
        image = Image.open(input_image_path)
        # Get the size of the watermark
        width, height = watermark.size
        # Get the size of the input image
        image_width, image_height = image.size

        # Calculate the position of the watermark
        if position == 'top-left':
            position = (0, 0)
        elif position == 'top-right':
            position = (image_width - width, 0)
        elif position == 'bottom-left':
            position = (0, image_height - height)
        elif position == 'bottom-right':
            position = (image_width - width, image_height - height)
        else:
            raise ValueError('Unknown position')
        # Add the watermark to the image
        image.paste(watermark, position, mask=watermark)
        # Save the image
        image.save(output_image_path)

        print('Watermarked image saved as', output_image_path)
    except Exception as e:
        print(e)

def main():
    # Get the folder path
    folder = sys.argv[1]
    print(f"Folder: {folder}")
    # Get the watermark path
    watermark = sys.argv[2]
    print(f"Watermark: {watermark}")
    # Get the position of the watermark
    position = sys.argv[3]
    print(f"Position: {position}")

    # Loop through the images in the folder
    for filename in os.listdir(folder):
        # Get the path to the image
        input_image_path = os.path.join(folder, filename)
        # Get the path to the output image
        output_image_path = os.path.join(folder, 'watermarked-' + filename)

        print(f"output_image_path : {output_image_path}")

        # Watermark the image
        watermark_image(input_image_path, output_image_path, watermark, position)

if __name__ == '__main__':
    main()


