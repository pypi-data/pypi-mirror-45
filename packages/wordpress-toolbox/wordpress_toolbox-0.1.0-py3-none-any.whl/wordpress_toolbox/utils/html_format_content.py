import re
from css_html_js_minify import html_minify


def add_to_string(string, index, addition):
    return string[:index] + addition + string[index:]


def format_as_html(text, opts):
    """
        format_as_html(text, {
            "h1": (
                (1,2),
            ),
            "p": (
                (2,3),
                (3)
            )
        })
    """
    sentences = text.strip().split("\n")
    for tag_name, positions in opts.items():
        opening_tag = "<{}>".format(tag_name)
        closing_tag = "</{}>".format(tag_name)
        for item in positions:
            start = item[0]
            try:
                end = item[1]
            except IndexError:
                end = len(sentences) - 1
            sentences[start] = add_to_string(
                sentences[start],
                0,
                opening_tag
            )
            sentences[end] = add_to_string(
                sentences[end],
                len(sentences[end]),
                closing_tag,
            )
    return html_minify("".join(sentences))
