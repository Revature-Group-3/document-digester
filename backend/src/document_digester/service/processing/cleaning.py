import re

# returns cleaned html
def clean_html(text: str) -> str:
    text = re.sub(r"^(.+)\n=+$", r"## \1", text, flags=re.MULTILINE)
    text = re.sub(r"^(.+)\n-+$", r"### \1", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*\[image\]\s*\n?", "", text, flags=re.MULTILINE)
    return str(text)
