import argparse
import os
import pyperclip
from file_extension_mappings import FILE_EXTENSION_MAPPINGS

IGNORED_DIRECTORIES = ['node_modules', '.git', '__pycache__']
IGNORED_FILES = ['.gitattributes', '.gitignore', 'LICENSE', 'README.md']

def display_files_in_directory(directory, depth=0, limit=500, depth_limit=None):
    output = ""

    # Stop if we've reached or exceeded the depth limit
    if depth_limit is not None and depth >= depth_limit:
        return ""

    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)

        # Skip ignored directories and files
        if item in IGNORED_DIRECTORIES or (os.path.isfile(item_path) and item in IGNORED_FILES):
            continue

        if os.path.isdir(item_path):
            output += "  " * depth + f"/{item}:\n"
            output += display_files_in_directory(item_path, depth+1, limit, depth_limit)
        else:
            with open(item_path, 'r') as file:
                content = file.read() if limit is None else file.read(limit + 1)
                truncated = False if limit is None else len(content) > limit
                content = content[:limit]
                
                file_output = "  " * depth + f"-- {item}:\n"
                if content:
                    language = FILE_EXTENSION_MAPPINGS.get(os.path.splitext(item)[1], '')
                    file_output += (
                        "```" + language + "\n" +
                        content +
                        ("...[more content...]" if truncated else "") + "\n" +
                        "```\n"
                    )
                else:
                    file_output += "[Empty File]\n"
                output += file_output

    return output

def main():
    parser = argparse.ArgumentParser(description="Display folder structure and file content.")
    parser.add_argument('path', help="Path to the directory you want to display.")
    parser.add_argument('-c', '--copy', action="store_true", help="Copy the output to the clipboard.")
    parser.add_argument('-m', '--limit', type=int, default=None, 
        help="Maximum number of characters to display from each file. No limit by default.")
    parser.add_argument('-d', '--depth', type=int, 
        help="Maximum depth to explore in the directory structure.")
    args = parser.parse_args()

    if os.path.exists(args.path):
        output = display_files_in_directory(args.path, limit=args.limit, depth_limit=args.depth)
        if args.copy:
            pyperclip.copy(output)
        else:
            print(output)
    else:
        print(f"Path '{args.path}' not found.")

if __name__ == "__main__":
    main()
