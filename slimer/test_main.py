import os
import sys
import tempfile

from slimer.main import is_binary_file
from slimer.main import should_exclude
from slimer.main import read_file_content
from slimer.main import remove_comments
from slimer.main import generate_output_for_file
from slimer.main import display_files_in_directory

"""
  Testing is_binary_file
"""

def test_is_binary_file():
    assert is_binary_file("test.jpg") == True
    assert is_binary_file("test.txt") == False

"""
  Testing should_exclude
"""

def test_should_exclude_exact_match():
    patterns = {'temp', 'logs'}
    assert should_exclude('temp', patterns) == True
    assert should_exclude('logs', patterns) == True
    assert should_exclude('src', patterns) == False

def test_should_exclude_wildcard():
    patterns = {'*.log', '*.tmp'}
    assert should_exclude('error.log', patterns) == True
    assert should_exclude('temp.tmp', patterns) == True
    assert should_exclude('temp.txt', patterns) == False

def test_should_exclude_path():
    patterns = {'src/temp/*', 'logs/*'}
    assert should_exclude('src/temp/file.txt', patterns) == True
    assert should_exclude('logs/error.log', patterns) == True
    assert should_exclude('src/file.txt', patterns) == False

def test_should_exclude_no_patterns():
    patterns = set()
    assert should_exclude('src', patterns) == False
    assert should_exclude('error.log', patterns) == False

def test_should_exclude_case_insensitive():
    patterns = {'*.LOG'}
    assert should_exclude('ERROR.LOG', patterns) == True
    assert should_exclude('error.log', patterns) == True

def test_should_exclude_with_windows_paths():
    patterns = {'src\\temp\\*', 'logs\\*'}
    assert should_exclude('src\\temp\\file.txt', patterns) == True
    assert should_exclude('logs\\error.log', patterns) == True
    assert should_exclude('src\\file.txt', patterns) == False

"""
  Testing read_file_content
"""

CAN_DELETE_TEMP_FILES = sys.platform != 'win32'

def test_read_file_content_full():
    with tempfile.NamedTemporaryFile(delete=CAN_DELETE_TEMP_FILES) as temp_file:
        content = "This is a test content."
        temp_file.write(content.encode())
        temp_file.flush()

        read_content, truncated = read_file_content(temp_file.name)
        assert read_content == content
        assert not truncated

def test_read_file_content_partial():
    with tempfile.NamedTemporaryFile(delete=CAN_DELETE_TEMP_FILES) as temp_file:
        content = "This is a test content."
        temp_file.write(content.encode())
        temp_file.flush()

        limit = 5
        read_content, truncated = read_file_content(temp_file.name, limit=limit)
        assert read_content == content[:limit]
        assert truncated

def test_read_file_content_with_special_chars():
    with tempfile.NamedTemporaryFile(delete=CAN_DELETE_TEMP_FILES) as temp_file:
        content = "Test content with special chars: áéíóúñ."
        temp_file.write(content.encode())
        temp_file.flush()

        read_content, truncated = read_file_content(temp_file.name)
        assert read_content == content
        assert not truncated

def test_read_file_content_empty():
    with tempfile.NamedTemporaryFile(delete=CAN_DELETE_TEMP_FILES) as temp_file:
        temp_file.write(b"")
        temp_file.flush()

        read_content, truncated = read_file_content(temp_file.name)
        assert read_content == ""
        assert not truncated

"""
  Testing remove_comments
"""

def test_remove_comments_single_line_python():
    code = "# This is a comment\nprint('Hello World')\n# Another comment"
    expected = "\nprint('Hello World')\n"
    assert remove_comments(code, 'python') == expected

def test_remove_comments_multi_line_python():
    code = "'''\nMulti-line comment\nAnother line\n'''\nprint('Hello World')"
    expected = "\nprint('Hello World')"
    assert remove_comments(code, 'python') == expected

def test_remove_comments_single_line_javascript():
    code = "// This is a comment\nconsole.log('Hello World');\n// Another comment"
    expected = "\nconsole.log('Hello World');\n"
    assert remove_comments(code, 'javascript') == expected

def test_remove_comments_multi_line_javascript():
    code = "/*\nMulti-line comment\nAnother line\n*/\nconsole.log('Hello World');"
    expected = "\nconsole.log('Hello World');"
    assert remove_comments(code, 'javascript') == expected

def test_remove_comments_mixed_python():
    code = "# Single line comment\nprint('Hello')\n'''\nMulti-line comment\n'''\nprint('World')"
    expected = "\nprint('Hello')\n\nprint('World')"
    assert remove_comments(code, 'python') == expected

def test_remove_comments_mixed_javascript():
    code = "// Single line comment\nconsole.log('Hello');\n/*\nMulti-line comment\n*/\nconsole.log('World');"
    expected = "\nconsole.log('Hello');\n\nconsole.log('World');"
    assert remove_comments(code, 'javascript') == expected

def test_remove_comments_no_comments_python():
    code = "print('Hello World')"
    expected = "print('Hello World')"
    assert remove_comments(code, 'python') == expected

def test_remove_comments_no_comments_javascript():
    code = "console.log('Hello World');"
    expected = "console.log('Hello World');"
    assert remove_comments(code, 'javascript') == expected

"""
  Testing generate_output_for_file
"""

def create_temporary_file(content):
    fd, path = tempfile.mkstemp()
    with os.fdopen(fd, 'w') as tmp:
        tmp.write(content)
    return path

def test_generate_output_for_empty_file():
    temp_file_path = create_temporary_file("")
    output = generate_output_for_file("test.txt", temp_file_path, 0, None, False)
    assert output == "-- test.txt (empty file)\n"
    if CAN_DELETE_TEMP_FILES:
        os.remove(temp_file_path)

def test_generate_output_for_text_file():
    temp_file_path = create_temporary_file("Hello, World!")
    output = generate_output_for_file("test.txt", temp_file_path, 0, None, False)
    expected_output = (
        "-- test.txt                                \n"
        "```\n"
        "Hello, World!\n"
        "```\n"
    )
    print(repr(output))
    print(repr(expected_output))
    assert output == expected_output
    if CAN_DELETE_TEMP_FILES:
        os.remove(temp_file_path)

def test_generate_output_with_comment_stripping():
    temp_file_path = create_temporary_file("# This is a comment\nprint('Hello, World!')")
    output = generate_output_for_file("test.py", temp_file_path, 0, None, True)
    expected_output = (
        "-- test.py                                 \n"
        "```python\n\n"
        "print('Hello, World!')\n"
        "```\n"
    )
    assert output == expected_output
    if CAN_DELETE_TEMP_FILES:
        os.remove(temp_file_path)

def test_generate_output_for_binary_file():
    binary_content = bytes([0xDE, 0xAD, 0xBE, 0xEF])
    fd, temp_file_path = tempfile.mkstemp(suffix=".bin")
    with os.fdopen(fd, 'wb') as tmp:
        tmp.write(binary_content)
    output = generate_output_for_file("test.bin", temp_file_path, 0, None, False)
    assert output == "-- test.bin (binary file)\n"
    if CAN_DELETE_TEMP_FILES:
        os.remove(temp_file_path)

"""
  Testing display_files_in_directory
"""

def test_display_files_in_basic_directory():
    with tempfile.TemporaryDirectory() as tempdir:
        with open(os.path.join(tempdir, 'file1.txt'), 'w') as f:
            f.write('Hello World!')

        output = display_files_in_directory(tempdir)
        assert "-- file1.txt" in output

def test_display_files_with_exclusion():
    with tempfile.TemporaryDirectory() as tempdir:
        with open(os.path.join(tempdir, 'file1.txt'), 'w') as f:
            f.write('Hello World!')

        with open(os.path.join(tempdir, 'file2.log'), 'w') as f:
            f.write('Logging...')

        output = display_files_in_directory(tempdir, exclusion_patterns=['*.log'])
        assert "-- file1.txt" in output
        assert "-- file2.log" not in output

def test_display_files_with_depth_limit():
    with tempfile.TemporaryDirectory() as tempdir:
        subdir = os.path.join(tempdir, 'subdir')
        os.mkdir(subdir)
        with open(os.path.join(subdir, 'file1.txt'), 'w') as f:
            f.write('Hello Subdir!')

        output = display_files_in_directory(tempdir, depth_limit=1)
        assert "/subdir:" in output
        assert "-- file1.txt" not in output

def test_display_files_with_content_limit():
    with tempfile.TemporaryDirectory() as tempdir:
        with open(os.path.join(tempdir, 'file1.txt'), 'w') as f:
            f.write('Hello World!')

        output = display_files_in_directory(tempdir, limit=5)
        assert "...[more content...]" in output

def test_display_files_skip_binary():
    with tempfile.TemporaryDirectory() as tempdir:
        with open(os.path.join(tempdir, 'image.jpg'), 'wb') as f:
            f.write(b'\xFF\xD8\xFF\xE0')

        output = display_files_in_directory(tempdir, include_binary=False)
        assert "(binary file)" not in output
        
        output = display_files_in_directory(tempdir, include_binary=True)
        assert "(binary file)" in output

def test_display_files_recent_limit():
    with tempfile.TemporaryDirectory() as tempdir:
        with open(os.path.join(tempdir, 'file1.txt'), 'w') as f:
            f.write('Hello World!')

        output = display_files_in_directory(tempdir, recent_minutes=0)
        assert "-- file1.txt" in output

def test_display_files_specific_extension():
    with tempfile.TemporaryDirectory() as tempdir:
        with open(os.path.join(tempdir, 'script.py'), 'w') as f:
            f.write('print("Hello Python!")')
        with open(os.path.join(tempdir, 'note.txt'), 'w') as f:
            f.write('Just a note.')

        output = display_files_in_directory(tempdir, file_extensions=['.py'])
        assert "-- script.py" in output
        assert "-- note.txt" not in output

def test_display_files_strip_comments():
    with tempfile.TemporaryDirectory() as tempdir:
        with open(os.path.join(tempdir, 'script.py'), 'w') as f:
            f.write('# This is a comment\nprint("Hello Python!")')

        output = display_files_in_directory(tempdir, strip_comments=True)
        assert '# This is a comment' not in output
        assert 'print("Hello Python!")' in output
