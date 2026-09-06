def looks_like_escaped_source(text:str) -> bool:
    """ True when the payload is one logical line stuffed with \\n sequences."""
    if "\\n" not in text :
        return False

    return text.count("\\n") <= 1 