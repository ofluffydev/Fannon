from tkinter import Tk, Label, Button, StringVar

from PIL import Image, ImageFont, ImageDraw


def get_choice(question, option_one='yes', option_two='no', option_three='cancel'):
    # Create a Tkinter window
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)

    # Set root title
    root.title("Image Text Utility")

    # Add label with the question
    label = Label(root, text=question)
    label.grid(row=0, column=0, columnspan=3)  # Place the label at the top

    # Variable to store the choice
    choice = StringVar()

    # Function to set the choice and close the window
    def set_choice(option):
        choice.set(option)
        root.destroy()

    # Add buttons for the options
    Button(root, text=option_one, command=lambda: set_choice(option_one)).grid(row=1, column=0)
    Button(root, text=option_two, command=lambda: set_choice(option_two)).grid(row=1, column=1)
    Button(root, text=option_three, command=lambda: set_choice(option_three)).grid(row=1, column=2)

    # Make root window 400x100
    root.geometry("400x100")

    root.deiconify()
    root.mainloop()

    return choice.get()


def add_text_to_image(image_path, text, font_path, font_size, position, font_color=(0, 0, 0)):
    # Open the image file
    with Image.open(image_path) as img:
        img = img.convert("RGB")
        draw = ImageDraw.Draw(img)

        # Load the font
        font = ImageFont.truetype(font_path, font_size)

        # Draw the text onto the image
        draw.text(position, text, font=font, fill=font_color)

        # Save the image with the text
        img.save("output.png")

        # Open the image
        img.show()

        # Ask if they would like to overwrite the original image with the new one in a tkinter window
        choice = get_choice("Would you like to overwrite the original image with the new one?")
        if choice == 'yes':
            img.save(image_path)
        elif choice == 'no':
            img.save("output.png")
        elif choice == 'cancel':
            pass
        else:
            raise ValueError("Invalid choice")


def get_center_position(file, font_path, font_size, text):
    with Image.open(file) as img:
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(font_path, font_size)
        image_width, image_height = img.size
        text_width = draw.textlength(text, font=font)

        position = ((image_width - text_width) / 2, image_height - font_size)
        # Raise the Y position by 10% of the font size
        position = (position[0], position[1] - font_size * 0.1)
    return position


def yes_no_cancel(question):
    choice = get_choice(question, 'yes', 'no', 'cancel')
    if choice == 'yes':
        return True
    elif choice == 'no':
        return False
    elif choice == 'cancel':
        raise ValueError("Operation cancelled")
    else:
        raise ValueError("Invalid choice")


def pick_color():
    # Choose black or white from tkinter window
    color = get_choice("Choose font color", 'black', 'white')
    if color == 'black':
        return 0, 0, 0
    elif color == 'white':
        return 255, 255, 255
    else:
        raise ValueError("Invalid color choice")
