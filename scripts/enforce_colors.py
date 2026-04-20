"""
Motec has default colors for channels representing each corner of the car, FL, FR, RL,
and RR, as well as default colors for channels representing the front and rear of the
car.

When channels are loaded from a log file, they are assigned a color based on the channel
name, i.e. if the channel name ends with "FL", it is assigned the FL color.

For math channels, colors are assigned in the xml, so we enforce that the colors in the
xmls match the default colors.
"""

import sys
from typing import List
from scripts.util import get_attribute, set_attribute


# Mapping of channel suffixes to Motec color codes
COLORS = {
    "FL": 0,
    "FR": 4,
    "RL": 6,
    "RR": 3,
    "Front": 1,
    "Rear": 5,
}


def fix_xml_colors(file_path: str) -> bool:
    """Set the colors of math channels in the xml file to match the default colors.

    Returns True if the file was modified, False otherwise.
    """

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = list(lines)

    for i, line in enumerate(lines):
        if "MathExpression" not in line:
            continue

        channel_name = get_attribute(line, "Id")
        suffix = channel_name.split(" ")[-1]

        for key, color in COLORS.items():
            if suffix == key:
                new_lines[i] = set_attribute(line, "DisplayColorIndex", str(color))
                break

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
        modified |= fix_xml_colors(path)

    # If we modified any file, fail so the user can add the changes and re-commit
    return 1 if modified else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
