import argparse
import os
import re

SLIMER_VERSION_FILE = os.path.join(os.path.dirname(__file__), '../slimer', '__version__.py')


def read_version():
    with open(SLIMER_VERSION_FILE, 'r') as f:
        contents = f.read()
        version_line = [line for line in contents.split("\n") if "__version__" in line][0]
        version_str = version_line.split("=")[-1].strip().strip('"')
        return version_str


def write_version(new_version, dry_run=False):
    with open(SLIMER_VERSION_FILE, 'r') as f:
        contents = f.read()

    new_contents = contents.replace(read_version(), new_version)

    if not dry_run:
        with open(SLIMER_VERSION_FILE, 'w') as f:
            f.write(new_contents)
    else:
        print("--Dry Run--")
        print("File would have been updated to:")
        print(new_contents)


def bump_version(version=None, major=False, minor=False, patch=False):
    if version:
        return version

    current_version = read_version()
    major_v, minor_v, patch_v = map(int, current_version.split('.'))

    if major:
        major_v += 1
        minor_v = 0
        patch_v = 0
    elif minor:
        minor_v += 1
        patch_v = 0
    elif patch:
        patch_v += 1

    return f"{major_v}.{minor_v}.{patch_v}"


def validate_version(version):
    pattern = re.compile(r'^\d+\.\d+\.\d+$')
    return bool(pattern.match(version))


if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(description="Bump version for Slimer project.")
        parser.add_argument("--major", action="store_true", help="Bump the major version.")
        parser.add_argument("--minor", action="store_true", help="Bump the minor version.")
        parser.add_argument("--patch", action="store_true", help="Bump the patch version.")
        parser.add_argument("--version", type=str, help="Specify the full version, e.g. 0.1.0, 1.2.3.")
        parser.add_argument("--dry-run", action="store_true", help="Perform a dry run without writing changes to file.")
        args = parser.parse_args()

        new_version = None

        if args.version:
            if not validate_version(args.version):
                raise ValueError(f"Invalid version format: {args.version}. Expected format: X.Y.Z")
            new_version = args.version
        else:
            new_version = bump_version(major=args.major, minor=args.minor, patch=args.patch)

        write_version(new_version, dry_run=args.dry_run)

        if args.dry_run:
            print(f"Version would be set to: {new_version}")
        else:
            print(f"Version updated to: {new_version}")

    except ValueError as e:
        print(f"Error: {e}")
