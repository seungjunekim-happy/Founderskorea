import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.tables import TableExtension
from markdown.extensions.toc import TocExtension


_md = markdown.Markdown(extensions=[
    FencedCodeExtension(),
    CodeHiliteExtension(css_class="highlight", linenums=False),
    TableExtension(),
    TocExtension(permalink=False),
    "markdown.extensions.nl2br",
    "markdown.extensions.smarty",
])


def render_markdown(text: str) -> str:
    _md.reset()
    return _md.convert(text)
