import pytest

from .. import helpers, longform_samples


def _strip_special_chars(result):
    return (result
            .replace("\xa0", " ")
            .replace("\xad", "")
            .strip())


def test_safety():
    text = """
I am a hacker. <script>alert("hello there!")</script>
    """
    assert "<script>" not in helpers.process_text(text)
    assert "<script>" in helpers.process_text(text, sanitize=False)


def test_p_stripping():
    text = "# The **big** thing"
    result = _strip_special_chars(helpers.process_text(text))
    assert result == "<h1>The <strong>big</strong> thing</h1>"


def test_linkification():
    text = """
There is a link https://google.com somewhere here

And we can have [markdown link](https://stripe.com)
    """
    result = _strip_special_chars(helpers.process_text(text))
    assert 'href=https://google.com' in result
    assert '>https://google.com</a>' in result
    assert 'href=https://stripe.com' in result
    assert '>markdown link</a>' in result


def test_smartypants():
    text = "Look... This is so smart --- you can have this, too"
    result = _strip_special_chars(helpers.process_text(text))
    assert "…" in result
    assert "—" in result


def test_hyphenation():
    text = "Strange word: impersonation"
    result = helpers.process_text(text)
    assert "im\xadper\xadson\xadation" in result


def test_widont_oneword():
    text = """
1. Study of the world around
2. Knowledge
3. The Earth
"""
    required_result = """
<ol>
<li>Study of the world\xa0around</li>
<li>Knowl\xadedge</li>
<li>The\xa0Earth</li>
</ol>
"""
    result = helpers.process_text(text)
    assert result.strip() == required_result.strip()
