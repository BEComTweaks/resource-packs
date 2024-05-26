# Made with ChatGPT.
import os
import random
import glob
import time
from shutil import get_terminal_size
if str(os.getcwd()).endswith("system32"):
    # This has to be in every script to prevent FileNotFoundError
    # Because for some reason, it runs it at C:\Windows\System32
    # Yeah, it is stupid, but I can't put these lines in custom_functions
    # Because that still brings up an error
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

from custom_functions import *
from selector import val_command
check("clrprint")
from clrprint import clrprint

check("PIL", "pillow")
from PIL import Image

def randrand(var, mini, maxi):
    if var + maxi > 255:
        maxi = 255 - var
    if var + mini < 0:
        mini = -var
    varc = var
    while varc == var:
        varc = var + random.randint(mini, maxi)
    return varc

def modify_pixel(pixel):
    r, g, b, a = pixel

    # Randomly change the RGB values within the range of +/- 6
    r = randrand(r, mini, maxi) % 256
    g = randrand(g, mini, maxi) % 256
    b = randrand(b, mini, maxi) % 256

    # Keep alpha value unchanged
    return (r, g, b, a)

def modify_image(image_path):
    # Open the image
    img = Image.open(image_path).convert("RGBA")

    # Get the image's width and height
    width, height = img.size

    # Create a new image to store the modified pixels
    new_img = Image.new("RGBA", (width, height))

    # Loop over all pixels
    for y in range(height):
        for x in range(width):
            # Get the pixel at the current position
            pixel = img.getpixel((x, y))
            # Modify the pixel with the new random range
            modified_pixel = modify_pixel(pixel)
            # Set the modified pixel in the new image
            new_img.putpixel((x, y), modified_pixel)
    # Save modified image in original
    new_img.save(image_path)

def modify_images_in_directory(directory):
    # Find all PNG files in the specified directory
    png_files = glob.glob(os.path.join(directory, "*.png"))

    # Modify each PNG file and save it back to its original location
    for png_file in png_files:
        # Modify the image and overwrite the original file
        modify_image(png_file)
        print(f'\r{png_file}{" " * (get_terminal_size().columns - len(str(png_file)))}')

def tweak_images():
    if os.name == "nt":
        clrprint(
            f"Enter the directory to the folder with PNG Files.\nExample: packs\\aesthetic\\AlternateCutCopper\\default\\textures\\blocks\\ \n{cdir()}\\",
            clr='b', end='')
        directory = f"{cdir()}\\{input()}"
    else:
        clrprint(
            f"Enter the directory to the folder with PNG Files.\nExample: packs/aesthetic/AlternateCutCopper/default/textures/blocks/ \n{cdir()}/",
            clr='b', end='')
        directory = f"{cdir()}/{input()}"
    # Changes each pixel withing a range of -6 to +6
    global mini, maxi
    mini, maxi = -6, 6
    if not os.path.isdir(directory):
        clrprint(f"{directory} is not valid.", clr="yellow")
        time.sleep(1)
        return 0

    modify_images_in_directory(directory)
    clrprint(f"\r\nModified all PNG files in {directory}")
    clrinput("Press Enter to exit.", clr="green")
    clear()

def compress_images():
    if os.name == "nt":
        clrprint(
            f"Enter the directory to the folder with PNG Files.\nExample: packs\\aesthetic\\AlternateCutCopper\\default\\textures\\blocks\\ \n{cdir()}\\",
            clr='b', end='')
        input_dir = f"{cdir()}\\{input()}"
    else:
        clrprint(
            f"Enter the directory to the folder with PNG Files.\nExample: packs/aesthetic/AlternateCutCopper/default/textures/blocks/ \n{cdir()}/",
            clr='b', end='')
        input_dir = f"{cdir()}/{input()}"
    compress_by = int(clrinput("Compress the images by:", clr='b'))
    # Walk through the directory tree
    for root, dirs, files in os.walk(input_dir):
        for filename in files:
            if filename.endswith('.png'):
                file_path = os.path.join(root, filename)
                broken = False
                # Open an existing PNG image
                with Image.open(file_path) as img:
                    try:
                        # Save the image with optimization and maximum compression level
                        img.save(file_path, optimize=True, compress_level=compress_by)
                        print(f'\r{str(file_path)[len(str(cdir())):]}{" " * (get_terminal_size().columns - len(str(file_path)[len(str(cdir())):]))}',end='')
                    except KeyboardInterrupt:
                        clrprint("KeyboardInterrupt raised!",clr="r")
                        img.save(file_path)
                        clrprint(f"Check whether {str(file_path)[len(str(cdir())):]} is still valid!",clr="p")
                        broken = True
                        break
    if not broken:
        clrprint(f"\r\nCompressed all PNG files in {input_dir[len(str(cdir())):]}")
    clrinput("Press Enter to exit.", clr="green")
    clear()

def image_utils():
    clrprint("Options:\n","Tweak Images in Directory\n","Compress Images in Directory","\nEnter your choice: ",clr="p,w,w,y",end="")
    progged = prog_search(input(),["tweak","compress"])
    if progged == 0:
        tweak_images()
    else:
        compress_images()

if __name__ == "__main__":
    image_utils()