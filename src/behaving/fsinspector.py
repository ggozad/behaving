import logging
import time
from shutil import rmtree
from pathlib import Path
import os

logger = logging.getLogger("behaving")


class FSInspector(object):
    def __init__(self, path, timeout=5):
        self.path = Path(path)
        self.timeout = timeout

    def messages_for_user(self, user):
        user_path = self.path / user
        try:
            root, dirs, paths = next(os.walk(user_path))
        except StopIteration:
            return []

        if paths:
            paths.sort()

        messages = []
        for path in paths:
            path = user_path / path
            with path.open("r") as f:
                messages.append(f.read())
        return messages

    def user_messages(self, user, f=None):
        messages = []
        start = time.time()
        while time.time() - start < self.timeout:
            messages = list(filter(f, self.messages_for_user(user)))
            if messages:
                break
            time.sleep(0.2)
        return messages

    def clear(self):
        dirs = self.path.dir()
        for dir_path in dirs:
            fn: Path = self.path / dir_path
            try:
                if fn.is_dir(fn):
                    rmtree(fn)
                else:
                    fn.unlink()
            except OSError:
                logger.error("Could not delete %s" % fn)
                exit(1)
