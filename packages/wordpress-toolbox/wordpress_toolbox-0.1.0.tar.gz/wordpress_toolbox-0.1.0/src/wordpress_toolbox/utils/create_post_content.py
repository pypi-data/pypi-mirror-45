from css_html_js_minify import html_minify

from .get_post_content import get_post_content
from .get_header_html import get_header_html
from .get_footer_html import get_footer_html
from .get_form_html import get_form_html


def create_post_content(url, content_html):
    html_template = get_post_content(url)
    header_html = get_header_html(html_template)
    footer_html = get_footer_html(html_template)
    form_html = get_form_html(html_template)
    return html_minify("{}{}{}{}".format(
        header_html, content_html, form_html, footer_html
    ))
