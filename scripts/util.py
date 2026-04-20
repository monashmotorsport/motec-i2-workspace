import os
import re
from lxml import etree


def load_xml(path: str) -> etree._ElementTree:
    """Load and parse the XML file from the given path."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"XML file not found: {path}")
    with open(path, "rb") as f:
        return etree.parse(f)


def load_schema(path: str) -> etree.XMLSchema:
    """Load and parse the XML schema from the given path."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Schema not found: {path}")
    with open(path, "rb") as f:
        schema_doc = etree.parse(f)
    return etree.XMLSchema(schema_doc)


def validate(xml_path: str, schema: etree.XMLSchema) -> int:
    """Validate the XML file at xml_path against the provided schema."""

    doc = load_xml(xml_path)
    valid = schema.validate(doc)

    if not valid:
        print(f"INVALID: {xml_path} does not conform to schema")
        for error in schema.error_log:
            print(f"  Line {error.line}: {error.message}")
        return 1

    return 0


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
