# Print every line in Text.txt

if __name__ == '__main__':
    path_to_text = 'Text.txt'

    with open(path_to_text, 'r') as file:
        lines = file.readlines()
        for line in lines:
            # Remove the newline character
            line = line.rstrip()
            print(line)
