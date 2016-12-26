from django.test import TestCase

from .. import helpers


def _strip_special_chars(result):
    return (result
            .replace("\xa0", " ")
            .replace("\xad", "")
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
