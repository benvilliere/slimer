
DEFAULT_EXCLUDED_DIRECTORIES = ['node_modules', '.git', '__pycache__']

DEFAULT_EXCLUDED_FILES = ['.gitattributes', '.gitignore', 'LICENSE', 'README.md']

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
    '.h': 'cpp',
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
