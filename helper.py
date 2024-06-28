from tkinter import Tk, Label, Button, StringVar, Entry, filedialog, Frame

from PIL import Image, ImageFont, ImageDraw


def submit(text_var, text_field, root):
    # Get the text from the text field
    text_var.set(text_field.get())
    # Close the window
    root.destroy()


def get_choice(question, option_one='yes', option_two='no', option_three='cancel') -> str:
    """
    Ask the user a question with three options and return the option they choose
    :param question: Question to ask the user
    :param option_one: First option
    :param option_two: Second option
    :param option_three: Third option
    :return: Choice the user made
    """
    # Create a Tkinter window
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)

    # Set root title
    root.title("Image Text Utility")

    # Create a frame to hold the widgets
    frame = Frame(root)
    frame.pack()

    # Add label with the question
    label = Label(frame, text=question)
    label.pack()

    # Variable to store the choice
    choice = StringVar()

    # Function to set the choice and close the window
    def set_choice(option):
        choice.set(option)
        root.destroy()

    # Add buttons for the options
    Button(frame, text=option_one, command=lambda: set_choice(option_one)).pack(side='left')
    Button(frame, text=option_two, command=lambda: set_choice(option_two)).pack(side='left')
    Button(frame, text=option_three, command=lambda: set_choice(option_three)).pack(side='left')

    # Make root window 400x100
    root.geometry("400x100")

    root.deiconify()
    root.mainloop()

    return choice.get()


def add_text_to_image(image_path, text, font_path, font_size, position, font_color=(0, 0, 0)):
    """
    Add text to an image
    :param image_path: Path to the image you want to add text to
    :param text: What text you want to add to the image
    :param font_path: Path to the font you want to use to add the text
    :param font_size: Size for the font
    :param position: Position to place the text
    :param font_color: Color of the text
    """
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


def get_center_position(file, font_path, font_size, text, top=False):
    """
    Get the position to center the text on the image
    :param file: File path of the image
    :param font_path: Path to the font you want to use
    :param font_size: Size of the font
    :param text: The text you want to center
    :param top: Whether to center the text at the top of the image or not
    :return: The resulting position to center the text
    """
    with Image.open(file) as img:
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(font_path, font_size)
        image_width, image_height = img.size
        text_width = draw.textlength(text, font=font)

        if top:
            position = ((image_width - text_width) / 2, 0)
            position = (position[0], position[1] + font_size * 0.1)
        else:
            position = ((image_width - text_width) / 2, image_height - font_size)
            position = (position[0], position[1] - font_size * 0.1)

    return position


def yes_no_cancel(question):
    """
    Wrapper around get_choice that asks a question with the options "yes", "no", and "cancel"
    :param question: The question to ask in the tkinter window
    :return: True if the user selects "yes", False if the user selects "no",
    and raises a ValueError if the user selects "cancel"
    """
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
    """
    Ask the user to pick a color for the font (Black or White)
    :return: Tuple of RGB values
    """
    color = get_choice("Choose font color", 'black', 'white')
    if color == 'black':
        return 0, 0, 0
    elif color == 'white':
        return 255, 255, 255
    else:
        raise ValueError("Invalid color choice")


def select_file():
    root = Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename()  # Open the file selector dialog
    # Close the root window
    root.destroy()
    return file_path


def get_text(file_to_preview):
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)

    # Set root title
    root.title("Image Text Utility")

    # Remove default window icon
    root.iconbitmap(default='')

    # Set root size
    root.geometry("400x100")

    # Create a label that says "Enter text:"
    label = Label(root, text="Enter text:")
    label.pack()

    # Create a text field
    text_var = StringVar()
    text_field = Entry(root, textvariable=text_var)
    # Set size of the text field
    text_field.config(width=200)
    text_field.pack()

    # Create a submit button and bind the submit function to it
    submit_button = Button(root, text="Submit", command=lambda: submit(text_var, text_field, root))
    submit_button.pack()

    # Also submit on Enter key press
    root.bind("<Return>", lambda event: submit(text_var, text_field, root))

    # Exit program on close button press
    root.protocol("WM_DELETE_WINDOW", lambda: exit(1))

    root.deiconify()

    # Ensure path is not a directory
    if not file_to_preview:
        print("No file selected")
        exit(1)

    # Open image to preview it with pillow show()
    with Image.open(file_to_preview) as img:
        img.show()

    root.mainloop()

    # Close the image preview
    img.close()

    # Return the text after the Tkinter main loop ends
    return text_var.get()


if __name__ == '__main__':
    print("This file is a helper file and should not be run directly. Run main.py instead.")
