import argparse
import os
import pytest
import sys
import tempfile
from unittest.mock import patch, mock_open, Mock

from slimer.main import is_binary_file
from slimer.main import should_exclude
from slimer.main import read_file_content
from slimer.main import remove_comments
from slimer.main import generate_output_for_file
from slimer.main import display_files_in_directory
from slimer.main import get_exclusion_patterns
from slimer.main import parse_arguments
from slimer.main import get_directory_output
from slimer.main import handle_arguments
from slimer.main import process_directory
from slimer.main import handle_output
from slimer.main import main
from slimer.constants import EXCLUDED_FILES, EXCLUDED_DIRECTORIES

"""
  tests for is_binary_file Function
"""


def test_is_binary_file():
    assert is_binary_file("test.jpg")
    assert not is_binary_file("test.txt")


"""
  tests for should_exclude
"""


def test_should_exclude_exact_match():
    patterns = {'temp', 'logs'}
    assert should_exclude('temp', patterns)
    assert should_exclude('logs', patterns)
    assert not should_exclude('src', patterns)


def test_should_exclude_wildcard():
    patterns = {'*.log', '*.tmp'}
    assert should_exclude('error.log', patterns)
    assert should_exclude('temp.tmp', patterns)
    assert not should_exclude('temp.txt', patterns)


def test_should_exclude_path():
    patterns = {'src/temp/*', 'logs/*'}
    assert should_exclude('src/temp/file.txt', patterns)
    assert should_exclude('logs/error.log', patterns)
    assert not should_exclude('src/file.txt', patterns)


def test_should_exclude_no_patterns():
    patterns = set()
    assert not should_exclude('src', patterns)
    assert not should_exclude('error.log', patterns)


def test_should_exclude_case_insensitive():
    patterns = {'*.LOG'}
    assert should_exclude('ERROR.LOG', patterns)
    assert should_exclude('error.log', patterns)


def test_should_exclude_with_windows_paths():
    patterns = {'src\\temp\\*', 'logs\\*'}
    assert not should_exclude('src\\temp\\file.txt', patterns)
    assert should_exclude('logs\\error.log', patterns)
    assert not should_exclude('src\\file.txt', patterns)


"""
  tests for read_file_content
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
  tests for remove_comments
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
  tests for generate_output_for_file
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
  tests for display_files_in_directory
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


"""
  tests for display_files_in_directory
"""


class ArgsMock:
    def __init__(self, exclude, include):
        self.exclude = exclude
        self.include = include


def test_get_exclusion_patterns_default():
    args = ArgsMock([], [])
    expected_patterns = set(EXCLUDED_FILES + EXCLUDED_DIRECTORIES)
    assert get_exclusion_patterns(args) == expected_patterns


def test_get_exclusion_patterns_exclude_custom():
    custom_exclusions = ['custom_file.txt', 'custom_folder/']
    args = ArgsMock(custom_exclusions, [])
    expected_patterns = set(EXCLUDED_FILES + EXCLUDED_DIRECTORIES + custom_exclusions)
    assert get_exclusion_patterns(args) == expected_patterns


def test_get_exclusion_patterns_include_overrides_default():
    override_items = ['override_file.txt', 'override_folder/']
    args = ArgsMock([], override_items)
    expected_patterns = set(EXCLUDED_FILES + EXCLUDED_DIRECTORIES) - set(override_items)
    assert get_exclusion_patterns(args) == expected_patterns


def test_get_exclusion_patterns_include_overrides_custom():
    custom_exclusions = ['custom_file.txt', 'custom_folder/']
    override_items = ['custom_file.txt']
    args = ArgsMock(custom_exclusions, override_items)
    expected_patterns = set(EXCLUDED_FILES + EXCLUDED_DIRECTORIES + ['custom_folder/'])
    assert get_exclusion_patterns(args) == expected_patterns


def test_get_exclusion_patterns_complex_scenario():
    custom_exclusions = ['custom1.txt', 'custom2.txt', 'custom_folder/']
    override_items = ['custom2.txt', 'override_file.txt', 'override_folder/']
    args = ArgsMock(custom_exclusions, override_items)
    expected_patterns = set(EXCLUDED_FILES + EXCLUDED_DIRECTORIES + ['custom1.txt', 'custom_folder/'])
    assert get_exclusion_patterns(args) == expected_patterns


"""
  tests for parse_arguments
"""


@pytest.fixture
def mock_argv(monkeypatch):
    def _mock_argv(args_list):
        monkeypatch.setattr(sys, 'argv', args_list)
    return _mock_argv


PROG_NAME = 'slimer'
TEST_PATH = './'


def test_parse_arguments_path(mock_argv):
    mock_argv([PROG_NAME, TEST_PATH])
    args = parse_arguments()
    assert args.path == TEST_PATH


def test_parse_arguments_copy(mock_argv):
    mock_argv([PROG_NAME, TEST_PATH, '--copy'])
    args = parse_arguments()
    assert args.copy


def test_parse_arguments_limit(mock_argv):
    mock_argv([PROG_NAME, TEST_PATH, '--limit', '5'])
    args = parse_arguments()
    assert args.limit == 5


def test_parse_arguments_depth(mock_argv):
    mock_argv([PROG_NAME, TEST_PATH, '--depth', '3'])
    args = parse_arguments()
    assert args.depth == 3


def test_parse_arguments_exclude(mock_argv):
    mock_argv([PROG_NAME, TEST_PATH, '--exclude', 'test1', 'test2'])
    args = parse_arguments()
    assert args.exclude == ["test1", "test2"]


"""
  tests for get_directory_output
"""


def test_prepend_append_args():
    mock_args = argparse.Namespace(
        prepend="PREPEND",
        append="APPEND",
        limit=None,
        depth=None,
        tree=False,
        binary=False,
        recent=None,
        file_extensions=None,
        strip_comments=False
    )

    with patch("slimer.main.get_exclusion_patterns", return_value=[]), \
            patch("slimer.main.display_files_in_directory", return_value="directory_output"):

        output = get_directory_output(mock_args, "/dummy/path")
        assert output == "PREPEND\ndirectory_output\nAPPEND"


def test_no_prepend_append_args():
    mock_args = argparse.Namespace(
        prepend=None,
        append=None,
        limit=None,
        depth=None,
        tree=False,
        binary=False,
        recent=None,
        file_extensions=None,
        strip_comments=False
    )

    with patch("slimer.main.get_exclusion_patterns", return_value=[]), \
            patch("slimer.main.display_files_in_directory", return_value="directory_output"):

        output = get_directory_output(mock_args, "/dummy/path")
        assert output == "directory_output"


"""
  tests for handle_arguments
"""


def test_handle_arguments_valid_path(mock_argv):
    mock_argv(['slimer', '/some/valid/path'])

    with patch('slimer.main.parse_arguments') as mock_parse, \
            patch('os.path.abspath', return_value='/absolute/path'), \
            patch('os.path.exists', return_value=True):

        mock_parse.return_value = argparse.Namespace(path='/some/valid/path')

        args, absolute_path = handle_arguments()
        assert args.path == '/some/valid/path'
        assert absolute_path == '/absolute/path'


def test_handle_arguments_invalid_path(capfd, mock_argv):
    mock_argv(['slimer', '/some/invalid/path'])

    with patch('slimer.main.parse_arguments') as mock_parse, \
            patch('os.path.abspath', return_value='/absolute/path'), \
            patch('os.path.exists', return_value=False):

        mock_parse.return_value = argparse.Namespace(path='/some/invalid/path')

        with pytest.raises(SystemExit) as exc:
            handle_arguments()

        assert exc.value.code == 1

        captured = capfd.readouterr()
        assert captured.out == "Path '/some/invalid/path' not found.\n"


"""
  tests for process_directory
"""


def test_process_directory():
    mock_args = argparse.Namespace(path='/some/path')
    absolute_path = '/absolute/path'

    with patch('slimer.main.get_directory_output') as mock_get_directory_output:
        mock_get_directory_output.return_value = "expected_directory_output"
        result = process_directory(mock_args, absolute_path)
        mock_get_directory_output.assert_called_once_with(mock_args, absolute_path)
        assert result == "expected_directory_output"


"""
  tests for handle_output
"""


def test_handle_output_to_file():
    mock_output = "some_output_content"
    mock_output_file = "/path/to/output_file.txt"
    # Using mock_open to mock the open function
    m = mock_open()
    with patch("builtins.open", m):
        handle_output(mock_output, copy_to_clipboard=False, output_file=mock_output_file)

    # Ensure file is opened in write mode and content is written
    m.assert_called_once_with(mock_output_file, 'w', encoding='utf-8')
    m().write.assert_called_once_with(mock_output)


def test_handle_output_to_clipboard():
    mock_output = "some_output_content"

    # Mocking pyperclip.copy to ensure it gets called correctly
    with patch("slimer.main.pyperclip.copy") as mock_pyperclip_copy:
        handle_output(mock_output, copy_to_clipboard=True, output_file=None)

    mock_pyperclip_copy.assert_called_once_with(mock_output)


def test_handle_output_to_console():
    mock_output = "some_output_content"

    # Mocking the print function to verify the output
    with patch("builtins.print") as mock_print:
        handle_output(mock_output, copy_to_clipboard=False, output_file=None)

    mock_print.assert_called_once_with(mock_output)


"""
  tests for main
"""


def test_main_happy_path():
    mock_args = Mock()
    mock_absolute_path = "mock/path"
    mock_output = "mock_output"

    # Mock the internal function calls to simulate a successful run
    with patch("slimer.main.handle_arguments", return_value=(mock_args, mock_absolute_path)), \
            patch("slimer.main.process_directory", return_value=mock_output), \
            patch("slimer.main.handle_output") as mock_handle_output:

        main()

        # Ensure the mocked functions were called with the right arguments
        mock_handle_output.assert_called_once_with(mock_output, mock_args.copy, mock_args.output)


def test_main_handle_arguments_exception():
    with patch("slimer.main.handle_arguments", side_effect=Exception("Test Error")), \
            patch("builtins.print") as mock_print:

        main()

        mock_print.assert_called_once_with("An unexpected error occurred: Test Error")


def test_main_process_directory_exception():
    with patch("slimer.main.handle_arguments", return_value=(Mock(), "mock/path")), \
            patch("slimer.main.process_directory", side_effect=Exception("Test Error")), \
            patch("builtins.print") as mock_print:

        main()

        mock_print.assert_called_once_with("An unexpected error occurred: Test Error")


def test_main_handle_output_exception():
    mock_args = Mock()
    mock_absolute_path = "mock/path"
    mock_output = "mock_output"

    with patch("slimer.main.handle_arguments", return_value=(mock_args, mock_absolute_path)), \
            patch("slimer.main.process_directory", return_value=mock_output), \
            patch("slimer.main.handle_output", side_effect=Exception("Test Error")), \
            patch("builtins.print") as mock_print:

        main()

        mock_print.assert_called_once_with("An unexpected error occurred: Test Error")
