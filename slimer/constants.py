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

SINGLE_LINE_COMMENT_PATTERNS = {
  'python': r'(?m)^\s*#.*?$',
  'ruby': r'(?m)^\s*#.*?$',
  'perl': r'(?m)^\s*#.*?$',
  'bash': r'(?m)^\s*#.*?$',
  'powershell': r'(?m)^\s*#.*?$',
  'r': r'(?m)^\s*#.*?$',
  'javascript': r'(?m)^\s*//.*?$',
  'typescript': r'(?m)^\s*//.*?$',
  'java': r'(?m)^\s*//.*?$',
  'c': r'(?m)^\s*//.*?$',
  'cpp': r'(?m)^\s*//.*?$',
  'csharp': r'(?m)^\s*//.*?$',
  'rust': r'(?m)^\s*//.*?$',
  'go': r'(?m)^\s*//.*?$',
  'php': r'(?m)^\s*//.*?$',
  'swift': r'(?m)^\s*//.*?$',
  'kotlin': r'(?m)^\s*//.*?$',
  'dart': r'(?m)^\s*//.*?$',
  'groovy': r'(?m)^\s*//.*?$',
  'sql': r'(?m)^\s*--.*?$'
}

MULTI_LINE_COMMENT_PATTERNS = {
  'python': r'''(\'\'\'.*?\'\'\'|\"\"\".*?\"\"\")''',
  'javascript': r'/\*.*?\*/',
  'typescript': r'/\*.*?\*/',
  'java': r'/\*.*?\*/',
  'c': r'/\*.*?\*/',
  'cpp': r'/\*.*?\*/',
  'csharp': r'/\*.*?\*/',
  'rust': r'/\*.*?\*/',
  'go': r'/\*.*?\*/',
  'php': r'/\*.*?\*/',
  'swift': r'/\*.*?\*/',
  'kotlin': r'/\*.*?\*/',
  'dart': r'/\*.*?\*/',
  'groovy': r'/\*.*?\*/'
}