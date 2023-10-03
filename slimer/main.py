import argparse
import os
import pyperclip
import constants

def is_binary_file(filename):
    return os.path.splitext(filename)[1] in constants.BINARY_FILE_EXTENSIONS

def display_files_in_directory(directory, depth=0, limit=500, depth_limit=None, excluded_items=[], included_items=[], include_binary=False, tree_only=False):
    output = ""
    
    if depth_limit is not None and depth >= depth_limit:
        return ""

    for item in os.listdir(directory):
        if item in excluded_items and item not in included_items:
            continue

        item_path = os.path.abspath(os.path.join(directory, item))

        if os.path.isdir(item_path):
            output += "  " * depth + f"/{item}:\n"
            output += display_files_in_directory(item_path, depth+1, limit, depth_limit, excluded_items, included_items, include_binary, tree_only)
        else:
            if tree_only:
                output += "  " * depth + f"-- {item}\n"
            else:
                if is_binary_file(item):
                    if include_binary:
                        file_output = "  " * depth + f"-- {item}:\n"
                        file_output += "[Binary File]\n"
                    else:
                        continue
                else:
                    with open(item_path, 'r') as file:
                        try:
                            content = file.read(limit + 1) if limit else file.read()
                            truncated = bool(limit) and len(content) > limit
                            content = content[:limit]

                            file_output = "  " * depth + f"-- {item}:\n"
                            if content:
                                language = constants.FILE_EXTENSION_MAPPINGS.get(os.path.splitext(item)[1], '')
                                file_output += (
                                    "```" + language + "\n" +
                                    content +
                                    ("...[more content...]" if truncated else "") + "\n" +
                                    "```\n"
                                )
                            else:
                                file_output += "[Empty File]\n"
                        except UnicodeDecodeError:
                            file_output = "  " * depth + f"-- {item}:\n"
                            file_output += "[Binary File]\n"
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
    parser.add_argument('-b', '--binary', action="store_true", 
        help="Include binary files with a [Binary File] flag.")
    parser.add_argument('-t', '--tree', action="store_true", help="Only display the folder structure without file content.")
    parser.add_argument('-p', '--prepend', type=str, default="", help="String to prepend at the beginning of the output.")
    parser.add_argument('-a', '--append', type=str, default="", help="String to append at the end of the output.")

    args = parser.parse_args()

    excluded_items = constants.EXCLUDED_FILES + constants.EXCLUDED_DIRECTORIES
    if args.exclude:
        excluded_items += args.exclude.split(",")
    if args.include:
        included_items = args.include.split(",")
        excluded_items = [item for item in excluded_items if item not in included_items]
    if not args.binary:
        excluded_items += [f for f in constants.BINARY_FILE_EXTENSIONS]

    absolute_path = os.path.abspath(args.path)

    if os.path.exists(absolute_path):
        output = args.prepend + "\n"
        output += display_files_in_directory(absolute_path, limit=args.limit, depth_limit=args.depth, excluded_items=excluded_items, include_binary=args.binary, tree_only=args.tree)
        output += "\n" + args.append
        
        if args.copy:
            pyperclip.copy(output)
        else:
            print(output)
    else:
        print(f"Path '{args.path}' not found.")

if __name__ == "__main__":
    main()
