import logging
import os
from pygit2 import (Repository, discover_repository)

logger = logging.getLogger(__name__)


class Artifact(object):
    def __init__(self, keyword, config={}, allow_dirty=False):
        self.keyword = keyword
        self.hashed_config = hash(''.join(
            ['{}{}'.format(k, v) for k, v in config.items()]))
        self.allow_dirty = allow_dirty
        self.repo = Repository(discover_repository(os.getcwd()))
        self.dirty_suffix = '-dirty'
        self.is_dirty = self.repo.diff().stats.files_changed > 0
        if self.is_dirty and self.allow_dirty:
            logger.warn('Repository has unstaged changes. '
                        'Creating artifacts, but marking them dirty.')
        elif self.is_dirty:
            raise OSError(
                'Refusing to create artifacts with a dirty repository.')

        self.commitish = str(self.repo.head.resolve().target)[:7] + (
            '-dirty' if self.is_dirty else '')

    def __call__(self, f):
        def rewritten(*args, **kwargs):
            output = kwargs.get(self.keyword) or ''
            if not output:
                raise KeyError('%s was not in kwargs for decorated function',
                               self.keyword)
            parts = os.path.split(output)
            fname, ext = parts[-1].split(os.path.extsep)
            with_info = fname + '-' + self.commitish + '-' + str(
                self.hashed_config)[:10] + os.path.extsep + ext
            kwargs[self.keyword] = os.path.join(
                *(list(parts)[:-1] + [with_info]))
            return f(*args, **kwargs)

        return rewritten
