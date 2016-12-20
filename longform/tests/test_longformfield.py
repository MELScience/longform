import pytest

from django.db import models

from ..fields import LongformField


class LongformModel(models.Model):
    text_raw = models.TextField()
    text = LongformField(raw_field='text_raw')


class LongformModelArgs(models.Model):
    text_raw = models.TextField()
    text = LongformField(raw_field='text_raw',
                         sanitize=False,
                         strip_outer_p=True)


@pytest.mark.django_db
def test_fill_on_save():
    instance = LongformModel(text_raw='*Pearl* Fountain')
    instance.save()
    instance.refresh_from_db()
    assert instance.text.strip() == '<p><em>Pearl</em>\xa0Foun\xadtain</p>'

    instance.text_raw = 'More <script>Stacks</script>'
    instance.save()
    instance.refresh_from_db()
    assert instance.text.strip() == \
        '<p>More\xa0&lt;script&gt;Stacks&lt;/script&gt;</p>'


@pytest.mark.django_db
def test_args():
    instance = LongformModelArgs(text_raw='Miami <script>Ultras</script>')
    instance.save()
    instance.refresh_from_db()
    assert instance.text.strip() == \
        'Mi\xada\xadmi\xa0<script>Ul\xadtras</script>'
