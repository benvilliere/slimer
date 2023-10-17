# Slimer

<p align="center">
  <img src="https://github.com/benvilliere/slimer/blob/main/slimer.svg?raw=true" width="320" title="Slimer" alt="Slimer" />
</p>

## Directory and File Content Visualisation CLI Tool

Slimer is a command line tool that helps you digest a folder structure and its file contents. It was designed to help with prompt engineering.

## Features

- Display directory structures in a tree-like format.
- Show the content of files in the structure with an optional character limit.
- Exclude or forcefully include specific files or directories.
- Recognize and tag binary files, with an option to include/exclude them.
- Limit the depth of directory exploration.
- Copy the result to the clipboard or output to a file.
- Filter the displayed files based on their modification time.
- Include specific files based on their extension.

## Installation

- Ensure you have Python installed.
- Install necessary dependencies:

```bash
pip install slimer
```

## Dependencies

- `pyperclip`: Used for copying output to clipboard.

## Usage

To use Slimer, execute the `slimer` command and provide the necessary arguments:

```bash
slimer /path/to/directory -c -l 500 -e __pycache__ temp
```

| Argument                                                            | Description                                                                                                              |
| ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| `-h, --help`                                                        | show this help message and exit                                                                                          |
| `-c, --copy`                                                        | Copy the output to the clipboard.                                                                                        |
| `-l LIMIT, --limit LIMIT`                                           | Maximum number of characters to display from each file. No limit by default.                                             |
| `-d DEPTH, --depth DEPTH`                                           | Maximum depth to explore in the directory structure.                                                                     |
| `-e [EXCLUDE ...], --exclude [EXCLUDE ...]`                         | List of files or directories to exclude.                                                                                 |
| `-i [INCLUDE ...], --include [INCLUDE ...]`                         | List of files or directories to forcefully include even if they are in the exclude list.                                 |
| `-b, --binary`                                                      | Include binary files with a [Binary File] flag.                                                                          |
| `-t, --tree`                                                        | Only display the folder structure without file content.                                                                  |
| `-p PREPEND, --prepend PREPEND`                                     | String to prepend at the beginning of the output.                                                                        |
| `-a APPEND, --append APPEND`                                        | String to append at the end of the output.                                                                               |
| `-o OUTPUT, --output OUTPUT`                                        | Path to a file where the output will be written. If not provided, prints to console.                                     |
| `-r RECENT, --recent RECENT`                                        | Only display files modified within the last N minutes. Defaults to 10 minutes when no value is provided to the argument. |
| `-f [FILE_EXTENSIONS ...], --file-extensions [FILE_EXTENSIONS ...]` | List of file extensions to exclusively display (e.g. .py .ts).                                                           |
| `-v, --version`                                                     | show program's version number and exit                                                                                   |
| `-s, --strip-comments`                                              | Strip comments from the code in the output.                                                                              |

## Author

Ben Villiere

## Contributing

If you'd like to contribute to the development of Slimer, please create an issue or pull request in the project repository.

## License

This project is licensed under the MIT License.
