from PIL import Image, ImageFont, ImageDraw
import os
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

path_to_text = '../Text.txt'
with open(path_to_text, 'r') as file:
    lines = file.readlines()

images_folder_path = r'C:\Users\PhotoShop1\Pictures\Fannon, Mona (Edited)'
new_folder_path = images_folder_path + ' (With Text)'

open_sans_font_path = r'C:\Users\PhotoShop1\PycharmProjects\Fannon\Font\static\OpenSans-Regular.ttf'
font_size = 16  # You can adjust the size as needed

font = ImageFont.truetype(open_sans_font_path, font_size)

# Check access to all the paths from above
for path in [path_to_text, images_folder_path, open_sans_font_path]:
    if not os.path.exists(path):
        print('Path does not exist: ' + path)
        exit()
    else:
        print('Path exists: ' + path)


def add_text_to_image(image_path, line, font_path):
    # Create text centered on the image towards the bottom
    print('Attempting to open ' + image_path + ' and add text to it.')
    image = Image.open(image_path)
    print('Opened ' + image_path)
    width, height = image.size
    print('Attempting to open font ' + font_path + ' with size ' + str(font_size))
    print('Opened font ' + font_path)
    print('Attempting to draw text on image')
    try:
        draw = ImageDraw.Draw(image)
    except Exception as e:
        print('Error creating draw object image: ' + str(e))
        exit(1)
    print('Draw variable created')
    try:
        # TODO: Fix "Process finished with exit code -1073741819 (0xC0000005)"
        print('Attempting to calculate text width with font ' + str(font) + ' and line ' + line)
        bbox = font.getbbox(line)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    except Exception as e:
        print(f"Error calculating text width: {e}")
        exit(1)
    print('Text width and height calculated')
    text_x = (width - text_width) / 2
    print('Text x location calculated')
    text_y = height - text_height - 20
    print('Text y location calculated')
    position = (text_x, text_y)
    print('Position calculated')
    white = (255, 255, 255)
    print('Attempting to draw text on image with position ' + str(position) + ' and color ' + str(white))
    draw.text(position, line, (255, 255, 255), fill=white, font=font)
    print('Text drawn on image')
    # Do not overwrite the original image, save the new image with the text in a new folder
    if not os.path.exists(new_folder_path):
        print('Creating folder ' + new_folder_path + ' to store new images')
        os.makedirs(new_folder_path)
    new_image_path = new_folder_path + '\\' + os.path.basename(image_path)
    print('Attempting to save new image to ' + new_image_path)
    image.save(new_image_path)
    print('Text added to ' + new_image_path)
    # Properly close everything
    image.close()
    exit(0)


def edit_images(folder_path):
    folder_item_count = len(
        [name for name in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, name))])
    print('Folder contains ' + str(folder_item_count) + ' images')

    for i in range(lines.__len__()):
        # Skip the first 14, I already put the text on them
        if i < 14:
            continue
        # Get the line from Text.txt using i
        line = lines[i]
        # Remove the newline character using strip
        line = line.strip()
        print(line)
        image_names = os.listdir(folder_path)
        image_name = image_names[i]
        image_path = folder_path + '\\' + image_name
        # Add the text to the image from the list using the pillow library and the font
        add_text_to_image(image_path, line, open_sans_font_path)


if not os.path.exists(images_folder_path):
    print('Folder does not exist')
    exit()
else:
    print('Folder exists')
    edit_images(images_folder_path)
