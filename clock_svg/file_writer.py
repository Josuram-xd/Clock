"""Writing the SVG to disk."""


def write_file(path, content):
    """Save the content in UTF-8 at the given path."""
    with open(path, "w", encoding="utf-8") as file:
        file.write(content)
