import os
from shutil import rmtree


class SMSChecker(object):

    def __init__(self, path):
        self.sms_path = path

    def messages_for_user(self, user):
        user_path = os.path.join(self.sms_path, user)
        try:
            root, dirs, sms_paths = os.walk(user_path).next()
        except StopIteration:
            return []

        if sms_paths:
            sms_paths.sort()

        messages = []
        for path in sms_paths:
            sms_path = os.path.join(user_path, path)
            with open(sms_path, 'r') as f:
                messages.append(f.read())
        return messages

    def clear(self):
        root, users, files = os.walk(self.sms_path).next()
        for user in users:
            dir_path = os.path.join(self.sms_path, user)
            rmtree(dir_path)
