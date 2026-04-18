def format_structure(structured_data):
    formatted = ""

    for block in structured_data:
        if block["type"] == "heading":
            formatted += f"\n\n# {block['content']}\n"
        else:
            formatted += block["content"] + "\n"

    return formatted