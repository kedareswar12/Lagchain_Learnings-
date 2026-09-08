from pathlib import Path
_ESCAPE_MAP = (
    ("\\n", "\n"),   # Newline
    ("\\t", "\t"),   # Tab
    ("\\r", "\r"),   # Carriage return
    ("\\b", "\b"),   # Backspace
    ("\\f", "\f"),   # Form feed
    ("\\v", "\v"),   # Vertical tab
    ("\\a", "\a"),   # Bell
    ("\\0", "\0"),   # Null
    ("\\\\", "\\"),  # Backslash itself
    ('\\"', '"'),    # Double quote
    ("\\'", "'"),    # Single quote
)

_HTML_ENTITY_MAP = (
    ("&amp;", "&"),
    ("&lt;", "<"),
    ("&gt;", ">"),
    ("&quot;", '"'),
    ("&apos;", "'"),
    ("&nbsp;", " "),
    ("&copy;", "©"),
    ("&reg;", "®"),
    ("&trade;", "™"),
    ("&mdash;", "—"),
    ("&ndash;", "–"),
    ("&hellip;", "…"),
    ("&cent;", "¢"),
    ("&pound;", "£"),
    ("&yen;", "¥"),
    ("&euro;", "€"),
    ("&sect;", "§"),
    ("&deg;", "°"),
    ("&plusmn;", "±"),
    ("&times;", "×"),
    ("&divide;", "÷"),
)

_MARKDOWN_SUFFIXES = {".md", ".markdown", ".mdx"}
_MARKUP_SUFFIXES = {".html", ".xml", ".xhtml" , ".svg"}


def looks_like_escaped_source(text:str) -> bool:
    """ True when the payload is one logical line stuffed with \\n sequences."""
    if "\\n" not in text :
        return False

    return text.count("\\n") > 1 

def normalize_source_text(text : str) -> str:
    """ Turns double escaped newlines/tabs into real ones """
    if not looks_like_escaped_source(text):
        return text 

    normalized =text 
    for escape ,raw in _ESCAPE_MAP:
        normalized = normalized.replace(escape,raw)
    return normalized

def unescape_html_entities(text:str)->str:
    """Undo HTML entities as some weaker model emit those instead of raw < , >  , & """
    if "&" not in text :
        return text 
    unescaped = text
    for entity, raw in _HTML_ENTITY_MAP:
        unescaped = unescaped.replace(entity,raw)
    return unescaped

def strip_markdown_fence(text:str)->str:
    """Drop a wrapping ```lang ,,,,, fence """
    if "```" not in text:
        return text 
    lines = text.split("\n")
    if lines and lines[0].lstrip().startswith("```"):
        lines = lines[1:]

    if lines and lines[-1].strip().endswith("```"):
        lines = lines[:-1]

    return "\n".join(lines)

def prepare_file_content(path :str , text:str)->str:

    """
    Normalize the tool payload text into file bites independet of language 

    1. Normalize newlines / tabs
    2. Drop Markdown Fenses
    3. Unescape html entities 

    """
    suffix = Path(path).suffix.lower()
    prepared =normalize_source_text(text)
    
    if suffix not  in _MARKDOWN_SUFFIXES:
        prepared = strip_markdown_fence(prepared)
    if suffix  not in  _MARKUP_SUFFIXES:
        prepared = unescape_html_entities(prepared)

    return prepared