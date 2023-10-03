import argparse
import os
import pyperclip
from file_extension_mappings import FILE_EXTENSION_MAPPINGS

DEFAULT_IGNORED_DIRECTORIES = ['node_modules', '.git', '__pycache__']
DEFAULT_IGNORED_FILES = ['.gitattributes', '.gitignore', 'LICENSE', 'README.md']

def display_files_in_directory(directory, depth=0, limit=500, depth_limit=None, ignored_dirs=[], ignored_files=[]):
    output = ""

    # Stop if we've reached or exceeded the depth limit
    if depth_limit is not None and depth >= depth_limit:
        return ""

    for item in os.listdir(directory):
        item_path = os.path.abspath(os.path.join(directory, item))

        # Check if the directory or file should be ignored.
        if os.path.isdir(item_path) and item in ignored_dirs:
            continue
        elif os.path.isfile(item_path) and item_path in ignored_files:
            continue

        print(item_path)

        if os.path.isdir(item_path):
            output += "  " * depth + f"/{item}:\n"
            output += display_files_in_directory(item_path, depth+1, limit, depth_limit, ignored_dirs, ignored_files)
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
    parser.add_argument('--ignored-dirs', type=str, default="", 
        help="Comma separated list of directories to ignore.")
    parser.add_argument('--ignored-files', type=str, default="", 
        help="Comma separated list of files to ignore.")
    
    args = parser.parse_args()

    # Note: Make paths absolute right from the start.
    ignored_dirs = DEFAULT_IGNORED_DIRECTORIES + args.ignored_dirs.split(",") if args.ignored_dirs else DEFAULT_IGNORED_DIRECTORIES
    ignored_files = [os.path.abspath(os.path.join(os.getcwd(), f)) for f in (DEFAULT_IGNORED_FILES + args.ignored_files.split(","))] if args.ignored_files else [os.path.abspath(os.path.join(os.getcwd(), f)) for f in DEFAULT_IGNORED_FILES]

    if os.path.exists(args.path):
        output = display_files_in_directory(args.path, limit=args.limit, depth_limit=args.depth, ignored_dirs=ignored_dirs, ignored_files=ignored_files)
        if args.copy:
            pyperclip.copy(output)
        else:
            print(output)
    else:
        print(f"Path '{args.path}' not found.")

if __name__ == "__main__":
    main()
