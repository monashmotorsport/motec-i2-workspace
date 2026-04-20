"""Validate XML files against the schemas in the schemas/ directory."""

import os
import sys
import glob
from scripts.util import load_schema, validate

SCHEMA_MAP = {
    "Channels": "aliases.xsd",
    "Maths": "maths.xsd",
}


def choose_schema(path: str) -> str | None:
    """Choose the appropriate schema file based on the path"""
    for key, schema in SCHEMA_MAP.items():
        if key in path:
            return schema
    return None


def main() -> int:

    failures = 0

    # Loop through all files in the current directory
    for path in glob.glob("**/*.xml", recursive=True):
        schema_file = choose_schema(path)

        if not schema_file:
            print(f"SKIP: No schema found for {path}")
            continue

        schema = load_schema(os.path.join("schemas", schema_file))
        failures += validate(path, schema)

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
