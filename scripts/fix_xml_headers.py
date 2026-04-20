"""
Enforce all xml files to have the same header, so users language settings don't pollute
the diff when they edit the file.
"""

import sys
from typing import List
from scripts.util import get_attribute, set_attribute


def fix_xml_header(file_path: str) -> bool:
    """Set the header of the xml file to a fixed value.

    Returns True if the file was modified, False otherwise.
    """

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = list(lines)
    for i in range(2):
        locale = get_attribute(lines[i], "Locale")
        if locale:
            new_lines[i] = set_attribute(lines[i], "Locale", "English_Australia.1252")

    if new_lines != lines:
        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
        return True
    return False


def main(argv: List[str]) -> int:
    if len(argv) < 2:
        print("No files provided. Pre-commit should pass filenames to this script.")
        return 1

    modified = False
    for path in argv[1:]:
        modified |= fix_xml_header(path)

    # If we modified any file, fail so the user can add the changes and re-commit
    return 1 if modified else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
