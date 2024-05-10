# Made with ChatGPT.
import os
import random
import glob
import time

if str(os.getcwd()).endswith("system32"):
    # This has to be in every script to prevent FileNotFoundError
    # Because for some reason, it runs it at C:\Windows\System32
    # Yeah, it is stupid, but I can't put these lines in custom_functions
    # Because that still brings up an error
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

from custom_functions import *

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

    # Save the modified image to the same file path, replacing the original
    new_img.save(image_path)


def modify_images_in_directory(directory):
    # Find all PNG files in the specified directory
    png_files = glob.glob(os.path.join(directory, "*.png"))

    # Modify each PNG file and save it back to its original location
    for png_file in png_files:
        # Modify the image and overwrite the original file
        modify_image(png_file)
        print(f"Modified {png_file}")


def tweakimage():
    if os.name == "nt":
        clrprint(
            f"Enter the directory to the folder with PNG Files.\nExample: packs\\aesthetic\\AlternateCutCopper\\default\\textures\\blocks\\ \n{cdir()}\\",
            clr='b', end='')
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
    clrprint(f"Modified all PNG files in {directory}")
    clrinput("Press Enter to exit.", clr="green", end="")
    clear()


if __name__ == "__main__":
    tweakimage()
