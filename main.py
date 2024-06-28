from helper import add_text_to_image, get_center_position, yes_no_cancel, pick_color, get_choice, get_text, select_file


def main():
    """
    Main function to run the program
    :return: None
    """
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
        # Center aligned at the bottom or top based on choice
        position_choice = get_choice("Where would you like the text to be placed?", "bottom", "top")

        if position_choice == "bottom":
            position = get_center_position(file, font_path, font_size, text)
        else:
            position = get_center_position(file, font_path, font_size, text, top=True)

        # Raise a little so it's not touching the bottom
        position = (position[0], position[1] - font_size * raise_factor)

        add_text_to_image(file, text, font_path, font_size, position, font_color)

        keep_running = yes_no_cancel("Would you like to add text to another image?")


if __name__ == '__main__':
    main()
