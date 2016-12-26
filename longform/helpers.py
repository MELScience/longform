import re

from urllib.parse import urlparse

import bleach
import CommonMark
import html5lib
import pyphen
import smartypants

from django.conf import settings
from html5lib.tokenizer import HTMLTokenizer


hyphen_dict = pyphen.Pyphen(lang="en_US")

re_hyphenate_word = re.compile(r"\w{5,}")


def _hyphenate(text):
    def add_hyphens(matchobj):
        # NOTE(si14): \xad = &shy;
        return hyphen_dict.inserted(matchobj.group(0), '\xad')
    return re_hyphenate_word.sub(add_hyphens, text)


def _hyphenate_html(html):
    def hyphen_gen(stream):
        for el in stream:
            if el["type"] == "Characters":
                text = el["data"]

                text = _hyphenate(el["data"])

                el['data'] = text

            yield el

    doc = html5lib.parseFragment(html, namespaceHTMLElements=False)
    walker = html5lib.getTreeWalker('etree')
    stream = walker(doc)
    stream = hyphen_gen(stream)

    return html5lib.serializer.HTMLSerializer().render(stream)


def _smartypants(text):
    attrs = (smartypants.Attr.b | smartypants.Attr.D | smartypants.Attr.e)
    return (smartypants.smartypants(text, attrs)
            .replace("&#8211;", "–")
            .replace("&#8212;", "—")
            .replace("&#8230;", "…")
            .replace("&#8220;", "“")
            .replace("&#8221;", "”"))


re_widont = re.compile(r"\s+([^\s^>]+\s*(</p>|</li>|</h\d>))")


def _widont(text, count=1):
    def add_nbsp(matchobj):
        # NOTE(si14): \xa0 is &nbsp;
        return "\xa0{}".format(matchobj.group(1))

    for i in range(count):
        text = re_widont.sub(add_nbsp, text)
    return text


def _linkify_all(html):
    def set_target(attrs, new=False):
        if attrs["href"].startswith("mailto:"):
            return attrs
        p = urlparse(attrs["href"])
        if p.netloc not in settings.OUR_DOMAINS:
            attrs["target"] = "_blank"
            attrs["rel"] = "noopener noreferrer nofollow"
            attrs["class"] = "external"
        return attrs
    # NOTE(si14): we use plain HTMLTokenizer here to avoid sanitizing by
    #             bleach
    return bleach.linkify(html, skip_pre=True, callbacks=[set_target],
                          tokenizer=HTMLTokenizer)


re_strip_outer_p = re.compile(r"^<p>(.*)</p>$", flags=re.DOTALL)


def _strip_outer_p(html):
    matchobj = re_strip_outer_p.match(html)
    if matchobj is None:
        return html
    else:
        return matchobj.group(1)


def process_text(raw, sanitize=True, strip_outer_p=False):
    """
    - sanitize (if sanitize parameter was not set to False)
    - hyphenate all text pieces
    - smartypants
    - widont on paragraphs and list items
    - render markdown
    - linkify (find links in the text, set target="_blank" properly on
      external links)
    Note: we use unescaped HTML entities (raw unicode symbols) to avoid
    blindly unescaping them in client-side JS. We don't want to accidentaly
    unescape &gt; :)
    """
    if sanitize:
        sanitized = bleach.clean(raw)
    else:
        sanitized = raw

    if not sanitized:
        return sanitized

    sanitized = _smartypants(sanitized)

    html = CommonMark.commonmark(sanitized)

    html = _widont(html)
    html = _linkify_all(html)
    html = _hyphenate_html(html)

    if strip_outer_p:
        html = _strip_outer_p(html)

    return html
