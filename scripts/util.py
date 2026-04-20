import re


def get_attribute(line: str, attribute: str) -> str | None:
    """Extract the value of an attribute from an xml line"""
    match = re.search(rf' {attribute}="([^"]+)"', line)
    return match.group(1) if match else None


def set_attribute(line: str, attribute: str, value: str) -> str:
    """Set the value of an attribute in an xml line"""
    pattern = re.compile(rf'( {attribute}=")([^"]*)(")')
    if pattern.search(line):
        return pattern.sub(lambda m: m.group(1) + value + m.group(3), line)
    else:
        # If the attribute doesn't exist, add it before the closing tag
        return line.replace("/>", f' {attribute}="{value}" />')
