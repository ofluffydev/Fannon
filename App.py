from tkinter import Tk, filedialog, Entry, Button, StringVar, Label

from PIL import Image, ImageFont, ImageDraw

from helper import add_text_to_image, get_center_position, yes_no_cancel, pick_color


def select_file():
    root = Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename()  # Open the file selector dialog
    # Close the root window
    root.destroy()
    return file_path


def submit(text_var, text_field, root):
    # Get the text from the text field
    text_var.set(text_field.get())
    # Close the window
    root.destroy()


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


def main():
    keep_running = True

    while keep_running:
        file = select_file()
        print(f"Selected file: {file}")
        text = get_text(file)
        print(f"Entered text: {text}")
        font_color = pick_color()

        font_path = "Font/static/OpenSans-Regular.ttf"
        font_size = 40
        raise_factor = 0.2
        # Center aligned at the bottom of the image
        position = get_center_position(file, font_path, font_size, text)

        # Raise a little so it's not touching the bottom
        position = (position[0], position[1] - font_size * raise_factor)

        add_text_to_image(file, text, font_path, font_size, position, font_color)

        keep_running = yes_no_cancel("Would you like to add text to another image?")


if __name__ == '__main__':
    main()
