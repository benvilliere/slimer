# shufti

CLI utility to quickly show and share your folder structure and code.

## Roadmap

### 1. Configurable Ignored Items

- **Description**: Allow users to provide additional directories or files they'd like to ignore through the CLI.
- **Implementation**: Extend the CLI argument system to accept lists or comma-separated items for ignored directories and files.

### 2. Encoding Handling

- **Description**: Handle potential encoding issues when reading files.
- **Implementation**: Implement error handling for different encodings and provide a CLI option for users to specify file encoding.

### 3. Recursive Limit

- **Description**: Limit the number of recursive calls or the number of files/folders processed.
- **Implementation**: Introduce counters and CLI arguments to set the maximum recursion level or processed items count.

### 4. Progress Indication

- **Description**: Provide feedback for processing large directories.
- **Implementation**: Integrate a progress bar or logging mechanism to show current processing status.

### 5. Different Output Formats

- **Description**: Allow output in formats other than Markdown.
- **Implementation**: Integrate format converters and allow users to select the desired output format via the CLI.

### 6. Enhanced File Truncation

- **Description**: Improve truncation to avoid cutting off content abruptly.
- **Implementation**: Revise the truncation logic to consider word or line boundaries.

### 7. Interactive Mode

- **Description**: Allow users to explore directories interactively.
- **Implementation**: Develop an interactive CLI interface using libraries like `prompt_toolkit` or `PyInquirer`.

### 8. Highlighting Changes

- **Description**: Highlight recent changes or diffs in the codebase.
- **Implementation**: Integrate with git or use diff tools to display changes since the last run or a specific commit.

### 9. Handle Binary Files

- **Description**: Gracefully handle binary files.
- **Implementation**: Check for binary files using file magic numbers and provide appropriate output or ignore them.

### 10. Error Handling and Logging

- **Description**: Improve resilience and feedback.
- **Implementation**: Implement try-except blocks at critical points and provide detailed error logs.

### 11. Performance

- **Description**: Optimize for directories with large numbers of files.
- **Implementation**: Profile the tool, identify bottlenecks, and implement necessary optimizations.

### 12. Customizable Display

- **Description**: Allow users to change the look of the output.
- **Implementation**: Introduce template systems or configuration files where users can define display preferences.
