import argparse
import os
import pyperclip
import constants

def is_binary_file(filename):
    _, ext = os.path.splitext(filename)
    return ext in constants.BINARY_FILE_EXTENSIONS

def read_file_content(item_path, limit=None):
    with open(item_path, 'r') as file:
        content = []
        while (line := file.readline()) and (not limit or file.tell() <= limit):
            content.append(line)
        truncated = bool(limit) and file.tell() > limit
        return ''.join(content), truncated

def generate_output_for_file(item, item_path, depth, limit):
    if is_binary_file(item):
        return f"{'  ' * depth}-- {item}:\n[Binary File]\n"
    
    try:
        content, truncated = read_file_content(item_path, limit)
        language = constants.FILE_EXTENSION_MAPPINGS.get(os.path.splitext(item)[1], '')
        return (
            f"{'  ' * depth}-- {item}:\n"
            f"```{language}\n"
            f"{content}"
            f"{'...[more content...]' if truncated else ''}\n"
            f"```\n"
        )
    except UnicodeDecodeError:
        return f"{'  ' * depth}-- {item}:\n[Binary File]\n"

def display_files_in_directory(directory, depth=0, limit=None, depth_limit=None, excluded_items=[], tree_only=False):
    if depth_limit is not None and depth >= depth_limit:
        return ""

    output = ""
    for item in os.listdir(directory):
        if item in excluded_items:
            continue

        item_path = os.path.abspath(os.path.join(directory, item))

        if os.path.isdir(item_path):
            output += f"{'  ' * depth}/{item}:\n"
            output += display_files_in_directory(item_path, depth + 1, limit, depth_limit, excluded_items, tree_only)
        elif tree_only:
            output += f"{'  ' * depth}-- {item}\n"
        else:
            output += generate_output_for_file(item, item_path, depth, limit)

    return output

def get_excluded_items(args):
    excluded = set(constants.EXCLUDED_FILES + constants.EXCLUDED_DIRECTORIES + args.exclude)
    if args.include:
        included = set(args.include)
        excluded -= included
    return excluded

def parse_arguments():
    parser = argparse.ArgumentParser(description="Display folder structure and file content.")
    parser.add_argument('path', help="Path to the directory you want to display.")
    parser.add_argument('-c', '--copy', action="store_true", help="Copy the output to the clipboard.")
    parser.add_argument('-m', '--limit', type=int, default=None, 
        help="Maximum number of characters to display from each file. No limit by default.")
    parser.add_argument('-d', '--depth', type=int, 
        help="Maximum depth to explore in the directory structure.")
    parser.add_argument('-e', '--exclude', nargs='*', default=[], 
        help="List of files or directories to exclude.")
    parser.add_argument('-i', '--include', nargs='*', default=[], 
        help="List of files or directories to forcefully include even if they are in the exclude list.")
    parser.add_argument('-b', '--binary', action="store_true", 
        help="Include binary files with a [Binary File] flag.")
    parser.add_argument('-t', '--tree', action="store_true", help="Only display the folder structure without file content.")
    parser.add_argument('-p', '--prepend', type=str, default="", help="String to prepend at the beginning of the output.")
    parser.add_argument('-a', '--append', type=str, default="", help="String to append at the end of the output.")
    return parser.parse_args()

def main():
    args = parse_arguments()
    excluded_items = get_excluded_items(args)
    absolute_path = os.path.abspath(args.path)

    if not os.path.exists(absolute_path):
        print(f"Path '{args.path}' not found.")
        return

    # Using binary argument to decide whether to include binary files or not.
    if not args.binary:
        excluded_items.update([item for item in os.listdir(absolute_path) if is_binary_file(item)])

    output_parts = []

    if args.prepend:
        output_parts.append(args.prepend)

    output_parts.append(display_files_in_directory(absolute_path, limit=args.limit, depth_limit=args.depth, excluded_items=excluded_items, tree_only=args.tree))

    if args.append:
        output_parts.append(args.append)

    output = '\n'.join(output_parts)

    if args.copy:
        pyperclip.copy(output)
    else:
        print(output)


if __name__ == "__main__":
    main()
