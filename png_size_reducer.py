from PIL import Image
import os

def resize_images(input_folder, output_folder, suffix='_small', target_resolution=(720, 1280)):
    # Ensure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Loop through each file in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith('.png'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename.replace('.png', f'{suffix}.png'))

            # Open the image
            with Image.open(input_path) as img:
                # Resize the image
                img_resized = img.resize(target_resolution, Image.ANTIALIAS)

                # Save the resized image
                img_resized.save(output_path, format='PNG')

if __name__ == "__main__":
    # Get user input for input and output folders
    input_folder = input("Enter the path of the folder containing PNG files: ")
    output_folder = input("Enter the path for the output folder: ")

    # Call the function to resize images
    resize_images(input_folder, output_folder)

    print("Image resizing complete.")
