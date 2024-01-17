from PIL import Image
import os
import tkinter as tk
from tkinter import filedialog


def convert_to_png_with_transparency(input_folder, max_size_kb=700):
    for filename in os.listdir(input_folder):
        if filename.endswith('.jpg'):
            jpg_path = os.path.join(input_folder, filename)
            png_path = os.path.join(input_folder, filename.replace('.jpg', '.png'))

            # Open the JPG image and convert to PNG
            with Image.open(jpg_path) as img:
                img_rgba = img.convert('RGBA')

                # Alternative alpha channel creation methods:
                # img_rgba.putalpha(255)  # Set fully transparent alpha values
                # or use image processing techniques to create a more selective alpha channel

                # Choose a compression level for PNG saving:
                compression_level = 6  # Adjust as needed

                img_rgba.save(png_path, format='PNG', compress_level=compression_level)

                # Resize and compress further if needed
                while os.path.getsize(png_path) > max_size_kb * 1024 and img_rgba.width > 1:
                    new_width = int(img_rgba.width * 0.9)
                    new_height = max(1, int(img_rgba.height * new_width / img_rgba.width))
                    img_rgba = img_rgba.resize((new_width, new_height), Image.LANCZOS)
                    img_rgba.save(png_path, format='PNG', compress_level=compression_level)



def resize_images_with_aspect_ratio(input_folder, suffix='_small', target_width=720):
    # Ensure output folder exists
    output_folder = input_folder

    # Loop through each file in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename.replace(filename.split('.')[-1], f'{suffix}.{filename.split(".")[-1]}'))

            # Open the image
            with Image.open(input_path) as img:
                original_width, original_height = img.size
                aspect_ratio = original_height / original_width
                new_height = int(target_width * aspect_ratio)

                # Resize the image while maintaining aspect ratio
                img_resized = img.resize((target_width, new_height), Image.LANCZOS)

                # Save the resized image with the correct format
                img_resized.save(output_path, format=filename.split('.')[-1].upper())

#


def browse_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        entry_path.delete(0, tk.END)
        entry_path.insert(0, folder_path)


def resize_and_convert_images():
    input_folder = entry_path.get()

    if os.path.isdir(input_folder):
        convert_to_png_with_transparency(input_folder)
        resize_images_with_aspect_ratio(input_folder)
        result_label.config(text="Image resizing and conversion complete.")
    else:
        result_label.config(text="Invalid folder path. Please choose a valid folder.")


def close_window():
    root.destroy()


# Create the main Tkinter window
root = tk.Tk()
root.title("Image Resizer")

# Create and place widgets
label_instruction = tk.Label(root, text="Select the folder containing PNG and JPG files:")
label_instruction.pack(pady=10)

entry_path = tk.Entry(root, width=50)
entry_path.pack(pady=10)

button_browse = tk.Button(root, text="Browse", command=browse_folder)
button_browse.pack(pady=10)

button_resize = tk.Button(root, text="Resize and Convert Images", command=resize_and_convert_images)
button_resize.pack(pady=10)

result_label = tk.Label(root, text="")
result_label.pack(pady=10)

button_exit = tk.Button(root, text="Exit", command=close_window)
button_exit.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
