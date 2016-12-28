import logging
import os

from django.apps import AppConfig
from django.conf import settings

logger = logging.getLogger(__name__)


class LongformConfig(AppConfig):

    name = 'longform'

    mj_script_path = None

    def _get_mj_path(self):
        relpath = os.path.join(
            os.path.split(__file__)[0], '..', 'js', 'single-eq.js'
        )
        abspath = os.path.abspath(relpath)
        if not os.path.exists(relpath):
            raise FileNotFoundError(abspath)
        return abspath

    def ready(self):
        if not getattr(settings, 'LONGFORM_ENABLE_MATHJAX', False):
            logger.debug('Mathjax processing disabled')
            return

        # dumb testing if node-nj available
        from .helpers import exec_mj_statement
        try:
            self.mj_script_path = self._get_mj_path()
            exec_mj_statement('x^2')
        except Exception:
            logger.warning('Mathjax initialization test failed!')
            raise
        logger.debug('Mathjax found at: {} and successfully enabled.'.format(
            self.mj_script_path))
