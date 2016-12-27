from django.test import TestCase

from .utils import setup_prealoder
from .. import helpers

preload_example = setup_prealoder(__file__)


def _strip_special_chars(result):
    return (result
            .replace('\xa0', ' ')
            .replace('\xad', '')
            .strip())


class ProcessTextTestCase(TestCase):

    def test_safety(self):
        text = """
I am a hacker. <script>alert("hello there!")</script>
        """
        self.assertNotIn("<script>", helpers.process_text(text))
        self.assertIn("<script>", helpers.process_text(text, sanitize=False))

    def test_p_stripping(self):
        text = "# The **big** thing"
        result = _strip_special_chars(helpers.process_text(text))
        self.assertEqual(result, "<h1>The <strong>big</strong> thing</h1>")

    def test_linkification(self):
        text = """
There is a link https://google.com somewhere here
And we can have [markdown link](https://stripe.com)
        """
        result = _strip_special_chars(helpers.process_text(text))

        self.assertIn("href=https://google.com", result)
        self.assertIn(">https://google.com</a>", result)
        self.assertIn("href=https://stripe.com", result)
        self.assertIn(">markdown link</a>", result)

    def test_smartypants(self):
        text = "Look... This is so smart --- you can have this, too"
        result = _strip_special_chars(helpers.process_text(text))
        self.assertIn("…", result)
        self.assertIn("—", result)

    def test_hyphenation(self):
        text = "Strange word: impersonation"
        result = helpers.process_text(text)
        self.assertIn("im\xadper\xadson\xadation", result)

    def test_subscript(self):
        text = 'H~2~O'
        result = helpers.process_text(text, strip_outer_p=True)
        self.assertEqual('H<sub>2</sub>O', result)

    def test_supscript(self):
        text = '10^2^'
        result = helpers.process_text(text, strip_outer_p=True)
        self.assertEqual('10<sup>2</sup>', result)

    def test_supscript_with_space(self):
        text = '10^2 ^'
        result = helpers.process_text(text, strip_outer_p=True)
        self.assertEqual('10^2 ^', result)

    def test_mj_emc_statement(self):
        text = 'here is mj: $E = mc^2$!'
        result = helpers.process_text(text)
        expected = preload_example('mj_emc_test.html')
        self.assertEqual(expected, result)

    def test_external_mj_processor(self):
        expected = preload_example('mj_x2.html')
        self.assertEqual(helpers.exec_mj_statement('x^2'), expected)

    def test_widont_oneword(self):
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
        self.assertEqual(result.strip(), required_result.strip())


class TestMJRegex(TestCase):

    mj_findall = helpers.re_mj_statement.findall

    def test_simple_math(self):
        self.assertEqual(self.mj_findall('$2 + 3$'), ['2 + 3'])

    def test_simple_math_plus_space(self):
        self.assertEqual(self.mj_findall('$2 + 3 $'), ['2 + 3'])

    def test_simple_false(self):
        self.assertEqual(self.mj_findall('$ 2 + 3 $'), [])

    def test_false_if_not_followed_by_space(self):
        self.assertEqual(self.mj_findall('$2 + 3$4'), [])

    def test_false_if_not_followed_by_space_and_space_before(self):
        self.assertEqual(self.mj_findall('$2 + 3 $4'), [])

    def test_true_if_followed_by_letter(self):
        self.assertEqual(self.mj_findall('$2 + 3$a4'), ['2 + 3'])

    def test_emc(self):
        text = 'here is mj: $E = mc^2$'
        self.assertEqual(helpers.re_mj_statement.findall(text), ['E = mc^2'])
