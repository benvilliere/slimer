import argparse
import os

def display_files_in_directory(directory, depth=0):
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            print("  " * depth + f"/{item}:")
            display_files_in_directory(item_path, depth+1)
        else:
            with open(item_path, 'r') as file:
                content = file.read()
                print("  " * depth + f"-- {item}:")
                print("```" + os.path.splitext(item)[1].replace('.', ''))
                print(content)
                print("```")

def main():
    parser = argparse.ArgumentParser(description="Display folder structure and file content.")
    parser.add_argument('path', help="Path to the directory you want to display.")
    args = parser.parse_args()

    if os.path.exists(args.path):
        display_files_in_directory(args.path)
    else:
        print(f"Path '{args.path}' not found.")

if __name__ == "__main__":
    main()
