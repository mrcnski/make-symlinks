# Easy, safe way to create symlinks in the home directory pointing to files in a
# given directory. The default mode of operation is a dry run with many prompts.
#
# Usage: python3 make-symlinks.py <source_root> <file1> <file2> ...
#
# Example: create symlinks in home dir to all files in ~/Sync/dotfiles:
# python3 ./make-symlinks.py ~/Sync/dotfiles
#
# Example: create symlinks in home dir to only certain folders in ~/Sync:
# python3 ./make-symlinks.py ~/Sync Code Repos

import os
import sys

DESTINATION_ROOT = "~"
REMOVE = [".DS_Store"]

source_root = sys.argv[1]
files = sys.argv[2:]

print("---")
print(f"About to start symlinking from '{source_root}' to '{DESTINATION_ROOT}'.")
if len(files) > 0:
    print(f"Will symlink these files/dirs: {files}")
else:
    print("Will symlink all files/dirs in source directory.")
print(f"Will remove all these files from '{source_root}': {REMOVE}")
print()

print("Overwrite existing files at destination? (If y, will still ask for confirmation.)")
overwrite = input("y/[n]/q > ").lower()
if overwrite == "q":
    exit()
overwrite = overwrite == "y"

print("Do a dry run?")
dry = input("[y]/n/q > ").lower()
if dry == "q":
    exit()
dry = dry != "n"

print("Display skipped files?")
display_skipped = input("[y]/n/q > ").lower()
if display_skipped == "q":
    exit()
display_skipped = display_skipped != "n"

print()

def handle_file_or_dir(name):
    if os.path.isdir(f"{source_root}/{name}"):
        type = "dir"
    else:
        type = "file"

    source_abs = os.path.abspath(f"{source_root}/{name}")

    if name in REMOVE:
        print(f"Removing: {type} '{name}'")
        if not dry:
            os.remove(source_abs)
        return

    destination = f"{DESTINATION_ROOT}/{name}"
    destination_abs = os.path.expanduser(destination)

    if os.path.exists(destination_abs):
        if not overwrite:
            if display_skipped:
                print(f"Skipping: {type} '{destination}' exists")
            return

        print(f"Overwrite {type} '{destination}'?")
        overwrite_this = input("[y]/n/q > ")
        if overwrite_this == "q":
            exit()
        overwrite_this = overwrite_this != "n"
        if overwrite_this:
            print(f"Removing: {type} '{destination}'")
            if not dry:
                os.remove(destination_abs)
        else:
            return
    else:
        # Check for broken symlinks.
        # This works because `os.path.exists` above returns False for broken links.
        if os.path.lexists(destination_abs):
            print(f"!BROKEN!: link '{destination}'")
            return

    print(f"Linking:  '{destination_abs}'")
    print(f"       -> '{source_abs}'")
    if not dry:
        os.symlink(source_abs, destination_abs)

if len(files) > 0:
    for file in files:
        handle_file_or_dir(file)
else:
    # Iterate over immediate files/dirs in `root`.
    for name in os.listdir(source_root):
        handle_file_or_dir(name)
