from django.db import models
from django.test import TestCase

from ..fields import LongformField


class LongformModel(models.Model):
    text_raw = models.TextField()
    text = LongformField(raw_field="text_raw")


class LongformModelArgs(models.Model):
    text_raw = models.TextField()
    text = LongformField(raw_field="text_raw",
                         sanitize=False,
                         strip_outer_p=True)


class LongformFieldTestCase(TestCase):
    def test_fill_on_save(self):
        instance = LongformModel(text_raw="*Pearl* Fountain")
        instance.save()
        instance.refresh_from_db()
        self.assertEqual(instance.text.strip(),
                         "<p><em>Pearl</em>\xa0Foun\xadtain</p>")

        instance.text_raw = "More <script>Stacks</script>"
        instance.save()
        instance.refresh_from_db()
        self.assertEqual(instance.text.strip(),
                         "<p>More\xa0&lt;script&gt;Stacks&lt;/script&gt;</p>")


    def test_args(self):
        instance = LongformModelArgs(text_raw="Miami <script>Ultras</script>")
        instance.save()
        instance.refresh_from_db()
        self.assertEqual(instance.text.strip(),
                         "Mi\xada\xadmi <script>Ul\xadtras</script>")
