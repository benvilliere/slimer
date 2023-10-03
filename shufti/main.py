import argparse
import os
import pyperclip
from file_extension_mappings import FILE_EXTENSION_MAPPINGS

DEFAULT_EXCLUDED_DIRECTORIES = ['node_modules', '.git', '__pycache__']
DEFAULT_EXCLUDED_FILES = ['.gitattributes', '.gitignore', 'LICENSE', 'README.md']

def display_files_in_directory(directory, depth=0, limit=500, depth_limit=None, excluded_items=[]):
    output = ""

    if depth_limit is not None and depth >= depth_limit:
        return ""

    for item in os.listdir(directory):
        if item in excluded_items:
            continue

        item_path = os.path.abspath(os.path.join(directory, item))

        if os.path.isdir(item_path):
            output += "  " * depth + f"/{item}:\n"
            output += display_files_in_directory(item_path, depth+1, limit, depth_limit, excluded_items)
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
    parser.add_argument('-e', '--exclude', type=str, default="", 
        help="Comma separated list of files or directories to exclude.")
    parser.add_argument('-i', '--include', type=str, default="", 
        help="Comma separated list of files or directories to forcefully include even if they are in the exclude list.")
    
    args = parser.parse_args()

    # Combine default excluded items and user-provided excluded items
    excluded_items = DEFAULT_EXCLUDED_FILES + DEFAULT_EXCLUDED_DIRECTORIES
    if args.exclude:
        excluded_items += args.exclude.split(",")
    if args.include:
        included_items = args.include.split(",")
        excluded_items = [item for item in excluded_items if item not in included_items]

    absolute_path = os.path.abspath(args.path)

    if os.path.exists(absolute_path):
        output = display_files_in_directory(absolute_path, limit=args.limit, depth_limit=args.depth, excluded_items=excluded_items)
        if args.copy:
            pyperclip.copy(output)
        else:
            print(output)
    else:
        print(f"Path '{args.path}' not found.")

if __name__ == "__main__":
    main()
