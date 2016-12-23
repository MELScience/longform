from .utils import setup_prealoder
from .. import helpers

preload_example = setup_prealoder(__file__)


def _strip_special_chars(result):
    return (result
            .replace('\xa0', ' ')
            .replace('\xad', '')
            .strip())


def test_safety():
    text = '''
I am a hacker. <script>alert("hello there!")</script>
    '''
    assert '<script>' not in helpers.process_text(text)
    assert '<script>' in helpers.process_text(text, sanitize=False)


def test_p_stripping():
    text = '# The **big** thing'
    result = _strip_special_chars(helpers.process_text(text))
    assert result == '<h1>The <strong>big</strong> thing</h1>'


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
    text = 'Look... This is so smart --- you can have this, too'
    result = _strip_special_chars(helpers.process_text(text))
    assert '…' in result
    assert '—' in result


def test_hyphenation():
    text = 'Strange word: impersonation'
    result = helpers.process_text(text)
    assert 'im\xadper\xadson\xadation' in result


def test_subscript():
    text = 'H~2~O'
    result = helpers.process_text(text, strip_outer_p=True)
    assert 'H<sub>2</sub>O' == result


def test_supscript():
    text = '10^2^'
    result = helpers.process_text(text, strip_outer_p=True)
    assert '10<sup>2</sup>' == result


def test_supscript_with_space():
    text = '10^2 ^'
    result = helpers.process_text(text, strip_outer_p=True)
    assert '10^2 ^' == result


def test_mj_emc_statement():
    text = 'here is mj: $E = mc^2$!'
    result = helpers.process_text(text)
    expected = preload_example('mj_emc_test.html')
    assert expected == result


def test_external_mj_processor():
    expected = preload_example('mj_x2.html')
    assert helpers.exec_mj_statement('x^2') == expected


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
