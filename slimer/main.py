"""
Slimer: Directory and File Content Visualisation Tool

This script provides a tool to visualize the directory structure along with the content
of the files within the specified directory. Users can utilize various command-line arguments
to customize the output. Some of the primary functionalities include:

- Display directory structures in a tree-like format.
- Show the content of files in the structure with an optional character limit.
- Exclude or forcefully include specific files or directories.
- Recognize and tag binary files, with an option to include/exclude them.
- Limit the depth of directory exploration.
- Copy the result to the clipboard or output to a file.
- Filter the displayed files based on their modification time.
- Include specific files based on their extension.

Usage:
    Run the script with python and provide the necessary arguments. 
    Use the `-h` or `--help` option for more details on available command-line arguments.

Dependencies:
    - pyperclip: Used for copying output to clipboard.

Example:
    $ python main.py /path/to/directory -c -m 500 -e __pycache__ temp

Author:
    Ben Villiere

Date:
    03/10/2023
"""

import argparse
import fnmatch
import os
import pyperclip
import re
import time

from slimer.constants import EXCLUDED_DIRECTORIES, EXCLUDED_FILES, BINARY_FILE_EXTENSIONS, FILE_EXTENSION_MAPPINGS, SINGLE_LINE_COMMENT_PATTERNS, MULTI_LINE_COMMENT_PATTERNS
from slimer.__version__ import __version__

def is_binary_file(filename):
    """Check if the provided filename has a binary extension."""
    _, ext = os.path.splitext(filename)
    return ext in BINARY_FILE_EXTENSIONS

def should_exclude(item, exclusion_patterns):
    """
    Determines if an item should be excluded based on some conditions.

    Parameters:
    - item (str): The path or item to check.
    - exclusion_patterns (set, optional): Set of patterns used to exclude filenames or directory names.

    Returns:
    - bool: True if the item should be excluded, False otherwise.
    """
    unix_path = item.replace(os.sep, '/')
    return any(fnmatch.fnmatch(unix_path, pattern) for pattern in exclusion_patterns)

def read_file_content(item_path, limit=None, chunk_size=4096):
    """
    Read the content of a file up to a given limit using chunks.
    
    Args:
    - item_path (str): Path to the file.
    - limit (int, optional): Maximum number of characters to read. Reads the entire file if not provided.
    - chunk_size (int, optional): Size of each chunk to be read from the file.
    
    Returns:
    - tuple: The content of the file and a flag indicating if the content was truncated.
    """
    content = []
    truncated = False

    with open(item_path, 'r', encoding='utf-8', errors='replace') as file:
        bytes_read = 0
        while not limit or bytes_read < limit:
            if limit:
                chunk = file.read(min(chunk_size, limit - bytes_read))
            else:
                chunk = file.read(chunk_size)

            if not chunk:
                break

            content.append(chunk)
            bytes_read += len(chunk.encode('utf-8'))  # considering bytes and not just characters

        truncated = bool(limit) and file.read(1)  # Check if there is more content left

    return ''.join(content), truncated

def remove_comments(code, language):
    """
    Removes single and multi-line comments from the provided code for the specified language.
    
    Args:
    - code (str): The source code from which comments need to be removed.
    - language (str): The programming language of the source code. It determines which comment 
                      patterns to use for removal.
                      
    Returns:
    - str: Source code with comments removed.
    
    Note:
    The function currently supports comment patterns for languages like Python, JavaScript, 
    TypeScript, Java, C, C++, and others. If a language is not supported, the original code 
    will be returned without any modifications.
    """
    single_line_pattern = SINGLE_LINE_COMMENT_PATTERNS.get(language, '')
    multi_line_pattern = MULTI_LINE_COMMENT_PATTERNS.get(language, '')
    
    code = re.sub(single_line_pattern, '', code)
    code = re.sub(multi_line_pattern, '', code, flags=re.DOTALL)
    
    return code

def generate_output_for_file(item, item_path, depth, limit, strip_comments):
    """
    Generate the formatted output string for a given file.

    Args:
    - item (str): Name of the file.
    - item_path (str): Absolute path of the file.
    - depth (int): Depth of the file in the directory structure.
    - limit (int, optional): Maximum characters to display from the file.
    - strip_comments (bool): Wether to strip comments from file contents.

    Returns:
    - str: Formatted output string for the file.
    """
    # Use f-string alignment to ensure uniform width for file names
    spacer = f"{'  ' * depth}-- {item:<40}"

    if is_binary_file(item):
        return f"{'  ' * depth}-- {item} (binary file)\n"
    
    content, truncated = read_file_content(item_path, limit)

    # Getting programming language from file extension
    language = FILE_EXTENSION_MAPPINGS.get(os.path.splitext(item)[1], '')
    
    if strip_comments:
        content = remove_comments(content, language)

    if not content.strip():
        return f"{'  ' * depth}-- {item} (empty file)\n"
    
    return (
        f"{spacer}\n"
        f"```{language}\n"
        f"{content}"
        f"{'...[more content...]' if truncated else ''}\n"
        f"```\n"
    )

def display_files_in_directory(directory, depth=0, limit=None, depth_limit=None, 
                               exclusion_patterns=None, tree_only=False, 
                               include_binary=False, recent_minutes=None,
                               file_extensions=None, strip_comments=False):
    """
    Display the directory structure and file content recursively.

    Args:
    - directory (str): Path to the directory to display.
    - depth (int, optional): Current depth of recursion. Defaults to 0.
    - limit (int, optional): Maximum characters to display from each file.
    - depth_limit (int, optional): Maximum depth to explore in the directory structure.
    - exclusion_patterns (set, optional): Patterns used to exclude filenames or directory names.
    - tree_only (bool, optional): If True, only the directory structure is displayed.
    - include_binary (bool, optional): If True, binary files are included with a flag.
    - recent_minutes (int, optional): Only display files modified within the last N minutes.
    - file_extensions (list, optional): List of file extensions to exclusively display.
    - strip_comments (bool, optional): Wether to strip comments from file contents.

    Returns:
    - str: Formatted string of the directory structure and file content.
    """
    if exclusion_patterns is None:
        exclusion_patterns = []

    if depth_limit is not None and depth >= depth_limit:
        return ""

    output = ""

    for item in os.listdir(directory):
        if should_exclude(item, exclusion_patterns):
            continue

        item_path = os.path.join(directory, item)

        # If the recent_minutes argument is used, check the file modification time.
        if recent_minutes is not None:
            file_mod_time = os.path.getmtime(item_path)
            current_time = time.time()
            seconds_in_a_minute = 60
            if current_time - file_mod_time > recent_minutes * seconds_in_a_minute:
                continue  # Skip this file if it wasn't modified within the recent_minutes timeframe
        
        if os.path.isdir(item_path):
            output += f"{'  ' * depth}/{item}:\n"
            output += display_files_in_directory(
                item_path, depth + 1, limit, depth_limit, 
                exclusion_patterns, tree_only, include_binary, 
                recent_minutes, file_extensions, strip_comments)
        elif tree_only:
            output += f"{'  ' * depth}-- {item:<40}\n" 
        else:
            if file_extensions and os.path.splitext(file)[1] not in file_extensions:
                continue
            if not include_binary and is_binary_file(item):
                continue
            output += generate_output_for_file(item, item_path, depth, limit, strip_comments)

    return output


def get_exclusion_patterns(args):
    """
    Get the set of items to be excluded based on provided arguments and constants.

    Args:
    - args (Namespace): Parsed arguments from argparse.

    Returns:
    - set: Set of patterns to use for excluding itemss.
    """
    exclusions = set(EXCLUDED_FILES + EXCLUDED_DIRECTORIES + args.exclude)
    inclusions = set(args.include)
    return exclusions - inclusions

def parse_arguments():
    """
    Parse command line arguments using argparse.

    Returns:
    - Namespace: Namespace object containing parsed arguments.
    """
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
    parser.add_argument('-o', '--output', type=str, default=None, 
        help="Path to a file where the output will be written. If not provided, prints to console.")
    parser.add_argument('-r', '--recent', type=int, default=None, 
        help="Only display files modified within the last N minutes. Defaults to 10 minutes when no value is provided to the argument.")
    parser.add_argument('-f', '--file-extensions', nargs='*', default=[], 
        help="List of file extensions to exclusively display (e.g. .py .ts).")
    parser.add_argument('-v', '--version', action='version', version=f"Slimer v{__version__}")
    parser.add_argument('-s', '--strip-comments', action="store_true", 
        help="Strip comments from the code in the output.")
    
    return parser.parse_args()

def get_directory_output(args, absolute_path):
    """
    Get the formatted directory structure and content based on provided arguments.

    Args:
    - args (Namespace): Parsed arguments from argparse.
    - absolute_path (str): Absolute path of the directory to display.

    Returns:
    - str: Formatted string of the directory structure and content.
    """
    exclusion_patterns = get_exclusion_patterns(args)

    output_parts = []

    if args.prepend:
        output_parts.append(args.prepend)

    output_parts.append(display_files_in_directory(
        absolute_path, 
        limit=args.limit, 
        depth_limit=args.depth, 
        exclusion_patterns=exclusion_patterns, 
        tree_only=args.tree,
        include_binary=args.binary,  
        recent_minutes=args.recent,
        file_extensions=args.file_extensions,
        strip_comments=args.strip_comments
    ))

    if args.append:
        output_parts.append(args.append)

    return '\n'.join(output_parts)

def handle_arguments():
    """
    Handles command line arguments.

    Returns:
    - Namespace: Namespace object containing parsed arguments.
    """
    args = parse_arguments()
    absolute_path = os.path.abspath(args.path)

    if not os.path.exists(absolute_path):
        print(f"Path '{args.path}' not found.")
        exit(1)

    return args, absolute_path

def process_directory(args, absolute_path):
    """
    Processes the directory based on provided arguments.

    Args:
    - args (Namespace): Parsed arguments from argparse.
    - absolute_path (str): Absolute path of the directory to display.

    Returns:
    - str: Formatted string of the directory structure and content.
    """
    return get_directory_output(args, absolute_path)

def handle_output(output, copy_to_clipboard, output_file=None):
    """
    Handles the output, either by printing it, copying it to clipboard, or writing to an output file.

    Args:
    - output (str): The string to be output.
    - copy_to_clipboard (bool): Whether to copy the output to clipboard.
    - output_file (str): Path to the file where the output will be written.
    """
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(output)
    elif copy_to_clipboard:
        pyperclip.copy(output)
    else:
        print(output)

def main():
    """
    Main function to execute the program. 
    """
    try:
        args, absolute_path = handle_arguments()
        output = process_directory(args, absolute_path)
        handle_output(output, args.copy, args.output)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()