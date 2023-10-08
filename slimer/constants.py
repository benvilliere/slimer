EXCLUDED_DIRECTORIES = [
    'node_modules',
    '.git',
    '__pycache__'
]

EXCLUDED_FILES = [
    '.gitattributes',
    '.gitignore',
    'LICENSE',
    'README.md'
]

BINARY_FILE_EXTENSIONS = [
    '.exe', '.dll', '.bin', '.o', '.a', '.lib',
    '.so', '.dylib', '.bmp', '.gif', '.jpg', '.jpeg',
    '.png', '.webp', '.mp3', '.wav', '.ogg', '.mp4',
    '.webm', '.zip', '.tar', '.gz', '.bz2', '.7z',
    '.rar', '.pdf', '.doc', '.docx', '.xls', '.xlsx',
    '.ppt', '.pptx', '.odt', '.ods'
]

FILE_EXTENSION_MAPPINGS = {
    '.py': 'python',
    '.ts': 'typescript',
    '.js': 'javascript',
    '.html': 'html',
    '.css': 'css',
    '.php': 'php',
    '.cpp': 'cpp',
    '.c': 'c',
    '.h': 'c',
    '.java': 'java',
    '.rb': 'ruby',
    '.go': 'go',
    '.rs': 'rust',
    '.swift': 'swift',
    '.sh': 'bash',
    '.md': 'markdown',
    '.xml': 'xml',
    '.json': 'json',
    '.yml': 'yaml',
    '.yaml': 'yaml',
    '.cs': 'csharp',
    '.f': 'fortran',
    '.r': 'r',
    '.pl': 'perl',
    '.lua': 'lua',
    '.kt': 'kotlin',
    '.dart': 'dart',
    '.groovy': 'groovy',
    '.ps1': 'powershell',
    '.m': 'matlab',
    '.sql': 'sql',
}

HASH_COMMENT_REGEX = r'(?m)^\s*#.*?$'
DOUBLE_SLASH_COMMENT_REGEX = r'(?m)^\s*//.*?$'
DOUBLE_DASH_COMMENT_REGEX = r'(?m)^\s*--.*?$'

SINGLE_LINE_COMMENT_PATTERNS = {
    'python': HASH_COMMENT_REGEX,
    'ruby': HASH_COMMENT_REGEX,
    'perl': HASH_COMMENT_REGEX,
    'bash': HASH_COMMENT_REGEX,
    'powershell': HASH_COMMENT_REGEX,
    'r': HASH_COMMENT_REGEX,
    'javascript': DOUBLE_SLASH_COMMENT_REGEX,
    'typescript': DOUBLE_SLASH_COMMENT_REGEX,
    'java': DOUBLE_SLASH_COMMENT_REGEX,
    'c': DOUBLE_SLASH_COMMENT_REGEX,
    'cpp': DOUBLE_SLASH_COMMENT_REGEX,
    'csharp': DOUBLE_SLASH_COMMENT_REGEX,
    'rust': DOUBLE_SLASH_COMMENT_REGEX,
    'go': DOUBLE_SLASH_COMMENT_REGEX,
    'php': DOUBLE_SLASH_COMMENT_REGEX,
    'swift': DOUBLE_SLASH_COMMENT_REGEX,
    'kotlin': DOUBLE_SLASH_COMMENT_REGEX,
    'dart': DOUBLE_SLASH_COMMENT_REGEX,
    'groovy': DOUBLE_SLASH_COMMENT_REGEX,
    'sql': DOUBLE_DASH_COMMENT_REGEX
}

BLOCK_COMMENT_REGEX = r'/\*.*?\*/'
DOCSTRING_REGEX = r'''(\'\'\'.*?\'\'\'|\"\"\".*?\"\"\")'''

MULTI_LINE_COMMENT_PATTERNS = {
    'python': DOCSTRING_REGEX,
    'javascript': BLOCK_COMMENT_REGEX,
    'typescript': BLOCK_COMMENT_REGEX,
    'java': BLOCK_COMMENT_REGEX,
    'c': BLOCK_COMMENT_REGEX,
    'cpp': BLOCK_COMMENT_REGEX,
    'csharp': BLOCK_COMMENT_REGEX,
    'rust': BLOCK_COMMENT_REGEX,
    'go': BLOCK_COMMENT_REGEX,
    'php': BLOCK_COMMENT_REGEX,
    'swift': BLOCK_COMMENT_REGEX,
    'kotlin': BLOCK_COMMENT_REGEX,
    'dart': BLOCK_COMMENT_REGEX,
    'groovy': BLOCK_COMMENT_REGEX
}
