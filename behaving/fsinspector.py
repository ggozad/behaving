import os
from shutil import rmtree


class FSInspector(object):

    def __init__(self, path):
        self.path = path

    def messages_for_user(self, user):
        user_path = os.path.join(self.path, user)
        try:
            root, dirs, paths = os.walk(user_path).next()
        except StopIteration:
            return []

        if paths:
            paths.sort()

        messages = []
        for path in paths:
            path = os.path.join(user_path, path)
            with open(path, 'r') as f:
                messages.append(f.read())
        return messages

    def clear(self):

        dirs = os.listdir(self.path)
        for dir_path in dirs:
            rmtree(os.path.join(self.path, dir_path))
