import re


def extract_structure(text):
    """
    Detect headings + numbering patterns.
    Returns structured representation.
    """

    lines = text.split("\n")
    structure = []

    for line in lines:
        if re.match(r"^(Chapter|Unit|Section)\s*\d+", line):
            structure.append({
                "type": "heading",
                "content": line.strip()
            })
        else:
            structure.append({
                "type": "text",
                "content": line.strip()
            })

    return structure